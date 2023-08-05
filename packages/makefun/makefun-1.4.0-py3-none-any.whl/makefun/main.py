from __future__ import print_function
import re
import sys
import itertools
from collections import OrderedDict
from copy import copy

try:  # python 3.3+
    from inspect import signature, Signature, Parameter
except ImportError:
    from funcsigs import signature, Signature, Parameter

try:
    from inspect import iscoroutinefunction
except ImportError:
    # let's assume there are no coroutine functions in old Python
    def iscoroutinefunction(f):
        return False

try:
    from inspect import isgeneratorfunction
except ImportError:
    # assume no generator function in old Python versions
    def isgeneratorfunction(f):
        return False

try:  # python 3.5+
    from typing import Callable, Any, Union, Iterable
except ImportError:
    pass


# macroscopic signature strings checker (we do not look inside params, `signature` will do it for us)
FUNC_DEF = re.compile('(?s)^\s*(?P<funcname>[_\w][_\w\d]*)\s*'
                      '\(\s*(?P<params>.*?)\s*\)\s*'
                      '((?P<typed_return_hint>->\s*.+)|:\s*#\s*(?P<comment_return_hint>.+))*$')


def create_wrapper(wrapped,
                   wrapper,
                   func_name=None,             # type: str
                   inject_as_first_arg=False,  # type: bool
                   addsource=True,             # type: bool
                   addhandler=True,            # type: bool
                   doc=None,                   # type: str
                   modulename=None,            # type: str
                   **attrs
                   ):
    """
    Creates a signature-preserving wrapper function.

    It is similar in behaviour to `functools.update_wrapper`, but relies on a proper dynamically-generated function.
    Therefore as opposed to `functools.update_wrapper`, the wrapper body will not be executed if the arguments provided
    are not compliant with the signature - instead a `TypeError` will be raised before entering the wrapper body.

    WARNING: the order of arguments is the same than in `create_function` so it is reversed with respect to
    `functools.update_wrapper`.

    This function is just an alias for

        `create_function(wrapped, wrapper, __wrapped__=f, **kwargs)`

    In other words, we just set the additional `__wrapped__` attribute on the created function, to stay compliant with
    the `functools.update_wrapper` convention.
    See https://docs.python.org/3/library/functools.html#functools.update_wrapper
    :return:
    """
    return create_function(wrapped, wrapper, func_name=func_name, inject_as_first_arg=inject_as_first_arg,
                           addsource=addsource, addhandler=addhandler, doc=doc, modulename=modulename,
                           __wrapped__=wrapped, **attrs)


def create_function(func_signature,             # type: Union[str, Signature, Callable[[Any], Any]]
                    func_handler,               # type: Callable[[Any], Any]
                    func_name=None,             # type: str
                    inject_as_first_arg=False,  # type: bool
                    addsource=True,             # type: bool
                    addhandler=True,            # type: bool
                    doc=None,                   # type: str
                    modulename=None,            # type: str
                    **attrs):
    """
    Creates a function with signature <func_signature> that will call <func_handler> with its arguments in order
    when called.

    :param func_signature: either a string without 'def' such as "foo(a, b: int, *args, **kwargs)", a callable, or a
        `Signature` object, for example from the output of `inspect.signature` or from the `funcsigs.signature`
        backport. Note that these objects can be created and edited too. If this is a `Signature`, then a non-none
        `func_name` should be provided. If this is a string, `func_name` should not be provided.
    :param func_handler:
    :param inject_as_first_arg: if True, the created function will be injected as the first positional argument of the
        function handler. This can be handy in case the handler is shared between several facades and needs to know
        from which context it was called. Default=False
    :param func_name: mandatory if func_signature is a `Signature` object, indeed these objects do not contain any name.
    :param addsource: a boolean indicating if a '__source__' annotation should be added to the generated function
        (default: True)
    :param addhandler: a boolean indicating if a '__call_handler__' annotation should be added to the generated function
        (default: True)
    :param doc: a string representing the docstring that will be used to set the __doc__ attribute on the generated
        function. If None (default), the doc of func_handler will be used.
    :param modulename: the name of the module to be set on the function (under __module__ ). If None (default), the
        caller module name will be used.
    :param attrs: other keyword attributes that should be set on the function
    :return:
    """
    # grab context from the caller frame
    try:
        attrs.pop('_with_sig_')
        # called from `@with_signature`
        frame = _get_callerframe(offset=1)
    except KeyError:
        frame = _get_callerframe()
    evaldict, _modulename = extract_module_and_evaldict(frame)
    modulename = modulename if modulename is not None else _modulename

    # input signature handling
    if isinstance(func_signature, str):
        # func_name should not be provided
        if func_name is not None:
            raise ValueError("func_name should not be provided when the signature is provided as a string")

        # transform the string into a Signature and make sure the string contains ":"
        func_name, func_signature, func_signature_str = get_signature_from_string(func_signature, evaldict)

    elif isinstance(func_signature, Signature):
        # func name should be provided
        if func_name is None:
            raise ValueError("a non-None func_name should be provided when a `Signature` is provided")

        # create the signature string
        func_signature_str = get_signature_string(func_name, func_signature, evaldict)

    elif callable(func_signature):
        # grab the func name
        if func_name is None:
            func_name = func_signature.__name__

        # inspect the signature
        func_signature = signature(func_signature)

        # create the signature string
        func_signature_str = get_signature_string(func_name, func_signature, evaldict)
    else:
        raise TypeError("Invalid type for `func_signature`: %s" % type(func_signature))

    # extract all information needed from the `Signature`
    posonly_names, kwonly_names, varpos_names, varkw_names, unrestricted_names = get_signature_params(func_signature)
    params_names = posonly_names + unrestricted_names + varpos_names + kwonly_names + varkw_names
    annotations, defaults, kwonlydefaults = get_signature_details(func_signature)

    # create the body of the function to compile
    assignments = posonly_names + [("%s=%s" % (k, k)) if k[0] != '*' else k
                                   for k in unrestricted_names + varpos_names + kwonly_names + varkw_names]
    params_str = ', '.join(assignments)
    if inject_as_first_arg:
        params_str = "%s, %s" % (func_name, params_str)

    if (3, 5) <= sys.version_info < (3, 6):
        # with Python 3.5 isgeneratorfunction returns True for all coroutines
        # however we know that it is NOT possible to have a generator
        # coroutine in python 3.5: PEP525 was not there yet
        generatorcaller = isgeneratorfunction(func_handler) and not iscoroutinefunction(func_handler)
    else:
        generatorcaller = isgeneratorfunction(func_handler)

    if generatorcaller:
        if sys.version_info >= (3, 3):
            body = "def %s\n    yield from _call_handler_(%s)\n" % (func_signature_str, params_str)
        else:
            from makefun._main_legacy_py import get_legacy_py_generator_body_template
            body = get_legacy_py_generator_body_template() % (func_signature_str, params_str)
    else:
        body = "def %s\n    return _call_handler_(%s)\n" % (func_signature_str, params_str)

    if iscoroutinefunction(func_handler):
        body = ("async " + body).replace('return', 'return await')

    # create the function by compiling code, mapping the `_call_handler_` symbol to `func_handler`
    protect_eval_dict(evaldict, func_name, params_names)
    evaldict['_call_handler_'] = func_handler
    f = _make(func_name, params_names, body, evaldict)

    # add the source annotation if needed
    if addsource:
        attrs['__source__'] = body

    # add the handler if needed
    if addhandler:
        attrs['__call_handler__'] = func_handler

    # by default the doc is the one from the provided handler
    if doc is None:
        doc = getattr(func_handler, '__doc__', None)

    # update the signature
    _update_fields(f, name=func_name, doc=doc, annotations=annotations,
                   defaults=tuple(defaults), kwonlydefaults=kwonlydefaults,
                   module=modulename, **attrs)

    return f


class DefaultHolder:
    __slots__ = 'varname'

    def __init__(self, varname):
        self.varname = varname

    def __repr__(self):
        return self.varname


def get_signature_string(func_name, func_signature, evaldict):
    """
    Returns the string to be used as signature.
    If there is a non-native symbol in the defaults, it is created as a variable in the evaldict
    :param func_name:
    :param func_signature:
    :return:
    """
    # protect the parameters if needed
    new_params = []
    for p_name, p in func_signature.parameters.items():
        if p.default is not Parameter.empty and not isinstance(p.default, (int, str, float, bool)):
            # check if the repr() of the default value is equal to itself.
            needs_protection = True
            try:
                deflt = eval(repr(p.default))
                needs_protection = deflt != p.default
            except SyntaxError:
                pass

            # if we have any problem, we need to protect the default value
            if needs_protection:
                # store the object in the evaldict and insert name
                varname = "DEFAULT_%s" % p_name
                evaldict[varname] = p.default
                p = Parameter(p.name, kind=p.kind, default=DefaultHolder(varname), annotation=p.annotation)

        new_params.append(p)

    # copy signature object
    s = Signature(parameters=new_params, return_annotation=func_signature.return_annotation)

    # return the final string representation
    return "%s%s:" % (func_name, s)


def get_signature_from_string(func_sig_str, evaldict):
    """
    Creates a `Signature` object from the given function signature string.

    :param func_sig_str:
    :return: (func_name, func_sig, func_sig_str). func_sig_str is guaranteed to contain the ':' symbol already
    """
    # escape leading newline characters
    if func_sig_str.startswith('\n'):
        func_sig_str = func_sig_str[1:]

    # match the provided signature. note: fullmatch is not supported in python 2
    def_match = FUNC_DEF.match(func_sig_str)
    if def_match is None:
        raise SyntaxError('The provided function template is not valid: "%s" does not match '
                          '"<func_name>(<func_args>)[ -> <return-hint>]".\n For information the regex used is: "%s"'
                          '' % (func_sig_str, FUNC_DEF.pattern))
    groups = def_match.groupdict()

    # extract function name and parameter names list
    func_name = groups['funcname']
    # params_str = groups['params']
    # params_names = extract_params_names(params_str)

    # find the keyword parameters and the others
    # posonly_names, kwonly_names, unrestricted_names = separate_positional_and_kw(params_names)

    cmt_return_hint = groups['comment_return_hint']
    if cmt_return_hint is None or len(cmt_return_hint) == 0:
        func_sig_str = func_sig_str + ':'

    # Create a dummy function
    body = 'def %s\n    pass\n' % func_sig_str
    dummy_f = _make(func_name, [], body, evaldict)

    # return its signature
    return func_name, signature(dummy_f), func_sig_str


# def extract_params_names(params_str):
#     return [m.groupdict()['name'] for m in PARAM_DEF.finditer(params_str)]


# def separate_positional_and_kw(params_names):
#     """
#     Extracts the names that are positional-only, keyword-only, or non-constrained
#     :param params_names:
#     :return:
#     """
#     # by default all parameters can be passed as positional or keyword
#     posonly_names = []
#     kwonly_names = []
#     other_names = params_names
#
#     # but if we find explicit separation we have to change our mind
#     for i in range(len(params_names)):
#         name = params_names[i]
#         if name == '*':
#             del params_names[i]
#             posonly_names = params_names[0:i]
#             kwonly_names = params_names[i:]
#             other_names = []
#             break
#         elif name[0] == '*' and name[1] != '*':  #
#             # that's a *args. Next one will be keyword-only
#             posonly_names = params_names[0:(i + 1)]
#             kwonly_names = params_names[(i + 1):]
#             other_names = []
#             break
#         else:
#             # continue
#             pass
#
#     return posonly_names, kwonly_names, other_names


def get_signature_params(s):
    """
    Utility method to return the parameter names in the provided `Signature` object, by group of kind

    :param s:
    :return:
    """
    posonly_names, kwonly_names, varpos_names, varkw_names, unrestricted_names = [], [], [], [], []
    for p_name, p in s.parameters.items():
        if p.kind is Parameter.POSITIONAL_ONLY:
            posonly_names.append(p_name)
        elif p.kind is Parameter.KEYWORD_ONLY:
            kwonly_names.append(p_name)
        elif p.kind is Parameter.POSITIONAL_OR_KEYWORD:
            unrestricted_names.append(p_name)
        elif p.kind is Parameter.VAR_POSITIONAL:
            varpos_names.append("*" + p_name)
        elif p.kind is Parameter.VAR_KEYWORD:
            varkw_names.append("**" + p_name)
        else:
            raise ValueError("Unknown kind: %s" % p.kind)

    return posonly_names, kwonly_names, varpos_names, varkw_names, unrestricted_names


def get_signature_details(s):
    """
    Utility method to extract the annotations, defaults and kwdefaults from a `Signature` object

    :param s:
    :return:
    """
    annotations = dict()
    defaults = []
    kwonlydefaults = dict()
    if s.return_annotation is not s.empty:
        annotations['return'] = s.return_annotation
    for p_name, p in s.parameters.items():
        if p.annotation is not s.empty:
            annotations[p_name] = p.annotation
        if p.default is not s.empty:
            # if p_name not in kwonly_names:
            if p.kind is not Parameter.KEYWORD_ONLY:
                defaults.append(p.default)
            else:
                kwonlydefaults[p_name] = p.default
    return annotations, defaults, kwonlydefaults


def extract_module_and_evaldict(frame):
    """
    Utility function to extract the module name from the given frame,
    and to return a dictionary containing globals and locals merged together

    :param frame:
    :return:
    """
    try:
        # get the module name
        modulename = frame.f_globals.get('__name__', '?')

        # construct a dictionary with all variables
        # this is required e.g. if a symbol is used in a type hint
        evaldict = copy(frame.f_globals)
        evaldict.update(frame.f_locals)

    except AttributeError:
        # either the frame is None of the f_globals and f_locals are not available
        modulename = '?'
        evaldict = dict()

    return evaldict, modulename


def protect_eval_dict(evaldict, func_name, params_names):
    """
    remove all symbols that could be harmful in evaldict

    :param evaldict:
    :param func_name:
    :param params_names:
    :return:
    """
    try:
        del evaldict[func_name]
    except KeyError:
        pass
    for n in params_names:
        try:
            del evaldict[n]
        except KeyError:
            pass

    return evaldict


# Atomic get-and-increment provided by the GIL
_compile_count = itertools.count()


def _make(funcname, params_names, body, evaldict=None):
    """
    Make a new function from a given template and update the signature

    :param func_name:
    :param params_names:
    :param body:
    :param evaldict:
    :param addsource:
    :return:
    """
    evaldict = evaldict or {}
    for n in params_names:
        if n in ('_func_', '_call_handler_'):
            raise NameError('%s is overridden in\n%s' % (n, body))

    if not body.endswith('\n'):  # newline is needed for old Pythons
        raise ValueError("body should end with a newline")

    # Ensure each generated function has a unique filename for profilers
    # (such as cProfile) that depend on the tuple of (<filename>,
    # <definition line>, <function name>) being unique.
    filename = '<makefun-gen-%d>' % (next(_compile_count),)
    try:
        code = compile(body, filename, 'single')
        exec(code, evaldict)
    except:
        print('Error in generated code:', file=sys.stderr)
        print(body, file=sys.stderr)
        raise

    # extract the function from compiled code
    func = evaldict[funcname]

    return func


def _update_fields(func, name, doc=None, annotations=None, defaults=(), kwonlydefaults=None, module=None, **kw):
    """
    Update the signature of func with the provided information

    This method merely exists to remind which field have to be filled.

    :param self:
    :param func:
    :param kw:
    :return:
    """
    func.__name__ = name
    func.__doc__ = doc
    func.__dict__ = kw

    func.__defaults__ = defaults
    if len(kwonlydefaults) == 0:
        kwonlydefaults = None
    func.__kwdefaults__ = kwonlydefaults

    func.__annotations__ = annotations
    func.__module__ = module


def _get_callerframe(offset=0):
    try:
        # inspect.stack is extremely slow, the fastest is sys._getframe or inspect.currentframe().
        # See https://gist.github.com/JettJones/c236494013f22723c1822126df944b12
        frame = sys._getframe(2 + offset)
        # frame = currentframe()
        # for _ in range(2 + offset):
        #     frame = frame.f_back

    except AttributeError:  # for IronPython and similar implementations
        frame = None

    return frame


def wraps(f,
          func_name=None,             # type: str
          inject_as_first_arg=False,  # type: bool
          addsource=True,   # type: bool
          addhandler=True,  # type: bool
          doc=None,         # type: str
          modulename=None,  # type: str
          **attrs
          ):
    """
    Decorator to create a signature-preserving wrapper function.

    It is similar to `functools.wraps`, but relies on a proper dynamically-generated function. Therefore as opposed to
    `functools.wraps`, the wrapper body will not be executed if the arguments provided are not
    compliant with the signature - instead a `TypeError` will be raised before entering the wrapper body.

    This decorator is just an alias for

        `with_signature(f, __wrapped__=f, **kwargs)`

    In other words, we just set the additional `__wrapped__` attribute on the created function, to stay compliant with
    the `functools.wraps` convention. See https://docs.python.org/3/library/functools.html#functools.wraps
    :return:
    """
    return with_signature(f, func_name=func_name, inject_as_first_arg=inject_as_first_arg, addsource=addsource,
                          addhandler=addhandler, doc=doc, modulename=modulename, __wrapped__=f, **attrs)


def with_signature(func_signature,             # type: Union[str, Signature]
                   func_name=None,             # type: str
                   inject_as_first_arg=False,  # type: bool
                   addsource=True,             # type: bool
                   addhandler=True,            # type: bool
                   doc=None,                   # type: str
                   modulename=None,            # type: str
                   **attrs
                   ):
    """
    A decorator for functions, to change their signature. The new signature should be compliant with the old one.

    If `func_signature` is set to `None`, then no new function is created: this simply applies the new metadata (name,
    doc, modulename) to the decorated function. `addsource`, `addhandler` and `inject_as_first_arg` should not be set
    in this case.

    :param func_signature: the new signature of the decorated function. Either a string without 'def' such as
        "foo(a, b: int, *args, **kwargs)", a callable, or a `Signature` object, for example from the output of
        `inspect.signature` or from the `funcsigs.signature` backport. Note that these objects can be created and
        edited too. If this is a `Signature`, then a non-None `func_name` should be provided. If this is a string,
        `func_name` should not be provided. Finally `None` can be provided to indicate that user wants to only change
        the medatadata (func_name, doc, modulename) but without generating a new function.
    :param func_name: mandatory if func_signature is a `Signature` object, indeed these objects do not contain any name.
    :param addsource: a boolean indicating if a '__source__' annotation should be added to the generated function
        (default: True)
    :param addhandler: a boolean indicating if a '__call_handler__' annotation should be added to the generated function
        (default: True)
    :param doc: a string representing the docstring that will be used to set the __doc__ attribute on the generated
        function. If None (default), the doc of func_handler will be used.
    :param modulename: the name of the module to be set on the function (under __module__ ). If None (default), the
        caller module name will be used.
    :param attrs: other keyword attributes that should be set on the function
    :return:
    """
    if func_signature is None:
        # make sure that user does not provide non-default other args
        if inject_as_first_arg or not addsource or not addhandler or len(attrs) > 0:
            raise ValueError("If `func_signature=None` no new signature will be generated so only `func_name`, "
                             "`modulename` and `doc` should be provided, to modify the metadata.")
        else:
            def replace_f(f):
                # manually apply all the metadata, but do not generate code - that's useless
                if func_name is not None:
                    f.__name__ = func_name
                if doc is not None:
                    f.__doc__ = doc
                if modulename is not None:
                    f.__module__ = modulename
                return f
    else:
        def replace_f(f):
            return create_function(func_signature=func_signature if func_signature is not None else f,
                                   func_handler=f,
                                   func_name=func_name if func_name is not None
                                             else (f.__name__ if isinstance(func_signature, Signature) else None),
                                   inject_as_first_arg=inject_as_first_arg,
                                   addsource=addsource,
                                   addhandler=addhandler,
                                   doc=doc,
                                   modulename=modulename,
                                   _with_sig_=True,  # special trick to tell create_function that we're @with_signature
                                   **attrs
                                   )

    return replace_f


def remove_signature_parameters(s, *param_names):
    """
    Removes the provided parameters from the signature s (returns a new signature instance).

    :param s:
    :param param_names: a list of parameter names to remove
    :return:
    """
    params = OrderedDict(s.parameters.items())
    for param_name in param_names:
        del params[param_name]
    return s.replace(parameters=params.values())


def add_signature_parameters(s,         # type: Signature
                             first=(),  # type: Union[Parameter, Iterable[Parameter]]
                             last=(),   # type: Union[Parameter, Iterable[Parameter]]
                             ):
    """
    Adds the provided parameters to the signature s (returns a new signature instance).

    :param s:
    :param first: a single element or a list of `Parameter` instances to be added at the beginning of the parameter's
        list
    :param last: a single element or a list of `Parameter` instances to be added at the end of the parameter's list
    :return:
    """
    params = OrderedDict(s.parameters.items())
    lst = list(params.values())

    # prepend
    try:
        for param in first:
            if param.name in params:
                raise ValueError("Parameter with name '%s' is present twice in the signature to create" % param.name)
            else:
                lst.insert(0, param)
    except TypeError:
        # a single argument
        if first.name in params:
            raise ValueError("Parameter with name '%s' is present twice in the signature to create" % first.name)
        else:
            lst.insert(0, first)

    # append
    try:
        for param in last:
            if param.name in params:
                raise ValueError("Parameter with name '%s' is present twice in the signature to create" % param.name)
            else:
                lst.append(param)
    except TypeError:
        # a single argument
        if last.name in params:
            raise ValueError("Parameter with name '%s' is present twice in the signature to create" % last.name)
        else:
            lst.append(last)

    return s.replace(parameters=lst)

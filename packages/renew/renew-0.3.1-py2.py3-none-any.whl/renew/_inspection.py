import inspect
import sys

import six


def implements_constructor(given_class):
    try:
        return check_and_evaluate_arguments_specification(given_class)
    except TypeError:
        return


def check_and_evaluate_arguments_specification(decorated_class):
    try:
        inspect.getfile(decorated_class.__init__)
    except TypeError:
        fields = getattr(decorated_class, "_fields", None)
        if not fields:
            raise TypeError("The class {} does not implement constructor.".format(decorated_class.__name__))
        return inspect.ArgSpec(*fields)

    if sys.version[0] < '3':
        args_spec = inspect.getargspec(decorated_class.__init__)
        unsupported = "keywords",
    else:
        args_spec = inspect.getfullargspec(decorated_class.__init__)
        unsupported = "varkw", "kwonlyargs", "kwonlydefaults"

    for kind in unsupported:
        if getattr(args_spec, kind, None):
            TypeError("pytocopy does not support syntax containing '%s'." % kind)
    return args_spec


def collect_attributes(object_, spec_):
    any_skipped_already = False
    for argument_name, has_default, default_value in _bind_defaults(spec_)[1:]:
        value = _get_attribute_or_raise(object_, argument_name)
        if has_default:
            if value == default_value:
                any_skipped_already = True
            elif any_skipped_already:
                yield argument_name, value
            else:
                yield None, value
        else:
            yield None, value

    if spec_.varargs:
        variadic_arg = _get_attribute_or_raise(object_, spec_.varargs)
        if isinstance(variadic_arg, set):
            # order doesn't matter for a set, but its presentation needs to be kept always in the same order
            variadic_arg = sorted(variadic_arg)

        for attribute_object in variadic_arg:
            yield None, attribute_object


def make_referencing_evaluators(dependency, namespace):
    """
        Return methods to be used to get referencable name for given class. We need methods instead of static
        string values, because the "decision" has to be made at runtime. This function is being executed
        at moment of make_renew_reprs decorator creation (far before actual decoration).
    """

    if dependency is not None:
        msg = "Expecting dependency to be a non empty string or None"
        assert isinstance(dependency, six.string_types) and dependency, msg

    if namespace is None:
        """
            # direct importing by class name:

            from <dependency or cls.__module__> import <cls.__name__>
            that_object = <cls.__name__>(...)
        """

        def get_direct_import_def(cls):
            return (dependency or cls.__module__), cls.__name__

        def get_direct_referable_name(cls):
            return cls.__name__

        return get_direct_referable_name, get_direct_import_def
    elif namespace and isinstance(namespace, six.string_types):
        """
            # indirect importing - via namespace

            import <namespace>
            # or if dependency provided:
            from <dependency> import <namespace>

            that_object = <namespace>.<cls.__name__>(...)
        """

        def get_namespaced_import_def(_):
            return dependency, namespace

        def get_namespaced_ref(cls):
            return "%s.%s" % (namespace, cls.__name__)

        return get_namespaced_ref, get_namespaced_import_def
    else:
        raise ValueError("Expecting namespace value to be either a string or None. Got {}".format(type(namespace)))


def _bind_defaults(spec_):
    if not spec_.defaults:
        return tuple((name, False, None) for name in spec_.args)
    defaults_len = len(spec_.defaults or ())
    blanks_len = len(spec_.args) - defaults_len
    has_default = (False,) * blanks_len + (True,) * defaults_len
    defaults = (None,) * blanks_len + spec_.defaults
    return tuple(zip(spec_.args, has_default, defaults))


def _get_attribute_or_raise(object_, name):
    if not hasattr(object_, name):
        msg = "{} has no '{}' attribute. Constructor args have to be named same as class attributes."
        raise AttributeError(msg.format(object_.__class__.__name__, name))
    return getattr(object_, name)

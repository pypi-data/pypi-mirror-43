import codecs

from . import _inspection, _py_lang, _renderer

__all__ = [
    "make_renew_reprs",
    "make_reproducible",
    "reproduction",
    "serialize",
    "serialize_in_order",
]


def make_renew_reprs(namespace=None, dependency=None):
    """
        A decorator that simplifies creating such a class which instance can be reproduced by evaluating
        a string returned by call result of reproduction function or its __repr__ method.
        I.e.:

        >>> @make_renew_reprs(namespace="my_pkg")
        ... class ThatNiceClass(object):
        ...     # manual implementation of __init__ is needed. Constructor_arguments
        ...     # have to be actual names of this class attributes
        ...     def __init__(self, f_a, f_b, *f_c):
        ...         self.f_a, self.f_b, self.f_c = f_a, f_b, f_c


        >>> ThatNiceClass(1, None)
        my_pkg.ThatNiceClass(1, None)

        >>> nice = ThatNiceClass(1, 2, 3.14159, "four")
        >>> repr(nice)
        "my_pkg.ThatNiceClass(1, 2, 3.14159, 'four')"

        Limitations:
        * constructor arguments have to get exactly same name as instance attributes
        * given object have to be fully reproduced with single constructor call
        * each constructor argument used - have to implement __repr__ in make_renew_reprs flavor
        * no keyword-arguments are supported
        * dictionaries get single indent level no mather what (just ugly but syntax valid)

     """

    def decorator(decorated_class):
        _inspection.check_and_evaluate_arguments_specification(decorated_class)
        name_getter, dep_getter = _inspection.make_referencing_evaluators(dependency, namespace)
        decorated_class.__repr__ = reproduction
        decorated_class._get_referable_name = classmethod(name_getter)
        decorated_class._renew_dependency = classmethod(dep_getter)
        return decorated_class

    return decorator


def make_reproducible(namespace=None, dependency=None):
    name_getter, dep_getter = _inspection.make_referencing_evaluators(dependency, namespace)

    class Reproducible(object):

        def __repr__(self):
            if _inspection.implements_constructor(self.__class__):
                return reproduction(self)
            else:
                return super(Reproducible, self).__repr__()

        _get_referable_name = classmethod(name_getter)
        _renew_dependency = classmethod(dep_getter)

    return Reproducible


def reproduction(object_):
    """ Tries to return a reproducible repr for given object_
        Falls back to native repr, so the reproducibility is not guaranteed.

        >>> class ThatNiceClass(object):
        ...     # manual implementation of __init__ is needed. Constructor_arguments
        ...     # have to be actual names of this class attributes
        ...     def __init__(self, f_a, f_b, *f_c):
        ...         self.f_a, self.f_b, self.f_c = f_a, f_b, f_c

        >>> nice = ThatNiceClass(1, 2, 3.14159, "four")
        >>> reproduction(nice)
        "ThatNiceClass(1, 2, 3.14159, 'four')"
        >>> reproduction([10, 20, nice, 40.5])
        "[10, 20, ThatNiceClass(1, 2, 3.14159, 'four'), 40.5]"
    """
    return _py_lang.ReprDispatcher().render(object_)


def serialize(output_file_path, **objects):
    """
        Dumps objects into a python file.
        Objects are ordered alphabetically to make it able to be handled by VCSs.
    """
    return serialize_in_order(output_file_path, *sorted(objects.items()))


def serialize_in_order(output_file_path, *objects):
    """
        Keep order of serialized values if it matters for you.
        instead of using kw-arguments, call it with name-value tuples, e.g.:
        serialize_in_order(output_file_path, ('name_1', 'value_1'), ('name_2', 'value_2'))
    """
    _renderer.validate_output_path(output_file_path)
    _renderer.validate_objects(objects)
    snippets = []

    d = _py_lang.ReprDispatcher()
    for reference_name, object_ in objects:
        snippet = d.render(object_)
        snippets.append("{} = {}\n".format(reference_name, snippet))

    content = _renderer.PY_FILE_HEADER + _renderer.build_imports(d.dependencies) + "\n".join(snippets)

    with codecs.open(output_file_path, 'w', encoding="utf-8") as f:
        return f.write(content)

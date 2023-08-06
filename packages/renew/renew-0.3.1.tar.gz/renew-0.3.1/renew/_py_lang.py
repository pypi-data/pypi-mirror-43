import six

from . import _inspection, _renderer


class ReprDispatcher(object):
    def __init__(self):
        self.dependencies = []

    def append_dep(self, dependency):
        if dependency not in self.dependencies:
            _renderer.validate_dependency(dependency)
            self.dependencies.append(dependency)

    def render(self, object_):
        return "".join(self.dispatch(object_, True))

    def dispatch(self, object_, top_level=False):
        is_nicely_reproducible = hasattr(object_, "_get_referable_name")
        correct_ctor_args = _inspection.implements_constructor(object_.__class__)

        if is_nicely_reproducible:
            deps = getattr(object_, "_renew_dependency", None)
            if deps:
                self.append_dep(deps())
            items_reprs = [(kw, list(self.dispatch(value))) for kw, value in
                           _inspection.collect_attributes(object_, correct_ctor_args)]
            for element in _make_a_markup("%s(" % object_._get_referable_name(), items_reprs, ")"):
                yield element
        elif correct_ctor_args:
            items_reprs = [(kw, list(self.dispatch(value))) for kw, value in
                           _inspection.collect_attributes(object_, correct_ctor_args)]
            for element in _make_a_markup("%s(" % object_.__class__.__name__, items_reprs, ")"):
                yield element
        elif isinstance(object_, list):
            items_reprs = [(None, list(self.dispatch(item))) for item in object_]
            for element in _make_a_markup("[", items_reprs, "]"):
                yield element
        elif isinstance(object_, tuple) and not hasattr(object_, '_fields'):
            items_reprs = [(None, list(self.dispatch(item))) for item in object_]
            for element in _make_a_markup("(", items_reprs, ")"):
                yield element
        elif isinstance(object_, set):
            items_reprs = [(None, list(self.dispatch(item))) for item in sorted(object_)]
            for element in _make_a_markup("{", items_reprs, "}"):
                yield element
        elif isinstance(object_, dict):
            items_reprs = [(kw, list(self.dispatch(value)))
                           for kw, value in sorted(object_.items(), key=lambda x: str(x[0]))]
            for element in _make_a_markup("{", items_reprs, "}", as_dict=True):
                yield element
        elif isinstance(object_, six.string_types) and len(object_) > 80:
            if top_level:
                yield "(\n"
                indent = "    "
            else:
                indent = ""
            for line in _split_long_string(object_):
                yield indent + repr(line) + "\n"
            if top_level:
                yield ")"

        else:
            yield repr(object_)


def _make_a_markup(begin, items_reprs, end, item_delimiter=",", as_dict=False):
    single_line_body = ", ".join(_form_single_line(items_reprs, as_dict))
    single_line_reproduction = begin + single_line_body + end
    if len(single_line_reproduction) <= 100 or not items_reprs:
        yield single_line_reproduction
    else:
        yield begin + "\n"
        for element in _form_multi_line(items_reprs, item_delimiter, as_dict):
            yield element
        yield end


def _form_single_line(items_representations, as_dict):
    kw_delimiter = ": " if as_dict else "="
    for keyword, value_reps in items_representations:
        if keyword:
            if as_dict:
                keyword = repr(keyword)
            preamble = keyword + kw_delimiter
        else:
            preamble = ""
        yield preamble + "".join(value_reps)


def _form_multi_line(items_reprs, item_delimiter, as_dict):
    kw_delimiter = ": " if as_dict else "="
    indent = "    "
    for keyword, value_reps in items_reprs:
        is_first = True
        for argument_reproduction in value_reps:
            if is_first and keyword is not None:
                if as_dict:
                    keyword = repr(keyword)
                preamble = keyword + kw_delimiter
            else:
                preamble = ""
            optional_break = (item_delimiter + "\n") if not argument_reproduction.endswith("\n") else ""
            is_first = False
            yield indent + preamble + argument_reproduction + optional_break


def _split_long_string(long_string, max_line_width=80):
    lines = long_string.split("\n")
    if not any(len(line) > max_line_width for line in lines):
        for not_last, line in enumerate(lines, 1 - len(lines)):
            yield line + ("\n" if not_last else "")
    else:
        words = long_string.split(" ")
        if not any(len(word) > max_line_width for word in words):
            line, pos = "", 0
            for not_last, word in enumerate(words, 1 - len(words)):
                word += " " if not_last else ""
                line += word
                pos += len(word)
                if pos >= 80:
                    yield line
                    line, pos = "", 0
            if line:
                yield line
        else:
            pos = 0
            while pos < len(long_string):
                yield long_string[pos:pos + max_line_width]
                pos += max_line_width

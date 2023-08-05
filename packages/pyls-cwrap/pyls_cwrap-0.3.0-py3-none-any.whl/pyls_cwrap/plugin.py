from typing import Any, Dict

from pyls import hookimpl

from pyls_cwrap.wrap import format_text


@hookimpl(hookwrapper=True)
def pyls_format_document(document):
    outcome = yield
    format_document(document, outcome)


@hookimpl(hookwrapper=True)
def pyls_format_range(document, range):
    outcome = yield
    format_document(document, outcome, range)


def format_document(document, outcome, range=None):
    if range is None:
        range = {
            "start": {"line": 0, "character": 0},
            "end": {"line": len(document.lines), "character": 0},
        }
        text = document.source
    else:
        range["start"]["character"] = 0
        range["end"]["character"] = 0
        # range["end"]["line"] += 1  # For cursor staying.
        start = range["start"]["line"]
        end = range["end"]["line"]
        text = "".join(document.lines[start:end])

    result = outcome.get_result()
    if result:
        text = result[0]["newText"]

    config = load_config(document.path)

    formatted_text = format_text(text, **config)

    if formatted_text == text:
        return

    result = [{"range": range, "newText": formatted_text}]
    outcome.force_result(result)


def load_config(filename: str) -> Dict[str, Any]:
    defaults = {"max_line_length": 79}

    try:
        import pycodestyle
    except ImportError:
        return defaults

    try:
        style_guide = pycodestyle.StyleGuide(parse_argv=True)
        max_line_length = style_guide.options.max_line_length
    except Exception:
        return defaults

    config = {"max_line_length": max_line_length}

    return {**defaults, **config}

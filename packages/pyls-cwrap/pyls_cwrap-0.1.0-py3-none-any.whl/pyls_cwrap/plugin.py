# import os

from pyls import hookimpl
from pyls_cwrap.wrap import beautify


def wrap(document, override=None):
    source = override or document.source
    wrapped_source = beautify(source)

    if source == wrapped_source:
        return

    return [{
        'range': {'start': {'line': 0, 'character': 0},
                  'end': {'line': len(document.lines), 'character': 0}},
        'newText': wrapped_source
    }]


@hookimpl(hookwrapper=True)
def pyls_format_document(document):
    outcome = yield
    results = outcome.get_result()
    if results:
        newResults = wrap(document, results[0]['newText'])
    else:
        newResults = wrap(document)

    if newResults:
        outcome.force_result(newResults)


@hookimpl(hookwrapper=True)
def pyls_format_range(document, range):
    outcome = yield
    results = outcome.get_result()
    if results:
        newResults = wrap(document, results[0]['newText'])
    else:
        newResults = wrap(document)

    if newResults:
        outcome.force_result(newResults)

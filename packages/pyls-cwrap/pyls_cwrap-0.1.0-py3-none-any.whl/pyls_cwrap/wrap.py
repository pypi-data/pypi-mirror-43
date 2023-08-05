import re
import unicodedata
from enum import Enum
from functools import reduce
from itertools import accumulate
from typing import Iterator, Tuple


class Kind(Enum):
    COMMENT = 1
    CODE = 2


COMMENT_HEADER = re.compile(r'^#[\s#]*')


def _new_line(source):
    return '\r\n' if '\r\n' in source else '\n'


def beautify(source: str, length: int = 79) -> str:
    nl = _new_line(source)
    return nl.join(wrapper(source, length))


def wrapper(source: str, length: int) -> Iterator[str]:
    for kind, line in joiner(source):
        if kind == Kind.CODE:
            yield line
        else:
            yield from wrap(line, length)


def wrap(line: str, length: int, pre: str = '# ') -> Iterator[str]:
    length -= len(pre)
    is_wides = [is_wide(x) for x in line]
    position = list(accumulate(2 if x else 1 for x in is_wides))
    splitterable = [False] + [x == ' ' or (is_wides[k] and is_wides[k + 1])
                              for k, x in enumerate(line[1:])]

    begin = end = head = 0
    while True:
        if splitterable[head]:
            end = head
        head += 1
        if head >= len(line):
            yield pre + line[begin:].strip()
            break
        elif position[head] - position[begin] - 1 >= length and begin != end:
            yield pre + line[begin:end + 1].strip()
            begin = end = end + 1


def is_wide(character: str) -> bool:
    return unicodedata.east_asian_width(character) in ['F', 'W']


def is_splittable(line, head) -> bool:
    return line[head] == ' ' or is_wide(head - 1) or is_wide(head)


def joiner(source: str) -> Iterator[Tuple[Kind, str]]:
    iterator = splitter(source)

    def joint(tail: str, head: str) -> str:
        if is_wide(tail) and is_wide(head):
            return ''
        else:
            return ' '

    def join(first: str, second: str) -> str:
        return joint(first[-1], second[0]).join([first, second])

    for kind, line in iterator:
        if kind == Kind.CODE:
            yield Kind.CODE, line
        else:
            lines = []
            for kind, line_ in iterator:
                if kind == Kind.COMMENT:
                    lines.append(line_)
                else:
                    yield Kind.COMMENT, reduce(join, lines, line)
                    yield Kind.CODE, line_
                    break
            else:
                yield Kind.COMMENT, reduce(join, lines, line)


def splitter(source: str) -> Iterator[Tuple[Kind, str]]:
    nl = _new_line(source)
    for line in source.split(nl):
        if line.startswith('#'):
            line = re.sub(COMMENT_HEADER, '', line)
            if line:  # Drop comment line without any text.
                yield Kind.COMMENT, line
        else:
            yield Kind.CODE, line

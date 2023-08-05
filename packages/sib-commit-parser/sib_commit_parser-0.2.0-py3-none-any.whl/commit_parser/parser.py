"""StartinBlox commit style parser"""

import re
from typing import Tuple
from semantic_release.errors import UnknownCommitMessageStyleError
from semantic_release.history.parser_helpers import parse_text_block

re_parser = re.compile(
    r'(?P<type>\w+)'
    r'(?:\((?P<scope>[\w _\-]+)\))?: '
    r'(?P<subject>[^\n]+)'
    r'(:?\n\n(?P<text>.+))?',
    re.DOTALL
)

TYPES = [
    'major',
    'minor',
    'feature',
    'update',
    'bugfix',
    'ui',
    'syntax',
    'other'
]


def parse_commit_message(message: str) -> Tuple[int, str, str, Tuple[str, str, str]]:
    """
    Parses a commit message according to the StartinBlox release rules
    :param message: A string of the commit message
    :return: A tuple of (level to bump, type of change, scope of change, a tuple with descriptions)
    """

    try:
        # default to patch
        level_bump = 1

        # parse message
        parsed = re_parser.match(message)

        # catch type
        _type = parsed.group('type')
        if _type not in TYPES:
            _type = 'other'

        # calculate release level
        if _type == 'major':
            level_bump = 3

        elif _type == 'minor':
            level_bump = 2

        subject = parsed.group('subject')
        body, footer = parse_text_block(parsed.group('text'))

    except AttributeError:
        # if regex doesn't match make a patch with raw commit message
        _type = 'other'
        subject = message.split("\n", 1)[0]
        try:
            body, footer = parse_text_block(message.split("\n", 1)[1])
        except IndexError:
            body = ''
            footer = ''

    return (
        level_bump,
        _type,
        '',
        (subject, body, footer)
    )

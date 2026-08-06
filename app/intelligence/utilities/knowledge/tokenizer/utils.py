"""
Tokenizer Utility Functions
"""

import re


def clean_spaces(text):

    return re.sub(

        r"\s+",

        " ",

        text,

    ).strip()


def strip_empty(values):

    return [

        value

        for value in values

        if value.strip()

    ]


def lowercase(text):

    return text.lower()
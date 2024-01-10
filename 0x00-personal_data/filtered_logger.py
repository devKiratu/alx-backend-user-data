#!/usr/bin/env python3
"""
defines function for obfuscating PII
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    returns the log message obfuscated
    Args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating all
            fields in the log line (message)
    """
    for field in fields:
        match = re.search(r"{}=([^{}]+)".format(field, separator), message)
        if match:
            message = re.sub(match.group(1), redaction, message)
    return message

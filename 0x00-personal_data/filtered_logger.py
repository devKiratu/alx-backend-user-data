#!/usr/bin/env python3
"""
defines function for obfuscating PII
"""
from typing import List
import re
import logging
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initialize RedactingFormatter class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        masked_message = filter_datum(self.fields, self.REDACTION,
                                      record.getMessage(), self.SEPARATOR)
        """format log message by masking PII data"""
        record.msg = masked_message
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    creates a custome logging object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger

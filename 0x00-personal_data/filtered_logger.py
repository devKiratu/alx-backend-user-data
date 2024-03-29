#!/usr/bin/env python3
"""
defines function for obfuscating PII
"""
from typing import List
import re
import logging
import mysql.connector
import os

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
        """format log message by masking PII data"""
        masked_message = filter_datum(self.fields, self.REDACTION,
                                      record.getMessage(), self.SEPARATOR)
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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    returns a connector to a mysql database
    """
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connection.MySQLConnection(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )
    return conn


def main() -> None:
    """
    obtains a database connection using get_db and retrieve all rows in the
    users table and display each row under a filtered format
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    keys = [col[0] for col in cursor.description]
    for row in cursor:
        formatted_row = " ".join("{}={};".format(key, val)
                                 for key, val in zip(keys, row))
        logger.info(formatted_row)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()

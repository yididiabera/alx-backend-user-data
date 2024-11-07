#!/usr/bin/env python3
"""A module for a function that obfuscates sensitive data"""
import logging
import re
import os
import mysql.connector
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns an obfuscated version of message"""
    return re.sub(f"({'|'.join(fields)})=[^{separator}]*",
                  lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """A method for formatting log records"""
        msg = record.getMessage()
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  msg, self.SEPARATOR)
        return super().format(record)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """Get a logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connection to a mysql database"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    name = os.getenv("PERSONAL_DATA_DB_NAME")
    connection = mysql.connector.connect(
        host=host,
        database=name,
        user=username,
        password=password
    )
    return connection


def main() -> None:
    """Main control flow"""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        log_message = "; ".join(
                f"{key}={row[key]}" if key not in PII_FIELDS else f"{key}=***"
                for key in row
            )
        print(log_message)


if __name__ == "__main__":
    main()

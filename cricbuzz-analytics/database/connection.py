import mysql.connector
from mysql.connector import MySQLConnection

from config import MYSQL_CONFIG


def get_connection() -> MySQLConnection:
    return mysql.connector.connect(**MYSQL_CONFIG)

import mysql.connector
import os

DB_CONFIG = {
    'host': os.getenv("MYSQL_HOST", "host.docker.internal"),
    'port': int(os.getenv("MYSQL_PORT", 3306)),
    'user': os.getenv("MYSQL_USER", "root"),
    'password': os.getenv("MYSQL_PASSWORD", "root"),
    'database': os.getenv("MYSQL_DATABASE", "mydb")
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
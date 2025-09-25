import os
import logging

from flask import current_app, g
from contextlib import contextmanager

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

pool = None

def setup():
    global pool
    DATABASE_URL = os.environ["DATABASE_URL"]
    #current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode="require")

@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)

@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
        cursor = connection.cursor(cursor_factory=DictCursor)
        try:
            yield cursor
            if commit:
                connection.commit()
        finally:
            cursor.close()

def add_content(name, message):
    with get_db_cursor(True) as cur:
        #current_app.logger.info("Adding person %s", name)
        cur.execute("INSERT INTO guestbook (name, message) values (%s, %s);", (name, message))

def get_guestbook():
    info = []
    with get_db_cursor(False) as cur:
        with get_db_cursor() as cur:
            cur.execute("SELECT * from guestbook")
            for row in cur:
                info.append({"name": row["name"], "message": row["message"]})
    return info
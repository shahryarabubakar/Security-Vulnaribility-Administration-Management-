"""
seed_users.py
Run once after: mysql -u root -p < sql/schema.sql

Sets real Werkzeug-hashed passwords for the placeholder users
that the schema inserted.

Usage:
    python seed_users.py
"""
import os
import MySQLdb
from werkzeug.security import generate_password_hash
from config import Config

DB = {
    'host':   os.environ.get('MYSQL_HOST',     Config.MYSQL_HOST),
    'port':   int(os.environ.get('MYSQL_PORT', str(Config.MYSQL_PORT))),
    'user':   os.environ.get('MYSQL_USER',     Config.MYSQL_USER),
    'passwd': os.environ.get('MYSQL_PASSWORD', Config.MYSQL_PASSWORD),
    'db':     os.environ.get('MYSQL_DB',       Config.MYSQL_DB),
}

USERS = [
    # (username,   plain_password,  role)
    ('admin',    'admin123',    'admin'),
    ('analyst1', 'analyst123',  'analyst'),
]


def seed():
    conn = MySQLdb.connect(**DB)
    cur  = conn.cursor()

    for username, password, role in USERS:
        hashed = generate_password_hash(password)
        cur.execute(
            """
            INSERT INTO users (username, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE password_hash = VALUES(password_hash)
            """,
            (username, f'{username}@svams.local', hashed, role),
        )
        print(f'  ✓  {username}  ({role})  →  password: {password}')

    conn.commit()
    cur.close()
    conn.close()
    print('\nDone. You can now log in at http://localhost:5000')


if __name__ == '__main__':
    seed()

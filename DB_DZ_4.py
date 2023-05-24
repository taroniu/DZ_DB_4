import psycopg2


with psycopg2.connect(database="DZ_DB_4", user="postgres", password="9ZUkK4725") as conn:
    def create_db(conn):
        with conn.cursor() as cur:
            cur.execute('''
                DROP TABLE phone_numbers;
                DROP TABLE users;
                ''')
            cur.execute('''CREATE TABLE if not exists users(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(60) NOT NULL,
                last_name VARCHAR(60) NOT NULL,
                email VARCHAR(60) UNIQUE NOT NULL
                );
                ''')

            cur.execute('''
                    CREATE TABLE IF NOT EXISTS phone_numbers (
                    client_id INTEGER NOT NULL REFERENCES users(id),
                    phone_id SERIAL PRIMARY KEY,
                    phone VARCHAR(20) UNIQUE
                    );
                    ''')
            # conn.commit()
            cur.execute('''
                    select * from users
                    ''')
            print(cur.fetchone())

    def add_client(conn, first_name, last_name, email, phones=None):
        cur =  conn.cursor()
        cur.execute(f'''
                INSERT INTO users (first_name, last_name, email) VALUES ('{first_name}', '{last_name}', '{email}')
                returning id, first_name, last_name, email;
                ''')
        print(cur.fetchone())

    def add_phone(conn, client_id, phone):
        cur = conn.cursor()
        cur.execute(f'''
                INSERT INTO phone_numbers (client_id, phone) VALUES ('{client_id}', '{phone}')
                RETURNING client_id, phone_id, phone;
                ''')
        print(cur.fetchone())

    def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
        cur = conn.cursor()
        cur.execute(f'''
                UPDATE users SET first_name = '{first_name}', last_name = '{last_name}', email = '{email}' 
                WHERE id = {client_id}
                RETURNING id, first_name, last_name, email;
                ''')
        print(cur.fetchone())
        # pass

    def delete_phone(conn, client_id, phone):
        cur = conn.cursor()
        cur.execute(f'''
                DELETE FROM phone_numbers
                WHERE client_id = {client_id} AND phone = '{phone}' RETURNING client_id, phone_id, phone;
                ''')
        print(cur.fetchone())
        # pass

    def delete_client(conn, client_id):
        cur = conn.cursor()
        cur.execute(f'''
                DELETE FROM users
                WHERE id = {client_id} RETURNING id, first_name, last_name;
                ''')
        print(cur.fetchone())
        # pass

    def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
        cur = conn.cursor()
        cur.execute(f'''
                SELECT id, first_name, last_name, email, phone FROM users, phone_numbers
                WHERE first_name = '{first_name}' OR last_name = '{last_name}' OR email = '{email}'
                ''')
        print(cur.fetchone())
        # pass

create_db(conn)
add_client(conn, 'dart', 'vader', 'bebra@gmail.com')
add_client(conn, 'obivan', 'kenobi', 'obivanbalaban@gmail.com')
add_phone(conn, 1, 89137654321)
add_phone(conn, 2, 89995672345)
change_client(conn, client_id=1, first_name='bolbo', last_name='bilbo', email='bilbodildo@gmail.com')
delete_phone(conn, 1, 89137654321)
delete_client(conn, 1)
find_client(conn, first_name='obivan')



# conn = psycopg2.connect(database='DZ_DB_4', user='postgres', password='9ZUkK4725')
# # cur = conn.cursor()
# # cur.execute('')
# with conn.cursor() as cur:
#     cur.execute('''
#     DROP TABLE phone_numbers;
#     DROP TABLE users;
#     ''')
#
#     cur.execute('''CREATE TABLE if not exists users(
#                 id SERIAL PRIMARY KEY,
#                 name VARCHAR(60) NOT NULL,
#                 surname VARCHAR(60) NOT NULL,
#                 email VARCHAR(60) UNIQUE NOT NULL
#                 );
#                 ''')
#
#     cur.execute('''
#             CREATE TABLE IF NOT EXISTS phone_numbers (
#             user_id INTEGER NOT NULL REFERENCES users(id),
#             phone_id SERIAL PRIMARY KEY,
#             phone_number BIGINT UNIQUE
#             );
#             ''')
#     conn.commit()
#
#     cur.execute('''
#             INSERT INTO users (name, surname, email) VALUES ('Obivan', 'Kenobi', 'obivankenobi@gmail.com')
#             RETURNING id, name, surname, email;
#             ''')
#     print(cur.fetchone())
#
#     cur.execute('''
#                 INSERT INTO users (name, surname, email) VALUES ('Master', 'Yoda', 'masteryoda@gmail.com')
#                 RETURNING id, name, surname, email;
#                 ''')
#     print(cur.fetchone())
#
#     cur.execute('''
#             INSERT INTO phone_numbers (user_id, phone_number) VALUES (1, 79131234567)
#             RETURNING user_id, phone_id, phone_number;
#             ''')
#     print(cur.fetchone())
#
#     cur.execute('''
#               INSERT INTO phone_numbers (user_id, phone_number) VALUES (2, 79139872434)
#               RETURNING user_id, phone_id, phone_number;
#               ''')
#     print(cur.fetchone())
#
#     cur.execute('''
#             UPDATE users SET email = 'obivango@gmail.com' WHERE id = 1 RETURNING id, name, surname, email;
#             ''')
#     print(cur.fetchone())
#
#     cur.execute('''
#             DELETE FROM phone_numbers
#             WHERE user_id = 1 RETURNING user_id, phone_id, phone_number;
#             ''')
#     print(cur.fetchall())
#
#     cur.execute('''
#             DELETE FROM users
#             WHERE id = 1 RETURNING id, name, surname, email;
#             ''')
#     print(cur.fetchall())
#
#     cur.execute('''
#             SELECT name, surname, email, phone_number FROM users, phone_numbers
#             WHERE surname = 'Yoda';
#
#             ''')
#     print(cur.fetchone())
#
#     cur.execute('''
#             SELECT name, surname, email, phone_number FROM users, phone_numbers
#             WHERE phone_number = 79131234567;
#             ''')
#     print(cur.fetchone())
#
# # cur.close()
# conn.close()
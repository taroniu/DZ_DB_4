import psycopg2


conn = psycopg2.connect(database='DZ_DB_4', user='postgres', password='9ZUkK4725')
# cur = conn.cursor()
# cur.execute('')
with conn.cursor() as cur:
    cur.execute('''
    DROP TABLE phone_numbers;
    DROP TABLE users;
    ''')

    cur.execute('''CREATE TABLE if not exists users(
                id SERIAL PRIMARY KEY,
                name VARCHAR(60) NOT NULL,
                surname VARCHAR(60) NOT NULL,
                email VARCHAR(60) UNIQUE NOT NULL
                );
                ''')

    cur.execute('''
            CREATE TABLE IF NOT EXISTS phone_numbers (
            user_id INTEGER NOT NULL REFERENCES users(id),
            phone_id SERIAL PRIMARY KEY,
            phone_number BIGINT UNIQUE
            );
            ''')
    conn.commit()

    cur.execute('''
            INSERT INTO users (name, surname, email) VALUES ('Obivan', 'Kenobi', 'obivankenobi@gmail.com')
            RETURNING id, name, surname, email;
            ''')
    print(cur.fetchone())

    cur.execute('''
                INSERT INTO users (name, surname, email) VALUES ('Master', 'Yoda', 'masteryoda@gmail.com')
                RETURNING id, name, surname, email;
                ''')
    print(cur.fetchone())

    cur.execute('''
            INSERT INTO phone_numbers (user_id, phone_number) VALUES (1, 79131234567) RETURNING user_id, phone_id, phone_number;
            ''')
    print(cur.fetchone())

    cur.execute('''
              INSERT INTO phone_numbers (user_id, phone_number) VALUES (2, 79139872434) RETURNING user_id, phone_id, phone_number;
              ''')
    print(cur.fetchone())

    cur.execute('''
            UPDATE users SET email = 'obivango@gmail.com' WHERE id = 1 RETURNING id, name, surname, email; 
            ''')
    print(cur.fetchone())

    cur.execute('''
            DELETE FROM phone_numbers
            WHERE user_id = 1 RETURNING user_id, phone_id, phone_number;
            ''')
    print(cur.fetchall())

    cur.execute('''
            DELETE FROM users
            WHERE id = 1 RETURNING id, name, surname, email;
            ''')
    print(cur.fetchall())

    cur.execute('''
            SELECT name, surname, email, phone_number FROM users, phone_numbers
            WHERE surname = 'Yoda';
            
            ''')
    print(cur.fetchone())

    cur.execute('''
            SELECT name, surname, email, phone_number FROM users, phone_numbers
            WHERE phone_number = 79131234567;
            ''')
    print(cur.fetchone())

# cur.close()
conn.close()
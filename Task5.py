
import psycopg2

def remove_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phone_customer;
        DROP TABLE customer;
        DROP TABLE name;
        DROP TABLE surname;
        DROP TABLE email;
        DROP TABLE phone;

        """);
        conn.commit()

def create_db(conn):
    
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS name(
            name_id SERIAL PRIMARY KEY,
            name VARCHAR(40) UNIQUE
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS surname(
            surname_id SERIAL PRIMARY KEY,
            surname VARCHAR(40) UNIQUE
        );
        """)   
        cur.execute("""
        CREATE TABLE IF NOT EXISTS email(
            email_id SERIAL PRIMARY KEY,
            email VARCHAR(40) UNIQUE
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone(
            phone_id SERIAL PRIMARY KEY,
            phone VARCHAR(20) UNIQUE
        );
        """)
   
        cur.execute("""
        CREATE TABLE IF NOT EXISTS customer(
            customer_id SERIAL PRIMARY KEY,
            customer_name INTEGER NOT NULL REFERENCES name(name_id),
            customer_surname INTEGER NOT NULL REFERENCES surname(surname_id),
            customer_email INTEGER NOT NULL REFERENCES email(email_id)
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_customer(
            id SERIAL PRIMARY KEY,
            customer_id INTEGER NOT NULL REFERENCES customer(customer_id),
            phone_id INTEGER NOT NULL REFERENCES phone(phone_id)
        );
        """)

        conn.commit()




def add_customer(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO name(name) VALUES(%s) ON CONFLICT DO NOTHING;
        """,(first_name,))
        cur.execute("""
        INSERT INTO surname(surname) VALUES(%s) ON CONFLICT DO NOTHING;
        """,(last_name,))
        cur.execute("""
        INSERT INTO email(email) VALUES(%s) ON CONFLICT DO NOTHING;
        """,(email,))
        conn.commit()

        if phones == 0:
            cur.execute("""
            INSERT INTO phone(phone) VALUES(%s) ON CONFLICT DO NOTHING;
            """,(0,))
        else:
            for i in phones:
                cur.execute("""
                INSERT INTO phone(phone) VALUES(%s) ON CONFLICT DO NOTHING;
                """,(i,))
        conn.commit()

        cur.execute(""" 
        SELECT name_id FROM name WHERE name=%s;
        """,(first_name,))
        name_id = cur.fetchone()[0]

        cur.execute(""" 
        SELECT surname_id FROM surname WHERE surname=%s;
        """,(last_name,))
        surname_id = cur.fetchone()[0]

        cur.execute(""" 
        SELECT email_id FROM email WHERE email=%s;
        """,(email,))
        email_id = cur.fetchone()[0]
        

        cur.execute("""
        INSERT INTO customer(customer_name, customer_surname, customer_email) VALUES(%s,%s,%s);
        """,(name_id,surname_id, email_id))

        conn.commit()
        

        

        
        
        
        #INSERT INTO phone_customer(customer_id) VALUES(SELECT customer_id FROM customer JOIN email ON customer(customer_email) = email(email_id) WHERE email=email);
        #INSERT INTO phone_customer(phone_id)
        

def add_phone(conn, client_id, phone):
    pass

def change_customer(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    pass

def delete_phone(conn, client_id, phone):
    pass

def delete_customer(conn, client_id):
    pass

def find_customer(conn, first_name=None, last_name=None, email=None, phone=None):
    pass

def get_customer_name():
    while True:
        name = input('Введите имя клиента (поле не может быть пустым):').lstrip().rstrip()
        if name:
            break
        else:
            continue
    return name

def get_customer_surname():
    while True:
        surname = input('Введите фамилию клиента (поле не может быть пустым):').lstrip().rstrip()
        if surname:
            break
        else:
            continue
    return surname

def get_customer_email():
    while True:
        email = input('Введите email клиента (поле не может быть пустым):').lstrip().rstrip()
        if email and '@' in email:
            break
        else:
            continue
    return email

def get_customer_phones():
    number_of_phones = int(input('Введите кол-во телефонных номеров клиента:'))
    client_phones = []
    if number_of_phones == 0:
        return 0
    else:
        for i in range(1, number_of_phones+1):
            while True:
                phone = input(f'Введите телефон {i} клиента (поле не может быть пустым):').lstrip().rstrip()
                if phone:
                    break
                else:
                    continue
            client_phones.append(phone)
        return client_phones


    
with psycopg2.connect(database="task5", user="postgres", password="Maxim0055!!!") as conn:
    remove_db(conn)
    create_db(conn)
    for i in range(3):
        add_customer(conn, get_customer_name(), get_customer_surname(), get_customer_email(), get_customer_phones())
    
conn.close()


﻿
import psycopg2

def remove_db(conn, cur):
    cur.execute("""
        DROP TABLE phone_customer;
        DROP TABLE customer;
        DROP TABLE name;
        DROP TABLE surname;
        DROP TABLE email;
        DROP TABLE phone;
        """);
    conn.commit()            

def create_db(conn, cur):
    
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
    #индентификатор телефона и клиента уникальны
    cur.execute(""" ALTER TABLE phone_customer
    ADD CONSTRAINT phone_cust UNIQUE (customer_id, phone_id);
    
    """)

    conn.commit()




def add_customer(conn, cur, first_name, last_name, email, phones='0'):
    # вносим данные в таблицы имя, фамилия, email, телефоны
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

    for i in phones:
        cur.execute("""
        INSERT INTO phone(phone) VALUES(%s) ON CONFLICT DO NOTHING;
        """,(i,))
        conn.commit()

    # определяем данные для создания записи в таблицу клиентов
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
        
    # заносим данные в таблицу клиентов
    cur.execute("""
    INSERT INTO customer(customer_name, customer_surname, customer_email) VALUES(%s,%s,%s);
    """,(name_id,surname_id, email_id))
    conn.commit()
        
    #определяем данные для таблицы клиент-телефоны
    cur.execute(""" 
    SELECT customer_id FROM customer WHERE customer_email=%s;
    """,(email_id,))
    customer_id = cur.fetchone()[0]
        
    phone_id = []
        
    for i in phones:
        cur.execute(""" 
        SELECT phone_id FROM phone WHERE phone=%s;
        """,(i,))
        phone_id.append(cur.fetchone()[0])
     
    # заносим данные в таблицу клиент-телефоны   
    for i in phone_id:
        cur.execute("""
        INSERT INTO phone_customer(customer_id, phone_id) VALUES(%s,%s) ON CONFLICT DO NOTHING;
        """,(customer_id,i))
        conn.commit()
        
        

def add_phone(conn, cur, customer_id, phone):

    #заносим данные в таблицу телефонов
    cur.execute("""
    INSERT INTO phone(phone) VALUES(%s) ON CONFLICT DO NOTHING;
    """,(phone,))
    conn.commit()

    #определяем данные для таблицы клиент-телефоны
    cur.execute(""" 
    SELECT phone_id FROM phone WHERE phone=%s;
    """,(phone,))
    phone_id = cur.fetchone()[0]

    # заносим данные в таблицу клиент-телефоны 
    cur.execute("""
    INSERT INTO phone_customer(customer_id, phone_id) VALUES(%s,%s) ON CONFLICT DO NOTHING;
    """,(customer_id, phone_id))
    conn.commit()
      
        

def change_customer(conn, cur, client_id, first_name=None, last_name=None, email=None, phones=None):
    pass

def delete_phone(conn, cur, phone):

  #определяем id телефона
    cur.execute(""" 
    SELECT phone_id FROM phone WHERE phone=%s;
    """,(phone,))
    phone_id = cur.fetchone()[0]

  # удаляем данные из таблицы клиент-телефоны и телефоны (считаем, что номер телефона в базе уникален)
    cur.execute(""" 
    DELETE FROM phone_customer WHERE phone_id=%s;
    """,(phone_id,))
    cur.execute(""" 
    DELETE FROM phone WHERE phone_id=%s;
    """,(phone_id,))
    conn.commit()

def delete_customer(conn, cur, customer_id):
    # получаем адрес электронной почты клиента
    cur.execute(""" 
    SELECT customer_email FROM customer WHERE customer_id=%s;
    """,(customer_id,))
    email_id = cur.fetchone()[0]

    # получаем телефоны клиента
    cur.execute(""" 
    SELECT phone_id FROM phone_customer WHERE customer_id=%s;
    """,(customer_id,))
    phone_id = cur.fetchall()
    
    # удаляем клиента, адрес электронной почты и телефоны клиента
    for i in phone_id:
        if i[0] != '0':
            cur.execute(""" 
            DELETE FROM phone_customer WHERE phone_id=%s;
            """,(i,))
        else:
            continue
    
    
    cur.execute(""" 
    DELETE FROM customer WHERE customer_id=%s;
    """,(customer_id,))

    cur.execute(""" 
    DELETE FROM phone_customer WHERE customer_id=%s;
    """,(customer_id,))

    cur.execute(""" 
    DELETE FROM email WHERE email_id=%s;
    """,(email_id,))

    

    conn.commit()


def find_customer(conn, cur, first_name=None, last_name=None, email=None, phone=None):
    pass







    
with psycopg2.connect(database="task5", user="postgres", password="Maxim0055!!!") as conn:
    
    customers = [
        {'first_name': 'maxim', 'last_name':'pavlenko', 'email':'mpavl@gmail.com'},
        {'first_name': 'maximus', 'last_name':'pavlenko', 'email':'mpavlen@gmail.com', 'phones' : ['89035586168']},
        {'first_name': 'maximus', 'last_name':'pavlenkos', 'email':'mpavlens@gmail.com', 'phones' : ['89055818031', '89055818031','89072251637']}]

    new_phones = [
        {'customer_id':1, 'phone':'89029351516'},
        {'customer_id':1, 'phone':'89029351516'},
        {'customer_id':2, 'phone':'89441634276'}]
    
    with conn.cursor() as cur:
        remove_db(conn, cur)
        create_db(conn, cur)
        print('База данных создана')
        
        for i in customers:
            add_customer(conn, cur, **i)
        print('База данных заполнена')

        for i in new_phones:
            add_phone(conn, cur, **i)
        print('Телефоны добавлены')

        
        
        
        delete_phone(conn, cur, '89441634276')
        print('Номер телефона удален')

        delete_customer(conn, cur, 1)
        print('Клиент удален')
    
conn.close()


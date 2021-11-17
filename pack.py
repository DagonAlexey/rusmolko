import psycopg2
from datetime import datetime, date
import pandas, openpyxl
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime

class Dbpsycopg2():
    def __init__(self):
        self.conn = psycopg2.connect(database="mdb", user="postgres",
        password="12345678", host="localhost", port=5432)
        
    def select(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        return result
    def delete(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        cur.close()
    def update(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        cur.close()
    def insert(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        cur.close()
    def close(self):
        self.conn.close()

def get_excel_report(self, file_dir):
    df = pandas.DataFrame({'Фамилия':self.f, 'Имя':self.i, 'Отчество':self.o, 'Возраст':self.age, 'Дата рождения':self.birthdate, 'Электронная почта':self.email, 'Телефон':self.telephone })
    df.index = df.index + 1
    df.to_excel(file_dir)


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def chek_user(login, password):
    conn = psycopg2.connect(database="mdb", user="postgres",
    password="12345678", host="localhost", port=5432)
    cur = conn.cursor()
    cur.execute(f"""select count(*) from adm_users where login='{login}'""")
    count = 0
    for row in cur: 
        count = int(row[0])
    if count > 0:
        id = []
        password_h = []
        cur.execute(f"""select id, password from adm_users where login='{login}'""")
        for row in cur: 
            id.append(int(row[0]))
            password_h.append(row[1])
        for i in range(len(id)):
            if (check_password_hash(password_h[i], password)):
                return str(id[i])
    else: return None
    cur.close()
    conn.close()

def encode_auth_token(user_id, app_server):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60*60),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app_server.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_auth_token(auth_token, app_server):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app_server.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
        

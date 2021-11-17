import psycopg2
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

conn = psycopg2.connect(database="mdb", user="postgres",
    password="12345678", host="localhost", port=5432)
cur = conn.cursor()

l_f = ["Евдокимов", 
"Кириллов", 
"Чернов", 
"Давыдов", 
"Пономарёв", 
"Егоров", 
"Дьячков", 
"Наумов", 
"Фролов", 
"Емельянов", 
"Емельянов", 
"Авдеев", 
"Капустин", 
"Зайцев", 
"Родионов", 
"Борисов", 
"Петухов", 
"Никитин", 
"Меркушев", 
"Фомичёв"]

l_i = ["Людвиг", 
"Феликс", 
"Борис", 
"Иннокентий", 
"Захар", 
"Владлен", 
"Герасим", 
"Герасим", 
"Даниил", 
"Захар", 
"Рубен", 
"Семен", 
"Клим", 
"Семен", 
"Иосиф", 
"Ким", 
"Аввакум", 
"Мартын", 
"Вольдемар", 
"Бронислав"
]

l_o = ["Георгиевич", 
"Яковлевич", 
"Онисимович", 
"Гордеевич", 
"Богданович", 
"Феликсович", 
"Львович", 
"Эдуардович", 
"Егорович", 
"Святославович", 
"Юрьевич", 
"Данилович", 
"Ростиславович", 
"Владиславович", 
"Улебович", 
"Робертович", 
"Ильяович", 
"Святославович", 
"Куприянович", 
"Мэлсович"]

l_birthdate = ["22.04.1974", 
"05.04.1979", 
"30.11.1982", 
"22.12.1982", 
"13.12.1984", 
"25.05.1987", 
"11.08.1987", 
"08.02.1989", 
"09.09.1992", 
"24.05.1993", 
"10.04.1996", 
"25.09.2000", 
"09.07.2002", 
"22.07.2002", 
"13.10.2005", 
"09.01.2006", 
"18.09.2008", 
"11.07.2012", 
"09.11.2015", 
"21.07.2017"]

l_email = ["o@outlook.com", 
"hr6zdl@yandex.ru", 
"kaft93x@outlook.com", 
"dcu@yandex.ru", 
"19dn@outlook.com", 
"pa5h@mail.ru", 
"281av0@gmail.com", 
"8edmfh@outlook.com", 
"sfn13i@mail.ru", 
"g0orc3x1@outlook.com", 
"rv7bp@gmail.com", 
"93@outlook.com", 
"er@gmail.com", 
"o0my@gmail.com", 
"715qy08@gmail.com", 
"vubx0t@mail.ru", 
"wnhborq@outlook.com", 
"gq@yandex.ru", 
"ic0pu@outlook.com", 
"o7khr@yandex.ru"]

l_telephone = ["17(7926)079-09-93", 
"369(524)920-05-16", 
"934(5076)667-60-69", 
"642(8781)970-53-98", 
"848(173)498-18-67", 
"8(264)430-58-44", 
"231(02)303-39-42", 
"25(870)156-10-56", 
"28(4097)283-67-78", 
"03(8171)274-33-08", 
"97(96)997-25-50", 
"80(5993)168-60-26", 
"855(5274)578-07-28", 
"047(87)568-58-44", 
"006(230)983-95-68", 
"73(72)074-83-33", 
"047(090)599-99-55", 
"830(1371)203-54-06", 
"729(3122)115-79-40", 
"3(30)333-79-88"]


cur.execute("CREATE TABLE public.slist_users (id integer NOT NULL, f character varying(50), i character varying(50), o character varying(50), birthdate date, email character varying(50), telephone character varying(20));")
cur.execute("CREATE TABLE public.adm_users (id integer NOT NULL, login character varying(30), password character varying(200), admin boolean NOT NULL );")
cur.execute("INSERT INTO adm_users (login, password, admin) VALUES (%s, %s, %s)", ("admin", "pbkdf2:sha256:260000$3lvKfbj5Jitl4naS$f0a730dbfe126427e44ed6f0c3abe946117dca09fb010ded11032b1f367aa7e3", True))
cur.execute("INSERT INTO adm_users (login, password, admin) VALUES (%s, %s, %s)", ("user", "pbkdf2:sha256:260000$uajBJY8kJSvgb4Vx$fdc7c5a2c44362a6b62fef1e1ab4bc20c68d76040b33a70faadbcccb8a531867", False))
conn.commit()

for i in range(len(l_f)):
    cur.execute("INSERT INTO list_users (f, i, o, birthdate, email, telephone) VALUES (%s, %s, %s, %s, %s, %s)", (l_f[i], l_i[i], l_o[i], l_birthdate[i], l_email[i], l_telephone[i]))
conn.commit()
conn.close()
from flask import Flask, jsonify, request, send_file
from flask import Flask, request, render_template, session, redirect, url_for, flash, json
import psycopg2, datetime, pack, pandas
from functools import wraps
import jwt #pyjwt==1.4.2
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash


app_server = Flask(__name__, static_folder="static")
app_server.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:12345678@localhost/mdb"
app_server.secret_key = 'Drmhze6EPcv0fN_81Bj-nADrmhze6EPcv0fN_81Bj-nA'


@app_server.route('/')
def index():
    dp = pack.Dbpsycopg2()
    res = dp.select('SELECT f, i, o, birthdate, email, telephone FROM list_users ORDER BY f')
    dp.close()
    list_users = []
    for r in res: list_users.append({'f':r[0], 'i':r[1], 'o':r[2], 'birthdate': r[3].strftime('%d.%m.%Y'), 'age': pack.calculate_age(r[3]), 'email':r[4], 'telephone':r[5]})
    return render_template('index.html', result='yes', list_users=list_users, len_list_users=len(list_users))
 
    

def login_required(var):
    @wraps(var)
    def wrap(*args, **kwargs):
        if 'user' in session:
            return var(*args, **kwargs)
        else: 
            return redirect(url_for('login'))
    return wrap
@app_server.route('/admin')
@login_required
def admin():
    
    dp = pack.Dbpsycopg2()
    list_users_select = dp.select('SELECT id, f, i, o, birthdate, email, telephone FROM list_users ORDER BY f')
    list_users = []
    for r in list_users_select: list_users.append({'_id':r[0], 'f':r[1], 'i':r[2], 'o':r[3], 'birthdate': r[4].strftime('%d.%m.%Y'), 'age': pack.calculate_age(r[4]), 'email':r[5], 'telephone':r[6]})
    

    auth_token  = session['user']
    if request.args.get('message') != None: flash(request.args.get('message'))
    get_id = None
    try: 
        get_id = pack.decode_auth_token(auth_token, app_server)
    except:
        return redirect(url_for('login', message = 'Авторизация просрочена'))
    is_admin = dp.select(f"SELECT admin FROM adm_users WHERE id={get_id};")
    
    adm_users_select = []
    adm_users = []
    if True in is_admin[0]:
        adm_users_select = dp.select('SELECT id, login, password, admin FROM adm_users')
        # print(adm_users_select)
    for r in adm_users_select: adm_users.append({'_id':r[0], 'login':r[1], 'password':r[2], 'admin':r[3]})
    return render_template('/admin.html', result='yes', adm_users=adm_users, len_adm_users=len(adm_users), list_users=list_users, len_list_users=len(list_users))


@app_server.route('/admin/add_adm_user', methods=['POST', 'GET'])
@login_required
def add_adm_user():
    login = request.form.get('login', None)
    password = request.form.get('password', None)
    password2 = request.form.get('password2', None)
    role = request.form.get('role', None)

    dp = pack.Dbpsycopg2()
    auth_token  = session['user']
    get_id = pack.decode_auth_token(auth_token, app_server)    
    is_admin = dp.select(f"SELECT admin FROM adm_users WHERE id={get_id};")
    dp.close()

    if login is None and password is None and password2 is None and role is None:
        return render_template('/form_admin.html', result='yes')
    elif password == password2 and True in is_admin[0]:
        
        dp = pack.Dbpsycopg2()
        dp.insert(f"""INSERT INTO adm_users (login, password, admin) VALUES ('{login}', '{generate_password_hash(password)}', {role})""")
        dp.close()
        return redirect(url_for('admin', message = 'Пользователь успешно добавлен'))
    else: 
        return redirect(url_for('admin', message = 'Что то пошло не так'))



@app_server.route('/admin/del_adm_user/<int:id_user>')
@login_required
def del_adm_user(id_user):
    dp = pack.Dbpsycopg2()
    
    try:
        auth_token  = session['user']
        get_id = pack.decode_auth_token(auth_token, app_server)    
        is_admin = dp.select(f"SELECT admin FROM adm_users WHERE id={get_id};")
        if True in is_admin[0]:
            list_users_del = dp.delete(f"""DELETE FROM adm_users WHERE id={id_user}""")
            dp.close()
            return redirect(url_for('admin', message = 'Удаление успешно выполнено'))
        else: return redirect(url_for('admin', message = 'Ошибка при удалении'))
    except Exception as e:
        dp.close()
        print(e)
        return redirect(url_for('admin', message = 'Ошибка при удалении'))

@app_server.route('/admin/del_list_user/<int:id_user>')
@login_required
def del_list_user(id_user):
    dp = pack.Dbpsycopg2()
    try:
        list_users_del = dp.delete(f"""DELETE FROM list_users WHERE id={id_user}""")
        dp.close()
        return redirect(url_for('admin', message = 'Удаление успешно выполнено'))
    except Exception as e:
        dp.close()
        print(e)
        return redirect(url_for('admin', message = 'Ошибка при удалении')) 

@app_server.route('/admin/add_list_user/<int:id_user>', methods=['POST', 'GET'])
@login_required
def add_list_user(id_user):
    lastname = request.form.get('lastname', None)
    firstname = request.form.get('firstname', None)
    patronymic = request.form.get('patronymic', None)
    birth_date = request.form.get('birth_date', None)
    e_mail = request.form.get('e_mail', None)
    phone = request.form.get('phone', None)
    print(lastname, firstname, patronymic, birth_date, e_mail, phone)
    user = {}
    if id_user == 0:
        user = {'id':'0', 'lastname':'', 'firstname':'', 'patronymic':'', 'birthdate': '', 'e_mail':'', 'phone':''}
    else: 
        dp = pack.Dbpsycopg2()
        get_user = dp.select(f'SELECT f, i, o, birthdate, email, telephone FROM list_users WHERE id={id_user}')
        get_user = get_user[0]
        user = {'id':id_user, 'lastname':get_user[0], 'firstname':get_user[1], 'patronymic':get_user[2], 'birthdate':get_user[3].strftime('%d.%m.%Y'), 'e_mail':get_user[4], 'phone':get_user[5]}
        print(user)
        dp.close()

    if (lastname is None and firstname is None and patronymic is None and birth_date is None and e_mail is None and phone is None):
        return render_template('form_user.html', result='yes', user=user)
    elif (id_user == 0):
        dp = pack.Dbpsycopg2()
        dp.insert(f"""INSERT INTO list_users (f, i, o, birthdate, email, telephone) VALUES ('{lastname}', '{firstname}', '{patronymic}', '{datetime.strptime(birth_date, '%d.%m.%Y').date()}', '{e_mail}', '{phone}')""")
        dp.close()
        return redirect(url_for('admin', message = 'Успешно выполнено'))
    elif (id_user != 0):
        user = {'id':id_user, 'lastname':lastname, 'firstname':firstname, 'patronymic':patronymic, 'birthdate': birth_date, 'e_mail':e_mail, 'phone':phone}
        dp = pack.Dbpsycopg2()
        dp.update(f"""UPDATE list_users SET f='{lastname}', i='{firstname}', o='{patronymic}', birthdate='{datetime.strptime(birth_date, '%d.%m.%Y').date()}', email='{e_mail}', telephone='{phone}' WHERE id={id_user}""")
        dp.close()
        return redirect(url_for('admin', message = 'Успешно изменено'))
        
    

@app_server.route('/login', methods=['POST', 'GET'])
def login():
        login = request.form.get('login', None)
        password = request.form.get('password', None)
        if (login is None and password is None):
            return render_template('/login.html', result='yes')
        id = pack.chek_user(login, password)
        print(id)
        if (id == None):
            flash('Неверная пара логин и пароль')
            return render_template('/login.html', result='yes')
        else:
            session['user'] = pack.encode_auth_token(id, app_server)
            return redirect(url_for('admin'))
            

@app_server.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app_server.route('/download')
def xlsx_report():
    dp = pack.Dbpsycopg2()
    res = dp.select('SELECT f, i, o, birthdate, email, telephone FROM list_users ORDER BY f')
    dp.close()
    l_f, l_i, l_o, l_age, l_birthdate, l_email, l_telephone = [],[],[],[],[],[],[]
    dict_pandas = {}
    if (len(res) > 0):
        for r in res:
            l_f.append(r[0])
            l_i.append(r[1])
            l_o.append(r[2])
            l_age.append(pack.calculate_age(r[3]))
            l_birthdate.append(r[3].strftime('%d.%m.%Y'))
            l_email.append(r[4])
            l_telephone.append(r[5])
        for f in res:
            dict_pandas = {'Фамилия':l_f, 'Имя':l_i, 'Отчество':l_o, 'Возраст':l_age, 'Дата рождения':l_birthdate, 'Электронная почта':l_email, 'Телефон':l_telephone }
    df = pandas.DataFrame(dict_pandas)
    df.index = df.index + 1
    df.to_excel('static/download/Список пользователей.xlsx')

    return send_file('static/download/Список пользователей.xlsx',
                     mimetype='xlsx',
                     attachment_filename='Список пользователей.xlsx',
                     as_attachment=True)

if __name__ == "__main__":
    app_server.run(debug=True)
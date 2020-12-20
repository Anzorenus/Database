import psycopg2
from sqlalchemy import create_engine

fin = open('create.sql')
create_func = fin.read()
fin.close()
fin = open('fun.sql')
func = fin.read()
fin.close()


def connect_as_creator(username_creator, password_creator, main_db, create_func):
    engine = create_engine("postgresql+psycopg2://{}:{}@localhost/{}".format(username_creator, password_creator, main_db), echo=True)
    cursor = engine.connect()
    cursor.execute(create_func)
    return cursor


def create_database(db_name, username, create_func=create_func):
    cursor = connect_as_creator('admin', 'admin', 'laba', create_func)
    cursor.execute('SELECT create_db(\'{}\', \'{}\')'.format(db_name, username))
    cursor.close()


def drop_database(db_name, create_func=create_func):
    cursor = connect_as_creator('admin', 'admin', 'laba', create_func)
    cursor.execute('SELECT drop_db(\'{}\')'.format(db_name))


def connect_as_user(username, password, db_name, functions=func):
    connection = psycopg2.connect(host='127.0.0.1', database=db_name, user=username, password=password)
    cursor = connection.cursor()
    cursor.execute(functions)
    connection.commit()
    return connection


def disconnect_user(connection):
    connection.close()


def clear_all_tables(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_all_tables()')
    connection.commit()


def clear_employee(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_employee()')
    connection.commit()


def clear_bank(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_bank()')
    connection.commit()


def clear_department(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_department()')
    connection.commit()


def add_to_department(connection, new_id, new_name, new_phone, new_kpi):
    cursor = connection.cursor()
    cursor.execute('SELECT add_to_department({}, \'{}\', \'{}\', {})'.format(new_id, new_name, new_phone, new_kpi))
    connection.commit()


def add_to_bank(connection, new_id, new_name, new_address, new_interest):
    cursor = connection.cursor()
    cursor.execute('SELECT add_to_bank({}, \'{}\', \'{}\', {})'.format(new_id, new_name, new_address, new_interest))
    connection.commit()


def add_to_employee(connection, new_id, new_name, new_department, new_mobile_phone, new_bank, new_salary, new_prize):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT add_to_employee({}, \'{}\', {}, \'{}\', {}, {}, {})'.format(new_id, new_name, new_department, new_mobile_phone, new_bank, new_salary, new_prize))
    connection.commit()


def search_employee_by_mobile_phone(connection, mobile_phone):
    cursor = connection.cursor()
    cursor.execute('SELECT search_employee_by_mobile_phone(\'{}\')'.format(mobile_phone))
    table = cursor.fetchall()
    return table


def update_employee(connection, new_id, new_name, new_department, new_mobile_phone, new_bank, new_salary, new_prize):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT update_employee({}, \'{}\', {}, \'{}\', {}, {}, {})'.format(new_id, new_name, new_department, new_mobile_phone, new_bank, new_salary, new_prize))
    connection.commit()


def delete_employee_by_mobile_phone(connection, mobile_phone):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_employee_by_mobile_phone(\'{}\')'.format(mobile_phone))
    connection.commit()


def delete_employee_by_id(connection, new_id):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_employee_by_id({})'.format(new_id))
    connection.commit()


def delete_department_by_id(connection, new_id):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_department_by_id({})'.format(new_id))
    connection.commit()


def delete_bank_by_id(connection, new_id):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_bank_by_id({})'.format(new_id))
    connection.commit()


def print_table_department(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT print_table_department()')
    table = cursor.fetchall()
    return table


def print_table_bank(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT print_table_bank()')
    table = cursor.fetchall()
    return table


def print_table_employee(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT print_table_employee()')
    table = cursor.fetchall()
    return table

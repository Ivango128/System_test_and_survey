import os
from dotenv import load_dotenv

def laad_dotenv_first_power():
    load_dotenv()
    host_bd = os.getenv('host')
    port_bd = os.getenv('port')
    user_bd = os.getenv('user')
    password_bd = os.getenv('password')
    dbname_bd = os.getenv('db_name')
    password_admin = os.getenv('password_admin')
    if host_bd is None:
        host_bd = 'localhost'
    if port_bd is None:
        port_bd = 3306
    if user_bd is None:
        user_bd = 'root'
    if password_bd is None:
        password_bd = 'password'
    if dbname_bd is None:
        dbname_bd = 'mydb'
    return host_bd, port_bd, user_bd, password_bd, dbname_bd, password_admin
def load_dotenv_SK():
    load_dotenv()
    return os.getenv('seceretKey')
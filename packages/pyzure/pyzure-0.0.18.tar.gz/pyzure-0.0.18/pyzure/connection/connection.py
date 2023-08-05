from pyzure.connection.azure_credentials import credential
import pyodbc


def connect(instance):
    credentials = credential(instance)
    driver = credentials.get("driver")
    server = credentials.get("server")
    port = credentials.get("port")
    database = credentials.get("database")
    username = credentials.get("username")
    password = credentials.get("password")
    connection_string = 'SERVER=' + server + ';PORT=' + port + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password
    if driver:
        connection_string = 'DRIVER=' + driver + ';' + connection_string
    cnxn = pyodbc.connect(connection_string)

    return cnxn

import os
import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME')
    )
    return connection

def test_connection():
    # Cria uma conexão com o banco de dados
    connection = create_connection()

    # Cria um cursor
    cursor = connection.cursor()

    # Executa uma consulta SQL para buscar todas as tabelas
    cursor.execute("SHOW TABLES")

    # Busca todos os resultados da consulta
    tables = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    connection.close()

    # Imprime as tabelas
    for table in tables:
        print(table)

# Chama a função para testar a conexão
test_connection()
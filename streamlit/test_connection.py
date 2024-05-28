import streamlit as st
import mysql.connector

def test_connection():
    st.title("Teste de Conexão")
    try:
        cnx = mysql.connector.connect(user='root',
                                      password='1234vc',
                                      host='localhost',
                                      database='bibliotech')
        if cnx.is_connected():
            st.success("Conexão bem sucedida!")
        else:
            st.error("Falha na conexão.")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

test_connection()
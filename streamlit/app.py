import streamlit as st
import mysql.connector

# Conecte-se ao banco de dados MySQL
cnx = mysql.connector.connect(user='root', 
                              password='123456vc',
                              host='localhost',
                              database='bibliotech')

# Crie um cursor
cursor = cnx.cursor()

# Página de login
def login():
    st.title("Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        # Verifique as credenciais do usuário
        query = "SELECT * FROM usuarios WHERE usuario = %s AND senha = %s"
        cursor.execute(query, (usuario, senha))
        resultado = cursor.fetchone()
        if resultado:
            st.success("Entrou com sucesso")
            menu_principal()
        else:
            st.error("Usuário ou senha inválidos")

# Menu principal
def menu_principal():
    st.title("Menu Principal")
    opcao_menu = st.selectbox("Escolha uma opção", ["Reservar um livro", "Alugar um livro", "Comprar um livro", "Ver livros comprados ou alugados"])
    if opcao_menu == "Reservar um livro":
        reservar_livro()
    elif opcao_menu == "Alugar um livro":
        alugar_livro()
    elif opcao_menu == "Comprar um livro":
        comprar_livro()
    elif opcao_menu == "Ver livros comprados ou alugados":
        ver_livros()

# As funções reservar_livro, alugar_livro, comprar_livro e ver_livros precisam ser implementadas
# ...

# Inicie o aplicativo na página de login
login()
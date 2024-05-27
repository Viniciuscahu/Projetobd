import streamlit as st
import mysql.connector

# Conecte-se ao banco de dados MySQL
cnx = mysql.connector.connect(user='root', 
                              password='123456vc',
                              host='localhost',
                              database='bibliotech')

# Crie um cursor
cursor = cnx.cursor()

def tela_inicial():
    st.title("Bem-vindo ao nosso sistema de biblioteca")
    opcao_tela = st.sidebar.selectbox("Escolha uma opção", ["Login", "Cadastro"])
    if opcao_tela == "Login":
        login()
    elif opcao_tela == "Cadastro":
        cadastro()

def cadastro():
    st.title("Cadastro")
    nome = st.text_input("Nome")
    telefone = st.text_input("Telefone")
    email = st.text_input("Email")
    cpf = st.text_input("CPF")
    endereco = st.text_input("Endereço")
    if st.button("Cadastrar"):
        # Aqui você pode adicionar a lógica para salvar as informações do usuário no banco de dados
        query = "INSERT INTO usuarios (nome, telefone, email, cpf, endereco) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, telefone, email, cpf, endereco))
        cnx.commit()
        st.success("Usuário cadastrado com sucesso!")

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
def reservar_livro():
    st.title("Reservar um Livro")
    nome_livro = st.text_input("Nome do Livro")
    if st.button("Reservar"):
        # Aqui você pode adicionar a lógica para reservar o livro no banco de dados
        query = "UPDATE livros SET reservado = 1 WHERE nome = %s"
        cursor.execute(query, (nome_livro,))
        cnx.commit()
        st.success("Livro reservado com sucesso!")

def menu_principal():
    st.title("Menu Principal")
    opcao_menu = st.sidebar.selectbox("Escolha uma opção", ["Reservar um livro", "Alugar um livro", "Comprar um livro", "Ver livros comprados ou alugados"])
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
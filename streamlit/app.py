import streamlit as st
import mysql.connector

# Conecte-se ao banco de dados MySQL
cnx = mysql.connector.connect(user='root', 
                              password='1234vc',
                              host='localhost',
                              database='bibliotech')

cursor = cnx.cursor()

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "cart" not in st.session_state:
        st.session_state["cart"] = []
    if "purchased_books" not in st.session_state:
        st.session_state["purchased_books"] = []

    if st.session_state["logged_in"]:
        menu_principal()
    else:
        login_menu()

def login_menu():
    st.sidebar.title("Menu")
    opcao_menu = st.sidebar.selectbox("Escolha uma opção", ["Login", "Cadastro"], key="login_menu")

    if opcao_menu == "Login":
        login()
    elif opcao_menu == "Cadastro":
        cadastro()

def cadastro():
    st.title("Cadastro")
    nome = st.text_input("Nome", key="cadastro_nome")
    telefone = st.text_input("Telefone", key="cadastro_telefone")
    email = st.text_input("Email", key="cadastro_email")
    cpf = st.text_input("CPF", key="cadastro_cpf")
    endereco = st.text_input("Endereço", key="cadastro_endereco")
    senha = st.text_input("Senha", type='password', key="cadastro_senha") 

    if st.button("Cadastrar", key="cadastro_button"):
        query_check_cpf = "SELECT * FROM usuarios WHERE cpf = %s"
        cursor.execute(query_check_cpf, (cpf,))
        result_cpf = cursor.fetchall()

        query_check_telefone = "SELECT * FROM usuarios WHERE telefone = %s"
        cursor.execute(query_check_telefone, (telefone,))
        result_telefone = cursor.fetchall()

        query_check_email = "SELECT * FROM usuarios WHERE email = %s"
        cursor.execute(query_check_email, (email,))
        result_email = cursor.fetchall()

        if result_cpf:
            st.error("CPF já cadastrado.")
        elif result_telefone:
            st.error("Telefone já cadastrado.")
        elif result_email:
            st.error("Email já cadastrado.")
        else:
            query = "INSERT INTO usuarios (nome, telefone, email, cpf, endereco, senha) VALUES (%s, %s, %s, %s, %s, %s)"
            try:
                cursor.execute(query, (nome, telefone, email, cpf, endereco, senha))  
                cnx.commit()
                st.success("Usuário cadastrado com sucesso!")
            except Exception as e:
                st.error(f"Ocorreu um erro ao cadastrar o usuário: {e}")

def login():
    st.title("Login")
    usuario = st.text_input("Usuário", key="login_usuario")
    senha = st.text_input("Senha", type="password", key="login_senha")
    

    if st.button("Entrar", key="login_button"):
        query = "SELECT id FROM usuarios WHERE nome = %s AND senha = %s"
        cursor.execute(query, (usuario, senha))
        result = cursor.fetchone()

        if result:
            st.success("Login bem-sucedido!")
            st.session_state["logged_in"] = True
            st.session_state["usuario_id"] = result[0] 
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
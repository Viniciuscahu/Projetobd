import streamlit as st

def tela_inicial():
    st.title("Bem-vindo à BiblioTech!")
    
    st.sidebar.header("Usuário")
    opcao_usuario = st.sidebar.selectbox("", ["Login", "Cadastro"], key='user')
    if opcao_usuario == "Login":
        st.subheader("Login")
        login()
    elif opcao_usuario == "Cadastro":
        st.subheader("Cadastro")
        cadastro()
    
    st.sidebar.header("Funcionalidades")
    opcao_funcionalidade = st.sidebar.selectbox("", ["Alugar Livro", "Comprar Livro", "Ver Livros"], key='func')
    if opcao_funcionalidade == "Alugar Livro":
        st.subheader("Alugar Livro")
        alugar_livro()
    elif opcao_funcionalidade == "Comprar Livro":
        st.subheader("Comprar Livro")
        comprar_livro()
    elif opcao_funcionalidade == "Ver Livros":
        st.subheader("Seus Livros")
        ver_livros()

def login():
    usuario = st.text_input("Nome de usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        # Aqui você pode adicionar a lógica para verificar o nome de usuário e a senha
        pass

def cadastro():
    nome = st.text_input("Nome")
    telefone = st.text_input("Telefone")
    email = st.text_input("Email")
    cpf = st.text_input("CPF")
    endereco = st.text_input("Endereço")
    senha = st.text_input("Senha", type="password")
    if st.button("Cadastrar"):
        # Aqui você pode adicionar a lógica para cadastrar o usuário
        pass

def alugar_livro():
    # Aqui você pode adicionar a lógica para alugar um livro
    pass

def comprar_livro():
    # Aqui você pode adicionar a lógica para comprar um livro
    pass

def ver_livros():
    # Aqui você pode adicionar a lógica para mostrar os livros do usuário
    pass

tela_inicial()
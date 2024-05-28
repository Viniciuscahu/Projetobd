import streamlit as st
import mysql.connector

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

def menu_principal():
    st.sidebar.title("Menu")

    opcoes_menu = ["Filtragem", "Catálogo", "Carrinho", "Compras", "Criar Anúncio", "Top Livros", "Meus Anúncios"]
    opcao_selecionada = st.sidebar.selectbox("Escolha uma opção", opcoes_menu)

    if st.sidebar.button('Logout'):
        st.session_state["logged_in"] = False
        st.session_state["usuario_id"] = None
        st.success('Logout realizado com sucesso!')


    if opcao_selecionada == "Filtragem":
        mostrar_filtro()
    elif opcao_selecionada == "Catálogo":
        mostrar_catalogo()
    elif opcao_selecionada == "Carrinho":
        mostrar_carrinho()
    elif opcao_selecionada == "Compras":
        mostrar_compras()
    elif opcao_selecionada == "Criar Anúncio":
        criar_anuncio()
    elif opcao_selecionada == "Top Livros":
        mostrar_top_livros()
    elif opcao_selecionada == "Meus Anúncios":
        mostrar_meus_anuncios()
def mostrar_meus_anuncios():
    st.title("Meus Anúncios")

    query = "SELECT * FROM catalogo WHERE usuario_id = %s"
    cursor.execute(query, (st.session_state["usuario_id"],))
    anuncios = cursor.fetchall()

    for anuncio in anuncios:
        st.subheader(anuncio[1])
        st.write(f"Autor: {anuncio[2]}")
        st.write(f"Ano: {anuncio[3]}")
        st.write(f"Preço: R${anuncio[4]:.2f}")

        if st.button("Editar Anúncio", key=f"editar_anuncio_{anuncio[0]}"):
            editar_anuncio(anuncio)
        
        if st.button("Excluir Anúncio", key=f"excluir_anuncio_{anuncio[0]}"):
            excluir_anuncio(anuncio[0])

def excluir_anuncio(anuncio_id):
    query = "DELETE FROM catalogo WHERE id = %s"
    cursor.execute(query, (anuncio_id,))
    cnx.commit()
    st.success("Anúncio excluído com sucesso!")

def editar_anuncio(anuncio):
    st.title("Editar Anúncio")

    with st.form(key='edit_form'):
        nome = st.text_input("Nome do Livro", value=anuncio[1], key="editar_anuncio_nome")
        autor = st.text_input("Autor do Livro", value=anuncio[2], key="editar_anuncio_autor")
        ano = st.text_input("Ano de Publicação", value=anuncio[3], key="editar_anuncio_ano")
        preco = st.number_input("Preço do Livro", value=float(anuncio[4]), min_value=0.0, format="%.2f", key="editar_anuncio_preco")

        submit_button = st.form_submit_button(label='Salvar Alterações')

    if submit_button:
        query = "UPDATE catalogo SET nome = %s, autor = %s, ano_publicacao = %s, preco = %s WHERE id = %s"
        cursor.execute(query, (nome, autor, ano, preco, anuncio[0]))
        cnx.commit()
        st.success("Anúncio atualizado com sucesso!")
def mostrar_top_livros():
    st.title("Top Livros")

    query = """
    SELECT livro_id, nome, AVG(avaliacao) as media_avaliacao
    FROM avaliacoes
    JOIN catalogo ON avaliacoes.livro_id = catalogo.id
    GROUP BY livro_id, nome
    ORDER BY media_avaliacao DESC
    LIMIT 5
    """

    try:
        cursor.execute(query)
        top_livros = cursor.fetchall()

        for livro in top_livros:
            st.subheader(livro[1])
            st.write(f"Média de Avaliação: {livro[2]:.2f}")
    except Exception as e:
        st.error(f"Erro ao executar consulta SQL: {e}")
def mostrar_catalogo():
    st.title("Catálogo de Livros")

    query = "SELECT * FROM catalogo"
    cursor.execute(query)
    livros = cursor.fetchall()

    if not livros:   
        st.warning("Nenhum livro disponível no catálogo.")
    else:
        for livro in livros:
            st.subheader(livro[1])
            st.write(f"Autor: {livro[2]}")
            st.write(f"Ano: {livro[3]}")
            st.write(f"Preço: R${livro[4]:.2f}")

            if st.button("Adicionar ao Carrinho", key=f"add_to_cart_{livro[0]}"):
                adicionar_ao_carrinho(livro)

def adicionar_ao_carrinho(livro):
    st.session_state["cart"].append(livro)
    st.success("Livro adicionado ao carrinho com sucesso!")           
        
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
            st.error("Usuário ou senha incorretos.")

def mostrar_filtro():
    st.title("Filtragem de Livros")
    st.subheader("Pesquisar Livros")

    titulo_filtro = st.text_input("Título do Livro")
    autor_filtro = st.text_input("Autor")
    ano_filtro = st.text_input("Ano de Publicação")
    faixa_preco_filtro = st.slider("Faixa de Preço", 0.0, 100.0, (0.0, 100.0))

    preco_min, preco_max = faixa_preco_filtro

    query = "SELECT * FROM catalogo WHERE 1=1"
    if titulo_filtro:
        query += f" AND nome LIKE '%{titulo_filtro}%'"
    if autor_filtro:
        query += f" AND autor LIKE '%{autor_filtro}%'"
    if ano_filtro:
        query += f" AND ano_publicacao = {ano_filtro}"
    query += f" AND preco BETWEEN {preco_min} AND {preco_max}"

    try:
        cursor.execute(query)
        livros = cursor.fetchall()

        for livro in livros:
            st.subheader(livro[1])
            st.write(f"Autor: {livro[2]}")
            st.write(f"Ano: {livro[3]}")
            st.write(f"Preço: R${livro[4]:.2f}")

            st.write("Deixe sua avaliação (1 a 5):")
            avaliacao = st.slider("Avaliação", 1, 5, 3, key=f"avaliacao_{livro[0]}")
            comentario = st.text_area("Comentário", key=f"comentario_{livro[0]}")
            if st.button("Enviar Avaliação", key=f"enviar_avaliacao_{livro[0]}"):

                query_insert_avaliacao = "INSERT INTO avaliacoes (livro_id, usuario_id, avaliacao, comentario) VALUES (%s, %s, %s, %s)"
                try:
                    cursor.execute(query_insert_avaliacao, (livro[0], st.session_state["usuario_id"], avaliacao, comentario))
                    cnx.commit()
                    st.success("Avaliação enviada com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao enviar avaliação: {e}")
    except Exception as e:
        st.error(f"Erro ao executar consulta SQL: {e}")

def criar_anuncio():
    st.title("Criar Anúncio de Livro")
    nome = st.text_input("Nome do Livro", key="anuncio_nome")
    autor = st.text_input("Autor do Livro", key="anuncio_autor")
    ano = st.text_input("Ano de Publicação", key="anuncio_ano")
    preco = st.number_input("Preço do Livro", min_value=0.0, format="%.2f", key="anuncio_preco")

    if st.button("Criar Anúncio"):
        query = "INSERT INTO catalogo (nome, autor, ano_publicacao, preco, usuario_id) VALUES (%s, %s, %s, %s, %s)"
        try:
          
            cursor.execute(query, (nome, autor, ano, preco, st.session_state["usuario_id"]))
            cnx.commit()
            st.success("Anúncio criado com sucesso!")
        except Exception as e:
            st.error(f"Ocorreu um erro ao criar o anúncio: {e}")
def mostrar_carrinho():
    st.title("Meu Carrinho")
    if len(st.session_state["cart"]) == 0:
        st.write("Seu carrinho está vazio.")
    else:
        total = 0
        for item in st.session_state["cart"]:
            st.write(f"{item[1]} - R${item[4]:.2f}")
            total += item[4]
        st.write(f"Total: R${total:.2f}")
        if st.button('Pagar'):
            st.success("O pagamento foi processado com sucesso!")
            st.session_state["purchased_books"].extend(st.session_state["cart"])
            st.session_state["cart"] = []
            for book in st.session_state["purchased_books"]:
                cursor.execute("INSERT INTO livros_comprados (nome, autor, ano_publicacao, preco) VALUES (%s, %s, %s, %s)", (book[1], book[2], book[3], book[4]))
            cnx.commit()

def mostrar_compras():
    st.title("Livros Comprados")
    cursor.execute("SELECT * FROM livros_comprados")
    st.session_state["purchased_books"] = cursor.fetchall()
    if len(st.session_state["purchased_books"]) == 0:
        st.write("Você ainda não comprou nenhum livro.")
    else:
        for livro in st.session_state["purchased_books"]:
            st.write(f"{livro[1]} - R${livro[4]:.2f}")

def logout():
    if st.button('Logout'):
        st.session_state["logged_in"] = False
        st.session_state["usuario_id"] = None
        st.success("Logout realizado com sucesso!")

if __name__ == "__main__":
    main()
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
    

    opcoes_menu = ["Feedbacks", "Catálogo", "Carrinho", "Compras", "Criar Anúncio", "Top Livros", "Meus Anúncios"]
    opcao_selecionada = st.sidebar.selectbox("Escolha uma opção", opcoes_menu)

    if st.sidebar.button('Logout'):
        st.session_state["logged_in"] = False
        st.session_state["usuario_id"] = None
        st.success('Logout realizado com sucesso!')


    if opcao_selecionada == "Feedbacks":
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
    global cnx
    st.title("Meus Anúncios")

    cursor = cnx.cursor()
    query = "SELECT * FROM livros WHERE usuario_id = %s"
    cursor.execute(query, (st.session_state["usuario_id"],))
    anuncios = cursor.fetchall()

    if len(anuncios) == 0:
        st.write("Você ainda não criou nenhum anúncio.")
    else:
        for anuncio in anuncios:
            st.subheader(anuncio[1]) 
            st.text(anuncio[2])  
            if st.button('Excluir', key=f"excluir_{anuncio[0]}"):
                excluir_anuncio(anuncio[0])

    cursor.close() 

def excluir_anuncio(livro_id):
    cursor = cnx.cursor()
    query = "DELETE FROM avaliacoes WHERE livro_id = %s"
    cursor.execute(query, (livro_id,))
    cnx.commit()
    query = "DELETE FROM livros WHERE id = %s"
    try:
        cursor.execute(query, (livro_id,))
        cnx.commit()
        st.success("Anúncio excluído com sucesso!")
    except Exception as e:
        st.error(f"Erro ao excluir anúncio: {e}")

    cursor.close()


def mostrar_top_livros():
    st.title("Top Livros")

    query = """
    SELECT livros.*, editora.nome AS editora, AVG(avaliacoes.avaliacao) as avaliacao_media
    FROM livros
    LEFT JOIN avaliacoes ON livros.id = avaliacoes.livro_id
    INNER JOIN editora ON livros.editora_id = editora.id
    GROUP BY livros.id
    ORDER BY avaliacao_media DESC
    LIMIT 10
    """
    cursor.execute(query)
    livros = cursor.fetchall()

    for livro in livros:
        with st.container():
            st.subheader(livro[1])
            st.write(f"Autor: {livro[2]}")
            st.write(f"Ano: {livro[3]}")
            st.write(f"Preço: R${livro[4]:.2f}")
            st.write(f"Avaliação Média: {livro[5]:.2f}")
            st.write(f"Editora: {livro[8]}")
            
        query_avaliacoes = """
        SELECT avaliacoes.*, usuarios.nome
        FROM avaliacoes
        INNER JOIN usuarios ON avaliacoes.usuario_id = usuarios.id
        WHERE avaliacoes.livro_id = %s
        """
        cursor.execute(query_avaliacoes, (livro[0],))
        avaliacoes = cursor.fetchall()

        for avaliacao in avaliacoes:
            with st.expander(f"Avaliação por {avaliacao[5]}"):
                st.write(f"Avaliação: {avaliacao[3]}")
                st.write(f"Comentário: {avaliacao[4]}")
                
def mostrar_catalogo():
    st.title("Catálogo")

    autor = st.text_input("Filtrar por autor")
    editora = st.text_input("Filtrar por editora")

    autor = "%" if autor == "" else autor
    editora = "%" if editora == "" else editora

    try:
        cursor = cnx.cursor()
        query = """
        SELECT livros.*, editora.nome AS editora_nome
        FROM livros
        JOIN autor ON livros.autor_id = autor.id
        JOIN editora ON livros.editora_id = editora.id
        WHERE autor.nome LIKE %s AND editora.nome LIKE %s
        """
        cursor.execute(query, (f"%{autor}%", f"%{editora}%"))
        livros = cursor.fetchall()

        for livro in livros:
            with st.expander(livro[1], expanded=True):
                st.write(f"Nome: {livro[1]}")
                st.write(f"Autor: {livro[2]}")
                st.write(f"Editora: {livro[8]}") 
                st.write(f"Ano de Publicação: {livro[3]}")
                st.write(f"Preço: R${livro[5]:.2f}")

                if st.button("Adicionar ao Carrinho", key=f"add_to_cart_{livro[0]}"):
                    adicionar_ao_carrinho(livro)

    except mysql.connector.Error as e:
        st.error(f"Ocorreu um erro ao buscar os livros: {e}")
    finally:
        cursor.close()

    if not livros:   
        st.warning("Nenhum livro disponível no catálogo.")
                
def adicionar_ao_carrinho(livro):
    cursor = None
    try:
        if cnx.is_connected():
            cursor = cnx.cursor()
            query = """
                INSERT INTO carrinho (usuario_id, livro_id, nome, autor, editora, ano_publicacao, preco)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (st.session_state["usuario_id"], livro[0], livro[1], livro[2], livro[-1], livro[3], livro[4]))
            cnx.commit()
            st.success("Livro adicionado ao carrinho com sucesso!")
        else:
            st.error("A conexão com o banco de dados não está disponível.")
    except mysql.connector.Error as e:
        st.error(f"Ocorreu um erro ao adicionar o livro ao carrinho: {e}")
    finally:
        if cursor is not None:
            cursor.close()
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
    st.title("Feedback dos Livros")
    st.subheader("Pesquisar Livros")

    titulo_filtro = st.text_input("Título do Livro")
    autor_filtro = st.text_input("Autor")
    editora_filtro = st.text_input("Editora")
    ano_filtro = st.text_input("Ano de Publicação")
    preco_min = st.number_input("Preço mínimo", min_value=0.0, step=0.1, value=None)
    preco_max = st.number_input("Preço máximo", min_value=0.0, step=0.1, value=None)

    query = "SELECT * FROM livros WHERE 1=1"
    if titulo_filtro:
        query += f" AND nome LIKE '%{titulo_filtro}%'"
    if autor_filtro:
        query += f" AND autor LIKE '%{autor_filtro}%'"
    if ano_filtro:
        query += f" AND ano_publicacao = {ano_filtro}"
    if editora_filtro:
        query += f" AND editora_nome LIKE '%{editora_filtro}%'" 
    if preco_min is not None and preco_max is not None:
        query += f" AND preco BETWEEN {preco_min} AND {preco_max}"


    try:
        cursor.execute(query)
        livros = cursor.fetchall()

        for livro in livros:
            st.subheader(livro[1])
            st.write(f"Autor: {livro[2]}")
            st.write(f"Ano: {livro[3]}")
            st.write(f"Preço: R${livro[4]:.2f}")
            st.write(f"Editora: {livro[8]}")

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
    autor = st.text_input("Nome do Autor", key="anuncio_autor")
    ano = st.number_input("Ano de Publicação", min_value=0, max_value=9999, step=1, format="%i", key="anuncio_ano")
    preco = st.number_input("Preço do Livro", min_value=0.0, format="%.2f", key="anuncio_preco")
    editora = st.text_input("Nome da Editora", key="anuncio_editora")
   

    if st.button("Criar Anúncio"):
        try:
            cursor = cnx.cursor()

            query_autor = "INSERT INTO autor (nome) VALUES (%s)"
            cursor.execute(query_autor, (autor,))
            autor_id = cursor.lastrowid

   
            query_editora = "INSERT INTO editora (nome) VALUES (%s)"
            cursor.execute(query_editora, (editora,))
            editora_id = cursor.lastrowid

            usuario_id = st.session_state.get("usuario_id", None)
            if usuario_id is None:
                st.error("Você precisa estar logado para criar um anúncio.")
                return

    
            query_livro = "INSERT INTO livros (nome, autor, autor_id, ano_publicacao, preco, usuario_id, editora_id, editora_nome) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query_livro, (nome, autor, autor_id, ano, preco, usuario_id, editora_id, editora))
            cnx.commit()

            st.success("Anúncio criado com sucesso!")
        except mysql.connector.Error as e:
            st.error(f"Ocorreu um erro ao criar o anúncio: {e}")
        finally:
            cursor.close()
            cnx.close()
            
def mostrar_carrinho():
    st.title("Meu Carrinho")

    cursor = cnx.cursor()
    query = """
    SELECT carrinho.*, livros.nome AS livro_nome
    FROM carrinho
    JOIN livros ON carrinho.livro_id = livros.id
    WHERE carrinho.usuario_id = %s
    """
    cursor.execute(query, (st.session_state["usuario_id"],))
    livros_no_carrinho = cursor.fetchall()

    if len(livros_no_carrinho) == 0:
        st.write("Seu carrinho está vazio.")
    else:
        total = 0
        for livro in livros_no_carrinho:
            preco = 0
            try:
                preco = float(livro[6])
                total += preco
            except ValueError:
                st.write(f"Preço: {livro[4]} (não foi possível converter para float)")

            with st.expander(livro[3]):   
                st.write(f"Autor: {livro[4]}")
                st.write(f"Editora: {livro[7]}")  
                st.write(f"Ano de publicação: {livro[5]}")
                st.write(f"Preço: R${preco:.2f}")
                
                if st.button(f'Pagar por {livro[-1]}', key=livro[0]):  
                    st.success(f"O pagamento por {livro[-1]} foi processado com sucesso!")
                    cursor.execute("INSERT INTO livros_comprados (usuario_id, nome, autor, editora, ano_publicacao, preco) VALUES (%s, %s, %s, %s, %s, %s)", (st.session_state["usuario_id"], livro[3], livro[4], livro[7], livro[5], preco))
                    cnx.commit()
                    cursor.execute("DELETE FROM carrinho WHERE id = %s", (livro[0],))
                    cnx.commit()
                if st.button(f'Remover {livro[-1]} do carrinho', key=f'remove-{livro[0]}'): 
                    cursor.execute("DELETE FROM carrinho WHERE id = %s", (livro[0],))
                    cnx.commit()
                    st.success(f"{livro[-1]} foi removido do carrinho.")
        st.write(f"Total: R${total:.2f}")

    cursor.close()

def mostrar_compras():
    st.title("Livros Comprados")

    cursor = cnx.cursor()
    query = "SELECT * FROM livros_comprados WHERE usuario_id = %s"
    cursor.execute(query, (st.session_state["usuario_id"],))
    st.session_state["purchased_books"] = cursor.fetchall()

    if len(st.session_state["purchased_books"]) == 0:
        st.write("Você ainda não comprou nenhum livro.")
    else:
        for livro in st.session_state["purchased_books"]:
            with st.expander(f"{livro[1]} - R${livro[4]:.2f}"):
                st.write(f"Nome: {livro[1]}")
                st.write(f"Preço: R${livro[4]:.2f}")
                
                

    cursor.close()

def logout():
    if st.button('Logout'):
        st.session_state["logged_in"] = False
        st.session_state["usuario_id"] = None
        st.success("Logout realizado com sucesso!")

if __name__ == "__main__":
    main()
# 📚 BiblioTECH

## Sobre o Projeto
BiblioTECH é um sistema de gerenciamento de bibliotecas desenvolvido como parte da cadeira de Modelagem e Projeto de Banco de Dados. Nosso objetivo é facilitar o controle de empréstimos, catalogação de livros e gestão de usuários, proporcionando uma interface intuitiva e eficiente.

## Equipe de Desenvolvimento
- Thiago Costa Queiroz
- Vinicius Cahu
- Matheus Veloso

## Funcionalidades Principais
- 📖 **Gerenciamento de Livros**: Cadastro, edição, filtragem, adição ao carrinho, compra e exclusão de livros.
- - 📖 **Avaliação de Livros**: Opção de avaliação de livros e aba onde são exibidos os livros mais bem avaliados.
- 👤 **Gerenciamento de Usuários**: Cadastro de usuário.
- 🔍 **Busca Avançada**: Ferramenta de busca eficiente por título, ano, autor, preço.

## Tecnologias Utilizadas
- **Linguagem de Programação**: Python
- **Framework de Interface**: Streamlit
- **Banco de Dados**: SQL

## Como Executar o BiblioTECH

1. **Instalação das Dependências**: Certifique-se de ter Python e SQL instalados em seu sistema. Para a interface, você precisará do framework Streamlit.

2. **Configuração do Banco de Dados**: Configure seu banco de dados SQL com as tabelas necessárias para usuários, livros e empréstimos.

3. **Clonagem do Repositório**: Clone o repositório do BiblioTECH do GitHub para sua máquina local.

4. **Instalação do Streamlit**: Instale o Streamlit usando pip:

pip install streamlit

5. **Execução do Sistema**: Navegue até o diretório do projeto clonado e execute o comando:

streamlit run app.py

Substitua `app.py` pelo nome do arquivo principal do seu sistema.

6. **Acesso ao Sistema**: Abra seu navegador e acesse o endereço local fornecido pelo Streamlit, geralmente `http://localhost:8501`.

7. **Uso do BiblioTECH**: Utilize as funcionalidades do sistema conforme descrito na seção de funcionalidades principais do seu `README.md`.
8. Modelo Conceitual

![Captura de tela 2024-05-27 233826](https://github.com/Viniciuscahu/projetobd/assets/142367401/b8be7ea1-bee6-4c50-81d1-314ff7b67b8a)

9. 
Modelo lógico

![Captura de tela 2024-05-27 233843](https://github.com/Viniciuscahu/projetobd/assets/142367401/eb5d49bf-7f17-4ea7-aac2-502d10837f38)


10. Scripts: 
[Uploading Script- trabalhobd.sql…]()x
USE bibliotech;
SHOW DATABASES;
show tables;

select * from usuarios;
select * from livros;
select * from catalogo;
select * from avaliacoes ;
select * from top_livros_avaliados;
select * from livros_comprados; 

delete from usuarios;
delete from catalogo;
ALTER TABLE catalogo ADD COLUMN usuario_id INT;

 
CREATE TABLE IF NOT EXISTS livros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    ano_publicacao INT NOT NULL,
    reservado BOOLEAN DEFAULT FALSE,
    alugado BOOLEAN DEFAULT FALSE,
    comprado BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS catalogo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    ano_publicacao INT NOT NULL,
    preco DECIMAL(10, 2) NOT NULL
);
CREATE TABLE IF NOT EXISTS avaliacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    livro_id INT NOT NULL,
    usuario_id INT NOT NULL,
    avaliacao INT NOT NULL,
    comentario TEXT,
    FOREIGN KEY (livro_id) REFERENCES livros(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS top_livros_avaliados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    livro_id INT,
    FOREIGN KEY (livro_id) REFERENCES catalogo(id)
);

SELECT c.nome, c.autor, c.ano_publicacao, c.preco, AVG(a.avaliacao) AS media_avaliacao
FROM catalogo c
JOIN avaliacoes a ON c.id = a.livro_id
GROUP BY c.id
ORDER BY media_avaliacao DESC
LIMIT 10;

alter  TABLE catalogo
ADD COLUMN usuario_id INT NOT NULL,
ADD FOREIGN KEY (usuario_id) REFERENCES usuarios(id);


ALTER TABLE catalogo MODIFY ano_publicacao VARCHAR(255);


CREATE TABLE IF NOT EXISTS livros_comprados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    ano_publicacao INT NOT NULL,
    preco DECIMAL(10, 2) NOT NULL
);

SELECT * FROM livros_comprados ORDER BY nome;


CREATE TABLE IF NOT EXISTS carrinho (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    livro_id INT NOT NULL,
    nome VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    ano_publicacao INT NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (livro_id) REFERENCES livros(id)
);


ALTER TABLE livros
ADD COLUMN livro_id INT AUTO_INCREMENT PRIMARY KEY;


script 2:

[Uploading Script--- Usar a base de dados bibliotech
USE bibliotech;

-- Mostrar as bases de dados
SHOW DATABASES;

-- Mostrar as tabelas da base de dados bibliotech
SHOW TABLES;

-- Exibir dados das tabelas
SELECT * FROM usuarios;
SELECT * FROM livros;
SELECT * FROM catalogo;
SELECT * FROM avaliacoes;
SELECT * FROM top_livros_avaliados;
SELECT * FROM livros_comprados;

-- Limpar dados das tabelas
DELETE FROM usuarios;
DELETE FROM catalogo;

-- Adicionar coluna em catalogo
ALTER TABLE catalogo ADD COLUMN usuario_id INT;

-- Criar a tabela usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    cpf VARCHAR(14) UNIQUE,
    endereco TEXT,
    senha VARCHAR(255) NOT NULL
);

-- Criar a tabela livros
CREATE TABLE IF NOT EXISTS livros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    ano_publicacao INT NOT NULL,
    reservado BOOLEAN DEFAULT FALSE,
    alugado BOOLEAN DEFAULT FALSE,
    comprado BOOLEAN DEFAULT FALSE
);

-- Criar a tabela catalogo
CREATE TABLE IF NOT EXISTS catalogo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    ano_publicacao VARCHAR(255) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Criar a tabela avaliacoes
CREATE TABLE IF NOT EXISTS avaliacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    livro_id INT NOT NULL,
    usuario_id INT NOT NULL,
    avaliacao INT NOT NULL,
    comentario TEXT,
    FOREIGN KEY (livro_id) REFERENCES livros(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Criar a tabela top_livros_avaliados
CREATE TABLE IF NOT EXISTS top_livros_avaliados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    livro_id INT,
    FOREIGN KEY (livro_id) REFERENCES catalogo(id)
);

-- Exibir os 10 melhores livros avaliados
SELECT c.nome, c.autor, c.ano_publicacao, c.preco, AVG(a.avaliacao) AS media_avaliacao
FROM catalogo c
JOIN avaliacoes a ON c.id = a.livro_id
GROUP BY c.id
ORDER BY media_avaliacao DESC
LIMIT 10;

-- Criar a tabela livros_comprados
CREATE TABLE IF NOT EXISTS livros_comprados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    ano_publicacao INT NOT NULL,
    preco DECIMAL(10, 2) NOT NULL
);

-- Selecionar todos os livros comprados ordenados pelo nome
SELECT * FROM livros_comprados ORDER BY nome;

-- Criar a tabela carrinho
CREATE TABLE IF NOT EXISTS carrinho (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    livro_id INT NOT NULL,
    nome VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    ano_publicacao INT NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (livro_id) REFERENCES livros(id)
);

-- Modificar a tabela livros adicionando coluna livro_id
ALTER TABLE livros ADD COLUMN livro_id INT AUTO_INCREMENT PRIMARY KEY;

-- Inserir dados nas tabelas
-- Tabela usuarios(cadastro)
INSERT INTO usuarios (nome, email, telefone, cpf, endereco, senha) VALUES 
('João Silva', 'joao.silva@example.com', '11987654321', '123.456.789-10', 'Rua A, 123', 'senha123'),
('Maria Oliveira', 'maria.oliveira@example.com', '11987654322', '123.456.789-11', 'Rua B, 456', 'senha456'),
('Carlos Souza', 'carlos.souza@example.com', '11987654323', '123.456.789-12', 'Rua C, 789', 'senha789');

-- login
INSERT INTO usuarios (nome, email) VALUES 
('João Silva', 'joao.silva@example.com'),
('Maria Oliveira', 'maria.oliveira@example.com'),
('Carlos Souza', 'carlos.souza@example.com');

-- Tabela livros
INSERT INTO livros (nome, autor, ano_publicacao, reservado, alugado, comprado) VALUES 
('Livro A', 'Autor A', 2020, FALSE, FALSE, FALSE),
('Livro B', 'Autor B', 2019, FALSE, TRUE, FALSE),
('Livro C', 'Autor C', 2018, TRUE, FALSE, TRUE);

-- Tabela catalogo
INSERT INTO catalogo (nome, autor, ano_publicacao, preco, usuario_id) VALUES 
('Livro D', 'Autor D', '2021', 29.90, 1),
('Livro E', 'Autor E', '2022', 39.90, 2),
('Livro F', 'Autor F', '2020', 49.90, 3);

-- Tabela avaliacoes
INSERT INTO avaliacoes (livro_id, usuario_id, avaliacao, comentario) VALUES 
(1, 1, 5, 'Excelente!'),
(2, 2, 4, 'Muito bom!'),
(3, 3, 3, 'Bom');

-- Tabela top_livros_avaliados
INSERT INTO top_livros_avaliados (livro_id) VALUES 
(1),
(2);

-- Tabela livros_comprados
INSERT INTO livros_comprados (nome, autor, ano_publicacao, preco) VALUES 
('Livro G', 'Autor G', 2021, 59.90),
('Livro H', 'Autor H', 2022, 69.90);

-- Tabela carrinho
INSERT INTO carrinho (usuario_id, livro_id, nome, autor, ano_publicacao, preco) VALUES 
(1, 1, 'Livro A', 'Autor A', 2020, 29.90),
(2, 2, 'Livro B', 'Autor B', 2019, 39.90);



2 trabalhobd.sql…]()












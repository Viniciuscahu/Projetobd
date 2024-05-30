USE bibliotech;


DELETE FROM carrinho;
DELETE FROM livros_comprados;
DELETE FROM top_livros_avaliados;
DELETE FROM avaliacoes;
DELETE FROM catalogo;
DELETE FROM livros;
DELETE FROM usuarios;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    cpf VARCHAR(14) UNIQUE,
    endereco TEXT,
    senha VARCHAR(255) NOT NULL
);

INSERT INTO usuarios (nome, email, telefone, cpf, endereco, senha) VALUES 
('João Silva', 'joao.silva@example.com', '11987654321', '123.456.789-10', 'Rua A, 123', 'senha123'),
('Maria Oliveira', 'maria.oliveira@example.com', '11987654322', '123.456.789-11', 'Rua B, 456', 'senha456'),
('Carlos Souza', 'carlos.souza@example.com', '11987654323', '123.456.789-12', 'Rua C, 789', 'senha789');

CREATE TABLE IF NOT EXISTS livros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    ano_publicacao INT NOT NULL,
    reservado BOOLEAN DEFAULT FALSE,
    alugado BOOLEAN DEFAULT FALSE,
    comprado BOOLEAN DEFAULT FALSE,
    editora_nome VARCHAR(255)
);

INSERT INTO livros (nome, autor, ano_publicacao, reservado, alugado, comprado, editora_nome) VALUES 
('Livro A', 'Autor A', 2020, FALSE, FALSE, FALSE, 'Editora A'),
('Livro B', 'Autor B', 2019, FALSE, TRUE, FALSE, 'Editora B'),
('Livro C', 'Autor C', 2018, TRUE, FALSE, TRUE, 'Editora C');

CREATE TABLE IF NOT EXISTS catalogo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    ano_publicacao VARCHAR(255) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

INSERT INTO catalogo (nome, autor, ano_publicacao, preco, usuario_id) VALUES 
('Livro D', 'Autor D', '2021', 29.90, 1),
('Livro E', 'Autor E', '2022', 39.90, 2),
('Livro F', 'Autor F', '2020', 49.90, 3);


CREATE TABLE IF NOT EXISTS avaliacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    livro_id INT NOT NULL,
    usuario_id INT NOT NULL,
    avaliacao INT NOT NULL,
    comentario TEXT,
    FOREIGN KEY (livro_id) REFERENCES livros(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

INSERT INTO avaliacoes (livro_id, usuario_id, avaliacao, comentario) VALUES 
(1, 1, 5, 'Excelente!'),
(2, 2, 4, 'Muito bom!'),
(3, 3, 3, 'Bom');


CREATE TABLE IF NOT EXISTS top_livros_avaliados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    livro_id INT,
    FOREIGN KEY (livro_id) REFERENCES catalogo(id)
);

INSERT INTO top_livros_avaliados (livro_id) VALUES 
(1),
(2);


CREATE TABLE IF NOT EXISTS livros_comprados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    ano_publicacao INT NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    editora VARCHAR(255)
);

INSERT INTO livros_comprados (nome, autor, ano_publicacao, preco, editora) VALUES 
('Livro G', 'Autor G', 2021, 59.90, 'Editora G'),
('Livro H', 'Autor H', 2022, 69.90, 'Editora H');


CREATE TABLE IF NOT EXISTS carrinho (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    livro_id INT NOT NULL,
    nome VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    ano_publicacao INT NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    editora VARCHAR(255),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (livro_id) REFERENCES livros(id)
);

INSERT INTO carrinho (usuario_id, livro_id, nome, autor, ano_publicacao, preco, editora) VALUES 
(1, 1, 'Livro A', 'Autor A', 2020, 29.90, 'Editora A'),
(2, 2, 'Livro B', 'Autor B', 2019, 39.90, 'Editora B');

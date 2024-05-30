-- scripts

USE bibliotech;


SHOW DATABASES;

SHOW TABLES;


SELECT * FROM usuarios;
SELECT * FROM livros;
SELECT * FROM catalogo;
SELECT * FROM avaliacoes;
SELECT * FROM top_livros_avaliados;
SELECT * FROM livros_comprados;
DESCRIBE table livros;
select * from autor;
select * from editora;
select * from carrinho;


DELETE FROM usuarios;
DELETE FROM catalogo;
delete from livros;

ALTER TABLE catalogo ADD COLUMN usuario_id INT;


CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    cpf VARCHAR(14) UNIQUE,
    endereco TEXT,
    senha VARCHAR(255) NOT NULL
);


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
    ano_publicacao VARCHAR(255) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
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
ORDER BY media_avaliacao DESC
LIMIT 10;

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

ALTER TABLE livros ADD COLUMN livro_id INT AUTO_INCREMENT PRIMARY KEY;

ALTER TABLE avaliacoes
DROP FOREIGN KEY avaliacoes_ibfk_1,
ADD FOREIGN KEY (livro_id) REFERENCES livros (id) ON DELETE CASCADE;

ALTER TABLE carrinho ADD COLUMN editora VARCHAR(255);
ALTER TABLE livros_comprados ADD editora VARCHAR(255);

alter table livros add column editora_nome varchar(255);

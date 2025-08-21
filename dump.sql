-- "dump.sql" é um arquivo utilizado como script inicial do banco de dados.
CREATE TABLE produtos (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255) NOT NULL,
    preco DECIMAL(6, 2) NOT NULL,
    descricao VARCHAR(500),
    quantidade INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE clientes (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    fl_ativo BOOL NOT NULL DEFAULT true
);

CREATE TABLE vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_referencia DECIMAL(6, 2) NOT NULL,
    data_hora DATETIME NOT NULL,
    total DECIMAL(6, 2) NOT NULL,
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Dados iniciais
-- Produtos
INSERT INTO produtos (nome, preco, descricao, quantidade) VALUES
('Notebook Dell', 3500.00, 'Notebook Dell Inspiron 15 polegadas', 10),
('Smartphone Samsung', 2200.00, 'Galaxy S21 128GB', 15),
('Fone de Ouvido JBL', 350.00, 'Headset com Bluetooth', 30);

-- Clientes
INSERT INTO clientes (nome, email, data_nascimento, fl_ativo) VALUES
('Ana Silva', 'ana.silva@email.com', '1995-04-12', 1),
('Carlos Souza', 'carlos.souza@email.com', '1990-08-22', 1),
('Mariana Costa', 'mariana.costa@email.com', '2000-01-05', 1);

-- Vendas (exemplo: Ana comprou 1 notebook, Carlos comprou 2 fones)
INSERT INTO vendas (produto_id, cliente_id, quantidade, preco_referencia, data_hora, total) VALUES
(1, 1, 1, 3500.00, datetime('now'), 3500.00),
(3, 2, 2, 350.00, datetime('now'), 700.00);
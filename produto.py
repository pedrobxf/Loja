from db import get_db
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, date

@dataclass
class Produto:
    nome: str
    descricao: str
    preco: float
    quantidade_estoque: int
    id: Optional[int] = None

def buscar_produtos() -> list[Produto]:
    db = get_db()
    cursor = db.cursor()

    sql = '''
        SELECT nome, descricao, preco, quantidade, id
        FROM produtos
    '''

    cursor.execute(sql)
    produtos = cursor.fetchall()

    cursor.close()
    db.close()

    return [
        Produto(
            nome=produto[0],
            descricao=produto[1],
            preco=produto[2],
            quantidade_estoque=produto[3],
            id=produto[4]
        )
        for produto in produtos
    ]

def criar_produto(produto: Produto):
    db = get_db()
    cursor = db.cursor()

    sql = '''
        INSERT INTO produtos (nome, descricao, preco, quantidade)
        VALUES (?, ?, ?, ?)
    '''
    parameters = (
        produto.nome,
        produto.descricao,
        produto.preco,
        produto.quantidade_estoque
    )

    cursor.execute(sql, parameters)
    db.commit()
    cursor.close()
    db.close()

def atualizar_produto(produto: Produto):
    db = get_db()
    cursor = db.cursor()

    sql = '''
        UPDATE produtos
        SET nome = ?, descricao = ?, preco = ?, quantidade = ?
        WHERE id = ?
    '''
    parameters = (
        produto.nome,
        produto.descricao,
        produto.preco,
        produto.quantidade_estoque,
        produto.id
    )

    cursor.execute(sql, parameters)
    db.commit()
    cursor.close()
    db.close()

def produto_por_id(produto_id: int) -> Optional[Produto]:
    db = get_db()
    cursor = db.cursor()

    sql = '''
        SELECT nome, descricao, preco, quantidade, id
        FROM produtos
        WHERE id = ?
    '''
    cursor.execute(sql, (produto_id,))
    produto = cursor.fetchone()

    cursor.close()
    db.close()

    if produto:
        return Produto(
            nome=produto[0],
            descricao=produto[1],
            preco=produto[2],
            quantidade_estoque=produto[3],
            id=produto[4]
        )
    return None


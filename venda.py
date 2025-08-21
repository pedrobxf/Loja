from db import get_db
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, date

@dataclass
class Venda:
    cliente_id: int
    produto_id: int
    quantidade: int
    data_venda: datetime
    preco_referencia: float = None
    total: float = None
    id: Optional[int] = None

def buscar_vendas() -> list[Venda]:
    db = get_db()
    cursor = db.cursor()

    sql = '''
        SELECT cliente_id, produto_id, quantidade, data_hora, id, total, preco_referencia
        FROM vendas
    '''

    cursor.execute(sql)
    vendas = cursor.fetchall()

    cursor.close()
    db.close()

    return [
        Venda(
            cliente_id=venda[0],
            produto_id=venda[1],
            quantidade=venda[2],
            data_venda=venda[3],
            id=venda[4],
            total=venda[5],
            preco_referencia=venda[6]
        )
        for venda in vendas
    ]

def criar_venda(venda: Venda):
    db = get_db()
    cursor = db.cursor()

    sql = '''
        INSERT INTO vendas (cliente_id, produto_id, quantidade, data_hora, total, preco_referencia)
        VALUES (?, ?, ?, ?, ?, ?)
    '''
    parameters = (
        venda.cliente_id,
        venda.produto_id,
        venda.quantidade,
        venda.data_venda,
        venda.total,
        venda.preco_referencia
    )

    cursor.execute(sql, parameters)
    db.commit()
    cursor.close()
    db.close()

def excluir_venda(venda_id: int):
    db = get_db()
    cursor = db.cursor()

    sql = '''
        DELETE FROM vendas
        WHERE id = ?
    '''

    cursor.execute(sql, (venda_id,))
    db.commit()
    cursor.close()
    db.close()

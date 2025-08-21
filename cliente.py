from db import get_db
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class Cliente:
    nome: str
    email: str
    data_nascimento: date
    fl_ativo: bool = True
    id: Optional[int] = None


def buscar_clientes() -> list[Cliente]:
    # Connectando no Banco de Dados
    db = get_db() 

    # Criando o Cursor
    cursor = db.cursor()

    # Script SQL
    sql = '''
        SELECT nome, email, data_nascimento, fl_ativo, id
        FROM clientes
    '''

    # Executando SQL
    cursor.execute(sql)

    # Buscando dados resultantes
    clientes = cursor.fetchall()

    cursor.close()
    db.close()

    return [
        Cliente(
            nome=cliente[0], 
            email=cliente[1], 
            data_nascimento=datetime.strptime(cliente[2], '%Y-%m-%d').date(), 
            fl_ativo=cliente[3],
            id=cliente[4]
        )
        for cliente in clientes
    ]

def buscar_cliente_pelo_email(email: str) -> Optional[Cliente]:
    db = get_db()
    cursor = db.cursor()

    sql = '''
        SELECT nome, email, data_nascimento, fl_ativo, id
        FROM clientes
        WHERE email = ?
    '''

    cursor.execute(sql, (email,))
    cliente = cursor.fetchone()

    cursor.close()
    db.close()

    if cliente is None:
        return None

    return Cliente(
        nome=cliente[0], 
        email=cliente[1], 
        data_nascimento=datetime.strptime(cliente[2], '%Y-%m-%d').date(), 
        fl_ativo=cliente[3],
        id=cliente[4]
    )

def criar_cliente(cliente: Cliente) -> Cliente:
    # Connectando no Banco de Dados
    db = get_db() 

    # Criando o Cursor
    cursor = db.cursor()

    # Script SQL
    sql = '''
        INSERT INTO clientes (nome, email, data_nascimento, fl_ativo)
        VALUES (?, ?, ?, ?) RETURNING id
    '''
    parameters = (
        cliente.nome,
        cliente.email,
        cliente.data_nascimento.isoformat(),
        cliente.fl_ativo
    )

    cursor.execute(sql, parameters)

    cliente.id = cursor.fetchone()[0]
    db.commit()

    cursor.close()
    db.close()

    return cliente

def atualizar_cliente(cliente: Cliente):
    db = get_db()
    cursor = db.cursor()

    sql = '''
        UPDATE clientes
        SET nome = ?, email = ?, data_nascimento = ?, fl_ativo = ?
        WHERE id = ?
    '''
    parameters = (
        cliente.nome,
        cliente.email,
        cliente.data_nascimento.isoformat(),
        cliente.fl_ativo,
        cliente.id
    )

    cursor.execute(sql, parameters)

    db.commit()

    cursor.close()
    db.close()


def desativar_cliente(cliente_id: int):
    db = get_db()
    cursor = db.cursor()

    sql = '''
        UPDATE clientes
        SET fl_ativo = 0
        WHERE id = ?
    '''

    cursor.execute(sql, (cliente_id,))

    db.commit()

    cursor.close()
    db.close()

def cliente_por_id(cliente_id: int) -> Optional[Cliente]:
    db = get_db()
    cursor = db.cursor()

    sql = '''
        SELECT nome, email, data_nascimento, fl_ativo, id
        FROM clientes
        WHERE id = ?
    '''
    cursor.execute(sql, (cliente_id,))
    cliente = cursor.fetchone()

    cursor.close()
    db.close()

    if cliente is None:
        return None

    return Cliente(
        nome=cliente[0], 
        email=cliente[1], 
        data_nascimento=datetime.strptime(cliente[2], '%Y-%m-%d').date(), 
        fl_ativo=cliente[3],
        id=cliente[4]
    )
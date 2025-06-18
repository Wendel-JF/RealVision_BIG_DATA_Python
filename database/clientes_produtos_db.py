import random
import sqlite3

from faker import Faker


def clientes_produtos_db():
    conn = sqlite3.connect("RetailAnalytics.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes_produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        produto_id INTEGER,
        data_compra TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id),
        FOREIGN KEY(produto_id) REFERENCES produtos(id)
    )
    """)

    for _ in range(100):
        adicionar_clientes_produtos()

    conn.commit()
    conn.close()
    print("✅ Tabela cliente_produto criada e 100 registros inseridos.")


def adicionar_clientes_produtos():
    fake = Faker('pt_BR')
    # <<< cada chamada tem sua própria conexão
    with sqlite3.connect("RetailAnalytics.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
    cliente = random.randint(1, 100)
    produto = random.randint(1, 20)
    data_compra = fake.date_between(
        start_date='-1y', end_date='today').isoformat()

    cursor.execute("""
        INSERT INTO clientes_produtos (cliente_id, produto_id, data_compra)
        VALUES (?, ?, ?)
        """, (cliente, produto, data_compra))
    conn.commit()
    conn.close()

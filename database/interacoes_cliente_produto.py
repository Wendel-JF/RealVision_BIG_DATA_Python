import random
import sqlite3

from faker import Faker


def interacoes_cliente_produto_db(n=100):
    conn = sqlite3.connect("RetailAnalytics.db")
    cursor = conn.cursor()

    # Criar a tabela
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interacoes_cliente_produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        produto_id INTEGER,
        visualizacoes INTEGER DEFAULT 0,
        adicionou_carrinho INTEGER DEFAULT 0,
        comprou BOOLEAN DEFAULT 0,
        ultima_interacao DATETIME,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id),
        FOREIGN KEY(produto_id) REFERENCES produtos(id)
    )
    """)

    for _ in range(n):
        adicionar_interacoes_cliente_produto()

    conn.commit()
    conn.close()
    print(
        f"✅ Tabela interacoes_cliente_produto criada e {n} registros inseridos.")


def adicionar_interacoes_cliente_produto():
    fake = Faker('pt_BR')
    # <<< cada chamada tem sua própria conexão
    with sqlite3.connect("RetailAnalytics.db", check_same_thread=False) as conn:
        cursor = conn.cursor()
     # ajuste conforme total de clientes
    cliente_id = random.randint(1, 100)
    # ajuste conforme total de produtos
    produto_id = random.randint(1, 20)
    visualizacoes = random.randint(1, 10)
    adicionou_carrinho = random.randint(0, visualizacoes)
    comprou = 1 if random.random() < 0.5 else 0  # 30% chance de compra
    ultima_interacao = fake.date_time_between(
        start_date='-1y', end_date='now').isoformat()

    cursor.execute("""
        INSERT INTO interacoes_cliente_produto (
            cliente_id, produto_id, visualizacoes, adicionou_carrinho, comprou, ultima_interacao
        ) VALUES (?, ?, ?, ?, ?, ?)
        """, (cliente_id, produto_id, visualizacoes, adicionou_carrinho, comprou, ultima_interacao))
    conn.commit()
    conn.close()

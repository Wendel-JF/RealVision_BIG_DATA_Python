import random
import sqlite3
from datetime import timedelta

from faker import Faker


def eventos_cliente_db():
    conn = sqlite3.connect("RetailAnalytics.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos_cliente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        tipo_evento TEXT,
        produto_id INTEGER,
        timestamp DATETIME,
        duracao_segundos INTEGER,
        origem TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id),
        FOREIGN KEY(produto_id) REFERENCES produtos(id)
    )
    """)

    for _ in range(200):  # Número de eventos a gerar
        adicionar_evento_cliente()

    conn.commit()
    conn.close()

    print("✅ Tabela eventos_cliente criada e 200 registros inseridos.")


def adicionar_evento_cliente():
    fake = Faker('pt_BR')
    conn = sqlite3.connect("RetailAnalytics.db")
    cursor = conn.cursor()

    tipo_eventos = ['visualizou_produto',
                    'adicionou_ao_carrinho', 'comprou', 'visitou_loja']
    origens = ['app', 'web', 'loja_fisica']

    cliente_id = random.randint(1, 100)
    tipo_evento = random.choice(tipo_eventos)
    produto_id = random.randint(1, 20) if tipo_evento in [
        'visualizou_produto', 'adicionou_ao_carrinho', 'comprou'] else None
    timestamp = fake.date_time_between(start_date='-1y', end_date='now')
    duracao = random.randint(5, 600)
    origem = random.choice(origens)

    cursor.execute("""
        INSERT INTO eventos_cliente (cliente_id, tipo_evento, produto_id, timestamp, duracao_segundos, origem)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
        cliente_id, tipo_evento, produto_id, timestamp.isoformat(), duracao, origem
    ))

    conn.commit()
    conn.close()

# Ela transforma múltiplos registros de eventos em um resumo por cliente e produto.


def atualizar_interacoes():
    conn = sqlite3.connect("RetailAnalytics.db")
    cursor = conn.cursor()

    # Buscar todos os eventos
    cursor.execute("""
        SELECT cliente_id, produto_id, tipo_evento, timestamp
        FROM eventos_cliente
        ORDER BY timestamp
    """)
    eventos = cursor.fetchall()

    for cliente_id, produto_id, tipo_evento, timestamp in eventos:
        # Verifica se já existe uma linha para esse cliente e produto
        cursor.execute("""
            SELECT id, visualizacoes, adicionou_carrinho, comprou
            FROM interacoes_cliente_produto
            WHERE cliente_id = ? AND produto_id = ?
        """, (cliente_id, produto_id))
        resultado = cursor.fetchone()

        if resultado:
            id_interacao, visualizacoes, adicionou_carrinho, comprou = resultado

            # Atualiza contadores conforme o tipo do evento
            if tipo_evento == 'visualizou_produto':
                visualizacoes += 1
            elif tipo_evento == 'adicionou_ao_carrinho':
                adicionou_carrinho += 1
            elif tipo_evento == 'comprou':
                comprou = 1

            # Atualiza a linha existente
            cursor.execute("""
                UPDATE interacoes_cliente_produto
                SET visualizacoes = ?, adicionou_carrinho = ?, comprou = ?, ultima_interacao = ?
                WHERE id = ?
            """, (visualizacoes, adicionou_carrinho, comprou, timestamp, id_interacao))

        else:
            # Novo registro
            visualizacoes = 1 if tipo_evento == 'visualizou_produto' else 0
            adicionou_carrinho = 1 if tipo_evento == 'adicionou_ao_carrinho' else 0
            comprou = 1 if tipo_evento == 'comprou' else 0

            cursor.execute("""
                INSERT INTO interacoes_cliente_produto (
                    cliente_id, produto_id, visualizacoes, adicionou_carrinho, comprou, ultima_interacao
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (cliente_id, produto_id, visualizacoes, adicionou_carrinho, comprou, timestamp))

    conn.commit()
    conn.close()
    print("✅ Tabela consolidada atualizada com sucesso.")

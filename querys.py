import datetime
import random
import sqlite3
import threading
import time

import pandas as pd

from database.clientes_db import adicionar_clientes
from database.eventos_cliente import (adicionar_evento_cliente,
                                      atualizar_interacoes)
from database.interacoes_cliente_produto import \
    adicionar_interacoes_cliente_produto


# Função para pegar a quantidade total de clientes
def get_clientes():
    conn = sqlite3.connect("RetailAnalytics.db")
    df = pd.read_sql_query("SELECT * FROM clientes", conn)

    conn.close()
    return df

# Função para pegar a o Faturamento dos produtos Comprados


def get_faturamento_anual():
    # Pega o ano atual
    ano_atual = str(datetime.datetime.now().year)

    # SQL para somar os preços das compras feitas em 2024
    query = """
    SELECT SUM(p.preco) as faturamento
    FROM interacoes_cliente_produto icp
    JOIN produtos p ON icp.produto_id = p.id
    WHERE icp.comprou = 1 AND strftime('%Y', icp.ultima_interacao) = ?
    """

    conn = sqlite3.connect("RetailAnalytics.db")
    df = pd.read_sql_query(query, conn, params=(ano_atual,))
    total_valor = df["faturamento"].iloc[0] or 0  # garante que não será None

    # Formatar valor em reais
    valor_total_anual_formatado = f"R$ {total_valor:,.2f}".replace(
        ",", "X").replace(".", ",").replace("X", ".")

    conn.close()
    return valor_total_anual_formatado


def get_quantidade_de_vendas_por_produtos():
    # SQL para contar o número de vendas por produto
    df = """
    SELECT p.nome AS produto, COUNT(*) AS vendas
    FROM interacoes_cliente_produto icp
    JOIN produtos p ON icp.produto_id = p.id
    WHERE icp.comprou = 1
    GROUP BY p.nome
    ORDER BY vendas DESC
    LIMIT 6;
    """

    conn = sqlite3.connect("RetailAnalytics.db")
    venda = pd.read_sql_query(df, conn)
    conn.close()
    return venda


def get_produtos_mais_visualizados(limit=6):
    query = """
    SELECT p.nome AS produto, SUM(icp.visualizacoes) AS visualizacoes
    FROM interacoes_cliente_produto icp
    JOIN produtos p ON icp.produto_id = p.id
    GROUP BY p.nome
    ORDER BY visualizacoes DESC
    LIMIT ?
    """

    conn = sqlite3.connect("RetailAnalytics.db")
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df


# Objetivo: Identificar quais categorias geram mais receita.

def get_faturamento_por_categoria():
    df = """
    SELECT p.categoria as categoria, SUM(p.preco) AS faturamento
    FROM clientes_produtos cp
    JOIN produtos p ON cp.produto_id = p.id
    GROUP BY p.categoria
    """

    df = """
    SELECT p.categoria AS categoria, SUM(p.preco) AS faturamento
    FROM interacoes_cliente_produto icp
    JOIN produtos p ON icp.produto_id = p.id
    WHERE icp.comprou = 1
    GROUP BY p.categoria
    ORDER BY faturamento DESC
    LIMIT 6;
    """

    # Carregar dados em DataFrame
    conn = sqlite3.connect("RetailAnalytics.db")
    query = pd.read_sql_query(df, conn)
    conn.close()

    return query


def get_genero():

    # Consulta SQL para contar os clientes por gênero
    df = """
    SELECT genero, COUNT(*) AS total
    FROM clientes
    GROUP BY genero
    """

    # Carregar dados em DataFrame
    conn = sqlite3.connect("RetailAnalytics.db")
    genero = pd.read_sql_query(df, conn)
    conn.close()
    return genero


# Objetivo: Ver evolução mensal das vendas.
def get_faturamento_mensal():
    df = """SELECT strftime('%Y-%m', cp.data_compra) AS mes, SUM(p.preco) as faturamento
    FROM clientes_produtos cp
    JOIN produtos p ON cp.produto_id = p.id
    GROUP BY mes
    ORDER BY mes
    """

    conn = sqlite3.connect("RetailAnalytics.db")
    query = pd.read_sql_query(df, conn)
    conn.close()
    return query

# Objetivo: Ver qual dispositivo é mais usado.


def get_dispositivos_mais_usados():
    df = """SELECT dispositivo, COUNT(*) as total
    FROM clientes
    GROUP BY dispositivo
     """

    # Carregar dados em DataFrame
    conn = sqlite3.connect("RetailAnalytics.db")
    query = pd.read_sql_query(df, conn)
    conn.close()
    return query

# Objetivo: Entender o comportamento de compra por idade.


def get_clientes_por_faixa_etaria():
    df = """
    SELECT 
  CASE 
    WHEN idade < 25 THEN '18-24'
    WHEN idade < 35 THEN '25-34'
    WHEN idade < 45 THEN '35-44'
    WHEN idade < 55 THEN '45-54'
    ELSE '55+' 
  END AS faixa_etaria,
    COUNT(*) AS total
 FROM clientes
 GROUP BY faixa_etaria
     """

    # Carregar dados em DataFrame
    conn = sqlite3.connect("RetailAnalytics.db")
    query = pd.read_sql_query(df, conn)
    conn.close()
    return query


# Objetivo: Ver as regiões mais engajadas em compras.
def get_frequencia_compras_regiao():
    df = """SELECT regiao, SUM(frequencia_compras) AS total
    FROM clientes
    GROUP BY regiao
     """

    # Carregar dados em DataFrame
    conn = sqlite3.connect("RetailAnalytics.db")
    query = pd.read_sql_query(df, conn)
    conn.close()
    return query

# Objetivo: Ver quantos participam e quantos não.


def participao_programa_Fidelidade():
    df = """SELECT participa_fidelidade, COUNT(*) as total
    FROM clientes
    GROUP BY participa_fidelidade
     """

    # Carregar dados em DataFrame
    conn = sqlite3.connect("RetailAnalytics.db")
    query = pd.read_sql_query(df, conn)
    conn.close()
    return query


# Objetivo: Ver quantos tempo medio acessado na loja
def get_tempo_medio_na_loja():
    df = """
    SELECT 
        ROUND(AVG(duracao_segundos), 2) AS tempo_medio_segundos
    FROM eventos_cliente
    """

    conn = sqlite3.connect("RetailAnalytics.db")
    query = pd.read_sql_query(df, conn)
    conn.close()
    return query

# Objetivo: Desculpe a taxa de produtos deixados no carrinho sem comprar


def get_taxa_abandono_carrinho():
    query = """
    SELECT 
      ROUND(
        100.0 * SUM(CASE WHEN adicionou_carrinho > 0 AND comprou = 0 THEN 1 ELSE 0 END) / 
        NULLIF(SUM(CASE WHEN adicionou_carrinho > 0 THEN 1 ELSE 0 END), 0),
        2
      ) AS taxa_abandono
    FROM interacoes_cliente_produto;
    """
    conn = sqlite3.connect("RetailAnalytics.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df["taxa_abandono"].iloc[0] if not df.empty else 0


def get_taxa_conversao():
    conn = sqlite3.connect("RetailAnalytics.db")
    query = """
        SELECT 
            ROUND(
                CAST(SUM(comprou) AS FLOAT) / NULLIF(SUM(visualizacoes), 0) * 100, 
                2
            ) AS taxa_conversao
        FROM interacoes_cliente_produto
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.iloc[0]["taxa_conversao"]


def get_ultimo_evento():
    query = """
    SELECT 
        c.nome AS cliente,
        p.nome AS produto,
        e.tipo_evento,
        e.timestamp
    FROM eventos_cliente e
    JOIN (
        SELECT cliente_id, MAX(timestamp) AS ultimo_evento
        FROM eventos_cliente
        GROUP BY cliente_id
    ) ult ON e.cliente_id = ult.cliente_id AND e.timestamp = ult.ultimo_evento
    JOIN clientes c ON e.cliente_id = c.id
    LEFT JOIN produtos p ON e.produto_id = p.id
    ORDER BY e.timestamp DESC
    LIMIT 1
    """
    conn = sqlite3.connect("RetailAnalytics.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def atualizar_dados():
    r = random.randint(0, 1)
    if (r == 0):
        # Adicionar entre 0 e 10 clientes
        for _ in range(random.randint(1, 10)):
            adicionar_clientes()  # funcao para criar clientes novos
            adicionar_interacoes_cliente_produto()

    else:
        with sqlite3.connect("RetailAnalytics.db", check_same_thread=False) as conn:
            cursor = conn.cursor()

            # Remover entre 0 e 10 clientes aleatoriamente
        cursor.execute("SELECT id FROM clientes")
        ids = [row[0] for row in cursor.fetchall()]
        if ids:
            for _ in range(random.randint(0, 10)):
                if ids:
                    id_remover = random.choice(ids)
                    cursor.execute(
                        "DELETE FROM clientes WHERE id = ?", (id_remover,))
                    ids.remove(id_remover)
        conn.commit()
        conn.close()

    print("🔄 Atualização da Dashboard.")

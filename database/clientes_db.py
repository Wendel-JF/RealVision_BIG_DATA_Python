import random
import sqlite3
from datetime import date

from faker import Faker

# Listas para geração de dados
generos = ['Masculino', 'Feminino']
estados_civis = ['Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)']
canais_preferidos = ['Email', 'SMS', 'Telefone', 'WhatsApp']
categorias = ['Eletrônicos', 'Roupas', 'Alimentos', 'Beleza', 'Livros']
canais_utilizados = ['Loja física', 'E-commerce', 'App']
origens_trafego = ['Google', 'Facebook',
                   'Instagram', 'Email Marketing', 'Orgânico']
dispositivos = ['Desktop', 'Mobile', 'Tablet']
regioes = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']

hoje = date.today()

conn = sqlite3.connect("RetailAnalytics.db")
cursor = conn.cursor()


def clientes_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        data_nascimento TEXT,
        idade INTEGER,
        genero TEXT,
        estado_civil TEXT,
        cpf TEXT UNIQUE,
        endereco TEXT,
        cep TEXT,
        telefone TEXT,
        email TEXT,
        cidade TEXT,
        regiao TEXT,
        canal_preferido TEXT,
        frequencia_compras INTEGER,
        recencia_ultima_compra TEXT,
        valor_medio_gasto REAL,
        categorias_mais_compradas TEXT,
        canais_utilizados TEXT,
        participa_fidelidade BOOLEAN,
        pontos_acumulados INTEGER,
        origem_trafego TEXT,
        nps INTEGER,
        dispositivo TEXT
    )
    """)

    # Inserir 100 clientes fictícios com dados completos

    for _ in range(100):
        adicionar_clientes()

    conn.commit()
    conn.close()
    print("✅ Tabela Clientes criado e 100 clientes inseridos.")


def adicionar_clientes():
    fake = Faker('pt_BR')
    # <<< cada chamada tem sua própria conexão
    with sqlite3.connect("RetailAnalytics.db", check_same_thread=False) as conn:
        cursor = conn.cursor()

    nome = fake.name()
    data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=80)

    idade = hoje.year - data_nascimento.year - \
        ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    genero = random.choice(generos)
    estado_civil = random.choice(estados_civis)
    cpf = fake.unique.cpf()
    endereco = fake.street_address()
    cep = fake.postcode()
    telefone = fake.phone_number()
    email = fake.unique.email()
    cidade = fake.city()
    regiao = random.choice(regioes)
    canal_preferido = random.choice(canais_preferidos)
    frequencia_compras = random.randint(1, 50)
    recencia_ultima_compra = fake.date_this_year().isoformat()
    valor_medio_gasto = round(random.uniform(50, 1500), 2)
    categorias_mais_compradas = random.choice(categorias)
    canais = random.choice(canais_utilizados)
    participa_fidelidade = random.choice([True, False])
    pontos_acumulados = random.randint(
        0, 1000) if participa_fidelidade else 0
    origem_trafego = random.choice(origens_trafego)
    nps = random.randint(0, 10)
    dispositivo = random.choice(dispositivos)

    cursor.execute("""
        INSERT INTO clientes (
            nome, data_nascimento, idade, genero, estado_civil, cpf, endereco, cep, telefone,
            email, cidade, regiao, canal_preferido, frequencia_compras, recencia_ultima_compra,
            valor_medio_gasto, categorias_mais_compradas, canais_utilizados, participa_fidelidade,
            pontos_acumulados, origem_trafego, nps, dispositivo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
        nome, data_nascimento.isoformat(), idade, genero, estado_civil, cpf, endereco, cep,
        telefone, email, cidade, regiao, canal_preferido, frequencia_compras,
        recencia_ultima_compra, valor_medio_gasto, categorias_mais_compradas,
        canais, participa_fidelidade, pontos_acumulados, origem_trafego, nps, dispositivo
    ))
    conn.commit()
    conn.close()

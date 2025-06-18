import random
import sqlite3

from faker import Faker

# Produtos reais por categoria
produtos_por_categoria = {
    "Eletrônicos": ["iPhone 14", "PlayStation 5", "Samsung Galaxy S23", "Smart TV LG 55\"", "Notebook Dell XPS"],
    "Roupas": ["Camiseta Nike", "Calça Jeans Levi's", "Jaqueta Adidas", "Vestido Zara", "Tênis Puma"],
    "Alimentos": ["Arroz Tio João", "Feijão Carioca", "Chocolate Lindt", "Café Pilão", "Biscoito Oreo"],
    "Beleza": ["Perfume Chanel", "Creme Nívea", "Shampoo Pantene", "Maquiagem MAC", "Protetor Solar La Roche"],
    "Livros": ["1984", "O Pequeno Príncipe", "Harry Potter", "Dom Casmurro", "A Revolução dos Bichos"],
    "Brinquedos": ["LEGO", "Boneca Barbie", "Hot Wheels", "Quebra-Cabeça 1000 peças", "Jogo Uno"],
    "Esportes": ["Bola Adidas", "Raquete Wilson", "Camiseta Nike Sportswear", "Bicicleta Caloi", "Luva de Boxe Everlast"],
    "Móveis": ["Sofá 3 lugares", "Cama Queen", "Escrivaninha", "Mesa de Jantar", "Estante de Livros"]
}


def produtos_db():
    fake = Faker('pt_BR')
    conn = sqlite3.connect("RetailAnalytics.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        preco REAL,
        categoria TEXT
    )
    """)

    produtos_gerados = set()

    # Gerar até 20 produtos únicos
    while len(produtos_gerados) < 40:
        categoria = random.choice(list(produtos_por_categoria.keys()))
        nome = random.choice(produtos_por_categoria[categoria])
        preco = round(random.uniform(50, 7000), 2)
        produtos_gerados.add((nome, preco, categoria))

    # Inserir no banco
    cursor.executemany("""
    INSERT OR IGNORE INTO produtos (nome, preco, categoria)
    VALUES (?, ?, ?)
    """, list(produtos_gerados))

    conn.commit()
    conn.close()
    print("✅ Tabela Produtos criado e 20 produtos inseridos.")

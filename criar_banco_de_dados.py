from database.clientes_db import clientes_db
from database.clientes_produtos_db import clientes_produtos_db
from database.eventos_cliente import eventos_cliente_db
from database.interacoes_cliente_produto import interacoes_cliente_produto_db
from database.produtos_db import produtos_db


def main():
    clientes_db()
    produtos_db()
    clientes_produtos_db()
    eventos_cliente_db()
    interacoes_cliente_produto_db()


if __name__ == "__main__":
    main()

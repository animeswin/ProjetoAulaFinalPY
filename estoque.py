import sqlite3
from datetime import datetime

class EstoqueDB:
    def __init__(self, nome_banco="estoque.db"):
        self.conn = sqlite3.connect(nome_banco)
        self.criar_tabelas()

    def criar_tabelas(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_produto INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                data TEXT NOT NULL,
                FOREIGN KEY(id_produto) REFERENCES produtos(id)
            )
        ''')
        self.conn.commit()

    def adicionar_produto(self, produto):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO produtos (nome, descricao, quantidade, preco)
            VALUES (?, ?, ?, ?)
        ''', (produto.nome, produto.descricao, produto.quantidade, produto.preco))
        self.conn.commit()

    def listar_produtos(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM produtos')
        return cursor.fetchall()

    def atualizar_quantidade(self, id_produto, nova_quantidade):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_quantidade, id_produto))
        self.conn.commit()

    def remover_produto(self, id_produto):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM produtos WHERE id = ?', (id_produto,))
        self.conn.commit()

    def obter_produto(self, id_produto):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM produtos WHERE id = ?', (id_produto,))
        return cursor.fetchone()

    def registrar_venda(self, id_produto, quantidade):
        produto = self.obter_produto(id_produto)
        if not produto:
            return "Produto não encontrado."
        if produto[3] < quantidade:
            return "Quantidade insuficiente em estoque."

        nova_quantidade = produto[3] - quantidade
        self.atualizar_quantidade(id_produto, nova_quantidade)

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO vendas (id_produto, quantidade, data)
            VALUES (?, ?, ?)
        ''', (id_produto, quantidade, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()
        return "Venda registrada com sucesso."

    def listar_vendas(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT vendas.id, produtos.nome, vendas.quantidade, vendas.data
            FROM vendas
            JOIN produtos ON vendas.id_produto = produtos.id
        ''')
        return cursor.fetchall()

class Produto:
    def __init__(self, nome, descricao, quantidade, preco):
        self.nome = nome
        self.descricao = descricao
        self.quantidade = quantidade
        self.preco = preco

class Venda:
    def __init__(self, id_produto, quantidade):
        self.id_produto = id_produto
        self.quantidade = quantidade

def menu():
    print("\n=== Sistema de Gerenciamento de Estoque ===")
    print("1. Cadastrar produto")
    print("2. Listar produtos")
    print("3. Atualizar quantidade")
    print("4. Remover produto")
    print("5. Registrar venda")
    print("6. Listar vendas")
    print("0. Sair")

def main():
    db = EstoqueDB()

    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do produto: ")
            descricao = input("Descrição: ")
            quantidade = int(input("Quantidade: "))
            preco = float(input("Preço: "))
            produto = Produto(nome, descricao, quantidade, preco)
            db.adicionar_produto(produto)
            print("Produto cadastrado com sucesso.")

        elif opcao == "2":
            produtos = db.listar_produtos()
            print("\n--- Produtos Cadastrados ---")
            for p in produtos:
                print(f"ID: {p[0]} | {p[1]} | {p[2]} | Qtde: {p[3]} | R${p[4]:.2f}")

        elif opcao == "3":
            id_produto = int(input("ID do produto: "))
            nova_qtde = int(input("Nova quantidade: "))
            db.atualizar_quantidade(id_produto, nova_qtde)
            print("Quantidade atualizada com sucesso.")

        elif opcao == "4":
            id_produto = int(input("ID do produto a remover: "))
            db.remover_produto(id_produto)
            print("Produto removido com sucesso.")

        elif opcao == "5":
            id_produto = int(input("ID do produto: "))
            qtde = int(input("Quantidade vendida: "))
            resultado = db.registrar_venda(id_produto, qtde)
            print(resultado)

        elif opcao == "6":
            vendas = db.listar_vendas()
            print("\n--- Vendas Registradas ---")
            for v in vendas:
                print(f"Venda {v[0]} | Produto: {v[1]} | Qtde: {v[2]} | Data: {v[3]}")

        elif opcao == "0":
            print("Saindo do sistema.")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
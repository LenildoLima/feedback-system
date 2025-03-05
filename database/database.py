import sqlite3
import os

def criar_banco():
    # Caminho relativo para a pasta onde o banco de dados estará
    banco_dir = os.path.join(os.getcwd(), 'database')  # Obtém o diretório atual e adiciona 'database'
    
    # Verifica se o diretório existe, se não, cria
    if not os.path.exists(banco_dir):
        os.makedirs(banco_dir)  # Cria o diretório se não existir

    # Caminho relativo para o arquivo do banco de dados
    banco_path = os.path.join(banco_dir, 'feedback.db')

    # Conectar ao banco de dados (ou criar se não existir)
    conn = sqlite3.connect(banco_path)
    cursor = conn.cursor()

    # Criar tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        tipo_usuario TEXT NOT NULL,
        ano_turma TEXT,
        disciplinas TEXT
    )''')

    # Criar tabela de feedbacks com a adição do campo "data"
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedbacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        disciplina TEXT NOT NULL,
        professor TEXT NOT NULL,
        clareza INTEGER CHECK(clareza BETWEEN 1 AND 5),
        material_apoio INTEGER CHECK(material_apoio BETWEEN 1 AND 5),
        participacao INTEGER CHECK(participacao BETWEEN 1 AND 5),
        motivacao INTEGER NOT NULL,
        desafio TEXT,
        comentarios TEXT,
        data DATE NOT NULL,  -- Adiciona o campo data
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )''')

    # Salvar e fechar conexão
    print("Banco de dados e tabelas criadas com sucesso")
    conn.commit()
    conn.close()

def buscar_disciplinas_por_professor(nome_professor):
    # Caminho relativo para o banco de dados
    banco_dir = os.path.join(os.getcwd(), 'database')
    banco_path = os.path.join(banco_dir, 'feedback.db')

    # Conectar ao banco de dados
    conn = sqlite3.connect(banco_path)
    cursor = conn.cursor()

    # Buscar as disciplinas associadas ao professor
    cursor.execute("SELECT disciplinas FROM usuarios WHERE tipo_usuario = 'Professor' AND nome = ?", (nome_professor,))
    resultado = cursor.fetchone()
    
    conn.close()

    # Se o professor tiver disciplinas cadastradas
    if resultado:
        # Separamos as disciplinas em uma lista
        disciplinas = resultado[0].split(",")  # Aqui consideramos que as disciplinas são separadas por vírgula
        return disciplinas
    return None

# Função chamada para criar o banco
if __name__ == "__main__":
    criar_banco()

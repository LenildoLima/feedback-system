import sqlite3
import os
import matplotlib.pyplot as plt

def conectar_bd():
    # Caminho correto para o banco de dados 'feedback.db'
    banco_dir = os.path.join(os.getcwd(), 'database')  # Obtém o diretório atual e adiciona 'database'
    
    # Verifica se a pasta 'database' existe, se não, cria
    if not os.path.exists(banco_dir):
        os.makedirs(banco_dir)  # Cria a pasta 'database' se não existir
    
    db_path = os.path.join(banco_dir, 'feedback.db')  # Caminho correto para o banco de dados
    
    # Conectar ao banco de dados
    conn = sqlite3.connect(db_path)
    return conn

def obter_feedbacks_do_professor(nome_professor):
    conn = conectar_bd()
    cursor = conn.cursor()

    # Buscar os feedbacks dos alunos para o professor especificado
    cursor.execute('''
        SELECT u.nome, f.clareza, f.material_apoio, f.participacao, f.motivacao, f.desafio, f.comentarios
        FROM feedbacks f
        JOIN usuarios u ON f.usuario_id = u.id
        WHERE f.professor = ?
    ''', (nome_professor,))

    # Obter todos os feedbacks para o professor
    feedbacks = cursor.fetchall()
    conn.close()

    # Retornar a lista de feedbacks
    return feedbacks

def exibir_graficos_feedback(feedbacks):
    # Preparando dados para os gráficos
    clareza = []
    material_apoio = []
    participacao = []
    motivacao = []

    for feedback in feedbacks:
        clareza.append(feedback[1])
        material_apoio.append(feedback[2])
        participacao.append(feedback[3])
        motivacao.append(feedback[4])

    # Criar os gráficos
    fig, ax = plt.subplots(2, 2, figsize=(12, 10))

    # Clareza
    ax[0, 0].hist(clareza, bins=5, color='blue', alpha=0.7)
    ax[0, 0].set_title("Distribuição de Clareza")
    ax[0, 0].set_xlabel("Nota")
    ax[0, 0].set_ylabel("Quantidade de Feedbacks")

    # Material de Apoio
    ax[0, 1].hist(material_apoio, bins=5, color='green', alpha=0.7)
    ax[0, 1].set_title("Distribuição de Material de Apoio")
    ax[0, 1].set_xlabel("Nota")
    ax[0, 1].set_ylabel("Quantidade de Feedbacks")

    # Participação
    ax[1, 0].hist(participacao, bins=5, color='red', alpha=0.7)
    ax[1, 0].set_title("Distribuição de Participação")
    ax[1, 0].set_xlabel("Nota")
    ax[1, 0].set_ylabel("Quantidade de Feedbacks")

    # Motivação
    ax[1, 1].hist(motivacao, bins=5, color='purple', alpha=0.7)
    ax[1, 1].set_title("Distribuição de Motivação")
    ax[1, 1].set_xlabel("Nota")
    ax[1, 1].set_ylabel("Quantidade de Feedbacks")

    # Exibir os gráficos
    plt.tight_layout()
    plt.show()

def tela_professor():
    # Exemplo de interação com a tela do professor
    nome_professor = input("Digite o nome do professor para ver os feedbacks: ")
    
    # Obter os feedbacks
    feedbacks = obter_feedbacks_do_professor(nome_professor)
    
    # Exibir feedbacks e gráficos
    if feedbacks:
        # Exibir feedbacks de forma simples
        for feedback in feedbacks:
            print(f"Aluno: {feedback[0]}")
            print(f"Clareza: {feedback[1]}")
            print(f"Material de Apoio: {feedback[2]}")
            print(f"Participação: {feedback[3]}")
            print(f"Motivação: {feedback[4]}")
            print(f"Desafio: {feedback[5]}")
            print(f"Comentários: {feedback[6]}")
            print("-" * 40)

        # Exibir gráficos
        exibir_graficos_feedback(feedbacks)
    else:
        print(f"Nenhum feedback encontrado para o professor {nome_professor}.")

if __name__ == "__main__":
    tela_professor()




import streamlit as st
import sqlite3
import os
import matplotlib.pyplot as plt

def conectar_bd():
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
    clareza = []
    material_apoio = []
    participacao = []
    motivacao = []

    for feedback in feedbacks:
        clareza.append(feedback[1])
        material_apoio.append(feedback[2])
        participacao.append(feedback[3])
        motivacao.append(feedback[4])

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

    plt.tight_layout()
    plt.show()

def tela_professor():
    st.title("Feedback dos Alunos para o Professor")
    
    # Captura o nome do professor via Streamlit
    nome_professor = st.text_input("Digite o nome do professor para ver os feedbacks:")
    
    if nome_professor:
        # Obter feedbacks
        feedbacks = obter_feedbacks_do_professor(nome_professor)
        
        if feedbacks:
            # Exibir feedbacks de forma formatada
            for feedback in feedbacks:
                st.write(f"**Aluno**: {feedback[0]}")
                st.write(f"**Clareza**: {feedback[1]}")
                st.write(f"**Material de Apoio**: {feedback[2]}")
                st.write(f"**Participação**: {feedback[3]}")
                st.write(f"**Motivação**: {feedback[4]}")
                st.write(f"**Desafio**: {feedback[5]}")
                st.write(f"**Comentários**: {feedback[6]}")
                st.write("-" * 40)

            # Exibir gráficos
            exibir_graficos_feedback(feedbacks)
        else:
            st.write(f"Nenhum feedback encontrado para o professor {nome_professor}.")




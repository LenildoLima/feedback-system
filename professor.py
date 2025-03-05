import streamlit as st
import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt

def conectar_bd():
    return sqlite3.connect(os.path.join(os.getcwd(), 'database', 'feedback.db'), check_same_thread=False)

def obter_feedbacks_do_professor(nome_professor):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT f.disciplina, u.nome, f.clareza, f.material_apoio, f.participacao, f.motivacao, f.desafio, f.comentarios 
        FROM feedbacks f
        JOIN usuarios u ON f.usuario_id = u.id
        WHERE f.professor = ?
    """, (nome_professor,))
    
    feedbacks = cursor.fetchall()
    conn.close()
    return feedbacks

def gerar_relatorios(feedbacks):
    df = pd.DataFrame(feedbacks, columns=["Disciplina", "Aluno", "Clareza", "Material de Apoio", "Participação", "Motivação", "Desafio", "Comentários"])
    
    if df.empty:
        st.info("Nenhum feedback recebido ainda.")
        return
    
    medias = df[["Clareza", "Material de Apoio", "Participação"]].mean()
    st.write("### Médias das Avaliações")
    st.write(medias)
    
    fig, ax = plt.subplots()
    medias.plot(kind="bar", ax=ax, color=['blue', 'green', 'orange'])
    ax.set_ylabel("Média")
    ax.set_title("Média das Avaliações por Critério")
    st.pyplot(fig)
    
    motivados = df["Motivação"].sum() / len(df) * 100
    st.write(f"### Porcentagem de Alunos Motivados: {motivados:.2f}%")

def tela_professor():
    st.title(f"Feedbacks Recebidos - Professor {st.session_state.get('nome_usuario', 'Usuário')}")
    
    if "usuario_id" not in st.session_state or st.session_state.get("tipo_usuario") != "Professor":
        st.error("Acesso negado. Esta página é exclusiva para professores.")
        return
    
    nome_professor = st.session_state.get("nome_usuario")
    feedbacks = obter_feedbacks_do_professor(nome_professor)
    
    gerar_relatorios(feedbacks)




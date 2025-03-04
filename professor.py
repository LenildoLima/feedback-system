import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def conectar_bd():
    return sqlite3.connect(r"C:/Curso Python Estacio/feedback_alunos/database/feedback.db")

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
    
    # Cálculo das médias
    medias = df[["Clareza", "Material de Apoio", "Participação"]].mean()
    st.write("### Médias das Avaliações")
    st.write(medias)
    
    # Gráfico de médias
    fig, ax = plt.subplots()
    medias.plot(kind="bar", ax=ax, color=['blue', 'green', 'orange'])
    ax.set_ylabel("Média")
    ax.set_title("Média das Avaliações por Critério")
    st.pyplot(fig)
    
    # Porcentagem de alunos motivados
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
    
    st.write("### Feedbacks dos Alunos")
    for feedback in feedbacks:
        disciplina, nome_aluno, clareza, material_apoio, participacao, motivacao, desafio, comentarios = feedback
        st.subheader(f"Disciplina: {disciplina}")
        st.write(f"**Aluno:** {nome_aluno}")  
        st.write(f"**Clareza da explicação:** {clareza}/5")
        st.write(f"**Material de apoio:** {material_apoio}/5")
        st.write(f"**Participação:** {participacao}/5")
        st.write(f"**Professor motiva os alunos?** {'Sim' if motivacao == 1 else 'Não'}")
        st.write(f"**Desafios enfrentados:** {desafio}")
        st.write(f"**Comentários adicionais:** {comentarios}")
        st.markdown("---")

    if st.button("Sair"):
        st.session_state["logged_in"] = False
        st.session_state.pop("usuario_id", None)
        st.session_state.pop("nome_usuario", None)
        st.session_state["page"] = "login"
        st.rerun()



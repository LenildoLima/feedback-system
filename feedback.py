import streamlit as st
import sqlite3

# Caminho relativo do banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), "database", "feedback.db")

def conectar_bd():
    return sqlite3.connect(DB_PATH)

def buscar_disciplinas_por_professor(nome_professor):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT disciplinas FROM usuarios WHERE tipo_usuario = 'Professor' AND nome = ?", (nome_professor,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        disciplinas = resultado[0].split(",")  # Separa as disciplinas por vírgula
        return disciplinas
    return []

def enviar_feedback(usuario_id, disciplina, professor, clareza, material_apoio, participacao, motivacao, desafio, comentarios):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(""" 
        INSERT INTO feedbacks (usuario_id, disciplina, professor, clareza, material_apoio, participacao, motivacao, desafio, comentarios) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (usuario_id, disciplina, professor, clareza, material_apoio, participacao, motivacao, desafio, comentarios))
    conn.commit()
    conn.close()
    st.success("✅ Feedback enviado com sucesso!")

def tela_feedback():
    st.title(f"📌 Feedback de Aula - Bem-vindo, {st.session_state.get('nome_usuario', 'Usuário')}")

    if "usuario_id" not in st.session_state:
        st.error("❌ Erro: Usuário não autenticado.")
        return

    usuario_id = st.session_state["usuario_id"]

    # Se o usuário for aluno, exibir a lista de professores
    if st.session_state.get("tipo_usuario") == "Aluno":
        conn = conectar_bd()
        cursor = conn.cursor()

        # Buscar todos os professores cadastrados
        cursor.execute("SELECT nome FROM usuarios WHERE tipo_usuario = 'Professor'")
        professores = [p[0] for p in cursor.fetchall()]
        conn.close()

        if professores:
            professor = st.selectbox("👨‍🏫 Escolha um professor", professores)
            disciplinas = buscar_disciplinas_por_professor(professor)
            if disciplinas:
                disciplina = st.selectbox("📚 Disciplina", disciplinas)
            else:
                disciplina = st.text_input("📚 Disciplina")
        else:
            st.warning("⚠️ Nenhum professor cadastrado.")

    else:
        st.error("❌ Erro: Tipo de usuário inválido.")

    clareza = st.slider("📖 Clareza da explicação", 1, 5, 3)
    material_apoio = st.slider("📂 Qualidade do material de apoio", 1, 5, 3)
    participacao = st.slider("🎤 Possibilidade de participação", 1, 5, 3)
    motivacao = st.radio("🔥 O professor motiva os alunos?", [1, 0], format_func=lambda x: "Sim" if x == 1 else "Não")
    desafio = st.text_area("🚧 Desafios enfrentados")
    comentarios = st.text_area("📝 Comentários adicionais")

    if st.button("✅ Enviar Feedback"):
        if disciplina and professor:
            enviar_feedback(usuario_id, disciplina, professor, clareza, material_apoio, participacao, motivacao, desafio, comentarios)
        else:
            st.error("⚠️ Preencha todos os campos obrigatórios!")

    # 🔴 Botão de Logout (agora dentro da função)
    if st.button("🚪 Sair"):
        st.session_state["logged_in"] = False
        st.session_state.pop("usuario_id", None)
        st.session_state.pop("nome_usuario", None)
        st.session_state["page"] = "login"
        st.rerun()  # Atualiza a página e volta para o login

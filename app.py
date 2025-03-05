import streamlit as st
import sqlite3
import bcrypt
import os
from feedback import tela_feedback  # Importando a tela de feedback
from professor import tela_professor  # Importando a tela do professor

# Caminho relativo do banco de dados
DB_PATH = os.path.join(os.getcwd(), 'database', 'feedback.db')

# Função para conectar ao banco de dados
def conectar_bd():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# Função para cadastrar usuário
def cadastrar_usuario(nome, email, senha, tipo_usuario, ano_turma, disciplinas):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        cursor.execute("INSERT INTO usuarios (nome, email, senha, tipo_usuario, ano_turma, disciplinas) VALUES (?, ?, ?, ?, ?, ?)",
                       (nome, email, senha_hash, tipo_usuario, ano_turma, disciplinas))
        conn.commit()
        st.success("Usuário cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        st.error("Erro: Email já cadastrado!")
    finally:
        conn.close()

# Função para verificar login
def verificar_login(email, senha):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    conn.close()
    
    if usuario and bcrypt.checkpw(senha.encode(), usuario[3]):
        return usuario
    return None

# Gerenciando a navegação entre páginas
def tela_login():
    st.title("Sistema de Feedback - Login & Cadastro")
    
    menu = st.sidebar.selectbox("Menu", ["Login", "Cadastro"])
    
    if menu == "Cadastro":
        st.subheader("Cadastro de Usuário")
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        tipo_usuario = st.selectbox("Tipo de Usuário", ["Aluno", "Professor", "Administrador"])
        ano_turma = st.text_input("Ano/Turma (se aluno)")
        disciplinas = st.text_input("Disciplinas (se professor)")
        if st.button("Cadastrar"):
            cadastrar_usuario(nome, email, senha, tipo_usuario, ano_turma, disciplinas)
    
    elif menu == "Login":
        st.subheader("Login de Usuário")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            usuario = verificar_login(email, senha)
            if usuario:
                st.session_state["usuario_id"] = usuario[0]
                st.session_state["nome_usuario"] = usuario[1]
                st.session_state["tipo_usuario"] = usuario[4]  # Salva o tipo de usuário
                st.session_state["logged_in"] = True
                st.session_state["page"] = "menu"  # Define a página inicial após login
                st.rerun()
            else:
                st.error("Email ou senha incorretos!")

# Tela principal após login
def tela_menu():
    st.sidebar.title("Menu Principal")
    tipo_usuario = st.session_state.get("tipo_usuario", "")
    
    if tipo_usuario == "Aluno":
        st.sidebar.button("Feedback", on_click=lambda: st.session_state.update({"page": "feedback"}))
    elif tipo_usuario == "Professor":
        st.sidebar.button("Meus Feedbacks", on_click=lambda: st.session_state.update({"page": "professor"}))
    
    if st.sidebar.button("Sair"):
        st.session_state.clear()
        st.rerun()

# Controle de navegação
if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    if st.session_state["logged_in"]:
        if st.session_state["page"] == "feedback" and st.session_state["tipo_usuario"] == "Aluno":
            tela_feedback()
        elif st.session_state["page"] == "professor" and st.session_state["tipo_usuario"] == "Professor":
            tela_professor()  # Chamando a tela de feedback para o professor
        else:
            tela_menu()
    else:
        tela_login()




import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.markdown('<body>', unsafe_allow_html=True)
st.title("🤖 Chatbot - paso 2 - con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit.")

st.markdown(
    """
    <style>
    .stapp { 
        background-color: #e0ffe0;
    }
    [data-testid="stSidebar"] > div:first-child {
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    sidebar {
        background-color: #d0f0c0;
    }
    .sidebar-top {
        flex-grow: 1; 
    }
    .sidebar-bottom {
        margin-top: 0; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown('<div class="sidebar-top">', unsafe_allow_html=True)
    st.write("📂 Apartados principales")
    if st.button("Historial"):
        if "titulo_chat" in st.session_state:
            st.write(f"**Chat Actual:** {st.session_state.titulo_chat}")
        else:
            st.write("No hay historial activo.")
    if st.button("Ayuda"):
        st.write("Aquí mostrarías la ayuda o documentación")
    st.markdown('</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-bottom">', unsafe_allow_html=True)
    st.divider()
    st.write("⚙️ Configuración avanzada")

    model_options = ["gemini-1.5-flash", "gemini-1.5-pro"]
    selected_model = st.selectbox("Selecciona el modelo", model_options, index=0)

    temperature = st.slider("Temperatura", 0.0, 1.0, 0.7, 0.1)

    if st.button("Limpiar Chat"):
        st.session_state.mensajes = []
        if "titulo_chat" in st.session_state:
            del st.session_state.titulo_chat
        st.rerun()

    st.markdown('</div></body>', unsafe_allow_html=True)

chat_model = ChatGoogleGenerativeAI(model=selected_model, temperature=temperature)


if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)
    st.session_state.mensajes.append(HumanMessage(content=pregunta))

    respuesta = chat_model.invoke(st.session_state.mensajes)
    with st.chat_message("assistant"):
        st.markdown(respuesta.content)
    st.session_state.mensajes.append(respuesta)
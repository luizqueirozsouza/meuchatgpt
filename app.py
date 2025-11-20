import streamlit as st
from datetime import datetime
import requests
import json
from auth import login


# Configuração da página
st.set_page_config(
    page_title="Chat com IA",
    page_icon="🤖",
    layout="centered"
)

# Login
if not login():
    st.stop()


# Título do aplicativo
st.title("🤖 Chat com IA via OpenRouter")
st.write("Conteúdo protegido…")
# Sidebar com configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Input para API Key
    api_key = st.text_input(
        "OpenRouter API Key",
        type="password",
        help="Insira sua chave de API do OpenRouter"
    )
    
    # Seleção do modelo
    model = st.selectbox(
        "Modelo",
        [
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4-turbo",
            "openai/gpt-3.5-turbo",
            "google/gemini-2.5-flash",
            "google/gemini-2.5-pro",
            "meta-llama/llama-3.1-70b-instruct",
            "anthropic/claude-3-opus",
            "z-ai/glm-4.6"
        ],
        help="Escolha o modelo de IA"
    )
    
    # Temperatura
    temperature = st.slider(
        "Temperatura",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Controla a criatividade das respostas"
    )
    
    st.divider()
    
    # Botão limpar chat
    if st.button("🗑️ Limpar Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # Estatísticas
    st.subheader("📊 Estatísticas")
    if "messages" in st.session_state:
        total = len(st.session_state.messages)
        user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")
        assistant_msgs = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
        
        st.metric("Total de Mensagens", total)
        st.metric("Suas Mensagens", user_msgs)
        st.metric("Respostas da IA", assistant_msgs)

# Inicializar o histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "timestamp" in message:
            st.caption(message["timestamp"])

# Função para chamar a API do OpenRouter
def get_ai_response(messages, api_key, model, temperature):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Preparar mensagens para a API (sem timestamps)
    api_messages = [{"role": m["role"], "content": m["content"]} for m in messages]
    
    payload = {
        "model": model,
        "messages": api_messages,
        "temperature": temperature
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Erro ao comunicar com a API: {str(e)}"
    except (KeyError, json.JSONDecodeError) as e:
        return f"Erro ao processar resposta da API: {str(e)}"

# Input do usuário
if prompt := st.chat_input("Digite sua mensagem..."):
    if not api_key:
        st.error("⚠️ Por favor, insira sua API Key do OpenRouter na barra lateral.")
    else:
        # Adicionar mensagem do usuário
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": timestamp
        })
        
        # Exibir mensagem do usuário
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(timestamp)
        
        # Obter resposta da IA
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = get_ai_response(
                    st.session_state.messages,
                    api_key,
                    model,
                    temperature
                )
            
            st.markdown(response)
            timestamp_bot = datetime.now().strftime("%H:%M:%S")
            st.caption(timestamp_bot)
        
        # Adicionar resposta ao histórico
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "timestamp": timestamp_bot
        })

# Informações no rodapé
st.divider()
st.caption("💡 Powered by OpenRouter - Acesso a múltiplos modelos de IA em uma única API")
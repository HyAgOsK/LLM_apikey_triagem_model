import streamlit as st
import os
import google.generativeai as genai


# App title
st.set_page_config(page_title="Triagem Chat 📍", page_icon=":heavy_heart_exclamation_mark_ornament:")


# Initialize Gemini-Pro 
genai.configure(api_key="AIzaSyDvhexcZ8XV2qwMpDUHslpXCv0Tb6urrJI")
generation_config = {
    "candidate_count": 1,  # Número de sugestões a serem geradas
    "temperature": 0.5,   # Nível de criatividade (0 = mais conservador, 1 = mais criativo)
}

safety_settings = {
    'HATE': 'BLOCK_NONE',
    'HARASSMENT': 'BLOCK_NONE',
    'SEXUAL': 'BLOCK_NONE',
    'DANGEROUS': 'BLOCK_NONE'
}

model = genai.GenerativeModel(
model_name="gemini-1.0-pro",
generation_config=generation_config,
safety_settings=safety_settings,)

# Gemini uses 'model' for assistant; Streamlit uses 'assistant'
def role_to_streamlit(role):
  if role == "model":
    return "assistant"
  else:
    return role

# Add a Gemini Chat history object to Streamlit session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history = [
  {
    "role": "user",
    "parts": ["Como posso utilizar?"]
  },
  {
    "role": "model",
    "parts": ["Descreva, a necessidade, e se possível a área médica!"]
  },
])

# Título e Subtítulo
st.title(":blue[tr] :violet[IA] :blue[gem] :heart: :hospital: 📍")
st.subheader("Informe em uma linha apenas, sua necessidade :memo:")

# Instruções formatadas
st.markdown("""
<div style="background-color: #000; padding: 15px; border-radius: 10px;">
    <h4>Como utilizar:</h4>
    <ul>
      <li><strong>Intenção: </strong> <em>Necessidade, problema de saúde, urgência...</em></li>
      <li><strong>Setor da saúde: </strong> <em>Área da saúde, neurologia, cardiologia, psiquiatria...</em></li>
      <li><strong>Localidade: </strong> <em>Localidade mais próxima do posto de saúde UBS ou Hospital (Cidade, Estado, País)...</em></li>
    </ul>
</div>
""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
st.divider()

# Display chat messages from history above current input box
for message in st.session_state.chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("Descreva sua necessidade e se possível a área médica"):
    # Display user's last message
    st.chat_message("user").markdown(prompt)
    # Send user entry to Gemini and read the response
    response = st.session_state.chat.send_message(prompt) 
    
    # Display last 
    with st.chat_message("assistant"):
        st.markdown(response.text)
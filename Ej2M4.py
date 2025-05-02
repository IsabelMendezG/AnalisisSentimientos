import streamlit as st
from openai import OpenAI

# ⚠️ Configura tu clave API personal

API_KEY = st.secrets["OPENROUTER_API_KEY"]

# Inicializa el cliente de OpenAI vía OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

# Función para pedir análisis al modelo
def analizar_sentimiento_openai(texto):
    prompt = f"""
Analiza el siguiente texto en español y responde en formato JSON con:
- sentimiento: "positivo", "negativo" o "neutral"
- emoji: un solo emoji representativo
- justificacion: una frase que explique por qué se clasificó así

Texto:
\"\"\"{texto}\"\"\"
    """

    respuesta = client.chat.completions.create(
        model="qwen/qwen3-1.7b:free",
        messages=[
            {"role": "user", "content": prompt}
        ],
        extra_headers={
            "HTTP-Referer": "https://tu-sitio-ejemplo.com",  # Opcional
            "X-Title": "Analizador Sentimental",              # Opcional
        },
    )

    # Extraemos y evaluamos la respuesta como diccionario
    import json
    contenido = respuesta.choices[0].message.content
    try:
        resultado = json.loads(contenido)
        return resultado
    except Exception as e:
        return {"error": f"No se pudo interpretar la respuesta: {e}\nRespuesta: {contenido}"}

# ---- Streamlit UI ----

st.set_page_config(page_title="Análisis de Sentimiento (OpenAI)", page_icon="🧠")

st.title("🧠 Análisis de Sentimiento con OpenAI (Español)")
st.markdown("Usa un modelo de lenguaje para analizar el tono de un texto en español. El resultado incluye un emoji y una justificación breve.")

texto_usuario = st.text_area("✍️ Escribe tu texto aquí:", height=200)

if st.button("🔍 Analizar Sentimiento"):
    if texto_usuario.strip() == "":
        st.warning("Por favor escribe un texto para analizar.")
    else:
        with st.spinner("Consultando al modelo..."):
            resultado = analizar_sentimiento_openai(texto_usuario)

        if "error" in resultado:
            st.error(resultado["error"])
        else:
            st.markdown(f"### Resultado: {resultado['sentimiento'].capitalize()} {resultado['emoji']}")
            st.markdown(f"**Justificación:** {resultado['justificacion']}")

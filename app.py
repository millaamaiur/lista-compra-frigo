import json
import streamlit as st
from supabase import create_client

# --- Conexión a Supabase ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# --- Configuración de página ---
st.set_page_config(page_title="Falta comprar", page_icon="🛒", layout="centered")

# --- Meta tags para que se comporte como app nativa en iPhone ---
st.markdown(
    """
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Falta comprar">
    """,
    unsafe_allow_html=True,
)

# --- Estilos ---
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
    }

    .stApp {
        max-width: 480px;
        margin: 0 auto;
    }
    .block-container {
        padding-top: max(1.5rem, env(safe-area-inset-top));
        padding-bottom: 3rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }

    h1 {
        font-size: 28px !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-baseweb="select"] {
        font-size: 16px !important;
        min-height: 46px !important;
    }

    div[data-testid="stFormSubmitButton"] button {
        width: 100%;
        background: #34a853 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 15px !important;
    }

    hr {
        margin: 1.2rem 0 !important;
        opacity: 0.15;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🛒 Falta comprar")
st.caption("Añade lo que se acabe. Se guarda al momento para todos.")
st.divider()

# --- Añadir item ---
with st.form("form_anadir", clear_on_submit=True):
    entrada = st.text_input("Introduce lo que hay que comprar")
    enviado = st.form_submit_button("Enviar")

if enviado:
    texto = entrada.strip()
    if texto:
        supabase.table("items").insert({"texto": texto}).execute()
        st.toast("Añadido ✅")
        st.rerun()

st.divider()

# --- Vaciar lista tras la compra ---
if st.button("✅ Compra hecha"):
    supabase.table("items").delete().neq("id", 0).execute()
    st.toast("Lista vaciada 🧹")
    st.rerun()

st.divider()

# --- Mostrar la lista + botón de copiar ---
lista = supabase.table("items").select("*").order("creado_en").execute().data

if not lista:
    st.caption("No falta nada por ahora 🎉")
else:
    for diccionario in lista:
        st.write(diccionario["texto"])

    texto_lista = "\n".join(diccionario["texto"] for diccionario in lista)
    texto_js = json.dumps(texto_lista)

    st.components.v1.html(
        f"""
        <button id="btn-copiar" style="
            width: 100%;
            background: #34a853;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px;
            font-size: 15px;
            font-weight: 600;
            font-family: -apple-system, sans-serif;
            cursor: pointer;
            margin-top: 8px;
        ">📋 Copiar lista</button>

        <script>
        const boton = document.getElementById("btn-copiar");
        boton.addEventListener("click", () => {{
            navigator.clipboard.writeText({texto_js});
            boton.innerText = "✅ Copiado";
            setTimeout(() => {{ boton.innerText = "📋 Copiar lista"; }}, 1500);
        }});
        </script>
        """,
        height=60,
    )   
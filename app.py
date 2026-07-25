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

    div[data-testid="stHorizontalBlock"] {
        background: #f7f7f9;
        border-radius: 14px;
        padding: 10px 14px;
        margin-bottom: 8px;
        align-items: center;
    }

    div[data-testid="stHorizontalBlock"] button {
        border-radius: 50% !important;
        width: 38px;
        height: 38px;
        background: #eee !important;
        color: #888 !important;
        border: none !important;
        font-size: 15px !important;
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

# --- Mostrar la lista ---
lista = supabase.table("items").select("*").order("creado_en").execute().data

if not lista:
    st.caption("No falta nada por ahora 🎉")
else:
    for diccionario in lista:
        col_texto, col_borrar = st.columns([5, 1])
        with col_texto:
            st.write(f"🔹 {diccionario['texto']}")
        with col_borrar:
            if st.button("✕", key=f"borrar_{diccionario['id']}"):
                supabase.table("items").delete().eq("id", diccionario["id"]).execute()
                st.rerun()

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

# --- Vaciar lista tras la compra (con confirmación) ---
confirmar = st.checkbox("Confirmar vaciado de la lista")
if st.button("✅ Compra hecha", disabled=not confirmar):
    supabase.table("items").delete().neq("id", 0).execute()
    st.toast("Lista vaciada 🧹")
    st.rerun()
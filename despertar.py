from playwright.sync_api import sync_playwright

URL = "https://lista-compra-frigo.streamlit.app/"  # <-- pon aquí tu URL real

with sync_playwright() as p:
    navegador = p.chromium.launch()
    pagina = navegador.new_page()
    pagina.goto(URL, timeout=60000)

    # Si sale la pantalla de "app dormida", busca el botón y lo pulsa
    try:
        boton = pagina.get_by_text("get this app back up", exact=False)
        if boton.is_visible(timeout=5000):
            boton.click()
            print("App estaba dormida, despertando...")
            pagina.wait_for_timeout(15000)  # espera a que arranque
    except Exception:
        print("App ya estaba despierta, no hacía falta botón.")

    navegador.close()
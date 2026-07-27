from playwright.sync_api import sync_playwright

URL = "https://lista-compra-frigo.streamlit.app"

with sync_playwright() as p:
    navegador = p.chromium.launch()
    pagina = navegador.new_page()
    pagina.goto(URL, wait_until="networkidle", timeout=120000)

    try:
        boton = pagina.get_by_role("button", name="Yes, get this app back up!")
        if boton.is_visible(timeout=5000):
            print("App estaba dormida, despertando...")
            boton.click()
            pagina.wait_for_timeout(30000)  # espera a que arranque de verdad
        else:
            print("App ya estaba despierta.")
    except Exception:
        print("App ya estaba despierta.")

    # Simula actividad real y da tiempo a que la visita se registre
    pagina.mouse.click(200, 200)
    pagina.wait_for_timeout(30000)

    navegador.close()
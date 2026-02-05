"""
Versão alternativa usando Selenium para páginas com JavaScript.
Requer: pip install selenium webdriver-manager
"""
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  Selenium não instalado. Use: pip install selenium webdriver-manager")

import pandas as pd
from datetime import date
import time

B3_URL = (
    "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/mercado-de-derivativos/precos-referenciais/taxas-referenciais-bm-fbovespa/"
)

def extract_di_pre_selenium(data_base: date) -> pd.DataFrame:
    """
    Extração usando Selenium para renderizar JavaScript.
    Use esta função se a página carregar dados via JavaScript.
    """
    if not SELENIUM_AVAILABLE:
        raise ImportError("Selenium não está instalado. Instale com: pip install selenium webdriver-manager")
    
    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa sem abrir janela
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = None
    try:
        # Inicializar driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Construir URL com parâmetros
        params = f"?Data={data_base.strftime('%d/%m/%Y')}&Curva=DI x Pré"
        url = B3_URL + params
        
        print(f"🌐 Acessando: {url}")
        driver.get(url)
        
        # Aguardar carregamento (até 30 segundos)
        wait = WebDriverWait(driver, 30)
        
        # Aguardar tabela aparecer
        try:
            tabela = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            print("✅ Tabela encontrada!")
        except:
            print("⚠️  Tabela não encontrada, tentando aguardar mais...")
            time.sleep(5)  # Aguarda 5 segundos adicionais
            tabela = driver.find_element(By.TAG_NAME, "table")
        
        # Extrair dados da tabela
        dados = []
        linhas = tabela.find_elements(By.TAG_NAME, "tr")[1:]  # Pula cabeçalho
        
        for row in linhas:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 2:
                continue
            
            try:
                vertice = int(cols[0].text.strip())
                taxa_str = cols[1].text.strip().replace(",", ".").replace(" ", "").replace("%", "")
                taxa = float(taxa_str)
                
                dados.append({
                    "curva": "DI_PRE",
                    "data_base": data_base,
                    "vertice_dias": vertice,
                    "taxa": taxa
                })
            except (ValueError, IndexError):
                continue
        
        if not dados:
            raise ValueError("Nenhum dado extraído da tabela")
        
        print(f"✅ Extraídos {len(dados)} registros")
        return pd.DataFrame(dados)
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    from datetime import date, timedelta
    data_teste = date.today() - timedelta(days=1)
    df = extract_di_pre_selenium(data_teste)
    print(df.head())

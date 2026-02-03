import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date

B3_URL = (
    "https://www.b3.com.br/pt_br/market-data-e-indices/"
    "servicos-de-dados/market-data/consultas/"
    "mercado-de-derivativos/precos-referenciais/"
    "taxas-referenciais-bm-fbovespa/"
)

def extract_di_pre(data_base: date) -> pd.DataFrame:
    """
    Extração simplificada da curva DI x Pré para uma data-base.
    Implementação propositalmente enxuta (PoC para o case).
    """

    params = {
        "Data": data_base.strftime("%d/%m/%Y"),
        "Curva": "DI x Pré"
    }

    response = requests.get(B3_URL, params=params, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    tabela = soup.find("table")
    if not tabela:
        raise ValueError("Tabela de taxas não encontrada na página da B3")

    dados = []
    for row in tabela.find_all("tr")[1:]:
        cols = [c.text.strip() for c in row.find_all("td")]
        if len(cols) < 2:
            continue

        vertice = int(cols[0])
        taxa = float(cols[1].replace(",", "."))

        dados.append({
            "curva": "DI_PRE",
            "data_base": data_base,
            "vertice_dias": vertice,
            "taxa": taxa
        })

    return pd.DataFrame(dados)


if __name__ == "__main__":
    # Exemplo de uso
    from datetime import date, timedelta
    
    # Testa com ontem (geralmente tem dados)
    data_teste = date.today() - timedelta(days=1)
    
    print(f"Extraindo curva DI x Pré para: {data_teste}")
    df = extract_di_pre(data_teste)
    
    print(f"\n✅ Extraídos {len(df)} registros")
    print("\nPrimeiras linhas:")
    print(df.head())
"""
Script de debug para identificar problemas na extração da B3
"""
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta

B3_URL = (
    "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/mercado-de-derivativos/precos-referenciais/taxas-referenciais-bm-fbovespa/"
)

def debug_b3_page(data_teste=None):
    """Debug da página da B3"""
    
    if data_teste is None:
        data_teste = date.today() - timedelta(days=1)
    
    params = {
        "Data": data_teste.strftime("%d/%m/%Y"),
        "Curva": "DI x Pré"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    
    print("=" * 60)
    print(f"🔍 DEBUG - Extração B3 para {data_teste}")
    print("=" * 60)
    
    try:
        print(f"\n1️⃣  Fazendo requisição...")
        print(f"   URL: {B3_URL}")
        print(f"   Parâmetros: {params}")
        
        response = requests.get(B3_URL, params=params, headers=headers, timeout=30)
        
        print(f"\n2️⃣  Resposta recebida:")
        print(f"   Status: {response.status_code}")
        print(f"   URL final: {response.url}")
        print(f"   Tamanho HTML: {len(response.text)} caracteres")
        
        if response.status_code != 200:
            print(f"   ❌ Erro HTTP: {response.status_code}")
            return
        
        print(f"\n3️⃣  Analisando HTML...")
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Procura tabelas
        tabelas = soup.find_all("table")
        print(f"   Tabelas encontradas: {len(tabelas)}")
        
        if tabelas:
            for i, tabela in enumerate(tabelas):
                linhas = tabela.find_all("tr")
                print(f"   Tabela {i+1}: {len(linhas)} linhas")
                if linhas:
                    primeira_linha = [c.text.strip() for c in linhas[0].find_all(["td", "th"])]
                    print(f"      Primeira linha: {primeira_linha[:5]}...")
        else:
            print("   ⚠️  Nenhuma tabela encontrada!")
            
            # Procura por padrões
            texto = response.text.lower()
            if "taxa" in texto:
                print("   ✅ Palavra 'taxa' encontrada no HTML")
            if "di" in texto:
                print("   ✅ Palavra 'di' encontrada no HTML")
            if "javascript" in texto or "ajax" in texto:
                print("   ⚠️  Possível carregamento via JavaScript detectado")
            
            # Procura por divs com classes relacionadas
            divs_com_tabela = soup.find_all("div", class_=lambda x: x and ("table" in str(x).lower() or "data" in str(x).lower()))
            print(f"   Divs com 'table' ou 'data': {len(divs_com_tabela)}")
        
        print(f"\n4️⃣  Salvando HTML para análise...")
        with open("debug_b3.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"   ✅ HTML salvo em: debug_b3.html")
        
        print(f"\n5️⃣  Verificando se há mensagens de erro...")
        if "não encontrado" in response.text.lower() or "sem dados" in response.text.lower():
            print("   ⚠️  Possível mensagem de 'sem dados' encontrada")
        
        print("\n" + "=" * 60)
        print("✅ Debug concluído!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_b3_page()

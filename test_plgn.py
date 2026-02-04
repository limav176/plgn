"""
Script de teste para a função extract_di_pre

"""
from datetime import date, timedelta
from plgn import extract_di_pre

# Testa com a data de ontem (geralmente tem dados)
data_teste = date.today() - timedelta(days=1)

print(f"Testando extração para data-base: {data_teste}")
print("-" * 50)

try:
    df = extract_di_pre(data_teste)
    
    print(f"\n✅ Sucesso! Extraídos {len(df)} registros")
    print("\nPrimeiras linhas:")
    print(df.head(10))
    print(f"\nÚltimas linhas:")
    print(df.tail(5))
    print(f"\nEstatísticas:")
    print(df.describe())
    
except Exception as e:
    print(f"\n❌ Erro: {e}")
    print("\nDica: Tente com uma data mais antiga ou verifique sua conexão com a internet")

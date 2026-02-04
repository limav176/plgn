"""
Teste simplificado do pipeline - testa as funções sem Airflow
"""
from datetime import datetime, date, timedelta
import pandas as pd
from plgn import extract_di_pre

# Simula XCom (armazenamento entre tasks)
xcom_storage = {}

def check_business_day(ds):
    """Valida se é dia útil e não é data futura"""
    exec_date = datetime.strptime(ds, "%Y-%m-%d")
    exec_date_date = exec_date.date()
    
    # Validar se não é futuro
    if exec_date_date > date.today():
        raise ValueError(f"❌ {ds} é uma data futura - não há dados disponíveis na B3")
    
    # Validar se é dia útil
    if exec_date.weekday() >= 5:
        raise ValueError(f"❌ {ds} não é dia útil (B3 não opera em finais de semana)")
    
    print(f"✅ {ds} é dia útil")
    return True

def extract_taxas(ds):
    """Extrai taxas usando plgn.py"""
    data_base = datetime.strptime(ds, "%Y-%m-%d").date()
    df = extract_di_pre(data_base)
    xcom_storage["df_raw"] = df
    print(f"✅ Extraídos {len(df)} registros")
    return df

def validate_raw():
    """Validação básica dos dados"""
    df = xcom_storage.get("df_raw")
    if df is None or df.empty:
        raise ValueError("DataFrame vazio")
    print(f"✅ Validação OK: {len(df)} registros")
    return True

def transform_to_silver():
    """Transformação mínima para Silver"""
    df = xcom_storage.get("df_raw")
    df = df.copy()
    df["processed_at"] = datetime.now()
    xcom_storage["df_silver"] = df
    print(f"✅ Silver: {len(df)} registros")
    return df

def publish_gold():
    """Publica dados Gold"""
    df = xcom_storage.get("df_silver")
    print(f"✅ Gold publicado: {len(df)} registros")
    print("\nPrimeiras linhas:")
    print(df.head())
    return df

def update_control_table(ds):
    """Atualiza controle"""
    print(f"✅ Controle atualizado para {ds}")

def testar_pipeline(data_teste=None):
    """Testa o pipeline completo"""
    
    if data_teste is None:
        # Usa ontem e vai retrocedendo até encontrar dia útil
        data_teste = date.today() - timedelta(days=1)
        max_tentativas = 7  # Evita loop infinito
        tentativas = 0
        
        while data_teste.weekday() >= 5 and tentativas < max_tentativas:
            data_teste = data_teste - timedelta(days=1)
            tentativas += 1
    
    # Validar que não é data futura
    if data_teste > date.today():
        raise ValueError(f"❌ Data de teste ({data_teste}) não pode ser futura!")
    
    ds = data_teste.strftime("%Y-%m-%d")
    
    print("=" * 60)
    print(f"🧪 TESTANDO PIPELINE PARA DATA: {data_teste}")
    print(f"   Data de hoje: {date.today()}")
    print("=" * 60)
    
    try:
        # 1. Check Business Day
        print("\n1️⃣  check_business_day")
        check_business_day(ds)
        
        # 2. Extract
        print("\n2️⃣  extract_taxas")
        extract_taxas(ds)
        
        # 3. Validate
        print("\n3️⃣  validate_raw")
        validate_raw()
        
        # 4. Transform to Silver
        print("\n4️⃣  transform_to_silver")
        transform_to_silver()
        
        # 5. Publish Gold
        print("\n5️⃣  publish_gold")
        publish_gold()
        
        # 6. Update Control
        print("\n6️⃣  update_control_table")
        update_control_table(ds)
        
        print("\n" + "=" * 60)
        print("✅ PIPELINE TESTADO COM SUCESSO!")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ ERRO: {str(e)}")
        print("=" * 60)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_pipeline()
    
    print("\n" + "-" * 60)
    print("💡 Dica: Para testar com outra data, use:")
    print("   testar_pipeline(date(2024, 1, 15))")

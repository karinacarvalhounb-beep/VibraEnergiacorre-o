"""
01_importacao_dados.py
Geração e estruturação da base sintética de Intangíveis (520.126 linhas).
Semente aleatória: 200058789 (Matrícula UnB)
"""

import numpy as np
import pandas as pd
import gzip

def gerar_base_sintetica(n_registros=520126, seed=200058789):
    np.random.seed(seed)
    print(f"Gerando base sintética com {n_registros} registros (Semente: {seed})...")
    
    ids = [f"REG-{i+1:07d}" for i in range(n_registros)]
    datas = pd.date_range(start="2025-01-01", end="2025-12-31", periods=n_registros)
    
    cgus = np.random.choice(["Comerc Energia", "Rede Postos", "Aviação", "Lubrificantes", "Conveniência"], 
                            size=n_registros, p=[0.35, 0.30, 0.15, 0.10, 0.10])
    
    contas = np.random.choice(["1.2.01.01", "1.2.01.02", "1.2.01.03", "1.2.01.04"], 
                              size=n_registros, p=[0.40, 0.30, 0.15, 0.15])
    
    descricoes_map = {
        "1.2.01.01": "Ágio por Expectativa de Rentabilidade Futura (Goodwill) - Aq. Comerc",
        "1.2.01.02": "Licenças de Software ERP e Sistemas de Gestão de Frota",
        "1.2.01.03": "Marcas e Patentes Comerciais Registradas",
        "1.2.01.04": "Direitos de Exploração e Concessões Operacionais"
    }
    descricoes = [descricoes_map[c] for c in contas]
    
    # Valores históricos (distribuição log-normal realista)
    valores_historicos = np.round(np.random.lognormal(mean=8.5, sigma=1.2, size=n_registros), 2)
    # Ajuste para garantir que ágios tenham valores maiores
    valores_historicos = np.where(contas == "1.2.01.01", valores_historicos * 3.5, valores_historicos)
    
    taxa_amortizacao = np.where(contas == "1.2.01.01", 0.0,
                         np.where(contas == "1.2.01.02", 0.20,
                           np.where(contas == "1.2.01.03", 0.10, 0.05)))
    
    vida_util = np.where(contas == "1.2.01.01", 0,
                  np.where(contas == "1.2.01.02", 60,
                    np.where(contas == "1.2.01.03", 120, 240)))
    
    amort_acumulada = np.round(valores_historicos * taxa_amortizacao * np.random.uniform(0.1, 0.8, size=n_registros), 2)
    valor_liquido = np.round(valores_historicos - amort_acumulada, 2)
    
    indicador_impairment = np.random.choice([0, 1], size=n_registros, p=[0.97, 0.03])
    
    df = pd.DataFrame({
        "id_registro": ids,
        "data_lancamento": datas.strftime("%Y-%m-%d"),
        "cgu_unidade": cgus,
        "conta_contabil": contas,
        "descricao_ativo": descricoes,
        "valor_historico": valores_historicos,
        "amortizacao_acumulada": amort_acumulada,
        "valor_liquido": valor_liquido,
        "taxa_amortizacao_anual": taxa_amortizacao,
        "vida_util_meses": vida_util,
        "indicador_impairment": indicador_impairment
    })
    
    return df

if __name__ == "__main__":
    df = gerar_base_sintetica()
    output_path = "dados/dados_originais/base_intangivel_sintetica.csv.gz"
    df.to_csv(output_path, index=False, compression="gzip")
    print(f"Base sintética gravada com sucesso em {output_path} ({len(df)} linhas).")

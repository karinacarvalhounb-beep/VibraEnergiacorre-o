"""
02_tratamento_dados.py
Injeção de erros de controle (T-01 a T-09) e geração das bases tratadas e verdade de terreno.
"""

import pandas as pd
import numpy as np

def injetar_erros(df_input):
    df = df_input.copy()
    erros = []
    
    # T-01: Amortização indevida sobre ágio (vida útil indefinida)
    mask_t01 = (df['conta_contabil'] == '1.2.01.01')
    idx_t01 = df[mask_t01].sample(n=150, random_state=42).index
    for idx in idx_t01:
        val_orig = df.loc[idx, 'amortizacao_acumulada']
        erro_val = round(df.loc[idx, 'valor_historico'] * 0.10, 2)
        df.loc[idx, 'amortizacao_acumulada'] += erro_val
        df.loc[idx, 'valor_liquido'] -= erro_val
        erros.append({
            'id_registro': df.loc[idx, 'id_registro'],
            'teste': 'T-01',
            'descricao': 'Amortização indevida calculada sobre ágio de vida útil indefinida',
            'valor_distorcao': erro_val
        })
        
    # T-02: Erro de cálculo na taxa de amortização de softwares (ERP)
    mask_t02 = (df['conta_contabil'] == '1.2.01.02')
    idx_t02 = df[mask_t02].sample(n=200, random_state=42).index
    for idx in idx_t02:
        erro_val = round(df.loc[idx, 'valor_historico'] * 0.05, 2)
        df.loc[idx, 'amortizacao_acumulada'] += erro_val
        df.loc[idx, 'valor_liquido'] -= erro_val
        erros.append({
            'id_registro': df.loc[idx, 'id_registro'],
            'teste': 'T-02',
            'descricao': 'Taxa de amortização incorreta aplicada a softwares',
            'valor_distorcao': erro_val
        })
        
    # T-03: Falta de teste de impairment na CGU Comerc Energia com indicativo de perda
    mask_t03 = (df['cgu_unidade'] == 'Comerc Energia') & (df['indicador_impairment'] == 1)
    idx_t03 = df[mask_t03].sample(n=100, random_state=42).index
    for idx in idx_t03:
        erro_val = round(df.loc[idx, 'valor_liquido'] * 0.25, 2)
        erros.append({
            'id_registro': df.loc[idx, 'id_registro'],
            'teste': 'T-03',
            'descricao': 'Falta de reconhecimento de perda por impairment na CGU Comerc Energia',
            'valor_distorcao': erro_val
        })

    # T-04 a T-09 Erros adicionais sintéticos de classificação, duplicidade e corte
    idx_outros = df.drop(index=list(idx_t01) + list(idx_t02) + list(idx_t03)).sample(n=350, random_state=42).index
    testes_list = ['T-04', 'T-05', 'T-06', 'T-07', 'T-08', 'T-09']
    for i, idx in enumerate(idx_outros):
        t_code = testes_list[i % len(testes_list)]
        erro_val = round(df.loc[idx, 'valor_liquido'] * 0.15, 2)
        erros.append({
            'id_registro': df.loc[idx, 'id_registro'],
            'teste': t_code,
            'descricao': f'Inconsistência identificada no teste substantivo {t_code}',
            'valor_distorcao': erro_val
        })
        
    df_erros = pd.DataFrame(erros)
    return df, df_erros

if __name__ == "__main__":
    df_orig = pd.read_csv("dados/dados_originais/base_intangivel_sintetica.csv.gz")
    df_trat, df_erros = injetar_erros(df_orig)
    
    df_trat.to_csv("dados/dados_tratados/base_intangivel_tratada.csv.gz", index=False, compression="gzip")
    df_erros.to_csv("dados/dados_tratados/registro_erros_inseridos.csv", index=False)
    df_orig.to_csv("dados/dados_tratados/verdade_terreno_valores_corretos.csv.gz", index=False, compression="gzip")
    print("Processamento de dados e injeção de erros finalizados.")

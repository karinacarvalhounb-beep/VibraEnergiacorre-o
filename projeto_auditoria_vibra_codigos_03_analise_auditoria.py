"""
03_analise_auditoria.py
Cálculo de materialidade (PT 320) e sensibilidade de Impairment (PT 540).
"""
import pandas as pd
import numpy as np

def calcular_materialidade():
    # Referência Vibra Energia 2025: Lucro Antes dos Impostos / Lucro Operacional R$ 3,2 Bi
    base_calculo = 3200000000.0  # R$ 3,2 Bilhões
    pm_pct = 0.05                # 5% do benchmark
    te_pct = 0.75                # 75% da PM
    ctt_pct = 0.05               # 5% da PM
    
    pm = base_calculo * pm_pct
    te = pm * te_pct
    ctt = pm * ctt_pct
    
    df_mat = pd.DataFrame([{
        "Métrica": "Base de Calculo (LAIR Estimado)",
        "Percentual (%)": "-",
        "Valor (R$)": base_calculo
    }, {
        "Métrica": "Materialidade Planejada (PM - PT 320)",
        "Percentual (%)": "5.0%",
        "Valor (R$)": pm
    }, {
        "Métrica": "Distorção Tolerável (TE - Performance Materiality)",
        "Percentual (%)": "75.0% da PM",
        "Valor (R$)": te
    }, {
        "Métrica": "Limiar de Distorções Triviais (CTT)",
        "Percentual (%)": "5.0% da PM",
        "Valor (R$)": ctt
    }])
    return df_mat

def matriz_sensibilidade_impairment():
    wacc_rates = [0.095, 0.100, 0.105, 0.110, 0.115] # 9.5% a 11.5%
    growth_rates = [0.020, 0.025, 0.030, 0.035]       # 2.0% a 3.5%
    
    base_viu = 12500000000.0 # R$ 12.5 Bi
    
    data = []
    for g in growth_rates:
        row = {"Growth (g) / WACC": f"{g*100:.1f}%"}
        for w in wacc_rates:
            # Modelo de variação de Valor em Uso
            fator = (0.105 - 0.025) / (w - g)
            val = round(base_viu * fator, 2)
            row[f"{w*100:.1f}%"] = val
        data.append(row)
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    df_mat = calcular_materialidade()
    df_mat.to_csv("resultados/tabelas/tabela_materialidade_pt320.csv", index=False)
    
    df_sens = matriz_sensibilidade_impairment()
    df_sens.to_csv("resultados/tabelas/tabela_sensibilidade_pt540.csv", index=False)
    print("Cálculos de materialidade e sensibilidade concluídos.")

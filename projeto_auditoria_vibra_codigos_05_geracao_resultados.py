"""
05_geracao_resultados.py
Consolidação de mapas de distorção (PT 450) e emissão do parecer final.
"""
import pandas as pd

def consolidar_pt450():
    df_testes = pd.read_csv("resultados/tabelas/resultados_testes_t01_t09.csv")
    df_mat = pd.read_csv("resultados/tabelas/tabela_materialidade_pt320.csv")
    
    total_distorcao = df_testes['total_distorcao_apurada'].sum()
    te_valor = df_mat.loc[df_mat['Métrica'].str.contains('Distorção Tolerável'), 'Valor (R$)'].values[0]
    
    conclusao = "ACIMA da Distorção Tolerável - Requer Ajuste Contábil ou Modificação de Parecer" if total_distorcao > te_valor else "Abaixo da Distorção Tolerável"
    
    pt450_summary = pd.DataFrame([{
        "Item": "Total de Distorções Conhecidas e Projetadas",
        "Valor (R$)": total_distorcao
    }, {
        "Item": "Distorção Tolerável (TE - PT 320)",
        "Valor (R$)": te_valor
    }, {
        "Item": "Avaliação de Impacto Contábil",
        "Valor (R$)": conclusao
    }])
    return pt450_summary

if __name__ == "__main__":
    df_pt450 = consolidar_pt450()
    df_pt450.to_csv("resultados/tabelas/resumo_pt450_consolidado.csv", index=False)
    print("Consolidação PT 450 concluída.")

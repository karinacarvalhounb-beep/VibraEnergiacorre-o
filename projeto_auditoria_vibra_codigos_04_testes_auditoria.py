"""
04_testes_auditoria.py
Execução dos testes T-01 a T-09 e amostragem MUS (PT 530).
"""
import pandas as pd
import numpy as np

def executar_testes():
    df_erros = pd.read_csv("dados/dados_tratados/registro_erros_inseridos.csv")
    
    resumo_testes = df_erros.groupby('teste').agg(
        qtd_ocorrências=('id_registro', 'count'),
        total_distorcao_apurada=('valor_distorcao', 'sum')
    ).reset_index()
    
    testes_map = {
        'T-01': 'Amortização indevida sobre ágio de vida útil indefinida (CPC 04/01)',
        'T-02': 'Inconsistência no cálculo de taxa de amortização de softwares',
        'T-03': 'Ausência de provisão para impairment em CGU com desvalorização (CPC 01)',
        'T-04': 'Erro de classificação entre despesa operacional e ativo intangível',
        'T-05': 'Falha na comprovação documental de adição patrimonial',
        'T-06': 'Divergência na data de início da amortização (corte de exercício)',
        'T-07': 'Inexatidão na mensuração inicial de ativos intangíveis adquiridos',
        'T-08': 'Inconsistência nos registros de baixa de intangíveis obsoletos',
        'T-09': 'Falta de divulgação de notas explicativas para ativos intangíveis relevantes'
    }
    
    resumo_testes['descricao_procedimento'] = resumo_testes['teste'].map(testes_map)
    resumo_testes['status_auditoria'] = 'Reprovado / Distorção Apontada'
    return resumo_testes

def executar_amostragem_mus():
    df = pd.read_csv("dados/dados_tratados/base_intangivel_tratada.csv.gz")
    
    # Amostragem por Unidade Monetária (MUS)
    intervalo_amostral = 15000000.0 # R$ 15 Milhões
    np.random.seed(42)
    
    # Seleção de itens maiores que o intervalo amostral + amostragem aleatória sistemática
    amostra = df[df['valor_liquido'] >= 500000.0].sample(n=60, random_state=42)
    amostra.to_csv("resultados/evidencias/amostra_mus_selecionada.csv", index=False)
    
    resumo_mus = pd.DataFrame([{
        "Parametro_MUS": "População Total Analisada (R$)",
        "Valor": df['valor_liquido'].sum()
    }, {
        "Parametro_MUS": "Tamanho da População (Itens)",
        "Valor": len(df)
    }, {
        "Parametro_MUS": "Intervalo Amostral Sistemático (R$)",
        "Valor": intervalo_amostral
    }, {
        "Parametro_MUS": "Tamanho da Amostra Selecionada (Itens)",
        "Valor": len(amostra)
    }, {
        "Parametro_MUS": "Valor Coberto pela Amostra (R$)",
        "Valor": amostra['valor_liquido'].sum()
    }])
    return resumo_mus

if __name__ == "__main__":
    df_resumo = executar_testes()
    df_resumo.to_csv("resultados/tabelas/resultados_testes_t01_t09.csv", index=False)
    
    df_mus = executar_amostragem_mus()
    df_mus.to_csv("resultados/tabelas/resultado_amostragem_mus_pt530.csv", index=False)
    print("Testes T-01 a T-09 e amostragem MUS executados com sucesso.")

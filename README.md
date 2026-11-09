# Projeto de Auditoria Independente — Vibra Energia S.A. (2025)

**Curso:** Ciências Contábeis — Universidade de Brasília (UnB)  
**Disciplina:** Auditoria 1 (CCA0024, Turma 02)  
**Professor:** Dr. Lucas Oliveira Gomes Ferreira  
**Auditor Responsável (Aluno):** Karina Xavier Alves de Carvalho  
**Matrícula:** 200058789  
**Semente de Reprodutibilidade:** 200058789  

---

## 1. Objetivo do Projeto
Este repositório acadêmico contém a execução completa do **Dossiê de Auditoria Independente** referente ao exercício social encerrado em 31 de dezembro de 2025 da **Vibra Energia S.A.** (CNPJ: 34.274.233/0001-02). O trabalho contempla a aplicação integral das **NBCs TA (Estrutura Conceitual e séries 200 a 600)**, relacionando dados reais públicos extraídos da CVM/B3 com rotinas automatizadas de auditoria aplicadas sobre uma base de dados sintética analítica do Ativo Intangível (520.126 linhas).

---

## 2. Tecnologias e Bibliotecas Utilizadas
- **Python 3.10+**
- **Pandas:** Leitura, manipulação e agregação de dados.
- **NumPy:** Vetorização estatística, geração pseudoaleatória e amostragem MUS.
- **OpenPyXL:** Formatação e exportação da planilha editável de trabalho.
- **Gzip:** Compactação nativa de dados de alta volumetria.

---
## 3. Instruções para Instalação e Execução

### Passo 1: Clonar o Repositório
```bash
git clone [https://github.com/SEU-USUARIO/projeto-auditoria-vibra-2025.git](https://github.com/SEU-USUARIO/projeto-auditoria-vibra-2025.git)
cd projeto-auditoria-vibra-2025
Passo 2: Instalar as Dependências
Bash
pip install -r requirements.txt
Passo 3: Executar a Sequência de Scripts Python
Para executar o pipeline completo de auditoria e recalcular todas as tabelas e evidências:

Bash
python codigos/01_importacao_dados.py
python codigos/02_tratamento_dados.py
python codigos/03_analise_auditoria.py
python codigos/04_testes_auditoria.py

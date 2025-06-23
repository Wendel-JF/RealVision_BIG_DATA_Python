# Retail Vision
### Documentação do Projeto

#### Alunos: 

Wendel José Frazão - 202303890321

Victor Pierre Nascimento Medeiros - 202402399781

Arthur Batista Braga - 202403124386

John Flavio da Silva - 202404268128

### 1. Introdução
O projeto Retail Vision tem como objetivo principal a análise do comportamento de clientes no varejo a partir de dados simulados. Utilizando Python, Streamlit., o projeto realiza consultas, visualizações e exibição de dashboards interativos para ajudar na tomada de decisões.

<p align='center'>
  <img width='500' src='dashboard.gif'>
</p>

### 2. Objetivo

Analisar os dados de clientes gerados artificialmente, criando visualizações, métricas e dashboards para identificar padrões de comportamento e preferências no setor varejista.

### 3. Estrutura do Projeto

- `app.py`: Aplicação principal usando Streamlit.
- `criar_banco_de_dados.py`: Criação do banco de dados e inserção dos dados simulados.
- `criar_graficos.py`: arquivo com as funções para criação de gráficos.
- `querys.py`: Arquivo com as queries SQL utilizadas.
- `css.py`: Estilização personalizada para o app Streamlit.

### 4. Tecnologias Utilizadas
- Python 3
- Streamlit
- SQLite
- Pandas, 
- Plotly

### 5. Como Rodar o Projeto 

- Instalar as dependências com `pip install streamlit pandas plotly faker streamlit-autorefresh`
- Executar o script `python criar_banco_de_dados.py` para criar e gerar os dados no banco de dados
- Iniciar a aplicação Streamlit com `python -m streamlit run app.py`

### 6. Conclusão
O projeto demonstra a importância do uso de ferramentas de análise de dados no varejo, destacando como dashboards e visualizações interativas podem oferecer insights valiosos sobre o comportamento do consumidor.


<<<<<<< HEAD
=======
O arquivo app.py contém o código da aplicação web interativa
>>>>>>> 3b50d7f8bfaa4334b266535a3d1b6625622120d3

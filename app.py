import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from criar_graficos import (grafico_coluna, grafico_coluna_lateral,
                            grafico_linha, grafico_pizza)
# Importar estilos css personalizar de outro arquivo
from css import Styles
from querys import (atualizar_dados, get_clientes,
                    get_clientes_por_faixa_etaria,
                    get_dispositivos_mais_usados, get_faturamento_anual,
                    get_faturamento_mensal, get_faturamento_por_categoria,
                    get_frequencia_compras_regiao, get_genero,
                    get_produtos_mais_visualizados,
                    get_quantidade_de_vendas_por_produtos,
                    get_taxa_abandono_carrinho, get_taxa_conversao,
                    get_tempo_medio_na_loja, get_ultimo_evento)

# Configuração inicial da página
st.set_page_config(
    page_title="Dashboard Clientes - Retail Vision", layout="wide", initial_sidebar_state="expanded")
st.title("📊 Dashboard de Clientes - Retail Vision")

# Atualização automática (a cada 5 segundos)
st_autorefresh(interval=5000, key="refresh")  # milissegundos

# Atualização da dashboard com novos dados
atualizar_dados()

# Carregar os dados
df_clientes = get_clientes()
df_faturamento_anual = get_faturamento_anual()

# Importar estilos css personalizar de outro arquivo
Styles()

# Contagem total de clientes
total_clientes = df_clientes.shape[0]

# Criar Colunas de MEtricas
# Layout com duas colunas
col1, col2, col3, col4, col5 = st.columns(5)


# Obter o tempo médio em segundos
tempo_df = get_tempo_medio_na_loja()
tempo_medio_segundos = tempo_df["tempo_medio_segundos"].iloc[0] if not tempo_df.empty else 0

# Converter para minutos e segundos
minutos = int(tempo_medio_segundos // 60)
segundos = int(tempo_medio_segundos % 60)
tempo_formatado = f"{minutos}m {segundos}s"


# Total de Visitantes
with col1:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Total de Visitantes</div>
        <div class="metric-value">{total_clientes}</div>
    </div>
    """, unsafe_allow_html=True)

# Faturamento Anual
with col2:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Faturamento Anual</div>
        <div class="metric-value">{df_faturamento_anual}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Taxa de Abandono de Carrinho</div>
        <div class="metric-value">{get_taxa_abandono_carrinho()}%</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">🎯 Taxa de Conversão</div>
        <div class="metric-value">{get_taxa_conversao()}%</div>
    </div>
    """, unsafe_allow_html=True)
with col5:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">⏱️ Tempo Médio na Loja</div>
        <div class="metric-value">{tempo_formatado}</div>
    </div>
    """, unsafe_allow_html=True)


# ----- Criar gráfico de colunas de produtos mais vistos ------

fig_visualizacoes = grafico_coluna(
    get_produtos_mais_visualizados(),
    X="produto",
    Y="visualizacoes",
    title="Produtos Mais Visualizados",
    label={"produto": "Produto", "visualizacoes": "Visualizações"},
    color="produto",
    x_title="Produto",
    y_title="Visualizações"
)

# ----- Criar gráfico de colunas da quantidade vendas por produto ------

fig_coluna_vendas = grafico_coluna(get_quantidade_de_vendas_por_produtos(), "produto", "vendas",
                                   "Vendas de Produto", {"produto": "Produto", "vendas": "Número de Vendas"}, "vendas", "Produto", "Número de Vendas")

# ----- Criar gráfico de colunas de faturamento por categoria ------

fig_coluna_faturamento_por_categoria = grafico_coluna_lateral(get_faturamento_por_categoria(), "categoria", "faturamento", "Faturamento por Categoria",
                                                              {"categoria": "Categoria", "faturamento": "Faturamento"}, "categoria", "Faturamento", "Número de Vendas")

# ----- Criar gráfico de colunas fatumento do mes ------
fig_faturamento_mensal = grafico_linha(
    get_faturamento_mensal(),
    X="mes",
    Y="faturamento",
    title="Faturamento Mensal",
    label={"mes": "Mês", "faturamento": "Faturamento (R$)"},
    x_title="Mês",
    y_title="Faturamento (R$)",
    altura=400
)

# ---- Criar gráfico de pizza com informacoes de genero dos clientes ----
cores = {'Masculino': 'blue', 'Feminino': 'red'}
fig_genero = grafico_pizza(get_genero(), "genero",
                           "total", "genero", cores, "Gênero")


# ---- Criar gráfico de pizza com Tipo de Dispositivo mais Usado ----
cores = {'Desktop': 'black', 'Tablet': 'yellow', 'mobile': 'green'}
fig_dispositivo = grafico_pizza(get_dispositivos_mais_usados(), "dispositivo",
                                "total", "dispositivo", cores, "Dispositivos")

# ---- Criar gráfico de Faixa Etaria dos Clientes ----

fig_faixa_etaria = grafico_coluna(
    get_clientes_por_faixa_etaria(),
    X="faixa_etaria",
    Y="total",
    title="Distribuição de Clientes por Faixa Etária",
    label={"faixa_etaria": "Faixa Etária", "total": "Total de Clientes"},
    color="faixa_etaria",
    x_title="Faixa Etária",
    y_title="Total de Clientes"
)

# ---- Criar gráfico de Frequência de Compras por Região ----

fig_frequencia_compras_regiao = grafico_coluna(
    get_frequencia_compras_regiao(),
    X="regiao",
    Y="total",
    title="Regiaoes mais Vendias",
    label={"regiao": "Região", "total": "Total"},
    color="regiao",
    x_title="Região",
    y_title="Total"
)


# Criar 3 colunas lado a lado
col1, col2, col3, col4 = st.columns(4)

# --- Exibir Grafico de Coluna de Visualizacao de Produtos
col1.plotly_chart(fig_visualizacoes, use_container_width=True,
                  config={"displayModeBar": False})

# --- Exibir Grafico de Coluna de Venda dos Produtos
col2.plotly_chart(fig_coluna_vendas, use_container_width=True)

# Exibir Grafico de Coluna Lateral de Faturamento Por Categoria na pagina
col3.plotly_chart(fig_coluna_faturamento_por_categoria,
                  use_container_width=True)


col4.plotly_chart(fig_faturamento_mensal, use_container_width=True)

# --- Exibir outra linha com mais colunas
col5, col6, col7, col8 = st.columns(4)

# Exibir Grafico de Pizza dos tipos de Dispositivos mais usados
col5.plotly_chart(fig_dispositivo, use_container_width=True)

# Exibir Grafico de Coluna de faixa Etaria de Idade por Cliente
col6.plotly_chart(fig_faixa_etaria, use_container_width=True)

# Exibir Grafico de Coluna das Frequencia de Compra por Região
col7.plotly_chart(fig_frequencia_compras_regiao, use_container_width=True)

# Exibir Grafico de Pizza de genero na pagina
col8.plotly_chart(fig_genero, use_container_width=True)

# st.subheader("🕓 Último Evento por Cliente")

# df_eventos = get_ultimo_evento()
# df_eventos["timestamp"] = pd.to_datetime(
# df_eventos["timestamp"]).dt.strftime("%d/%m/%Y %H:%M")

# st.dataframe(df_eventos, use_container_width=True)

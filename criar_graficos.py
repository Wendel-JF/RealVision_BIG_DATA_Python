
import plotly.express as px
import streamlit as st

height = 400

# ----- Criar gráfico de colunas Vertial ------


def grafico_coluna(dados, X, Y, title, label, color, x_title, y_title):
    fig = px.histogram(
        dados,
        x=X,
        y=Y,
        color=color,
        labels=label,
    )

    # Adicionar os valores dentro das barras
    fig.update_traces(
        texttemplate='%{y}',     # mostra o valor de y (número de vendas)
        textposition='inside',   # posiciona o texto dentro das colunas
        insidetextanchor='middle',
        textfont=dict(color="white", size=14)  # cor e tamanho do texto
    )

    fig.update_layout(
        showlegend=False,
        height=height,  # ← define a altura aqui (em pixels)
        xaxis_title=x_title,
        yaxis_title=y_title,
        paper_bgcolor="#2d3748",  # fundo fora da área do gráfico
        plot_bgcolor="#2d3748",   # fundo da área do gráfico
        bargap=0.2,
        uniformtext_minsize=8,
        uniformtext_mode='hide',

        title_text=title,      # ou title=title
        title_x=0.5,           # centraliza horizontalmente
        title_y=0.95,           # ajusta posição vertical (opcional)
        title_xanchor='center',
        title_yanchor='top',

        font=dict(
            family="Poppins, sans-serif",
            size=18,
            color="RebeccaPurple",
            variant="small-caps",
        )
    )
    return fig

# ----- Criar gráfico de colunas Horizontal ------


def grafico_coluna_lateral(dados, X, Y, title, label, color, x_title, y_title):
    fig = px.histogram(
        dados,
        y=X,  # <-- INVERTE aqui
        x=Y,  # <-- INVERTE aqui
        color=color,
        title=title,
        labels=label,
        orientation='h'  # <-- Indica orientação horizontal
    )

    # Adicionar os valores dentro das barras
    fig.update_traces(
        texttemplate='%{x}',  # <-- Mostra valor de x agora
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color="white", size=14)
    )

    fig.update_layout(
        showlegend=False,
        height=height,  # ← define a altura aqui (em pixels)
        xaxis_title=y_title,  # Eixo X agora mostra valor
        yaxis_title=x_title,  # Eixo Y agora mostra categorias
        paper_bgcolor="#2d3748",
        plot_bgcolor="#2d3748",
        bargap=0.2,
        uniformtext_minsize=8,
        uniformtext_mode='hide',

        title_text=title,      # ou title=title
        title_x=0.5,           # centraliza horizontalmente
        title_y=0.95,           # ajusta posição vertical (opcional)
        title_xanchor='center',
        title_yanchor='top',

        font=dict(
            family="Poppins, sans-serif",
            size=18,
            color="RebeccaPurple",
            variant="small-caps",
        )
    )
    return fig

# ----- Criar gráfico de Pizza ------


def grafico_pizza(dados, name, value, color, cores, title):
    fig = px.pie(
        dados,
        names=name,
        values=value,
        color=color,
        color_discrete_map=cores,
    )

    # Adicionar os rótulos dentro das fatias
    fig.update_traces(textinfo='label+percent', textposition='inside')

    fig.update_layout(
        height=height,  # ← define a altura aqui (em pixels)
        showlegend=False,
        paper_bgcolor="#2d3748",  # fundo fora da área do gráfico
        plot_bgcolor="#2d3748",   # fundo da área do gráfico
        bargap=0.2,
        font_color="white",

        title_text=title,      # ou title=title
        title_x=0.5,           # centraliza horizontalmente
        title_y=0.95,           # ajusta posição vertical (opcional)
        title_xanchor='center',
        title_yanchor='top',

        font=dict(
            family="Poppins, sans-serif",
            size=18,
            color="RebeccaPurple",
            variant="small-caps",
        )
    )
    return fig


def grafico_linha(dados, X, Y, title, label, x_title, y_title, altura):
    fig = px.line(
        dados,
        x=X,
        y=Y,
        labels=label,
        markers=True  # mostra os pontos nas linhas
    )

    # Adicionar estilo visual
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8, color='white', line=dict(
            width=2, color='RebeccaPurple')),
    )

    fig.update_layout(
        height=altura,  # ← define a altura aqui (em pixels)
        xaxis_title=x_title,
        yaxis_title=y_title,
        paper_bgcolor="#2d3748",
        plot_bgcolor="#2d3748",
        title_text=title,
        title_x=0.5,
        title_y=0.9,
        title_xanchor='center',
        title_yanchor='top',
        font=dict(
            family="Poppins, sans-serif",
            size=18,
            color="RebeccaPurple",
            variant="small-caps",
        ),
    )

    return fig

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px

def plot_cash_flows(fem, lang='ru'):
    """
    Визуализация денежных потоков.
    
    :param fem: DataFrame с финансово-экономической моделью
    :param lang: язык интерфейса ('ru' или 'en')
    """
    titles = {
        'ru': "Динамика денежных потоков",
        'en': "Cash Flow Dynamics"
    }
    labels = {
        'ru': {
            'year': 'Год',
            'cash_flow': 'Денежный поток',
            'cfo': 'CFO (Операционный денежный поток)',
            'cfi': 'CFI (Инвестиционный денежный поток)',
            'cf': 'CF (Совокупный денежный поток)'
        },
        'en': {
            'year': 'Year',
            'cash_flow': 'Cash Flow',
            'cfo': 'CFO (Operating Cash Flow)',
            'cfi': 'CFI (Investment Cash Flow)',
            'cf': 'CF (Total Cash Flow)'
        }
    }
    
    fig = px.line(fem, x=fem.index, y=['CFO', 'CFI', 'CF'], 
                  labels={'index': labels[lang]['year'], 'value': labels[lang]['cash_flow'], 'variable': 'Type'},
                  title=titles[lang])
    fig.update_layout(legend_title_text=None)
    st.plotly_chart(fig)

def plot_npv(fem, lang='ru'):
    """
    Визуализация расчета NPV по годам.
    
    :param fem: DataFrame с финансово-экономической моделью
    :param lang: язык интерфейса ('ru' или 'en')
    """
    titles = {
        'ru': "Расчет NPV по годам",
        'en': "NPV Calculation by Year"
    }
    labels = {
        'ru': {'year': 'Год', 'npv': 'NPV'},
        'en': {'year': 'Year', 'npv': 'NPV'}
    }
    
    fig = px.line(fem, x=fem.index, y='NPV', 
                  labels={'index': labels[lang]['year'], 'NPV': labels[lang]['npv']},
                  title=titles[lang])
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)

def plot_sensitivity_analysis(sensitivity_data, lang='ru'):
    """
    Визуализация анализа чувствительности.
    
    :param sensitivity_data: DataFrame с результатами анализа чувствительности
    :param lang: язык интерфейса ('ru' или 'en')
    """
    titles = {
        'ru': "Анализ чувствительности",
        'en': "Sensitivity Analysis"
    }
    labels = {
        'ru': {
            'parameter': 'Параметр',
            'change': 'Изменение параметра'
        },
        'en': {
            'parameter': 'Parameter',
            'change': 'Parameter Change'
        }
    }
    
    fig = px.imshow(sensitivity_data, 
                    labels=dict(x=labels[lang]['change'], y=labels[lang]['parameter'], color="NPV Change"),
                    title=titles[lang])
    st.plotly_chart(fig)

# TODO: Реализовать выбор типа графика пользователем
# TODO: Добавить возможность экспорта графиков

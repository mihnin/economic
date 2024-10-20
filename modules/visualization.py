import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(fem.index, fem['CFO'], label=labels[lang]['cfo'], marker='o')
    ax.plot(fem.index, fem['CFI'], label=labels[lang]['cfi'], marker='s')
    ax.plot(fem.index, fem['CF'], label=labels[lang]['cf'], marker='^')
    
    ax.set_xlabel(labels[lang]['year'])
    ax.set_ylabel(labels[lang]['cash_flow'])
    ax.legend()
    ax.grid(True)
    
    plt.title(titles[lang])
    st.pyplot(fig)

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
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(fem.index, fem['NPV'], marker='o')
    ax.fill_between(fem.index, 0, fem['NPV'], alpha=0.2)
    
    ax.set_xlabel(labels[lang]['year'])
    ax.set_ylabel(labels[lang]['npv'])
    ax.grid(True)
    
    # Добавление горизонтальной линии на уровне NPV = 0
    ax.axhline(y=0, color='r', linestyle='--')
    
    plt.title(titles[lang])
    st.pyplot(fig)

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
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(sensitivity_data, annot=True, cmap='coolwarm', ax=ax)
    
    ax.set_xlabel(labels[lang]['change'])
    ax.set_ylabel(labels[lang]['parameter'])
    
    plt.title(titles[lang])
    st.pyplot(fig)

# TODO: Добавить интерактивные графики с использованием Plotly
# TODO: Реализовать выбор типа графика пользователем
# TODO: Добавить возможность экспорта графиков

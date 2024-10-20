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
    
    st.subheader(titles[lang])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(fem.index, fem['CFO'], label=labels[lang]['cfo'])
    ax.plot(fem.index, fem['CFI'], label=labels[lang]['cfi'])
    ax.plot(fem.index, fem['CF'], label=labels[lang]['cf'])
    
    ax.set_xlabel(labels[lang]['year'])
    ax.set_ylabel(labels[lang]['cash_flow'])
    ax.legend()
    ax.grid(True)
    
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
    
    st.subheader(titles[lang])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(fem.index, fem['NPV'], marker='o')
    
    ax.set_xlabel(labels[lang]['year'])
    ax.set_ylabel(labels[lang]['npv'])
    ax.grid(True)
    
    # Добавление горизонтальной линии на уровне NPV = 0
    ax.axhline(y=0, color='r', linestyle='--')
    
    st.pyplot(fig)

def plot_project_comparison(base_fem, project_fem, lang='ru'):
    """
    Визуализация сравнения базового и проектного вариантов.
    
    :param base_fem: DataFrame с финансово-экономической моделью базового варианта
    :param project_fem: DataFrame с финансово-экономической моделью проектного варианта
    :param lang: язык интерфейса ('ru' или 'en')
    """
    titles = {
        'ru': "Сравнение базового и проектного вариантов",
        'en': "Comparison of Base and Project Variants"
    }
    labels = {
        'ru': {
            'year': 'Год',
            'cash_flow': 'Совокупный денежный поток',
            'base': 'Базовый вариант',
            'project': 'Проектный вариант'
        },
        'en': {
            'year': 'Year',
            'cash_flow': 'Total Cash Flow',
            'base': 'Base Variant',
            'project': 'Project Variant'
        }
    }
    
    st.subheader(titles[lang])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(base_fem.index, base_fem['CF'], label=labels[lang]['base'])
    ax.plot(project_fem.index, project_fem['CF'], label=labels[lang]['project'])
    
    ax.set_xlabel(labels[lang]['year'])
    ax.set_ylabel(labels[lang]['cash_flow'])
    ax.legend()
    ax.grid(True)
    
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
    
    st.subheader(titles[lang])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(sensitivity_data, annot=True, cmap='coolwarm', ax=ax)
    
    ax.set_xlabel(labels[lang]['change'])
    ax.set_ylabel(labels[lang]['parameter'])
    
    st.pyplot(fig)

def plot_prediction_results(actual, predicted, lang='ru'):
    """
    Визуализация результатов прогнозирования.
    
    :param actual: фактические значения
    :param predicted: прогнозируемые значения
    :param lang: язык интерфейса ('ru' или 'en')
    """
    titles = {
        'ru': "Результаты прогнозирования",
        'en': "Prediction Results"
    }
    labels = {
        'ru': {
            'actual': 'Фактические значения',
            'predicted': 'Прогнозируемые значения'
        },
        'en': {
            'actual': 'Actual Values',
            'predicted': 'Predicted Values'
        }
    }
    
    st.subheader(titles[lang])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(actual, predicted)
    ax.plot([actual.min(), actual.max()], [actual.min(), actual.max()], 'r--', lw=2)
    
    ax.set_xlabel(labels[lang]['actual'])
    ax.set_ylabel(labels[lang]['predicted'])
    ax.grid(True)
    
    st.pyplot(fig)

# TODO: Добавить интерактивные графики с использованием Plotly
# TODO: Реализовать выбор типа графика пользователем
# TODO: Добавить возможность экспорта графиков

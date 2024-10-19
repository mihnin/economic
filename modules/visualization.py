import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_cash_flows(fem):
    """
    Визуализация денежных потоков.
    
    :param fem: DataFrame с финансово-экономической моделью
    """
    st.subheader("Динамика денежных потоков")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(fem.index, fem['CFO'], label='CFO (Операционный денежный поток)')
    ax.plot(fem.index, fem['CFI'], label='CFI (Инвестиционный денежный поток)')
    ax.plot(fem.index, fem['CF'], label='CF (Совокупный денежный поток)')
    
    ax.set_xlabel('Год')
    ax.set_ylabel('Денежный поток')
    ax.legend()
    ax.grid(True)
    
    st.pyplot(fig)

def plot_npv(fem):
    """
    Визуализация расчета NPV по годам.
    
    :param fem: DataFrame с финансово-экономической моделью
    """
    st.subheader("Расчет NPV по годам")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(fem.index, fem['NPV'], marker='o')
    
    ax.set_xlabel('Год')
    ax.set_ylabel('NPV')
    ax.grid(True)
    
    # Добавление горизонтальной линии на уровне NPV = 0
    ax.axhline(y=0, color='r', linestyle='--')
    
    st.pyplot(fig)

def plot_project_comparison(base_fem, project_fem):
    """
    Визуализация сравнения базового и проектного вариантов.
    
    :param base_fem: DataFrame с финансово-экономической моделью базового варианта
    :param project_fem: DataFrame с финансово-экономической моделью проектного варианта
    """
    st.subheader("Сравнение базового и проектного вариантов")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(base_fem.index, base_fem['CF'], label='Базовый вариант')
    ax.plot(project_fem.index, project_fem['CF'], label='Проектный вариант')
    
    ax.set_xlabel('Год')
    ax.set_ylabel('Совокупный денежный поток')
    ax.legend()
    ax.grid(True)
    
    st.pyplot(fig)

def plot_sensitivity_analysis(sensitivity_data):
    """
    Визуализация анализа чувствительности.
    
    :param sensitivity_data: DataFrame с результатами анализа чувствительности
    """
    st.subheader("Анализ чувствительности")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(sensitivity_data, annot=True, cmap='coolwarm', ax=ax)
    
    ax.set_xlabel('Изменение параметра')
    ax.set_ylabel('Параметр')
    
    st.pyplot(fig)

def plot_prediction_results(actual, predicted):
    """
    Визуализация результатов прогнозирования.
    
    :param actual: фактические значения
    :param predicted: прогнозируемые значения
    """
    st.subheader("Результаты прогнозирования")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(actual, predicted)
    ax.plot([actual.min(), actual.max()], [actual.min(), actual.max()], 'r--', lw=2)
    
    ax.set_xlabel('Фактические значения')
    ax.set_ylabel('Прогнозируемые значения')
    ax.grid(True)
    
    st.pyplot(fig)

# TODO: Добавить интерактивные графики с использованием Plotly
# TODO: Реализовать выбор типа графика пользователем
# TODO: Добавить возможность экспорта графиков

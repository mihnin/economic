import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from modules.calculate import calculate_npv

def render():
    st.header("Анализ чувствительности")

    if 'calculation_results' not in st.session_state:
        st.warning("Пожалуйста, сначала выполните расчеты на странице 'Расчеты'")
        return

    results = st.session_state['calculation_results']
    df = results['df'].copy()
    original_npv = results['npv']
    impact_duration = int(st.session_state['project_data']['impact_duration'])

    st.subheader("Изменение параметров")

    # Создаем слайдеры для каждого параметра
    params = {
        'Выручка': st.slider("Изменение выручки (%)", -50, 50, 0),
        'Фиксированные операционные затраты': st.slider("Изменение фиксированных операционных затрат (%)", -50, 50, 0),
        'Капитальные затраты': st.slider("Изменение капитальных затрат (%)", -50, 50, 0),
        'Переменные операционные затраты': st.slider("Изменение переменных операционных затрат (%)", -50, 50, 0),
        'Ставка дисконтирования': st.slider("Изменение ставки дисконтирования (процентные пункты)", -5.0, 5.0, 0.0, step=0.1)
    }

    # Применяем изменения к DataFrame
    for param, change in params.items():
        if param != 'Ставка дисконтирования':
            df[param] *= (1 + change / 100)
        else:
            new_rate = st.session_state['project_data']['discount_rate'] + change / 100
            st.write(f"Новая ставка дисконтирования: {new_rate:.2%}")

    # Пересчитываем NPV
    df['CFO'] = df['Выручка'] - df['Фиксированные операционные затраты'] - df['Переменные операционные затраты']
    df['CFI'] = -df['Капитальные затраты']
    df['CF'] = df['CFO'] + df['CFI']
    new_npv = calculate_npv(df['CF'], new_rate, impact_duration)

    # Отображаем результаты
    st.subheader("Результаты анализа")
    st.write(f"Исходное значение NPV: {original_npv:.2f}")
    st.write(f"Новое значение NPV: {new_npv:.2f}")
    change_percent = (new_npv - original_npv) / original_npv * 100
    st.write(f"Изменение NPV: {change_percent:.2f}%")

    # График изменения NPV
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 1], y=[original_npv, new_npv], mode='lines+markers'))
    fig.update_layout(title='Изменение NPV', xaxis_title='', yaxis_title='NPV',
                      xaxis=dict(tickmode='array', tickvals=[0, 1], ticktext=['Исходное', 'Новое']))
    st.plotly_chart(fig)

    # Диаграмма торнадо
    tornado_data = []
    for param, change in params.items():
        if param != 'Ставка дисконтирования':
            low_npv = calculate_npv(df['CF'] * (1 - abs(change) / 100), new_rate, impact_duration)
            high_npv = calculate_npv(df['CF'] * (1 + abs(change) / 100), new_rate, impact_duration)
        else:
            low_npv = calculate_npv(df['CF'], new_rate - abs(change) / 100, impact_duration)
            high_npv = calculate_npv(df['CF'], new_rate + abs(change) / 100, impact_duration)
        tornado_data.append((param, low_npv - original_npv, high_npv - original_npv))

    tornado_data.sort(key=lambda x: abs(x[2] - x[1]), reverse=True)

    fig_tornado = go.Figure()
    for param, low, high in tornado_data:
        fig_tornado.add_trace(go.Bar(y=[param], x=[high], orientation='h', name=f'{param} (Верх)'))
        fig_tornado.add_trace(go.Bar(y=[param], x=[low], orientation='h', name=f'{param} (Низ)'))

    fig_tornado.update_layout(title='Диаграмма торнадо: Влияние параметров на NPV',
                              barmode='relative',
                              yaxis={'categoryorder': 'total ascending'},
                              xaxis_title='Изменение NPV')
    st.plotly_chart(fig_tornado)

if __name__ == "__main__":
    render()

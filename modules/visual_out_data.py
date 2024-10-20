import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def render():
    st.header("Визуализация результатов")

    if 'calculation_results' not in st.session_state:
        st.warning("Пожалуйста, сначала выполните расчеты на странице 'Расчеты'")
        return

    results = st.session_state['calculation_results']
    df = results['df']

    st.subheader("График изменения CF и дисконтированного CF по годам")
    fig_cf = go.Figure()
    fig_cf.add_trace(go.Scatter(x=df['Год'], y=df['CF'], mode='lines+markers', name='CF'))
    fig_cf.add_trace(go.Scatter(x=df['Год'], y=df['Дисконтированный CF'], mode='lines+markers', name='Дисконтированный CF'))
    fig_cf.update_layout(title='Денежные потоки по годам', xaxis_title='Год', yaxis_title='Значение')
    st.plotly_chart(fig_cf)

    st.subheader("Структура затрат")
    costs_data = {
        'Категория': ['Фиксированные операционные', 'Переменные операционные', 'Капитальные'],
        'Сумма': [
            df['Фиксированные операционные затраты'].sum(),
            df['Переменные операционные затраты'].sum(),
            df['Капитальные затраты'].sum()
        ]
    }
    fig_costs = px.pie(costs_data, values='Сумма', names='Категория', title='Структура затрат')
    st.plotly_chart(fig_costs)

    st.subheader("График накопленного NPV")
    df['Накопленный NPV'] = df['Дисконтированный CF'].cumsum()
    fig_npv = px.line(df, x='Год', y='Накопленный NPV', title='Накопленный NPV по годам')
    st.plotly_chart(fig_npv)

    st.subheader("Тепловая карта переменных операционных затрат")
    var_costs = pd.DataFrame(st.session_state['project_data']['var_costs'])
    var_costs['Общие затраты'] = var_costs['Количество'] * var_costs['Ставка'] * var_costs['Коэффициент'].map(st.session_state['project_data']['coefficients'])
    fig_heatmap = px.imshow(var_costs['Общие затраты'].values.reshape(1, -1),
                            labels=dict(x="Категория специалистов", y="", color="Затраты"),
                            x=var_costs.index,
                            title="Тепловая карта переменных операционных затрат")
    st.plotly_chart(fig_heatmap)

if __name__ == "__main__":
    render()

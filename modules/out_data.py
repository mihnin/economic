import streamlit as st
import pandas as pd
import numpy as np
from scipy import optimize

def render():
    st.header("Результаты расчетов")

    if 'calculation_results' not in st.session_state:
        st.warning("Пожалуйста, сначала выполните расчеты на странице 'Расчеты'")
        return

    results = st.session_state['calculation_results']
    df = results['df']
    npv = results['npv']

    st.subheader("Таблица результатов по годам")
    st.dataframe(df)

    st.subheader("Итоговые показатели")
    st.write(f"**NPV:** {npv:.2f}")
    st.write("**Определение NPV:**")
    st.write("NPV (Net Present Value) или Чистая приведенная стоимость - это разница между текущей стоимостью будущих денежных поступлений и текущей стоимостью инвестиций.")
    st.write("**Цель расчета NPV:**")
    st.write("NPV рассчитывается для оценки экономической эффективности инвестиционного проекта. Этот показатель позволяет определить, превысит ли прибыль от проекта затраты на его реализацию с учетом временной стоимости денег.")
    st.write("**Интерпретация значений NPV:**")
    st.write("NPV > 0: Проект прибылен и может быть принят к реализации.")
    st.write("NPV = 0: Проект не принесет ни прибыли, ни убытка.")
    st.write("NPV < 0: Проект убыточен и должен быть отклонен.")

    # Дополнительные ключевые показатели
    total_revenue = df['Выручка'].sum()
    total_costs = df['Фиксированные операционные затраты'].sum() + df['Переменные операционные затраты'].sum()
    total_capex = df['Капитальные затраты'].sum()
    total_cf = df['CF'].sum()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Общая выручка", f"{total_revenue:.2f}")
    with col2:
        st.metric("Общие затраты", f"{total_costs:.2f}")
    with col3:
        st.metric("Общие капитальные затраты", f"{total_capex:.2f}")
    with col4:
        st.metric("Общий денежный поток", f"{total_cf:.2f}")

    # Расчет дополнительных показателей
    payback_period = calculate_payback_period(df)
    irr = calculate_irr(df['CF'])
    profitability_index = calculate_profitability_index(npv, total_capex)

    st.subheader("Дополнительные показатели эффективности")
    col1, col2, col3 = st.columns(3)
    with col1:
        if payback_period == float('inf'):
            st.metric("Срок окупаемости (лет)", "-")
        else:
            st.metric("Срок окупаемости (лет)", f"{payback_period:.2f}")
    with col2:
        if irr is not None:
            st.metric("IRR", f"{irr:.2%}")
        elif np.all(df['CF'] < 0):
            st.error("Для проектов или ЗНИ с исключительно отрицательными денежными потоками IRR не существует в реальном числовом пространстве.")
        else:
            st.error("Не удалось рассчитать IRR")
            if payback_period > 0:
                st.write("**Определение IRR:**")
                st.write("IRR (Internal Rate of Return) - это ставка дисконтирования, при которой NPV (чистая приведенная стоимость) проекта равна нулю.")
                st.write("**Экономическая интерпретация:**")
                st.write("Такая структура денежных потоков нетипична для обычных инвестиционных проектов. Она показывает, что проект генерирует доход практически с самого начала, без значительных начальных инвестиций.")
    with col3:
        st.metric("Индекс прибыльности", f"{profitability_index:.2f}")

def calculate_payback_period(df):
    cumulative_cf = df['CF'].cumsum()
    if (cumulative_cf > 0).any():
        return cumulative_cf[cumulative_cf > 0].index[0]
    else:
        return float('inf')

def calculate_irr(cash_flows):
    if len(cash_flows) < 2 or np.all(cash_flows == 0):
        return None

    def npv_func(rate, cash_flows):
        return np.sum(cash_flows / (1 + rate) ** np.arange(len(cash_flows)))
    try:
        return optimize.brentq(lambda r: npv_func(r, cash_flows), -1.0, 1.0)
    except ValueError:
        return None

def calculate_profitability_index(npv, total_capex):
    return (npv + total_capex) / total_capex

if __name__ == "__main__":
    render()

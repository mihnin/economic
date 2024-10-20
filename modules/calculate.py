import streamlit as st
import pandas as pd
import numpy as np

def calculate_cf(revenue, fixed_costs, var_costs):
    """Расчет денежного потока"""
    return revenue - fixed_costs - var_costs

def calculate_npv(cash_flows, discount_rate):
    """Расчет NPV"""
    return np.sum(cash_flows / (1 + discount_rate) ** np.arange(len(cash_flows)))

def render():
    st.header("Расчеты")

    if 'project_data' not in st.session_state:
        st.warning("Пожалуйста, сначала введите данные на странице 'Ввод данных'")
        return

    data = st.session_state['project_data']
    
    # Создаем DataFrame для расчетов
    df = pd.DataFrame(data['yearly_data'])
    df['Год'] = range(1, len(df) + 1)
    
    # Преобразуем столбцы в числовой формат
    for col in ['Выручка', 'Фиксированные операционные затраты', 'Капитальные затраты']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Расчет переменных операционных затрат
    var_costs = pd.DataFrame(data['var_costs'])
    var_costs['Количество'] = pd.to_numeric(var_costs['Количество'], errors='coerce')
    var_costs['Ставка'] = pd.to_numeric(var_costs['Ставка'], errors='coerce')
    
    coefficients = {k: float(v) for k, v in data['coefficients'].items()}
    total_var_costs = (var_costs['Количество'] * var_costs['Ставка'] * 
                       var_costs['Коэффициент'].map(coefficients)).sum()
    
    df['Переменные операционные затраты'] = total_var_costs
    
    # Расчет CFO, CFI и CF
    df['CFO'] = calculate_cf(df['Выручка'], df['Фиксированные операционные затраты'], df['Переменные операционные затраты'])
    df['CFI'] = -df['Капитальные затраты']
    df['CF'] = df['CFO'] + df['CFI']
    
    # Расчет дисконтированного CF и NPV
    discount_rate = float(data['discount_rate'])
    df['Дисконтированный CF'] = df['CF'] / (1 + discount_rate) ** df['Год']
    
    impact_duration = int(data['impact_duration'])
    npv = calculate_npv(df['CF'][:impact_duration], discount_rate)
    
    st.subheader("Результаты расчетов")
    st.dataframe(df)
    
    st.subheader("Итоговые показатели")
    st.write(f"NPV: {npv:.2f}")
    
    # Сохранение результатов расчетов
    st.session_state['calculation_results'] = {
        'df': df,
        'npv': npv
    }
    
    st.success("Расчеты выполнены успешно!")

if __name__ == "__main__":
    render()

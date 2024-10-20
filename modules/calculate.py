import streamlit as st
import pandas as pd
import numpy as np

def calculate_cf(revenue, fixed_costs, var_costs):
    """Расчет денежного потока"""
    return revenue - fixed_costs - var_costs

def calculate_npv(cash_flows, discount_rate, impact_duration):
    """Расчет NPV с учетом срока влияния"""
    n = min(len(cash_flows), impact_duration)
    npv = 0
    for i in range(n):
        npv += cash_flows.iloc[i] / (1 + discount_rate) ** (i + 1)
    return npv

def render():
    st.header("Расчеты")

    if 'project_data' not in st.session_state:
        st.warning("Пожалуйста, сначала введите данные на странице 'Ввод данных' и сохраните их.")
        return

    data = st.session_state['project_data']
    
    # Создаем DataFrame для расчетов
    df = pd.DataFrame(data['yearly_data'])
    df['Год'] = range(1, len(df) + 1)
    
    # Преобразуем столбцы в числовой формат
    for col in ['Выручка', 'Фиксированные операционные затраты', 'Капитальные затраты']:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
    
    # Расчет переменных операционных затрат
    var_costs = pd.DataFrame(data['var_costs'])
    if 'Количество лет' in var_costs.columns:
        var_costs['Количество лет'] = pd.to_numeric(var_costs['Количество лет'], errors='coerce').astype(float)
    else:
        var_costs['Количество лет'] = pd.to_numeric(var_costs['Количество месяцев'], errors='coerce').astype(float)
    var_costs['Количество'] = pd.to_numeric(var_costs['Количество'], errors='coerce').astype(float)
    var_costs['Ставка'] = pd.to_numeric(var_costs['Ставка'], errors='coerce').astype(float)
    var_costs['Процент индексирования'] = pd.to_numeric(var_costs['Процент индексирования'], errors='coerce').astype(float)
    
    coefficients = {k: float(v) for k, v in data['coefficients'].items()}
    
    total_var_costs = []
    for year in range(1, len(df) + 1):
        year_var_costs = 0
        for _, row in var_costs.iterrows():
            if year <= row['Количество лет']:
                year_var_costs += row['Количество'] * row['Ставка'] * coefficients[row['Коэффициент']]
            else:
                year_var_costs += row['Количество'] * row['Ставка'] * coefficients[row['Коэффициент']] * (1 + row['Процент индексирования']) ** (year - 1)
        total_var_costs.append(year_var_costs)
    
    df['Переменные операционные затраты'] = total_var_costs
    
    # Расчет CFO, CFI и CF
    df['CFO'] = calculate_cf(df['Выручка'], df['Фиксированные операционные затраты'], df['Переменные операционные затраты'])
    df['CFI'] = -df['Капитальные затраты']
    df['CF'] = df['CFO'] + df['CFI']
    
    # Расчет дисконтированного CF и NPV
    discount_rate = float(data['discount_rate'])
    impact_duration = int(data['impact_duration'])
    df['Дисконтированный CF'] = df['CF'] / (1 + discount_rate) ** df['Год']
    npv = calculate_npv(df['CF'], discount_rate, impact_duration)
    
    st.subheader("Результаты расчетов")
    st.dataframe(df)
    
    st.subheader("Итоговые показатели")
    st.write(f"**NPV:** {npv:.2f}")
    
    # Проверка данных
    st.subheader("Проверка данных")
    
    # Проверка и вывод промежуточных результатов
    st.write("**Промежуточные результаты:**")
    st.write(f"**Выручка:**")
    st.write(df['Выручка'])
    st.write(f"**Фиксированные операционные затраты:**")
    st.write(df['Фиксированные операционные затраты'])
    st.write(f"**Переменные операционные затраты:**")
    st.write(df['Переменные операционные затраты'])
    st.write(f"**Капитальные затраты:**")
    st.write(df['Капитальные затраты'])
    st.write(f"**CF:**")
    st.write(df['CF'])
    st.write(f"**Срок влияния:** {impact_duration} лет")
    st.write(f"**Ставка дисконтирования:** {discount_rate:.2%}")
    st.write(f"**Дисконтированный CF:**")
    st.write(df['Дисконтированный CF'])
    
    # Проверка на наличие отрицательных или нулевых значений
    if (df['Выручка'] <= 0).any() or (df['Фиксированные операционные затраты'] <= 0).any() or \
       (df['Переменные операционные затраты'] <= 0).any() or (df['Капитальные затраты'] < 0).any():
        st.warning("Внимание: обнаружены отрицательные или нулевые значения в ключевых столбцах")

    # Проверка согласованности расчетов
    calculated_cf = df['Выручка'] - df['Фиксированные операционные затраты'] - \
                    df['Переменные операционные затраты'] - df['Капитальные затраты']
    if not np.allclose(calculated_cf, df['CF']):
        st.warning("Внимание: рассчитанный CF не соответствует значениям в столбце CF")
    
    # Проверка корректности расчета NPV
    calculated_npv = df['Дисконтированный CF'][:impact_duration].sum()
    if not np.isclose(calculated_npv, npv):
        st.warning(f"Внимание: Рассчитанный NPV ({calculated_npv:.2f}) не соответствует значению NPV ({npv:.2f})")
    
    # Дополнительная проверка расчета NPV
    npv_3_years = df['Дисконтированный CF'][:impact_duration].sum()
    npv_5_years = df['Дисконтированный CF'].sum()

    st.write(f"**NPV за {impact_duration} года (срок влияния):** {npv_3_years:.2f}")
    st.write(f"**NPV за все 5 лет:** {npv_5_years:.2f}")

    if np.isclose(npv, npv_3_years):
        st.success("NPV рассчитан корректно на основе срока влияния")
    elif np.isclose(npv, npv_5_years):
        st.warning("NPV рассчитан на основе всех 5 лет, а не срока влияния")
    else:
        st.error("NPV не соответствует ни расчету за срок влияния, ни расчету за все 5 лет")
    
    # Добавление подробного вывода расчета NPV по годам
    st.write("**Расчет NPV по годам:**")
    for year in range(1, impact_duration + 1):
        st.write(f"**Год {year}:** {df['Дисконтированный CF'].iloc[year-1]:.2f}")
    st.write(f"**Сумма (NPV):** {df['Дисконтированный CF'][:impact_duration].sum():.2f}")
    
    # Сохранение результатов расчетов
    st.session_state['calculation_results'] = {
        'df': df,
        'npv': npv
    }
    
    st.success("Расчеты выполнены успешно!")

if __name__ == "__main__":
    render()

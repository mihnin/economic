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
        st.warning("Пожалуйста, сначала введите данные на странице 'Ввод данных' и сохраните их.")
        return

    data = st.session_state['project_data']
    
    # Создаем DataFrame для расчетов
    df = pd.DataFrame(data['yearly_data'])
    df['Год'] = range(1, len(df) + 1)
    
    # Преобразуем столбцы в числовой формат
    for col in ['Выручка', 'Фиксированные операционные затраты', 'Капитальные затраты']:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)  # Преобразуем в float
    
    # Расчет переменных операционных затрат
    var_costs = pd.DataFrame(data['var_costs'])
    if 'Количество лет' in var_costs.columns:
        var_costs['Количество лет'] = pd.to_numeric(var_costs['Количество лет'], errors='coerce').astype(float)  # Преобразуем в float
    else:
        var_costs['Количество лет'] = pd.to_numeric(var_costs['Количество месяцев'], errors='coerce').astype(float)  # Преобразуем в float
    var_costs['Количество'] = pd.to_numeric(var_costs['Количество'], errors='coerce').astype(float)  # Преобразуем в float
    var_costs['Ставка'] = pd.to_numeric(var_costs['Ставка'], errors='coerce').astype(float)  # Преобразуем в float
    var_costs['Процент индексирования'] = pd.to_numeric(var_costs['Процент индексирования'], errors='coerce').astype(float)  # Преобразуем в float
    
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
    df['Дисконтированный CF'] = df['CF'] / (1 + discount_rate) ** df['Год']
    
    impact_duration = int(data['impact_duration'])
    npv = calculate_npv(df['CF'][:impact_duration], discount_rate)
    
    st.subheader("Результаты расчетов")
    st.dataframe(df)
    
    st.subheader("Итоговые показатели")
    st.write(f"NPV: {npv:.2f}")
    
    # Проверка данных
    st.subheader("Проверка данных")
    
    # Проверка и вывод промежуточных результатов
    st.write("Промежуточные результаты:")
    st.write(f"Выручка: {df['Выручка']}")
    st.write(f"Фиксированные операционные затраты: {df['Фиксированные операционные затраты']}")
    st.write(f"Переменные операционные затраты: {df['Переменные операционные затраты']}")
    st.write(f"Капитальные затраты: {df['Капитальные затраты']}")
    st.write(f"CF: {df['CF']}")

    # Проверка на наличие отрицательных или нулевых значений
    if (df['Выручка'] <= 0).any() or (df['Фиксированные операционные затраты'] <= 0).any() or \
       (df['Переменные операционные затраты'] <= 0).any() or (df['Капитальные затраты'] < 0).any():
        st.warning("Внимание: обнаружены отрицательные или нулевые значения в ключевых столбцах")

    # Проверка согласованности расчетов
    calculated_cf = df['Выручка'] - df['Фиксированные операционные затраты'] - \
                    df['Переменные операционные затраты'] - df['Капитальные затраты']
    if not np.allclose(calculated_cf, df['CF']):
        st.warning("Внимание: рассчитанный CF не соответствует значениям в столбце CF")
    
    # Сохранение результатов расчетов
    st.session_state['calculation_results'] = {
        'df': df,
        'npv': npv
    }
    
    st.success("Расчеты выполнены успешно!")

    # Добавление подробных формул и расчетов
    st.subheader("Подробные формулы и расчеты")
    st.write("""
    **CFO (Cash Flow from Operations):**
    CFO = Выручка - Фиксированные операционные затраты - Переменные операционные затраты
    """)
    st.write("""
    **CFI (Cash Flow from Investments):**
    CFI = -Капитальные затраты
    """)
    st.write("""
    **CF (Cash Flow):**
    CF = CFO + CFI
    """)
    st.write("""
    **Дисконтированный CF:**
    Дисконтированный CF = CF / (1 + Ставка дисконтирования) ^ Год
    """)

if __name__ == "__main__":
    render()

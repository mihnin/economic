import streamlit as st
import pandas as pd
import numpy as np

def generate_test_data(project_duration):
    # Генерация тестовых данных по годам
    yearly_data = pd.DataFrame({
        'Выручка': np.random.randint(1000000, 5000000, project_duration),
        'Фиксированные операционные затраты': np.random.randint(500000, 2000000, project_duration),
        'Капитальные затраты': np.random.randint(100000, 1000000, project_duration)
    }, index=range(1, project_duration + 1))
    
    # Генерация тестовых данных для переменных операционных затрат
    specialists = ['Методолог', 'Консультант', 'Архитектор', 'Подрядчик', 'Руководитель проекта', 'Стажер', 'Секретарь']
    var_costs = pd.DataFrame({
        'Коэффициент': ['K1', 'K2', 'K3', 'K4', 'K5', 'K1', 'K2'],
        'Количество': np.random.randint(1, 10, 7),
        'Ставка': np.random.randint(50000, 200000, 7)
    }, index=specialists)
    
    return yearly_data, var_costs

def render():
    st.header("Ввод данных")

    # Ввод основных параметров проекта
    col1, col2, col3 = st.columns(3)
    with col1:
        project_duration = st.slider("Срок проекта (лет)", 1, 15, 5)
    with col2:
        impact_duration = st.slider("Срок влияния (лет)", 1, 5, 3)
    with col3:
        discount_rate = st.number_input("Ставка дисконтирования", min_value=0.0, max_value=1.0, value=0.1, step=0.01)

    # Генерация тестовых данных
    if 'test_data' not in st.session_state:
        st.session_state['test_data'] = generate_test_data(project_duration)

    yearly_data, var_costs = st.session_state['test_data']

    # Отображение и редактирование данных по годам
    st.subheader("Данные по годам")
    edited_df = st.data_editor(yearly_data, num_rows="dynamic")

    # Ввод коэффициентов К1-К5
    st.subheader("Коэффициенты")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        k1 = st.number_input("K1", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
    with col2:
        k2 = st.number_input("K2", min_value=0.0, max_value=10.0, value=1.2, step=0.1)
    with col3:
        k3 = st.number_input("K3", min_value=0.0, max_value=10.0, value=1.5, step=0.1)
    with col4:
        k4 = st.number_input("K4", min_value=0.0, max_value=10.0, value=1.3, step=0.1)
    with col5:
        k5 = st.number_input("K5", min_value=0.0, max_value=10.0, value=1.1, step=0.1)

    # Отображение и редактирование переменных операционных затрат
    st.subheader("Переменные операционные затраты")
    edited_var_costs_df = st.data_editor(var_costs, num_rows="dynamic")

    # Сохранение введенных данных в session_state
    if st.button("Сохранить данные"):
        st.session_state['project_data'] = {
            'project_duration': project_duration,
            'impact_duration': impact_duration,
            'discount_rate': discount_rate,
            'yearly_data': edited_df.to_dict(),
            'coefficients': {'K1': k1, 'K2': k2, 'K3': k3, 'K4': k4, 'K5': k5},
            'var_costs': edited_var_costs_df.to_dict()
        }
        st.success("Данные успешно сохранены!")

if __name__ == "__main__":
    render()

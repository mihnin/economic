import pandas as pd
import streamlit as st

def manual_input():
    """
    Функция для ручного ввода данных через интерфейс Streamlit.
    """
    st.subheader("Ручной ввод данных")
    
    # Финансовые показатели
    revenue = st.number_input("Выручка", min_value=0.0, format="%f")
    opex = st.number_input("Операционные затраты", min_value=0.0, format="%f")
    capex = st.number_input("Капитальные затраты", min_value=0.0, format="%f")
    working_capital = st.number_input("Чистый оборотный капитал", format="%f")
    
    # Параметры проекта
    discount_rate = st.number_input("Ставка дисконтирования", min_value=0.0, max_value=1.0, format="%f")
    impact_period = st.number_input("Срок влияния (лет)", min_value=1, format="%d")
    calculation_period = st.number_input("Период расчета эффекта (лет)", min_value=1, format="%d")
    
    return {
        "revenue": revenue,
        "opex": opex,
        "capex": capex,
        "working_capital": working_capital,
        "discount_rate": discount_rate,
        "impact_period": impact_period,
        "calculation_period": calculation_period
    }

def file_upload():
    """
    Функция для загрузки данных из Excel-файла.
    """
    st.subheader("Загрузка Excel-файла")
    uploaded_file = st.file_uploader("Выберите Excel-файл", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.success("Файл успешно загружен!")
            return df
        except Exception as e:
            st.error(f"Ошибка при загрузке файла: {str(e)}")
            return None
    return None

# TODO: Реализовать функцию для обработки загруженных данных
# TODO: Добавить валидацию введенных данных
# TODO: Реализовать сохранение введенных данных для дальнейшего использования

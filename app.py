import streamlit as st
import pandas as pd
import numpy as np
from modules import data_input, calculations, prediction, visualization

def main():
    st.title("Расчет экономического эффекта инвестиционных IT-проектов")

    # Боковая панель для выбора языка (пока не реализовано)
    st.sidebar.selectbox("Выберите язык / Select language", ["Русский", "English"])

    # Вкладки для разных функций приложения
    tab1, tab2, tab3 = st.tabs(["Ввод данных", "Расчет эффекта", "Прогнозирование"])

    with tab1:
        st.header("Ввод данных")
        input_method = st.radio("Выберите метод ввода данных:", ["Ручной ввод", "Загрузка файла"])
        
        if input_method == "Ручной ввод":
            input_data = data_input.manual_input()
        else:
            uploaded_data = data_input.file_upload()
            if uploaded_data is not None:
                st.write(uploaded_data)
                input_data = uploaded_data.to_dict('records')[0]  # Предполагаем, что в файле одна строка данных
        
        if st.button("Сохранить данные"):
            st.session_state.input_data = input_data
            st.success("Данные успешно сохранены!")

    with tab2:
        st.header("Расчет экономического эффекта")
        if 'input_data' in st.session_state:
            data = st.session_state.input_data
            years = int(data['calculation_period'])
            
            fem = calculations.create_fem(data, years)
            st.write("Финансово-экономическая модель:")
            st.write(fem)
            
            npv = calculations.calculate_npv(fem['CF'], data['discount_rate'])
            st.write(f"NPV проекта: {npv:.2f}")
            
            visualization.plot_cash_flows(fem)
            visualization.plot_npv(fem)
        else:
            st.warning("Пожалуйста, введите данные на вкладке 'Ввод данных'")

    with tab3:
        st.header("Прогнозирование экономического эффекта")
        if 'input_data' in st.session_state:
            st.write("Для демонстрации функционала прогнозирования необходимы исторические данные.")
            st.write("В реальном приложении здесь будет реализовано:")
            st.write("1. Загрузка исторических данных")
            st.write("2. Обучение моделей (линейная регрессия и дерево решений)")
            st.write("3. Прогнозирование на основе введенных данных")
            st.write("4. Визуализация результатов прогнозирования")
            
            # Пример использования класса EconomicEffectPredictor
            predictor = prediction.EconomicEffectPredictor()
            st.write("Класс EconomicEffectPredictor создан и готов к использованию")
        else:
            st.warning("Пожалуйста, введите данные на вкладке 'Ввод данных'")

if __name__ == "__main__":
    main()

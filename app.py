import streamlit as st
import pandas as pd
import numpy as np
from modules import data_input, calculations, prediction, visualization

def main():
    # Инициализация состояния для языка
    if 'language' not in st.session_state:
        st.session_state.language = 'ru'

    # Словарь для перевода
    translations = {
        'ru': {
            'title': "Расчет экономического эффекта инвестиционных IT-проектов",
            'lang_selector': "Выберите язык",
            'input_tab': "Ввод данных",
            'calc_tab': "Расчет эффекта",
            'predict_tab': "Прогнозирование",
            'input_method': "Выберите метод ввода данных:",
            'manual_input': "Ручной ввод",
            'file_upload': "Загрузка файла",
            'save_data': "Сохранить данные",
            'data_saved': "Данные успешно сохранены!",
            'fem_title': "Финансово-экономическая модель:",
            'npv_result': "NPV проекта:",
            'input_warning': "Пожалуйста, введите данные на вкладке 'Ввод данных'",
            'predict_info': "Для демонстрации функционала прогнозирования необходимы исторические данные.",
            'predict_steps': [
                "В реальном приложении здесь будет реализовано:",
                "1. Загрузка исторических данных",
                "2. Обучение моделей (линейная регрессия и дерево решений)",
                "3. Прогнозирование на основе введенных данных",
                "4. Визуализация результатов прогнозирования"
            ],
            'predictor_ready': "Класс EconomicEffectPredictor создан и готов к использованию"
        },
        'en': {
            'title': "Calculation of Economic Effect of Investment IT Projects",
            'lang_selector': "Select language",
            'input_tab': "Data Input",
            'calc_tab': "Effect Calculation",
            'predict_tab': "Prediction",
            'input_method': "Choose data input method:",
            'manual_input': "Manual input",
            'file_upload': "File upload",
            'save_data': "Save data",
            'data_saved': "Data successfully saved!",
            'fem_title': "Financial and Economic Model:",
            'npv_result': "Project NPV:",
            'input_warning': "Please enter data in the 'Data Input' tab",
            'predict_info': "Historical data is required to demonstrate the prediction functionality.",
            'predict_steps': [
                "In the real application, the following will be implemented here:",
                "1. Loading historical data",
                "2. Training models (linear regression and decision trees)",
                "3. Prediction based on input data",
                "4. Visualization of prediction results"
            ],
            'predictor_ready': "EconomicEffectPredictor class is created and ready to use"
        }
    }

    # Выбор языка
    lang = st.sidebar.selectbox(
        translations[st.session_state.language]['lang_selector'],
        ['Русский', 'English']
    )
    st.session_state.language = 'ru' if lang == 'Русский' else 'en'

    # Получение текущего языка
    current_lang = st.session_state.language
    t = translations[current_lang]

    st.title(t['title'])

    # Вкладки для разных функций приложения
    tab1, tab2, tab3 = st.tabs([t['input_tab'], t['calc_tab'], t['predict_tab']])

    with tab1:
        st.header(t['input_tab'])
        input_method = st.radio(t['input_method'], [t['manual_input'], t['file_upload']])
        
        if input_method == t['manual_input']:
            input_data = data_input.manual_input(current_lang)
        else:
            input_data = data_input.file_upload(current_lang)
        
        if input_data and st.button(t['save_data']):
            st.session_state.input_data = input_data
            st.success(t['data_saved'])

    with tab2:
        st.header(t['calc_tab'])
        if 'input_data' in st.session_state:
            data = st.session_state.input_data
            years = int(data['calculation_period'])
            
            fem = calculations.create_fem(data, years)
            st.write(t['fem_title'])
            st.write(fem)
            
            npv = calculations.calculate_npv(fem['CF'], data['discount_rate'])
            st.write(f"{t['npv_result']} {npv:.2f}")
            
            visualization.plot_cash_flows(fem, current_lang)
            visualization.plot_npv(fem, current_lang)
        else:
            st.warning(t['input_warning'])

    with tab3:
        st.header(t['predict_tab'])
        if 'input_data' in st.session_state:
            st.write(t['predict_info'])
            for step in t['predict_steps']:
                st.write(step)
            
            # Пример использования класса EconomicEffectPredictor
            predictor = prediction.EconomicEffectPredictor()
            st.write(t['predictor_ready'])
        else:
            st.warning(t['input_warning'])

if __name__ == "__main__":
    main()

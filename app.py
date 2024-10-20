import streamlit as st
import pandas as pd
import numpy as np
from modules import data_input, calculations, visualization

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
            'input_method': "Выберите метод ввода данных:",
            'manual_input': "Ручной ввод",
            'file_upload': "Загрузка файла",
            'save_data': "Сохранить данные",
            'data_saved': "Данные успешно сохранены!",
            'fem_title': "Финансово-экономическая модель:",
            'npv_result': "NPV проекта:",
            'input_warning': "Пожалуйста, введите данные на вкладке 'Ввод данных'",
            'employee_data': "Данные о сотрудниках:",
            'total_opex': "Общие операционные затраты:"
        },
        'en': {
            'title': "Calculation of Economic Effect of Investment IT Projects",
            'lang_selector': "Select language",
            'input_tab': "Data Input",
            'calc_tab': "Effect Calculation",
            'input_method': "Choose data input method:",
            'manual_input': "Manual input",
            'file_upload': "File upload",
            'save_data': "Save data",
            'data_saved': "Data successfully saved!",
            'fem_title': "Financial and Economic Model:",
            'npv_result': "Project NPV:",
            'input_warning': "Please enter data in the 'Data Input' tab",
            'employee_data': "Employee data:",
            'total_opex': "Total operating expenses:"
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
    tab1, tab2 = st.tabs([t['input_tab'], t['calc_tab']])

    with tab1:
        st.header(t['input_tab'])
        input_method = st.radio(t['input_method'], [t['manual_input'], t['file_upload']])
        
        if input_method == t['manual_input']:
            input_data = data_input.manual_input(current_lang)
        else:
            input_data = data_input.file_upload(current_lang)
        
        if input_data:
            st.session_state.input_data = input_data
            st.success(t['data_saved'])
            
            # Отображение данных о сотрудниках
            st.subheader(t['employee_data'])
            st.dataframe(st.session_state.employee_data)
            
            # Отображение общих операционных затрат
            st.subheader(t['total_opex'])
            st.write(f"{input_data['total_opex']:.2f}")

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

if __name__ == "__main__":
    main()

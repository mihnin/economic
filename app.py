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
            'total_opex': "Общие операционные затраты:",
            'what_if': "Анализ 'Что если'",
            'update_params': "Обновить параметры",
            'fem_explanation': "Пояснение к ФЭМ:",
            'cash_flow_explanation': "Пояснение к графику денежных потоков:",
            'npv_explanation': "Пояснение к графику NPV:",
            'export_results': "Экспорт результатов в Excel",
            'revenue': "Выручка",
            'fixed_opex': "Фиксированные операционные затраты",
            'variable_opex': "Переменные операционные затраты",
            'capex': "Капитальные затраты",
            'working_capital': "Чистый оборотный капитал",
            'discount_rate': "Ставка дисконтирования"
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
            'total_opex': "Total operating expenses:",
            'what_if': "What-if Analysis",
            'update_params': "Update parameters",
            'fem_explanation': "FEM Explanation:",
            'cash_flow_explanation': "Cash Flow Chart Explanation:",
            'npv_explanation': "NPV Chart Explanation:",
            'export_results': "Export results to Excel",
            'revenue': "Revenue",
            'fixed_opex': "Fixed operating expenses",
            'variable_opex': "Variable operating expenses",
            'capex': "Capital expenditures",
            'working_capital': "Net working capital",
            'discount_rate': "Discount rate"
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
            st.session_state.input_data['variable_opex'] = input_data['total_opex'] - input_data['fixed_opex']
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
            
            # Анализ "Что если"
            st.subheader(t['what_if'])
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                data['revenue'] = st.number_input(t['revenue'], value=float(data['revenue']), step=10000.0)
            with col2:
                data['fixed_opex'] = st.number_input(t['fixed_opex'], value=float(data['fixed_opex']), step=10000.0)
            with col3:
                data['variable_opex'] = st.number_input(t['variable_opex'], value=float(data['variable_opex']), step=10000.0)
            with col4:
                data['capex'] = st.number_input(t['capex'], value=float(data['capex']), step=10000.0)
            with col5:
                data['working_capital'] = st.number_input(t['working_capital'], value=float(data['working_capital']), step=10000.0)
            with col6:
                data['discount_rate'] = st.number_input(t['discount_rate'], value=float(data['discount_rate']), min_value=0.0, max_value=1.0, step=0.01)

            if st.button(t['update_params']):
                fem = calculations.create_fem(data, years)
                st.session_state.fem = fem
                st.session_state.npv = calculations.calculate_npv(fem['CF'], data['discount_rate'])

            if 'fem' in st.session_state:
                fem = st.session_state.fem
                npv = st.session_state.npv
            else:
                fem = calculations.create_fem(data, years)
                npv = calculations.calculate_npv(fem['CF'], data['discount_rate'])

            st.subheader(t['fem_title'])
            st.dataframe(fem)
            st.write(t['fem_explanation'])
            st.write("ФЭМ показывает финансовые потоки проекта по годам, включая выручку, затраты и денежные потоки.")
            
            st.write(f"{t['npv_result']} {npv:.2f}")
            
            st.subheader(t['cash_flow_explanation'])
            st.write("График показывает динамику операционного (CFO), инвестиционного (CFI) и совокупного (CF) денежных потоков по годам.")
            visualization.plot_cash_flows(fem, current_lang)
            
            st.subheader(t['npv_explanation'])
            st.write("График отображает накопленный NPV проекта по годам. Положительное значение NPV указывает на экономическую эффективность проекта.")
            visualization.plot_npv(fem, current_lang)

            # Экспорт результатов в Excel
            st.subheader(t['export_results'])
            if st.button(t['export_results']):
                with pd.ExcelWriter('results.xlsx', engine='openpyxl') as writer:
                    fem.to_excel(writer, sheet_name='FEM')
                    st.session_state.employee_data.to_excel(writer, sheet_name='Employee Data')
                    st.write("Результаты успешно экспортированы в файл results.xlsx")

        else:
            st.warning(t['input_warning'])

if __name__ == "__main__":
    main()

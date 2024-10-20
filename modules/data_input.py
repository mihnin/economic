import pandas as pd
import streamlit as st

def manual_input(lang='ru'):
    """
    Функция для ручного ввода данных через интерфейс Streamlit.
    """
    labels = {
        'ru': {
            "Выручка": "Выручка",
            "Фиксированные операционные затраты": "Фиксированные операционные затраты",
            "Капитальные затраты": "Капитальные затраты",
            "Чистый оборотный капитал": "Чистый оборотный капитал",
            "Ставка дисконтирования": "Ставка дисконтирования",
            "Срок влияния (лет)": "Срок влияния (лет)",
            "Период расчета эффекта (лет)": "Период расчета эффекта (лет)",
            "Ставки сотрудников": "Ставки и часы работы сотрудников",
            "Консультант": "Консультант",
            "Методолог": "Методолог",
            "Разработчик": "Разработчик",
            "Подрядчик": "Подрядчик",
            "Ставка": "Ставка (в час)",
            "Часы": "Часы работы",
            "Сохранить": "Сохранить данные",
            "Категория": "Категория"
        },
        'en': {
            "Выручка": "Revenue",
            "Фиксированные операционные затраты": "Fixed operating expenses",
            "Капитальные затраты": "Capital expenditures",
            "Чистый оборотный капитал": "Net working capital",
            "Ставка дисконтирования": "Discount rate",
            "Срок влияния (лет)": "Impact period (years)",
            "Период расчета эффекта (лет)": "Calculation period (years)",
            "Ставки сотрудников": "Employee rates and working hours",
            "Консультант": "Consultant",
            "Методолог": "Methodologist",
            "Разработчик": "Developer",
            "Подрядчик": "Contractor",
            "Ставка": "Rate (per hour)",
            "Часы": "Working hours",
            "Сохранить": "Save data",
            "Категория": "Category"
        }
    }
    
    t = labels[lang]
    
    st.subheader({"ru": "Ручной ввод данных", "en": "Manual data input"}[lang])
    
    data = {}
    data['revenue'] = st.number_input(t["Выручка"], value=1000000, format="%f")
    data['fixed_opex'] = st.number_input(t["Фиксированные операционные затраты"], value=500000, format="%f")
    data['capex'] = st.number_input(t["Капитальные затраты"], value=200000, format="%f")
    data['working_capital'] = st.number_input(t["Чистый оборотный капитал"], value=50000, format="%f")
    data['discount_rate'] = st.number_input(t["Ставка дисконтирования"], min_value=0.0, max_value=1.0, value=0.1, format="%f")
    data['impact_period'] = st.number_input(t["Срок влияния (лет)"], min_value=1, value=5, format="%d")
    data['calculation_period'] = st.number_input(t["Период расчета эффекта (лет)"], min_value=1, value=10, format="%d")

    st.subheader(t["Ставки сотрудников"])
    
    # Создаем DataFrame для табличного ввода
    if 'employee_data' not in st.session_state:
        st.session_state.employee_data = pd.DataFrame({
            "Категория": [t["Консультант"], t["Методолог"], t["Разработчик"], t["Подрядчик"]],
            t["Ставка"]: [100, 80, 70, 90],
            t["Часы"]: [0, 0, 0, 0]
        })

    # Отображаем таблицу для редактирования
    edited_df = st.data_editor(
        st.session_state.employee_data,
        column_config={
            "Категория": st.column_config.TextColumn(t["Категория"], disabled=True),
            t["Ставка"]: st.column_config.NumberColumn(t["Ставка"], min_value=0, format="%.2f"),
            t["Часы"]: st.column_config.NumberColumn(t["Часы"], min_value=0, format="%d")
        },
        hide_index=True,
    )

    if st.button(t["Сохранить"]):
        st.session_state.employee_data = edited_df
        st.success({"ru": "Данные сохранены!", "en": "Data saved!"}[lang])

    # Расчет общих операционных затрат
    total_opex = data['fixed_opex']
    for _, row in st.session_state.employee_data.iterrows():
        total_opex += row[t["Ставка"]] * row[t["Часы"]]
    data['total_opex'] = total_opex

    # Сохраняем ставки в data для использования в других частях приложения
    for _, row in st.session_state.employee_data.iterrows():
        rate_key = f"{row['Категория'].lower()}_rate".replace("ь", "").replace("о", "o").replace("г", "g")
        data[rate_key] = row[t["Ставка"]]

    return data

def file_upload(lang='ru'):
    """
    Функция для загрузки данных из Excel-файла.
    """
    st.subheader({"ru": "Загрузка Excel-файла", "en": "Upload Excel file"}[lang])
    uploaded_file = st.file_uploader({"ru": "Выберите Excel-файл", "en": "Choose an Excel file"}[lang], type=["xlsx", "xls", "csv"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.success({"ru": "Файл успешно загружен!", "en": "File successfully uploaded!"}[lang])
            
            # Преобразование DataFrame в словарь
            data = df.iloc[0].to_dict()
            
            # Переименование ключей для соответствия ожидаемому формату
            key_mapping = {
                'Выручка': 'revenue',
                'Фиксированные операционные затраты': 'fixed_opex',
                'Капитальные затраты': 'capex',
                'Чистый оборотный капитал': 'working_capital',
                'Ставка дисконтирования': 'discount_rate',
                'Срок влияния': 'impact_period',
                'Период расчета эффекта': 'calculation_period',
                'Ставка консультанта': 'consultant_rate',
                'Ставка методолога': 'methodologist_rate',
                'Ставка разработчика': 'developer_rate',
                'Ставка подрядчика': 'contractor_rate'
            }
            data = {key_mapping.get(k, k): v for k, v in data.items()}
            
            return data
        except Exception as e:
            st.error(f"Ошибка при загрузке файла: {str(e)}")
            return None
    return None

# TODO: Добавить валидацию введенных данных
# TODO: Реализовать сохранение введенных данных для дальнейшего использования

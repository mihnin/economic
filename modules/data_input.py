import pandas as pd
import streamlit as st

def manual_input(lang='ru'):
    """
    Функция для ручного ввода данных через интерфейс Streamlit.
    """
    labels = {
        'ru': ["Выручка", "Операционные затраты", "Капитальные затраты", "Чистый оборотный капитал", 
               "Ставка дисконтирования", "Срок влияния (лет)", "Период расчета эффекта (лет)"],
        'en': ["Revenue", "Operating expenses", "Capital expenditures", "Net working capital", 
               "Discount rate", "Impact period (years)", "Calculation period (years)"]
    }
    
    st.subheader({"ru": "Ручной ввод данных", "en": "Manual data input"}[lang])
    
    data = {}
    for i, key in enumerate(['revenue', 'opex', 'capex', 'working_capital', 'discount_rate', 'impact_period', 'calculation_period']):
        if key in ['impact_period', 'calculation_period']:
            data[key] = st.number_input(labels[lang][i], min_value=1, value=5, format="%d")
        elif key == 'discount_rate':
            data[key] = st.number_input(labels[lang][i], min_value=0.0, max_value=1.0, value=0.1, format="%f")
        else:
            data[key] = st.number_input(labels[lang][i], value=1000000 if key == 'revenue' else 0, format="%f")
    
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
                'Операционные затраты': 'opex',
                'Капитальные затраты': 'capex',
                'Чистый оборотный капитал': 'working_capital',
                'Ставка дисконтирования': 'discount_rate',
                'Срок влияния': 'impact_period',
                'Период расчета эффекта': 'calculation_period'
            }
            data = {key_mapping.get(k, k): v for k, v in data.items()}
            
            return data
        except Exception as e:
            st.error(f"Ошибка при загрузке файла: {str(e)}")
            return None
    return None

# TODO: Добавить валидацию введенных данных
# TODO: Реализовать сохранение введенных данных для дальнейшего использования

import pandas as pd
import streamlit as st
from io import BytesIO
import numpy as np

def save_to_excel(data, filename="project_data.xlsx"):
    """
    Сохраняет данные проекта в Excel файл
    """
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    # Сохраняем основные параметры проекта
    pd.DataFrame([{
        'Срок проекта': data['project_duration'],
        'Срок влияния': data['impact_duration'],
        'Ставка дисконтирования': data['discount_rate']
    }]).to_excel(writer, sheet_name='Параметры проекта', index=False)

    # Сохраняем данные по годам
    pd.DataFrame(data['yearly_data']).to_excel(writer, sheet_name='Данные по годам')

    # Сохраняем коэффициенты
    pd.DataFrame([data['coefficients']]).to_excel(writer, sheet_name='Коэффициенты', index=False)

    # Сохраняем переменные операционные затраты
    pd.DataFrame(data['var_costs']).to_excel(writer, sheet_name='Переменные затраты')

    # Если есть результаты расчетов, сохраняем их
    if 'calculation_results' in st.session_state:
        results = st.session_state['calculation_results']
        results['df'].to_excel(writer, sheet_name='Результаты расчетов')
        pd.DataFrame([{'NPV': results['npv']}]).to_excel(writer, sheet_name='Итоговые показатели', index=False)

    writer.close()
    processed_data = output.getvalue()
    return processed_data

def load_from_excel(uploaded_file):
    """
    Загружает данные проекта из Excel файла
    """
    xls = pd.ExcelFile(uploaded_file)
    
    # Загружаем основные параметры проекта
    params = pd.read_excel(xls, 'Параметры проекта').iloc[0]
    
    # Загружаем данные по годам
    yearly_data = pd.read_excel(xls, 'Данные по годам', index_col=0).to_dict()
    
    # Загружаем коэффициенты
    coefficients = pd.read_excel(xls, 'Коэффициенты').iloc[0].to_dict()
    
    # Загружаем переменные операционные затраты
    var_costs = pd.read_excel(xls, 'Переменные затраты', index_col=0).to_dict()
    
    project_data = {
        'project_duration': params['Срок проекта'],
        'impact_duration': params['Срок влияния'],
        'discount_rate': params['Ставка дисконтирования'],
        'yearly_data': yearly_data,
        'coefficients': coefficients,
        'var_costs': var_costs
    }
    
    return project_data

def format_number(number):
    """
    Форматирует число для отображения
    """
    if abs(number) >= 1e6:
        return f"{number/1e6:.2f}M"
    elif abs(number) >= 1e3:
        return f"{number/1e3:.2f}K"
    else:
        return f"{number:.2f}"

def generate_test_excel(filename="test_project_data.xlsx"):
    """
    Генерирует тестовый Excel файл с примерными данными проекта
    """
    project_duration = 5
    impact_duration = 3
    discount_rate = 0.1

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

    # Создаем тестовые данные проекта
    test_data = {
        'project_duration': project_duration,
        'impact_duration': impact_duration,
        'discount_rate': discount_rate,
        'yearly_data': yearly_data.to_dict(),
        'coefficients': {'K1': 1.0, 'K2': 1.2, 'K3': 1.5, 'K4': 1.3, 'K5': 1.1},
        'var_costs': var_costs.to_dict()
    }

    # Сохраняем тестовые данные в Excel
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    # Сохраняем основные параметры проекта
    pd.DataFrame([{
        'Срок проекта': test_data['project_duration'],
        'Срок влияния': test_data['impact_duration'],
        'Ставка дисконтирования': test_data['discount_rate']
    }]).to_excel(writer, sheet_name='Параметры проекта', index=False)

    # Сохраняем данные по годам
    yearly_data.to_excel(writer, sheet_name='Данные по годам')

    # Сохраняем коэффициенты
    pd.DataFrame([test_data['coefficients']]).to_excel(writer, sheet_name='Коэффициенты', index=False)

    # Сохраняем переменные операционные затраты
    var_costs.to_excel(writer, sheet_name='Переменные затраты')

    writer.close()
    processed_data = output.getvalue()

    # Сохраняем файл
    with open(filename, 'wb') as f:
        f.write(processed_data)

    return filename

# Генерируем тестовый Excel файл
generate_test_excel()

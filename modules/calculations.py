import numpy as np
import pandas as pd

def calculate_npv(cash_flows, discount_rate):
    """
    Расчет Чистой Приведенной Стоимости (NPV).
    
    :param cash_flows: список денежных потоков
    :param discount_rate: ставка дисконтирования
    :return: значение NPV
    """
    npv = sum(cf / (1 + discount_rate)**i for i, cf in enumerate(cash_flows))
    return npv

def calculate_cf(revenue, total_opex, capex, working_capital):
    """
    Расчет Совокупного Денежного Потока (CF).
    
    :param revenue: выручка
    :param total_opex: общие операционные затраты
    :param capex: капитальные затраты
    :param working_capital: изменение чистого оборотного капитала
    :return: значение CF
    """
    cf = revenue - total_opex - capex - working_capital
    return cf

def create_fem(data, years):
    """
    Создание Финансово-Экономической Модели (ФЭМ).
    
    :param data: словарь с входными данными
    :param years: количество лет для расчета
    :return: DataFrame с ФЭМ
    """
    fem = pd.DataFrame(index=range(years))
    
    # Заполнение данными
    fem['Выручка'] = [data['revenue']] * years
    fem['Операционные затраты'] = [data['total_opex']] * years
    fem['Капитальные затраты'] = [data['capex']] * years
    fem['Чистый оборотный капитал'] = [data['working_capital']] * years
    
    # Расчет денежных потоков
    fem['CFO'] = fem['Выручка'] - fem['Операционные затраты']
    fem['CFI'] = -fem['Капитальные затраты'] - fem['Чистый оборотный капитал']
    fem['CF'] = fem['CFO'] + fem['CFI']
    
    # Расчет дисконтированных денежных потоков
    fem['Дисконтированный CF'] = fem['CF'] / (1 + data['discount_rate']) ** fem.index
    
    # Расчет NPV
    fem['NPV'] = fem['Дисконтированный CF'].cumsum()
    
    return fem

def calculate_irr(cash_flows):
    """
    Расчет Внутренней Нормы Доходности (IRR).
    
    :param cash_flows: список денежных потоков
    :return: значение IRR
    """
    return np.irr(cash_flows)

def calculate_payback_period(cash_flows):
    """
    Расчет Срока Окупаемости (PP).
    
    :param cash_flows: список денежных потоков
    :return: значение PP
    """
    cumulative_cash_flow = np.cumsum(cash_flows)
    payback_period = np.argmax(cumulative_cash_flow >= 0)
    return payback_period if payback_period > 0 else None

def calculate_discounted_payback_period(cash_flows, discount_rate):
    """
    Расчет Дисконтированного Срока Окупаемости (DPP).
    
    :param cash_flows: список денежных потоков
    :param discount_rate: ставка дисконтирования
    :return: значение DPP
    """
    discounted_cash_flows = [cf / (1 + discount_rate)**i for i, cf in enumerate(cash_flows)]
    return calculate_payback_period(discounted_cash_flows)

# TODO: Реализовать функцию для сравнения базового и проектного вариантов
# TODO: Реализовать анализ чувствительности

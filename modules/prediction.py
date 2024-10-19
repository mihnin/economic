import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

class EconomicEffectPredictor:
    def __init__(self):
        self.linear_model = LinearRegression()
        self.tree_model = DecisionTreeRegressor()
        
    def prepare_data(self, data):
        """
        Подготовка данных для обучения модели.
        
        :param data: DataFrame с историческими данными
        :return: X (признаки) и y (целевая переменная)
        """
        # TODO: Реализовать выбор признаков и целевой переменной
        # Пример:
        X = data[['revenue', 'opex', 'capex', 'working_capital']]
        y = data['economic_effect']
        return X, y
        
    def train_models(self, X, y):
        """
        Обучение моделей на исторических данных.
        
        :param X: признаки
        :param y: целевая переменная
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Обучение линейной регрессии
        self.linear_model.fit(X_train, y_train)
        linear_pred = self.linear_model.predict(X_test)
        linear_mse = mean_squared_error(y_test, linear_pred)
        linear_r2 = r2_score(y_test, linear_pred)
        
        # Обучение дерева решений
        self.tree_model.fit(X_train, y_train)
        tree_pred = self.tree_model.predict(X_test)
        tree_mse = mean_squared_error(y_test, tree_pred)
        tree_r2 = r2_score(y_test, tree_pred)
        
        return {
            'linear_mse': linear_mse,
            'linear_r2': linear_r2,
            'tree_mse': tree_mse,
            'tree_r2': tree_r2
        }
        
    def predict(self, data):
        """
        Прогнозирование экономического эффекта.
        
        :param data: данные для прогнозирования
        :return: прогнозы линейной регрессии и дерева решений
        """
        linear_prediction = self.linear_model.predict(data)
        tree_prediction = self.tree_model.predict(data)
        
        return {
            'linear_prediction': linear_prediction,
            'tree_prediction': tree_prediction
        }

# TODO: Реализовать функцию для загрузки исторических данных
# TODO: Добавить возможность выбора признаков для обучения модели
# TODO: Реализовать сравнение и выбор лучшей модели
# TODO: Добавить визуализацию результатов прогнозирования

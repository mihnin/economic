import streamlit as st
import os
from modules import input_data, calculate, out_data, visual_out_data, analiz_if
from utils import utils

def main():
    st.set_page_config(page_title="Экономический эффект проекта", layout="wide")
    st.title("Расчет экономического эффекта проекта")

    # Создаем тестовый Excel файл, если его еще нет
    test_file = "test_project_data.xlsx"
    if not os.path.exists(test_file):
        utils.generate_test_excel(test_file)
        st.success(f"Создан тестовый файл: {test_file}")

    # Добавляем функциональность сохранения и загрузки проекта
    st.sidebar.header("Управление проектом")

    # Сохранение проекта
    if st.sidebar.button("Сохранить проект"):
        if 'project_data' in st.session_state:
            project_name = st.sidebar.text_input("Введите название проекта")
            if project_name:
                st.session_state['project_name'] = project_name
                st.sidebar.success("Проект успешно сохранен")
                st.sidebar.info("Проект сохранен. Введите название проекта для сохранения.")
            else:
                st.sidebar.warning("Пожалуйста, введите название проекта")
        else:
            st.sidebar.warning("Нет данных для сохранения")

    # Загрузка проекта
    if 'project_name' in st.session_state:
        st.sidebar.info(f"Загруженный проект: {st.session_state['project_name']}")

    # Создаем боковую панель для навигации
    page = st.sidebar.selectbox(
        "Выберите раздел",
        ["Ввод данных", "Расчеты", "Результаты", "Визуализация", "Анализ чувствительности"]
    )

    if page == "Ввод данных":
        input_data.render()
    elif page == "Расчеты":
        calculate.render()
    elif page == "Результаты":
        out_data.render()
    elif page == "Визуализация":
        visual_out_data.render()
    elif page == "Анализ чувствительности":
        analiz_if.render()

    # Добавляем кнопку для сохранения результатов в Excel
    if 'calculation_results' in st.session_state:
        st.sidebar.header("Экспорт результатов")
        if st.sidebar.button("Сохранить результаты в Excel"):
            results_data = utils.save_to_excel(st.session_state['project_data'])
            st.sidebar.download_button(
                label="Скачать результаты",
                data=results_data,
                file_name="project_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    main()

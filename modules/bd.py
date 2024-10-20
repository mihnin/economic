import sqlite3
import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def create_connection():
    conn = sqlite3.connect('project_data.db')
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    # Удаляем существующую таблицу projects, если она существует
    cursor.execute('DROP TABLE IF EXISTS projects')
    cursor.execute('DROP TABLE IF EXISTS calculations')
    
    # Создаем таблицу projects заново с новым столбцом created_at
    cursor.execute('''
        CREATE TABLE projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            project_duration INTEGER NOT NULL,
            impact_duration INTEGER NOT NULL,
            discount_rate REAL NOT NULL,
            yearly_data TEXT NOT NULL,
            coefficients TEXT NOT NULL,
            var_costs TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            npv REAL NOT NULL,
            df TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    ''')
    conn.commit()

def save_project(conn, name, project_data):
    cursor = conn.cursor()
    logging.info(f"Saving project: {name}")
    logging.info(f"Project data: {project_data}")
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO projects (name, project_duration, impact_duration, discount_rate, yearly_data, coefficients, var_costs, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, project_data['project_duration'], project_data['impact_duration'], project_data['discount_rate'],
          pd.DataFrame(project_data['yearly_data']).to_json(), pd.DataFrame([project_data['coefficients']]).to_json(),
          pd.DataFrame(project_data['var_costs']).to_json(), created_at))
    project_id = cursor.lastrowid
    conn.commit()
    return project_id

def save_calculation(conn, project_id, npv, df):
    cursor = conn.cursor()
    logging.info(f"Saving calculation for project ID: {project_id}")
    logging.info(f"NPV: {npv}")
    logging.info(f"DF: {df}")
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO calculations (project_id, npv, df, created_at)
        VALUES (?, ?, ?, ?)
    ''', (project_id, npv, df.to_json(), created_at))
    conn.commit()

def load_projects(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects')
    return cursor.fetchall()

def load_project_data(conn, project_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
    project = cursor.fetchone()
    if project:
        project_data = {
            'id': project[0],
            'name': project[1],
            'project_duration': project[2],
            'impact_duration': project[3],
            'discount_rate': project[4],
            'yearly_data': pd.read_json(project[5]).to_dict(),
            'coefficients': pd.read_json(project[6]).iloc[0].to_dict(),
            'var_costs': pd.read_json(project[7]).to_dict(),
            'created_at': project[8]
        }
        return project_data
    return None

def load_calculation_data(conn, project_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM calculations WHERE project_id = ?', (project_id,))
    calculation = cursor.fetchone()
    if calculation:
        calculation_data = {
            'id': calculation[0],
            'project_id': calculation[1],
            'npv': calculation[2],
            'df': pd.read_json(calculation[3]),
            'created_at': calculation[4]
        }
        return calculation_data
    return None

def delete_project(conn, project_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM calculations WHERE project_id = ?', (project_id,))
    cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    conn.commit()

def update_project(conn, project_id, project_data):
    cursor = conn.cursor()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        UPDATE projects
        SET project_duration = ?, impact_duration = ?, discount_rate = ?, yearly_data = ?, coefficients = ?, var_costs = ?, created_at = ?
        WHERE id = ?
    ''', (project_data['project_duration'], project_data['impact_duration'], project_data['discount_rate'],
          pd.DataFrame(project_data['yearly_data']).to_json(), pd.DataFrame([project_data['coefficients']]).to_json(),
          pd.DataFrame(project_data['var_costs']).to_json(), created_at, project_id))
    conn.commit()

def update_calculation(conn, project_id, npv, df):
    cursor = conn.cursor()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        UPDATE calculations
        SET npv = ?, df = ?, created_at = ?
        WHERE project_id = ?
    ''', (npv, df.to_json(), created_at, project_id))
    conn.commit()

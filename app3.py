!pip install plotly

import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(layout="wide")

# Título de la aplicación
st.title("Dashboard de Datos de Energía con Plotly")

# Cargar datos de ejemplo (Reemplazar con tu dataset)
@st.cache_data
def load_data():
    return pd.DataFrame({
        "Tiempo": pd.date_range(start="2024-01-01", periods=100, freq="D"),
        "Variable 1": range(100),
        "Variable 2": [x**1.5 for x in range(100)],
        "Variable 3": [x*2 for x in range(100)],
        "Variable 4": [x**0.5 for x in range(100)],
        "Variable 5": [x*3 for x in range(100)],
        "Variable 6": [x/2 for x in range(100)]
    })

df = load_data()

# Crear dos columnas para organizar los gráficos
col1, col2 = st.columns(2)

# Graficar las variables con Plotly en columnas separadas
variables = df.columns[1:]

for i, var in enumerate(variables):
    fig = px.line(df, x="Tiempo", y=var, title=f"Evolución de {var}")
    
    if i % 2 == 0:
        col1.plotly_chart(fig, use_container_width=True)
    else:
        col2.plotly_chart(fig, use_container_width=True)

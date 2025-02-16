import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# Configuración de la página
st.set_page_config(layout="wide")

# Título de la aplicación
st.title("Dashboard de Datos de Energía con Animación en Plotly")

# # Cargar datos de ejemplo (Reemplazar con tu dataset real)
# @st.cache_data
# def load_data():
    # return pd.DataFrame({
        # "Tiempo": pd.date_range(start="2023-01-01", periods=365, freq="D"),
        # "Variable 1": range(365),
        # "Variable 2": [x**1.5 for x in range(365)],
        # "Variable 3": [x*2 for x in range(365)],
        # "Variable 4": [x**0.5 for x in range(365)],
        # "Variable 5": [x*3 for x in range(365)],
        # "Variable 6": [x/2 for x in range(365)]
    # })

# df = load_data()


import pandas as pd

df = pd.read_csv('dataset_limpio_carga_laboral.csv')

# Mostrar el DataFrame
print(df.head())


# Parámetro de ventana deslizante (1 semana de datos)
window_size = 7

# Inicializar sesión para la posición actual de la ventana
if "index" not in st.session_state:
    st.session_state.index = window_size

# Crear dos columnas para organizar los gráficos
col1, col2 = st.columns(2)

# Diccionario para los gráficos dinámicos
plotly_containers = {}

# Crear espacios para los gráficos
for i, var in enumerate(df.columns[1:]):
    if i % 2 == 0:
        plotly_containers[var] = col1.empty()
    else:
        plotly_containers[var] = col2.empty()

# Animación en tiempo real
while True:
    start_idx = max(0, st.session_state.index - window_size)
    end_idx = st.session_state.index

    df_window = df.iloc[start_idx:end_idx]

    for var in df.columns[1:]:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_window["Tiempo"], y=df_window[var], mode="lines", name=var))
        fig.update_layout(title=f"Evolución de {var}", xaxis_title="Tiempo", yaxis_title=var, xaxis_range=[df_window["Tiempo"].min(), df_window["Tiempo"].max()])

        # Actualizar el gráfico sin generar nuevos elementos
        plotly_containers[var].plotly_chart(fig, use_container_width=True)

    # Avanzar la ventana
    st.session_state.index = min(st.session_state.index + 1, len(df))

    # Esperar 500ms antes de la siguiente actualización
    time.sleep(0.5)

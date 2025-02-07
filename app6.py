import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# Configuración de la página
st.set_page_config(layout="wide")

# Título de la aplicación
st.title("Dashboard de Datos de Energía con Animación en Plotly")

# Cargar datos reales
df = pd.read_csv('dataset_limpio_carga_laboral.csv')

# Eliminar espacios en los nombres de las columnas
df.columns = df.columns.str.strip()

# Verificar nombres de columnas
st.write("Columnas disponibles en el dataset:", df.columns)

# Asegurar que la columna de tiempo exista y renombrarla si es necesario
if 'Tiempo' not in df.columns:
    df.rename(columns={df.columns[0]: 'Tiempo'}, inplace=True)

# Mostrar los primeros valores de la columna 'Tiempo' antes de la conversión
st.write("Primeros valores de la columna 'Tiempo' antes de conversión:", df['Tiempo'].head())

# Asegurar que la columna 'Tiempo' sea tipo string antes de la conversión
df['Tiempo'] = df['Tiempo'].astype(str)

# Intentar conversión a datetime con un formato específico si se conoce
df['Tiempo'] = pd.to_datetime(df['Tiempo'], errors='coerce')

# Mostrar valores únicos de la columna 'Tiempo' después de la conversión
st.write("Valores únicos en la columna 'Tiempo' después de conversión:", df['Tiempo'].unique()[:10])

# Mostrar el DataFrame
st.write("Vista previa de los datos:", df.head())

# Parámetro de ventana deslizante (1 semana de datos)
window_size = 7

# Inicializar sesión para la posición actual de la ventana
if "index" not in st.session_state:
    st.session_state.index = window_size

# Crear dos columnas para organizar los gráficos
col1, col2 = st.columns(2)

# Diccionario para los gráficos dinámicos
plotly_containers = {}

# Seleccionar las primeras 6 variables para graficar
variables_a_graficar = df.columns[1:7]  # Evitando la columna de tiempo
for i, var in enumerate(variables_a_graficar):
    if i % 2 == 0:
        plotly_containers[var] = col1.empty()
    else:
        plotly_containers[var] = col2.empty()

# Animación en tiempo real
while True:
    start_idx = max(0, st.session_state.index - window_size)
    end_idx = st.session_state.index

    df_window = df.iloc[start_idx:end_idx]

    for i, var in enumerate(variables_a_graficar):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_window["Tiempo"], y=df_window[var], mode="lines", name=var))
        fig.update_layout(title=f"Evolución de {var}", xaxis_title="Tiempo", yaxis_title=var,
                          xaxis_range=[df_window["Tiempo"].min(), df_window["Tiempo"].max()])

        # Actualizar el gráfico sin generar nuevos elementos con una clave única
        plotly_containers[var].plotly_chart(fig, use_container_width=True, key=f"plot_{var}")

    # Avanzar la ventana
    st.session_state.index = min(st.session_state.index + 1, len(df))

    # Esperar 500ms antes de la siguiente actualización
    time.sleep(0.5)

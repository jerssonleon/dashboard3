import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(layout="wide")

# Título de la aplicación
st.title("Dashboard de Datos de Energía con Plotly")

# Cargar datos reales
df = pd.read_csv('dataset_limpio_carga_laboral.csv')

# Eliminar espacios en los nombres de las columnas
df.columns = df.columns.str.strip()

# Verificar nombres de columnas
st.write("Columnas disponibles en el dataset:", df.columns)

# Crear una nueva columna 'Tiempo' a partir de Year, Month, Day, Hour, Minute
if {'Year', 'Month', 'Day', 'Hour', 'Minute'}.issubset(df.columns):
    df['Tiempo'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour', 'Minute']])
    st.write("Nueva columna 'Tiempo' creada exitosamente.")
else:
    st.write("Advertencia: No se encontraron todas las columnas necesarias para crear 'Tiempo'.")

# Mostrar el DataFrame
st.write("Vista previa de los datos:", df.head())

# Crear dos columnas para organizar los gráficos
col1, col2 = st.columns(2)

# Seleccionar las primeras 5 variables para graficar
variables_a_graficar = df.columns[0:5]

# Diccionario para los gráficos dinámicos
plotly_containers = {}
for i, var in enumerate(variables_a_graficar):
    if i % 2 == 0:
        plotly_containers[var] = col1.empty()
    else:
        plotly_containers[var] = col2.empty()

# Graficar la totalidad de los datos en el año
for var in variables_a_graficar:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Tiempo"], y=df[var], mode="lines", name=var))
    fig.update_layout(title=f"Evolución de {var}", xaxis_title="Tiempo", yaxis_title=var)
    plotly_containers[var].plotly_chart(fig, use_container_width=True)

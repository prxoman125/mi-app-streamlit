import streamlit as st
import pandas as pd
import numpy as np

st.title("Grafica de Tendencias Interactiva")

# 1. Barra deslizable colocada abajo (la declaramos primero para usar su valor)
# Controla la cantidad de dias o puntos a graficar
puntos = st.slider(
    label="Selecciona la cantidad de dias a mostrar en la grafica:",
    min_value=5,
    max_value=100,
    value=30
)

# 2. Generacion de datos aleatorios basados en la seleccion del usuario
# Creamos una secuencia de numeros que simula el comportamiento de una accion o temperatura
np.random.seed(42)
datos_linea = np.random.randn(puntos).cumsum()

# Convertimos los datos a una tabla estructurada
df = pd.DataFrame(
    datos_linea,
    columns=["Valor Actual"]
)

# 3. Mostrar la grafica en la pantalla
# Se dibuja arriba de la barra gracias a la organizacion del codigo de Streamlit
st.line_chart(df)

st.write(f"Mostrando el historico de los ultimos {puntos} dias.")

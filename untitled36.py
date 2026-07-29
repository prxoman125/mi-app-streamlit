import streamlit as st

st.title("🔢 Mi Contador Interactivo")

# 1. Creamos la barra deslizable y guardamos su valor en la variable 'numero'
numero = st.slider(
    label="Desliza para cambiar el número:",
    min_value=1,
    max_value=100,
    value=1  # Valor con el que inicia la barra
)

# 2. Mostramos el número seleccionado abajo de la barra
st.header(f"Número actual: {numero}")

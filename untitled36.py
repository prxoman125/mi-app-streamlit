import streamlit as st
import pandas as pd

st.title("Panel de Analisis Numerico")

# 1. Control del numero principal
numero = st.slider(
    label="Selecciona un numero para analizar:",
    min_value=1,
    max_value=100,
    value=1
)

st.header(f"Numero seleccionado: {numero}")

# 2. Visualizacion grafica del progreso (de 0.0 a 1.0)
st.progress(numero / 100)

# 3. Bloque de analisis matematico simple
st.subheader("Propiedades Matematicas")
col1, col2 = st.columns(2)

with col1:
    # Comprobar si es par o impar
    if numero % 2 == 0:
        st.write("Tipo de numero: Par")
    else:
        st.write("Tipo de numero: Impar")

with col2:
    # Calcular el cuadrado del numero
    cuadrado = numero ** 2
    st.write(f"Su valor al cuadrado es: {cuadrado}")

# 4. Generacion automatica de datos (Tabla de multiplicar)
st.subheader(f"Tabla de Multiplicar del {numero}")

# Creamos una lista de multiplicaciones del 1 al 10
datos_tabla = {
    "Multiplicador": [f"{numero} x {i}" for i in range(1, 11)],
    "Resultado": [numero * i for i in range(1, 11)]
}

# Convertimos los datos en una tabla dinamica de Streamlit
df = pd.DataFrame(datos_tabla)
st.dataframe(df, use_container_width=True)

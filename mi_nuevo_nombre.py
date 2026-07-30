import streamlit as st

# Título de la aplicación
st.title("Sumadora Simple")

st.write("Ingresa dos números a continuación para obtener su suma:")

# Entradas numéricas para el usuario
numero1 = st.number_input("Ingresa el primer número:", value=0.0, step=1.0)
numero2 = st.number_input("Ingresa el segundo número:", value=0.0, step=1.0)

# Botón para realizar el cálculo
if st.button("Sumar"):
    resultado = numero1 + numero2
    # Mostrar el resultado en pantalla
    st.success(f"El resultado de la suma es: **{resultado}**")

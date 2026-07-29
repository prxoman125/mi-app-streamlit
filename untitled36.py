import streamlit as st

st.title("🔢 Mi Contador Interactivo")

# 1. Creamos la variable en la "memoria" de Streamlit si aún no existe
if "contador" not in st.session_state:
    st.session_state.contador = 1  # Empezamos en 1

# 2. Mostramos el número actual en la pantalla en un tamaño grande
st.header(f"Número actual: {st.session_state.contador}")

# 3. Ponemos los botones uno al lado del otro
col1, col2 = st.columns(2)

with col1:
    # Botón de Sumar (solo funciona si no ha pasado de 100)
    if st.button("➕ Sumar"):
        if st.session_state.contador < 100:
            st.session_state.contador += 1
            st.rerun()  # Recarga la página inmediatamente para ver el cambio
        else:
            st.warning("¡Ya llegaste al límite máximo (100)!")

with col2:
    # Botón de Restar (solo funciona si no ha bajado de 1)
    if st.button("➖ Restar"):
        if st.session_state.contador > 1:
            st.session_state.contador -= 1
            st.rerun()  # Recarga la página inmediatamente para ver el cambio
        else:
            st.warning("¡Ya llegaste al límite mínimo (1)!")

import streamlit as st

st.title("🔢 Mi Contador Interactivo")

# 1. Inicializamos el contador en la memoria si no existe
if "contador" not in st.session_state:
    st.session_state.contador = 1

# 2. Mostramos el número actual destacado
st.header(f"Número actual: {st.session_state.contador}")

# 3. NUEVO: Barra deslizable sincronizada que va del 1 al 100
# Usamos 'key="contador"' para amarrarla directamente a la memoria de los botones
st.slider(
    label="Desliza para cambiar el número:",
    min_value=1,
    max_value=100,
    key="contador"
)

st.write("") # Un pequeño espacio en blanco de separación

# 4. Botones de + y - abajo de la barra
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Sumar"):
        if st.session_state.contador < 100:
            st.session_state.contador += 1
            st.rerun()
        else:
            st.warning("¡Ya llegaste al límite máximo (100)!")

with col2:
    if st.button("➖ Restar"):
        if st.session_state.contador > 1:
            st.session_state.contador -= 1
            st.rerun()
        else:
            st.warning("¡Ya llegaste al límite mínimo (1)!")

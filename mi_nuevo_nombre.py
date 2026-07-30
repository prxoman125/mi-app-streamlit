# 6. GENERACIÓN DEL GRÁFICO INTERACTIVO (Trayectorias)
st.subheader("📉 Simulación Visual de las Líneas de Visión (Vista Lateral)")

fig = go.Figure()

# Eje X: de 0 a la distancia configurada
x_trayectoria = np.array([0, distancia])

# Línea del Suelo (¡CORREGIDO AQUÍ! Ahora tiene un arreglo de ceros)
fig.add_trace(go.Scatter(
    x=x_trayectoria, y=np.array([0.0, 0.0]),
    mode='lines', name='Suelo', line=dict(color='green', width=2, dash='dash')
))

# Línea del Láser (Siempre recto horizontal al centro de la diana)
fig.add_trace(go.Scatter(
    x=x_trayectoria, y=[h_laser, h_centro_diana],
    mode='lines', name='Rayo Láser (Eje Horizontal)', line=dict(color='red', width=3)
))

# Línea de la Mira apuntando al objetivo elegido
fig.add_trace(go.Scatter(
    x=x_trayectoria, y=[h_mira_absoluta, h_punto_impacto],
    mode='lines', name='Línea de Visión de la Mira', line=dict(color='blue', width=2, dash='dot')
))

# Dibujar la Diana en el extremo final (Línea vertical que representa sus divisiones)
y_diana_superior = h_centro_diana + radio_diana
y_diana_inferior = h_centro_diana - radio_diana

# Sucesiones/Anillos de la diana (Cada 5 cm de división)
divisiones = np.arange(-radio_diana, radio_diana + 0.01, 0.05)
for div in divisiones:
    fig.add_trace(go.Scatter(
        x=[distancia, distancia], y=[h_centro_diana + div, h_centro_diana + div],
        mode='markers', marker=dict(size=8, color='black'), showlegend=False
    ))

# Cuerpo vertical de la diana
fig.add_trace(go.Scatter(
    x=[distancia, distancia], y=[y_diana_inferior, y_diana_superior],
    mode='lines', name='Cuerpo de la Diana', line=dict(color='black', width=6)
))

# Punto de impacto exacto elegido por el usuario
fig.add_trace(go.Scatter(
    x=[distancia], y=[h_punto_impacto],
    mode='markers', marker=dict(size=12, color='gold', symbol='star'), name='Punto de Apuntado'
))

# Configuración de diseño y escalas del gráfico
fig.update_layout(
    xaxis_title="Distancia Horizontal (Metros)",
    yaxis_title="Altura desde el Suelo (Metros)",
    hovermode="closest",
    height=500,
    legend=dict(orient="h", yanchor="bottom", y=1.12, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

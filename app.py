import streamlit as st
from src.data_loader import load_data
from src.home import show_home
from src.estadisticas import show_statistics
from src.grafics import show_graphics
from src.clustering import show_clustering

# Estilos personalizados para la app médica
st.markdown("""
    <style>
    div.stTabs > div > button {
        color: #ffffff;
        background-color: #007acc;
        border: 1px solid #007acc;
        font-size: 16px;
        font-weight: bold;
    }
    
    div.stTabs > div > button:hover {
        color: #ffffff;
        background-color: #005f99;
        border-color: #005f99;
    }
    
    div.stTabs > div > button[aria-selected="true"] {
        background-color: #005f99;
        color: #ffffff;
        border-color: #005f99;
    }
    
    body {
        background-color: #f0f2f6;
    }

    h1 {
        color: #007acc;
    }

    .stApp {
        background-color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# Título principal de la aplicación
st.title("Aplicación Médica de Clustering")

# Pestañas de navegación
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Home", "📂 Cargar Datos",  "📈 Estadísticas", "📉 Gráficos" ,"📊 Clustering"])

# Página de Home
with tab1:
    show_home()

# Página de Cargar Datos
with tab2:
    st.title("📂 Cargar Datos")
    data = load_data()

# Página de Clustering
with tab3:
    st.title("📈 Estadísticas de las Variables")
    show_statistics(data)
# Página de Estadísticas
with tab4:

    st.title("📉 Gráficos de las Variables")
    show_graphics(data)

# Página de Gráficos
with tab5:
    st.title("📊 lustering de Pacientes")
    show_clustering(data)

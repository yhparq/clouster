import streamlit as st

def show_home():
    st.title("Bienvenido a la Aplicación de Clustering")
    st.write("""
        Esta aplicación está diseñada para realizar clustering en datos cargados por el usuario.
        
        ### Funcionalidades:
        - **Cargar datos**: Puedes subir archivos CSV para analizarlos.
        - **Clustering**: Utiliza algoritmos de clustering para segmentar tus datos.
        
        ### ¿Qué es el Clustering?
        El clustering es una técnica de machine learning que agrupa datos en conjuntos de acuerdo a su similitud. Es ideal para:
        - Segmentación de clientes
        - Análisis de patrones en datos médicos
        - Agrupamiento de imágenes, entre otros.
        
        ### ¿Cómo usar la aplicación?
        1. Ve a la página de **Cargar Datos** para subir tu archivo CSV.
        2. Una vez cargados los datos, puedes ir a la sección de **Clustering** para analizar los datos.
        
        ¡Empieza a cargar tus datos y explorar la segmentación de manera fácil!
    """)

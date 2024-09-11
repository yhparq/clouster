import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def show_graphics(data):
    if data is not None:
        # Seleccionar el tipo de gráfico
        st.write("### Selecciona el tipo de gráfico:")
        chart_type = st.selectbox("Tipo de gráfico", ["Histograma", "Dispersión", "Boxplot"])
        
        # Seleccionar las variables a graficar
        st.write("### Selecciona las variables:")
        variables = data.columns.tolist()
        x_var = st.selectbox("Selecciona la variable para el eje X", variables)
        
        # Algunas gráficas requieren una segunda variable
        y_var = None
        if chart_type in ["Dispersión", "Boxplot"]:
            y_var = st.selectbox("Selecciona la variable para el eje Y", variables)
        
        # Generar gráfico según la selección del usuario
        if chart_type == "Histograma":
            plt.figure(figsize=(10, 6))
            sns.histplot(data[x_var], kde=True)
            plt.title(f"Histograma de {x_var}")
            st.pyplot(plt)
        
        elif chart_type == "Dispersión":
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x=data[x_var], y=data[y_var])
            plt.title(f"Gráfico de dispersión: {x_var} vs {y_var}")
            st.pyplot(plt)
        
        elif chart_type == "Boxplot":
            plt.figure(figsize=(10, 6))
            sns.boxplot(x=data[x_var], y=data[y_var])
            plt.title(f"Boxplot: {x_var} vs {y_var}")
            st.pyplot(plt)
    
    else:
        st.write("Primero carga los datos en la sección 'Cargar Datos' para generar gráficos.")

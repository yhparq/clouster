import os
import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans, DBSCAN
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import numpy as np

# Función para listar modelos ordenados por fecha de modificación
def listar_modelos_guardados(directory='models'):
    """Lista los archivos de modelos en un directorio ordenados por la fecha de modificación"""
    if not os.path.exists(directory):
        os.makedirs(directory)
    modelos = [f for f in os.listdir(directory) if f.endswith('.pkl')]
    modelos_ordenados = sorted(modelos, key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    return modelos_ordenados

# Función para cargar un modelo guardado
def cargar_modelo_guardado(directory='models', modelo_seleccionado=None):
    """Carga un modelo guardado desde el directorio"""
    if modelo_seleccionado:
        model_path = os.path.join(directory, modelo_seleccionado)
        try:
            model = joblib.load(model_path)
            st.success(f"Modelo '{modelo_seleccionado}' cargado correctamente")
            return model
        except Exception as e:
            st.error(f"Error al cargar el modelo: {e}")
            return None
    else:
        st.warning("Por favor, selecciona un modelo guardado.")
        return None

def show_clustering(data):
    if data is None:
        st.warning("Por favor, sube un archivo para empezar el análisis de clustering.")
        return

    # Seleccionar las variables para el clustering
    st.write("### Selecciona las variables para el clustering:")
    variables = data.columns.tolist()
    selected_vars = st.multiselect("Selecciona las variables", variables)

    if len(selected_vars) == 0:
        st.warning("Selecciona al menos una variable para realizar el clustering.")
        return

    # Filtrar solo las columnas numéricas
    cluster_data = data[selected_vars].select_dtypes(include=[float, int])
    
    if cluster_data.empty:
        st.error("Las variables seleccionadas no son numéricas. El clustering requiere datos numéricos.")
        return

    # Seleccionar si crear un nuevo modelo o cargar uno existente
    model_option = st.radio("¿Quieres crear un modelo nuevo o cargar uno existente?", ("Crear Modelo", "Cargar Modelo"))

    if model_option == "Crear Modelo":
        # Seleccionar el tipo de algoritmo de clustering
        st.write("### Selecciona el tipo de clustering:")
        cluster_type = st.selectbox("Algoritmo de clustering", ["K-Means", "DBSCAN"])

        # Mostrar parámetros específicos según el algoritmo seleccionado
        if cluster_type == "K-Means":
            st.write("### Parámetros para K-Means:")
            n_clusters = st.slider("Selecciona el número de clusters", min_value=2, max_value=10, value=3)
            model = KMeans(n_clusters=n_clusters)
            model.fit(cluster_data)
            data['Cluster'] = model.labels_
            centroids = model.cluster_centers_

            # Permitir guardar el modelo entrenado
            if st.button("Guardar modelo K-Means"):
                if not os.path.exists('models'):
                    os.makedirs('models')
                joblib.dump(model, 'models/modelo_kmeans.pkl')
                st.success("Modelo K-Means guardado como 'models/modelo_kmeans.pkl'")

        elif cluster_type == "DBSCAN":
            st.write("### Parámetros para DBSCAN:")
            eps = st.slider("Selecciona el valor de eps", min_value=0.1, max_value=5.0, value=0.5, step=0.1)
            min_samples = st.slider("Selecciona el número mínimo de muestras por cluster", min_value=1, max_value=10, value=5)
            model = DBSCAN(eps=eps, min_samples=min_samples)
            data['Cluster'] = model.fit_predict(cluster_data)
            # DBSCAN puede asignar -1 a puntos considerados como ruido
            data['Cluster'] = data['Cluster'].astype(str)

            # Permitir guardar el modelo entrenado
            if st.button("Guardar modelo DBSCAN"):
                if not os.path.exists('models'):
                    os.makedirs('models')
                joblib.dump(model, 'models/modelo_dbscan.pkl')
                st.success("Modelo DBSCAN guardado como 'models/modelo_dbscan.pkl'")

    elif model_option == "Cargar Modelo":
        # Mostrar un selectbox con los modelos guardados (el último modelo guardado aparece primero)
        modelos_disponibles = listar_modelos_guardados('models')
        modelo_seleccionado = st.selectbox("Selecciona un modelo guardado", modelos_disponibles)

        # Cargar y aplicar el modelo seleccionado
        if modelo_seleccionado:
            model = cargar_modelo_guardado('models', modelo_seleccionado)
            if isinstance(model, KMeans):
                st.write(f"### Usando modelo K-Means cargado con {model.n_clusters} clusters.")
                data['Cluster'] = model.predict(cluster_data)

            elif isinstance(model, DBSCAN):
                st.write("### Usando modelo DBSCAN cargado.")
                data['Cluster'] = model.fit_predict(cluster_data)
                data['Cluster'] = data['Cluster'].astype(str)

            # Predicción con el modelo cargado
            st.write("### Predicción de Clusters:")
            st.write("Puedes introducir nuevos valores para predecir el cluster.")
            inputs = []
            for var in selected_vars:
                val = st.number_input(f"Introduce valor para {var}", value=float(cluster_data[var].mean()))
                inputs.append(val)
            inputs = np.array(inputs).reshape(1, -1)

            if st.button("Predecir Cluster"):
                cluster_pred = model.predict(inputs)
                st.write(f"El nuevo dato fue asignado al **Cluster {cluster_pred[0]}**")

    # Mostrar los resultados del clustering
    st.write("### Resultados del clustering:")
    st.write(data[['Cluster'] + selected_vars].head())

    # Visualizar los clusters si hay dos variables seleccionadas
    if len(selected_vars) == 2:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=data[selected_vars[0]], y=data[selected_vars[1]], hue=data['Cluster'], palette="deep", s=30)

        if model_option == "Crear Modelo" and 'centroids' in locals():
            plt.scatter(centroids[:, 0], centroids[:, 1], c='black', marker='o', s=100, label='Centroides')

        plt.title(f"Clustering usando {selected_vars[0]} y {selected_vars[1]}")
        plt.legend()
        st.pyplot(plt)

    # Interpretación personalizada de los resultados
    st.write("### Interpretación del clustering:")
    if isinstance(model, KMeans):
        st.write(f"El algoritmo K-Means ha agrupado los datos en {model.n_clusters} clusters. Cada cluster representa un grupo de puntos que son similares entre sí en función de las variables seleccionadas.")
    elif isinstance(model, DBSCAN):
        st.write(f"El algoritmo DBSCAN ha detectado clusters basados en la densidad de los puntos. Los puntos que no pertenecen a ningún cluster son considerados como ruido (asignados como -1).")

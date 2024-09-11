import pandas as pd
import streamlit as st

def traducir_tipo(tipo):
    """Traducir los tipos de datos a términos en español"""
    if pd.api.types.is_integer_dtype(tipo):
        return "Entero"
    elif pd.api.types.is_float_dtype(tipo):
        return "Decimal"
    elif pd.api.types.is_object_dtype(tipo):
        return "Cadena"
    elif pd.api.types.is_datetime64_any_dtype(tipo):
        return "Fecha"
    else:
        return "Otro"

def traducir_estadisticas(df):
    """Traducir nombres de estadísticas básicas a español"""
    df = df.rename(index={
        "count": "Conteo",
        "mean": "Promedio",
        "std": "Desviación Estándar",
        "min": "Mínimo",
        "25%": "25%",
        "50%": "Mediana",
        "75%": "75%",
        "max": "Máximo"
    })
    return df

def show_statistics(data):
    if data is not None:
        
        # Mostrar la cantidad total de datos
        st.write(f"### Cantidad total de datos: {len(data)} registros")

        st.write("### 1. Cuadro de Variables y su Tipo:")
        
        # Obtener los tipos de variables traducidos al español
        variable_types = pd.DataFrame(data.dtypes, columns=["Tipo de Variable"])
        variable_types["Tipo de Variable"] = variable_types["Tipo de Variable"].apply(traducir_tipo)
        
        # Estilizar el cuadro de tipos de variables
        st.write(variable_types.style.set_caption("Tabla 1: Tipos de Variables").set_table_styles(
            [{'selector': 'thead th', 'props': [('background-color', '#dbeafe'), ('color', '#0d47a1'), ('font-weight', 'bold')]}]
        ))

        st.write("### 2. Estadísticas Básicas de las Variables:")
        
        # Mostrar estadísticas básicas con los nombres en español
        statistics = data.describe().T  # Transpuesta para mejor visualización
        statistics_traducidas = traducir_estadisticas(statistics)
        
        # Estilizar la tabla de estadísticas
        st.write(statistics_traducidas.style.set_caption("Tabla 2: Estadísticas Básicas").set_table_styles(
            [{'selector': 'thead th', 'props': [('background-color', '#d1fae5'), ('color', '#065f46'), ('font-weight', 'bold')]}]
        ))
    else:
        st.write("Por favor, carga los datos en la sección 'Cargar Datos' para ver las estadísticas.")

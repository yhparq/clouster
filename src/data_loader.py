import pandas as pd
import streamlit as st

def load_data():
    uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Datos cargados:")
        st.dataframe(df)
        return df
    else:
        st.write("Por favor sube un archivo CSV.")
        return None

import streamlit as st
from streamlit_option_menu import option_menu
# import snowflake.connector
import pandas as pd
from PIL import Image
import plotly.express as px
import numpy as np
# import base64
import time
# import altair as alt
import streamlit.components.v1 as components
import plotly.express as px 
import plotly.graph_objects as go

st.set_page_config(layout='wide')

# carga de archivos CSV
#------------------------------------------------------------------------------------------
df_empleo_aviso = pd.read_csv("EEPP/df_concursos_eepp_Aviso.csv", sep=";", encoding="utf-8")
df_empleo_postulacion = pd.read_csv("EEPP/df_concursos_eepp_Postulacion en linea.csv", sep=";", encoding="utf-8")
df_empleo=pd.concat([df_empleo_aviso,df_empleo_postulacion],axis=0)
organismos=df_empleo["Organismo"].unique()
#------------------------------------------------------------------------------------------



# This function sets the logo and company name inside the sidebar
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="./imagenes/logo.png", width=200, height=100)
st.image(my_logo)

# Set Page Header
st.header("Comparador de datos")
# Set custom CSS for hr element
st.markdown(
    """
        <style>
            hr {
                margin-top: 0.0rem;
                margin-bottom: 0.5rem;
                height: 3px;
                background-color: #333;
                border: none;
            }
        </style>
    """,
    unsafe_allow_html=True,
)

# Add horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

# define si se ven los ejes Y
visible_y_axis=True

with st.container():
    seleccion=st.selectbox("Selecciona el tipo de información a comparar",["Por región","Por organismo"])
    region=["Arica y Parinacota","Tarapacá","Antofagasta","Atacama","Coquimbo","Valparaíso","Metropolitana","O’Higgins","Maule","Ñuble","Biobío","Araucanía","Los Ríos","Los Lagos","Aysén","Magallanes"]

    tipo_info=["Convocatorias EEPP","Postulaciones EEPP","Concursos ADP","Nombramientos ADP","Postulaciones ADP","Prácticas Ofrecidas","Postulaciones Prácticas Chile","Convocatorias Directores Escuelas","Postulaciones Directores Escuelas","Capacitaciones","Postulaciones de Mujeres en ADP","Postulaciones Mujeres n EEPP"]
    tipo_info_organismos=["Convocatorias EEPP","Postulaciones EEPP","Concursos ADP","Nombramientos ADP","Postulaciones ADP","Prácticas Ofrecidas","Postulaciones Prácticas Chile","Capacitaciones","Postulaciones de Mujeres en ADP","Postulaciones Mujeres n EEPP"]
    periodo_años=range(2014,2025)
    if seleccion=="Por región":
        
        st.subheader("Seleccionar regiones a comparar")
        col1,col2=st.columns(2)
        with col1:
            select_region1=st.selectbox("Selecciona región N°1",region)
        with col2:
            select_region2=st.selectbox("Selecciona región N°2",region,placeholder="Seleccionar región")
        if select_region1==select_region2:
            st.error("No se pueden seleccionar dos regiones iguales")
            st.stop()
        
        col1,col2,col3=st.columns(3)
        with col1:
            #st.write("Selecciona el tipo de información a comparar")
            tipo=st.selectbox("Selecciona el tipo de información a comparar",tipo_info)
        with col2:
            #st.write("Selecciona año")
            Año=st.selectbox("Selecciona año",periodo_años)
        #fecha2=st.date_input("Fecha 2",value=pd.to_datetime("2021-09-01"))
        with col3:
            #st.write("Selecciona como quieres ver el dato")
            grafico=st.selectbox("Selecciona como quieres ver el dato",["Gráfico","Tabla"])
    
    if seleccion=="Por organismo":
        
        st.subheader("Seleccionar organismos a comparar")
        col1,col2=st.columns(2)
        with col1:
            select_organismo1=st.selectbox("Selecciona organismo N°1",organismos)
        with col2:
            select_organismo2=st.selectbox("Selecciona organismo N°2",organismos)
        if select_organismo1==select_organismo2:
            st.error("No se pueden seleccionar dos organismos iguales")
            st.stop()
        
        col1,col2,col3=st.columns(3)
        with col1:
            st.write("Selecciona el tipo de información a comparar")
            tipo=st.selectbox("Tipo de información",tipo_info_organismos)
        with col2:
            st.write("Selecciona año")
            Año=st.selectbox("Año",periodo_años)
        #fecha2=st.date_input("Fecha 2",value=pd.to_datetime("2021-09-01"))
        with col3:
            st.write("Selecciona como quieres ver el dato")
            grafico=st.selectbox("Tipo",["Gráfico","Tabla"])
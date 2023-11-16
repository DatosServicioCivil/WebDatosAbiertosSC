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

# This function sets the logo and company name inside the sidebar
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="./imagenes/logo.png", width=200, height=100)
st.image(my_logo)

# Set Page Header
st.header("Gestión de Personas en el Estado")
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
    
#https://framework.digital.gob.cl/colors.html
color_line='#2D717C'
color_bar='#6633CC'

with st.sidebar:
    a=st.radio('Gestión de Personas: ',['Normas de Gestión de Personas','Capacitación en el Estado','Integridad','Prevención de Maltrato y Acoso Laboral','Egresos ADP'])

def select_servicio(df, option):
    if option_3 == 'Todos':
        unique_servicio = df['Servicio'].unique()
    else:
        unique_servicio = df.query(f'Ministerio == "{option}"')['Servicio'].unique()
        Servicio = pd.DataFrame({'Servicio': unique_servicio})
        nuevo_registro = pd.DataFrame({'Servicio': ['Todos']})
        Servicio = pd.concat([nuevo_registro, Servicio]).Servicio.tolist()

    return Servicio



if a=='Capacitación en el Estado':
    import glob

    # consolidar los archivos csv en un solo dataframe
    # Ruta de los archivos CSV (ajusta la ruta según tu directorio)
    ruta_archivos = 'GestionPersonas/actividades_ejecutadas_sispubli*.csv'
    # Lista para almacenar los DataFrames de cada archivo
    dataframes = []
    # Itera sobre los archivos que coinciden con el patrón
    for archivo in glob.glob(ruta_archivos):
        # Lee cada archivo CSV y lo agrega a la lista
        df = pd.read_csv(archivo, sep=';')
        dataframes.append(df)
    # Combina todos los DataFrames en uno solo
    df_actividades_ejecutadas_sispubli = pd.concat(dataframes, ignore_index=True)
    df_actividades_ejecutadas_sispubli = df_actividades_ejecutadas_sispubli.rename(columns={'Nombre de Servicio': 'Servicio'})


    unique_ministerios = df_actividades_ejecutadas_sispubli.Ministerio.unique()
    Ministerios = pd.DataFrame({'Ministerio': unique_ministerios})
    nuevo_registro = pd.DataFrame({'Ministerio': ['Todos']})
    Ministerios = pd.concat([nuevo_registro, Ministerios])
    Ministerios = Ministerios.reset_index(drop=True)
    Ministerios = Ministerios['Ministerio'].tolist()

    unique_modalidad = df_actividades_ejecutadas_sispubli.Modalidad_de_Compra.unique()
    Modalidad_Compra = pd.DataFrame({'Modalidad_Compra': unique_modalidad})
    nuevo_registro = pd.DataFrame({'Modalidad_Compra': ['Todos']})
    Modalidad_Compra = pd.concat([nuevo_registro, Modalidad_Compra])
    Modalidad_Compra = Modalidad_Compra.reset_index(drop=True)
    Modalidad_Compra = Modalidad_Compra['Modalidad_Compra'].tolist()

    unique_metodologia = df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje.unique()
    Metodologia = pd.DataFrame({'Metodología_de_Aprendizaje': unique_metodologia})
    nuevo_registro = pd.DataFrame({'Metodología_de_Aprendizaje': ['Todos']})
    Metodologia = pd.concat([nuevo_registro, Metodologia])
    Metodologia = Metodologia.reset_index(drop=True)
    Metodologia = Metodologia['Metodología_de_Aprendizaje'].tolist()
    


    #filtros
    with st.container():
        col1,col2,col3,col4=st.columns(4,gap="large")
        with col1:
           option_1 = st.selectbox('Ministerio',Ministerios)
        with col2:
           option_2 = st.selectbox('Servicio',select_servicio(df_actividades_ejecutadas_sispubli,option_1))
        with col3:
            option_3=st.selectbox('Modalidad de Compra',Modalidad_Compra)
        with col4:
            option_4=st.selectbox('Metodología de Aprendizaje',Metodologia)

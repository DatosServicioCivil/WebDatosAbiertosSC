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
        if option == 'Todos':
            Servicio = df['Servicio'].unique()
        else:
            unique_servicio = df.query(f'Ministerio == "{option}"')['Servicio'].unique()
            Servicio = pd.DataFrame({'Servicio': unique_servicio})
            nuevo_registro = pd.DataFrame({'Servicio': ['Todos']})
            Servicio = pd.concat([nuevo_registro, Servicio]).Servicio.tolist()

        return Servicio


if a=='Capacitación en el Estado':
    import glob
    st.title('Capacitación en el Estado')
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
    df_actividades_ejecutadas_sispubli = df_actividades_ejecutadas_sispubli.rename(
    columns={'Nombre de Servicio': 'Servicio','Número correlativo':'id_actividad'})


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

    

    Actividades=df_actividades_ejecutadas_sispubli.groupby('Año').agg({'id_actividad':'count'}).reset_index()
    Actividades=Actividades.rename(columns={'id_actividad':'Actividades'})
    Inversion=df_actividades_ejecutadas_sispubli.groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
    Inversion=Inversion.rename(columns={'Gasto_monto_Item001':'Inversion'})
    

    graf1=px.bar(Actividades,x='Año',y='Actividades',title='<b>Cantidad de capacitaciones realizadas por año</b>',color_discrete_sequence=[color_bar]).\
                 update_yaxes(visible=visible_y_axis,title_text=None).\
                      update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    graf1.update_layout(yaxis_tickformat='.0f')

    graf2=px.line(Inversion,x='Año',y='Inversion',title='<b>Inversión en capacitación realizadas por año [MM$]</b>').\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    graf2.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_line)
    graf2.update_layout(yaxis_tickformat='.0f')

    with st.container():
        col1,col2=st.columns(2,gap='small')
        with col1:    
            st.plotly_chart(graf1,use_container_width=True)
        with col2:
            st.plotly_chart(graf2,use_container_width=True)


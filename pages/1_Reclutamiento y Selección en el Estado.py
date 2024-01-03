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
import pyarrow.parquet as pq

st.set_page_config(layout='wide')

# This function sets the logo and company name inside the sidebar
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="./imagenes/logo.png", width=150, height=150)
st.image(my_logo)

# Set Page Header
st.header("Reclutamiento y Selección de Personas en el Estado")
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
color_line='#4A4A4A' #dark grey
color_line_2='#E0701E' #orange
color_line_3='#006FB3' #blue
color_line_4='#A7ED74' #verde montaña
color_bar='#006FB3' #blue
color_bar_2='#0A132D' #dark blue
color_5="#B2FFFF" #celeste
color_6="#7CB2B2" #celeste orcuro
# Asignar colores de acuerdo a una paleta de colores a cada sexo
sexo_color_map = {'Mujeres': 'orange', 'Hombres': 'blue','Todos':'grey'}  # Mapeo de colores por sexo
sexo_color_map_2 = {'Mujer': 'orange', 'Hombre': 'blue','Todos':'grey'}  # Mapeo de colores por sexo
tipo_postulacion_color_map={'Aviso': 'orange', 'Postulacion en linea': 'blue'}# Mapeo de colores por tipo de postulacion
tipo_vacante_color_map={'Aviso': 'orange', 'Postulacion en linea': 'dark grey'}# Mapeo de colores por tipo de postulacion
estados_edu_color_map={'Nombrado': color_line_4, 'Desierto': color_6,'Anulado':'red','En Proceso':'pink'}# Mapeo de colores por tipo de postulacion
#estado_color_map={'Nombrado': 'orange', 'Postulacion en linea': 'blue'}# Mapeo de colores por tipo de postulacion

sexo_list = ['Todos','Mujer','Hombre']  # Lista de sexos

all_region=pd.read_excel('Regiones/all_region_values.xlsx',sheet_name='Sheet1')

#-------------------------------------------------------------------------------------------------------------
# carga datos adp
#-------------------------------------------------------------------------------------------------------------
#-----------------concursos adp
#-------------------------------------------------------------------------------------------------------------
df_concursos=pd.read_csv('ADP/df_concursos.csv',sep=';',encoding='utf-8')
#df_concursos=pq.read_table('ADP/df_concursos.parquet').to_pandas()
df_concursos=pd.merge(df_concursos,all_region,how='left',on='Region')
#-------------------------------------------------------------------------------------------------------------
#-----------------postulaciones adp
#-------------------------------------------------------------------------------------------------------------

@st.cache_data
def df_post_adp():
    df_post_adp_1=pq.read_table('ADP/df_postulaciones_adp_1.parquet').to_pandas()
    df_post_adp_2=pq.read_table('ADP/df_postulaciones_adp_2.parquet').to_pandas()
    df_post_adp_3=pq.read_table('ADP/df_postulaciones_adp_3.parquet').to_pandas()
    df_post_adp_4=pq.read_table('ADP/df_postulaciones_adp_4.parquet').to_pandas()
    df_postulaciones_adp=pd.concat([df_post_adp_1,df_post_adp_2,df_post_adp_3,df_post_adp_4])
    return df_postulaciones_adp

@st.cache_data
def tb_postulaciones_adp():
    tb_post_adp=pq.read_table('ADP/tb_postulaciones_adp.parquet').to_pandas()
    return tb_post_adp

@st.cache_data
def tabla_nombramientos_adp():
    tb_1=pq.read_table('ADP/tb_nombramientos_adp.parquet').to_pandas()
    tb_1.query('Año>1900',inplace=True)
    tb_nombramientos_adp=tb_1
    return tb_nombramientos_adp

@st.cache_data
def df_conc_ep():
    df_1=pq.read_table('EEPP/df_concursos_eepp_Aviso.parquet').to_pandas()
    df_2=pq.read_table('EEPP/df_concursos_eepp_Postulacion en linea.parquet').to_pandas()
    df_conc_ep=pd.concat([df_1,df_2])
    return df_conc_ep



unique_niveles = df_concursos['Nivel'].unique()
Nivel = pd.DataFrame({'Nivel': unique_niveles})
nuevo_registro = pd.DataFrame({'Nivel': ['Todos']})
Nivel = pd.concat([nuevo_registro, Nivel])
Nivel = Nivel.reset_index(drop=True)
Nivel = Nivel['Nivel'].tolist()

unique_ministerios = df_concursos['Ministerio'].unique()
Ministerios = pd.DataFrame({'Ministerio': unique_ministerios})
nuevo_registro = pd.DataFrame({'Ministerio': ['Todos']})
Ministerios = pd.concat([nuevo_registro, Ministerios])
Ministerios = Ministerios.reset_index(drop=True)
Ministerios = Ministerios['Ministerio'].tolist()

unique_region = df_concursos['Region_Homologada'].unique()
Region = pd.DataFrame({'Region': unique_region})
nuevo_registro = pd.DataFrame({'Region': ['Todos']})
Region = pd.concat([nuevo_registro, Region])
Region = Region.reset_index(drop=True)
Region = Region['Region'].tolist()

def select_servicio(df_concursos, option_3):
    if option_3 == 'Todos':
        unique_servicio = df_concursos['Servicio'].unique()
    else:
        unique_servicio = df_concursos.query(f'Ministerio == "{option_3}"')['Servicio'].unique()
    Servicio = pd.DataFrame({'Servicio': unique_servicio})
    nuevo_registro = pd.DataFrame({'Servicio': ['Todos']})
    Servicio = pd.concat([nuevo_registro, Servicio]).Servicio.tolist()

    return Servicio
    

def finalizado(Estado):
    if  Estado=='Nombrado' or Estado=='Desierto':
        return 1  
    else:
        return 0
    
def Fecha_Finalizado (Finalizado,Estado, Fecha_Nombramiento, Fecha_Desierto):
    if Finalizado==1 and Estado=='Nombrado':
        return Fecha_Nombramiento
    elif Finalizado==1 and Estado=='Desierto':
        return Fecha_Desierto
    else:
        return None

df_concursos['Finalizado']=df_concursos['Estado'].apply(finalizado) 
df_concursos['Fecha_Finalizado']=df_concursos.apply(lambda x: Fecha_Finalizado(x['Finalizado'],x['Estado'],x['Fecha_Nombramiento'],x['Fecha_Desierto']),axis=1)  
df_concursos['Year_Finalizado']=pd.to_datetime(df_concursos['Fecha_Finalizado']).dt.year
df_concursos['Year_Nombramiento']=pd.to_datetime(df_concursos['Fecha_Nombramiento']).dt.year


with st.sidebar:
    a=st.radio('Reclutamiento y Selección: ',['Alta Dirección Pública','Empleo Público','Directores para Chile','Prácticas Chile'])

if a=='Alta Dirección Pública':
    date=df_concursos.FechaActualizacion.max()#.strftime('%d/%m/%Y')
    with st.container():
        st.title('Estadísticas ADP')
        st.text(f'Fecha Actualización: {date}')
        #st.subheader(date)
        seleccion_adp=st.radio('Seleccionar: ',["Concursos", "Postulaciones","Nombramientos"],horizontal=True)
if a=='Empleo Público':
    with st.container():
       seleccion_eepp=st.radio('Seleccionar: ',["Convocatorias", "Postulaciones","Seleccionados"],horizontal=True)
if a=='Prácticas Chile':
    with st.container():
       seleccion_pch=st.radio('Seleccionar: ',["Convocatorias", "Postulaciones","Seleccionados"],horizontal=True)
if a=='Directores para Chile':
    with st.container():
       seleccion_dee=st.radio('Seleccionar: ',["Convocatorias", "Postulaciones","Seleccionados"],horizontal=True)


if a=='Alta Dirección Pública':
    if seleccion_adp=='Concursos':
        with st.container():
            col1,col2,col3,col4=st.columns(4,gap="large")
            with col1:
                option_1 = st.selectbox('Nivel Jerárquico',Nivel)
            with col2:
                option_2 = st.selectbox('Región',Region)
            with col3:
                option_3 = st.selectbox('Ministerio',Ministerios)
            with col4:
                option_4 = st.selectbox('Servicio',select_servicio(df_concursos,option_3))

    # para 4 variables que toman 2 valores las combinaciones son 16

        if option_1=='Todos' and option_2=='Todos' and option_3=='Todos' and option_4=='Todos': #1
            publicaciones=df_concursos.groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
            Nominas=df_concursos.query('Nomina==1').groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
            dias_concurso=df_concursos.query('Nomina==1').groupby('Year_Nomina').agg({'Duracion_Concurso':'mean'}).reset_index()
            desiertos=df_concursos.query('Desierto==1').groupby('Year_Desierto').agg({'CD_Concurso':'count'}).reset_index()
            finalizados=df_concursos.query('Finalizado==1').groupby('Year_Finalizado').agg({'CD_Concurso':'count'}).reset_index()
            nombramientos=df_concursos.query('Nombrado==1').groupby('Year_Nombramiento').agg({'CD_Concurso':'count'}).reset_index()
        if option_1=='Todos' and option_2!='Todos' and option_3=='Todos'and option_4=='Todos': #2
            publicaciones=df_concursos[(df_concursos.Region_Homologada==option_2)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
            Nominas=df_concursos.query('Nomina==1')[(df_concursos.Region_Homologada==option_2)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
            dias_concurso=df_concursos.query('Nomina==1')[(df_concursos.Region_Homologada==option_2)].groupby('Year_Nomina').agg({'Duracion_Concurso':'mean'}).reset_index()
            desiertos=df_concursos.query('Desierto==1')[(df_concursos.Region_Homologada==option_2)].groupby('Year_Desierto').agg({'CD_Concurso':'count'}).reset_index()
            finalizados=df_concursos.query('Finalizado==1')[(df_concursos.Region_Homologada==option_2)].groupby('Year_Finalizado').agg({'CD_Concurso':'count'}).reset_index()
            nombramientos=df_concursos.query('Nombrado==1')[(df_concursos.Region_Homologada==option_2)].groupby('Year_Nombramiento').agg({'CD_Concurso':'count'}).reset_index()
        if option_1=='Todos' and option_2!='Todos' and option_3!='Todos' and option_4=='Todos': #3
            publicaciones=df_concursos[(df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()    
            Nominas=df_concursos.query('Nomina==1')[(df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()    
            dias_concurso=df_concursos.query('Nomina==1')[(df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3)].groupby('Year_Nomina').agg({'Duracion_Concurso':'mean'}).reset_index()
            desiertos=df_concursos.query('Desierto==1')[(df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3)].groupby('Year_Desierto').agg({'CD_Concurso':'count'}).reset_index()
            finalizados=df_concursos.query('Finalizado==1')[(df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3)].groupby('Year_Finalizado').agg({'CD_Concurso':'count'}).reset_index()
            nombramientos=df_concursos.query('Nombrado==1')[(df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3)].groupby('Year_Nombramiento').agg({'CD_Concurso':'count'}).reset_index()
        if option_1=='Todos' and option_2!='Todos' and option_3!='Todos' and option_4!='Todos': #4
            publicaciones=df_concursos[(df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()    
            Nominas=df_concursos.query('Nomina==1')[(df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()    
            dias_concurso=df_concursos.query('Nomina==1')[(df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'Duracion_Concurso':'mean'}).reset_index()
            desiertos=df_concursos.query('Desierto==1')[(df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Desierto').agg({'CD_Concurso':'count'}).reset_index()
            finalizados=df_concursos.query('Finalizado==1')[(df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Finalizado').agg({'CD_Concurso':'count'}).reset_index()
            nombramientos=df_concursos.query('Nombrado==1')[(df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Nombramiento').agg({'CD_Concurso':'count'}).reset_index()
        if option_1!='Todos' and option_2=='Todos' and option_3=='Todos' and option_4=='Todos': #5
            publicaciones=df_concursos[(df_concursos.Nivel==option_1)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
            Nominas=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
            dias_concurso=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1)].groupby('Year_Nomina').agg({'Duracion_Concurso':'mean'}).reset_index()
            desiertos=df_concursos.query('Desierto==1')[(df_concursos.Nivel==option_1)].groupby('Year_Desierto').agg({'CD_Concurso':'count'}).reset_index()
            finalizados=df_concursos.query('Finalizado==1')[(df_concursos.Nivel==option_1)].groupby('Year_Finalizado').agg({'CD_Concurso':'count'}).reset_index()
            nombramientos=df_concursos.query('Nombrado==1')[(df_concursos.Nivel==option_1)].groupby('Year_Nombramiento').agg({'CD_Concurso':'count'}).reset_index()
        if option_1!='Todos' and option_2!='Todos' and option_3=='Todos' and option_4=='Todos': #6
            publicaciones=df_concursos[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
            Nominas=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
            dias_concurso=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2)].groupby('Year_Nomina').agg({'Duracion_Concurso':'mean'}).reset_index()
            desiertos=df_concursos.query('Desierto==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2)].groupby('Year_Desierto').agg({'CD_Concurso':'count'}).reset_index()
            finalizados=df_concursos.query('Finalizado==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2)].groupby('Year_Finalizado').agg({'CD_Concurso':'count'}).reset_index()
            nombramientos=df_concursos.query('Nombrado==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2)].groupby('Year_Nombramiento').agg({'CD_Concurso':'count'}).reset_index()
        if option_1!='Todos' and option_2!='Todos' and option_3!='Todos' and option_4=='Todos': #7
            publicaciones=df_concursos[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
            Nominas=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
            dias_concurso=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3)].groupby('Year_Nomina').agg({'Duracion_Concurso':'mean'}).reset_index()
            desiertos=df_concursos.query('Desierto==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3)].groupby('Year_Desierto').agg({'CD_Concurso':'count'}).reset_index()
            finalizados=df_concursos.query('Finalizado==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3)].groupby('Year_Finalizado').agg({'CD_Concurso':'count'}).reset_index()
            nombramientos=df_concursos.query('Nombrado==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3)].groupby('Year_Nombramiento').agg({'CD_Concurso':'count'}).reset_index()
        if option_1!='Todos' and option_2!='Todos' and option_3!='Todos' and option_4!='Todos': #8
            publicaciones=df_concursos[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
            Nominas=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
            dias_concurso=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'Duracion_Concurso':'mean'}).reset_index()
            desiertos=df_concursos.query('Desierto==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Desierto').agg({'CD_Concurso':'count'}).reset_index()
            finalizados=df_concursos.query('Finalizado==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Finalizado').agg({'CD_Concurso':'count'}).reset_index()
            nombramientos=df_concursos.query('Nombrado==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Nombramiento').agg({'CD_Concurso':'count'}).reset_index()
        if option_1=='Todos' and option_2=='Todos' and option_3!='Todos' and option_4!='Todos': #9
            publicaciones=df_concursos[(df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
            Nominas=df_concursos.query('Nomina==1')[(df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
            dias_concurso=df_concursos.query('Nomina==1')[(df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'Duracion_Concurso':'mean'}).reset_index()
            desiertos=df_concursos.query('Desierto==1')[(df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Desierto').agg({'CD_Concurso':'count'}).reset_index()
            finalizados=df_concursos.query('Finalizado==1')[(df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Finalizado').agg({'CD_Concurso':'count'}).reset_index()
            nombramientos=df_concursos.query('Nombrado==1')[(df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Nombramiento').agg({'CD_Concurso':'count'}).reset_index()
        if option_1!='Todos' and option_2=='Todos' and option_3!='Todos' and option_4!='Todos': #10
            publicaciones=df_concursos[(df_concursos.Nivel==option_1) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
            Nominas=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
            dias_concurso=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'Duracion_Concurso':'mean'}).reset_index()
            desiertos=df_concursos.query('Desierto==1')[(df_concursos.Nivel==option_1) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Desierto').agg({'CD_Concurso':'count'}).reset_index()
            finalizados=df_concursos.query('Finalizado==1')[(df_concursos.Nivel==option_1) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Finalizado').agg({'CD_Concurso':'count'}).reset_index()
            nombramientos=df_concursos.query('Nombrado==1')[(df_concursos.Nivel==option_1) & (df_concursos.Ministerio==option_3) & (df_concursos.Servicio==option_4)].groupby('Year_Nombramiento').agg({'CD_Concurso':'count'}).reset_index()
        if option_1=='Todos' and option_2=='Todos' and option_3=='Todos' and option_4!='Todos': #11
            publicaciones=df_concursos[(df_concursos.Servicio==option_4)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
            Nominas=df_concursos.query('Nomina==1')[(df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
            dias_concurso=df_concursos.query('Nomina==1')[(df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'Duracion_Concurso':'mean'}).reset_index()
            desiertos=df_concursos.query('Desierto==1')[(df_concursos.Servicio==option_4)].groupby('Year_Desierto').agg({'CD_Concurso':'count'}).reset_index()
            finalizados=df_concursos.query('Finalizado==1')[(df_concursos.Servicio==option_4)].groupby('Year_Finalizado').agg({'CD_Concurso':'count'}).reset_index()
            nombramientos=df_concursos.query('Nombrado==1')[(df_concursos.Servicio==option_4)].groupby('Year_Nombramiento').agg({'CD_Concurso':'count'}).reset_index()
        if option_1!='Todos' and option_2!='Todos' and option_3=='Todos' and option_4!='Todos': #12
            publicaciones=df_concursos[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Servicio==option_4)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
            Nominas=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
            dias_concurso=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'Duracion_Concurso':'mean'}).reset_index()
            desiertos=df_concursos.query('Desierto==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Servicio==option_4)].groupby('Year_Desierto').agg({'CD_Concurso':'count'}).reset_index()
            finalizados=df_concursos.query('Finalizado==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Servicio==option_4)].groupby('Year_Finalizado').agg({'CD_Concurso':'count'}).reset_index()
            nombramientos=df_concursos.query('Nombrado==1')[(df_concursos.Nivel==option_1) & (df_concursos.Region_Homologada==option_2) & (df_concursos.Servicio==option_4)].groupby('Year_Nombramiento').agg({'CD_Concurso':'count'}).reset_index()
        if option_1=='Todos' and option_2=='Todos' and option_3!='Todos' and option_4=='Todos': #13
            publicaciones=df_concursos[(df_concursos.Ministerio==option_3)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
            Nominas=df_concursos.query('Nomina==1')[(df_concursos.Ministerio==option_3)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
            dias_concurso=df_concursos.query('Nomina==1')[(df_concursos.Ministerio==option_3)].groupby('Year_Nomina').agg({'Duracion_Concurso':'mean'}).reset_index()
            desiertos=df_concursos.query('Desierto==1')[(df_concursos.Ministerio==option_3)].groupby('Year_Desierto').agg({'CD_Concurso':'count'}).reset_index()
            finalizados=df_concursos.query('Finalizado==1')[(df_concursos.Ministerio==option_3)].groupby('Year_Finalizado').agg({'CD_Concurso':'count'}).reset_index()
            nombramientos=df_concursos.query('Nombrado==1')[(df_concursos.Ministerio==option_3)].groupby('Year_Nombramiento').agg({'CD_Concurso':'count'}).reset_index()
        if option_1=='Todos' and option_2!='Todos' and option_3=='Todos' and option_4!='Todos': #14
            publicaciones=df_concursos[(df_concursos.Region_Homologada==option_2) & (df_concursos.Servicio==option_4)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
            Nominas=df_concursos.query('Nomina==1')[(df_concursos.Region_Homologada==option_2) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
            dias_concurso=df_concursos.query('Nomina==1')[(df_concursos.Region_Homologada==option_2) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'Duracion_Concurso':'mean'}).reset_index()
            desiertos=df_concursos.query('Desierto==1')[(df_concursos.Region_Homologada==option_2) & (df_concursos.Servicio==option_4)].groupby('Year_Desierto').agg({'CD_Concurso':'count'}).reset_index()
            finalizados=df_concursos.query('Finalizado==1')[(df_concursos.Region_Homologada==option_2) & (df_concursos.Servicio==option_4)].groupby('Year_Finalizado').agg({'CD_Concurso':'count'}).reset_index()
            nombramientos=df_concursos.query('Nombrado==1')[(df_concursos.Region_Homologada==option_2) & (df_concursos.Servicio==option_4)].groupby('Year_Nombramiento').agg({'CD_Concurso':'count'}).reset_index()
        if option_1!='Todos' and option_2=='Todos' and option_3=='Todos' and option_4!='Todos': #15
            publicaciones=df_concursos[(df_concursos.Nivel==option_1) & (df_concursos.Servicio==option_4)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
            Nominas=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
            dias_concurso=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Servicio==option_4)].groupby('Year_Nomina').agg({'Duracion_Concurso':'mean'}).reset_index()
            desiertos=df_concursos.query('Desierto==1')[(df_concursos.Nivel==option_1) & (df_concursos.Servicio==option_4)].groupby('Year_Desierto').agg({'CD_Concurso':'count'}).reset_index()
            finalizados=df_concursos.query('Finalizado==1')[(df_concursos.Nivel==option_1) & (df_concursos.Servicio==option_4)].groupby('Year_Finalizado').agg({'CD_Concurso':'count'}).reset_index()
            nombramientos=df_concursos.query('Nombrado==1')[(df_concursos.Nivel==option_1) & (df_concursos.Servicio==option_4)].groupby('Year_Nombramiento').agg({'CD_Concurso':'count'}).reset_index()
        if option_1!='Todos' and option_2=='Todos' and option_3!='Todos' and option_4=='Todos': #16
            publicaciones=df_concursos[(df_concursos.Nivel==option_1) & (df_concursos.Ministerio==option_3)].groupby('Year_Convocatoria').agg({'CD_Concurso':'count'}).reset_index()
            Nominas=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Ministerio==option_3)].groupby('Year_Nomina').agg({'CD_Concurso':'count'}).reset_index()
            dias_concurso=df_concursos.query('Nomina==1')[(df_concursos.Nivel==option_1) & (df_concursos.Ministerio==option_3)].groupby('Year_Nomina').agg({'Duracion_Concurso':'mean'}).reset_index()
            desiertos=df_concursos.query('Desierto==1')[(df_concursos.Nivel==option_1) & (df_concursos.Ministerio==option_3)].groupby('Year_Desierto').agg({'CD_Concurso':'count'}).reset_index()
            finalizados=df_concursos.query('Finalizado==1')[(df_concursos.Nivel==option_1) & (df_concursos.Ministerio==option_3)].groupby('Year_Finalizado').agg({'CD_Concurso':'count'}).reset_index()
            nombramientos=df_concursos.query('Nombrado==1')[(df_concursos.Nivel==option_1) & (df_concursos.Ministerio==option_3)].groupby('Year_Nombramiento').agg({'CD_Concurso':'count'}).reset_index()

    
        publicaciones=publicaciones.rename(columns={'CD_Concurso': 'Concursos','Year_Convocatoria':'Año'})
        Nominas=Nominas.rename(columns={'CD_Concurso': 'Concursos','Year_Nomina':'Año'})
        dias_concurso=dias_concurso.rename(columns={'Duracion_Concurso': 'Dias','Year_Nomina':'Año'})
        desiertos=desiertos.rename(columns={'CD_Concurso': 'Concursos','Year_Desierto':'Año'})
        finalizados=finalizados.rename(columns={'CD_Concurso': 'Concursos','Year_Finalizado':'Año'})
        nombramientos=nombramientos.rename(columns={'CD_Concurso': 'Concursos','Year_Nombramiento':'Año'})

        finalizados=pd.merge(finalizados,desiertos, how='left', on='Año')
        finalizados=finalizados.rename(columns={'Concursos_x': 'Finalizados','Concursos_y':'Desiertos'})
        finalizados['Porcentaje']=finalizados['Desiertos']/finalizados['Finalizados']

    # gráfico Convocatorias por Año
        graf1=px.bar(publicaciones,x='Año',y='Concursos',title='<b>Concursos publicados a cargos ADP por año</b>',color_discrete_sequence=[color_bar]).\
                    update_yaxes(visible=visible_y_axis,title_text=None).\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        graf1.update_layout(yaxis_tickformat='.0f')

    # gráfico nóminas por Año
        graf2=px.bar(Nominas,x='Año',y='Concursos',title='<b>Nóminas de concursos ADP enviadas por año</b>',color_discrete_sequence=[color_bar_2]).\
                    update_yaxes(visible=visible_y_axis,title_text=None).\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        graf2.update_layout(yaxis_tickformat='.0f')

    # gráfico Evolución de dias_concursos por Año
        graf3=px.line(dias_concurso,x='Año',y='Dias',title='<b>Evolución de dias de duración de concurso ADP por año</b>').\
                update_yaxes(visible=visible_y_axis,title_text=None).\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        graf3.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_line)
        graf3.update_layout(yaxis_tickformat='.0f')
    
    # gráfico concursos desiertos por año
        graf4=px.bar(desiertos,x='Año',y='Concursos',title='<b>Concursos desiertos por año</b>',color_discrete_sequence=[color_line_4]).\
                    update_yaxes(visible=visible_y_axis,title_text=None).\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        graf4.update_layout(yaxis_tickformat='.0f')

    # gráfico concursos desiertos por año
        graf5=px.bar(finalizados,x='Año',y='Finalizados',title='<b>Concursos finalizados por año</b>',color_discrete_sequence=[color_line_2]).\
                    update_yaxes(visible=visible_y_axis,title_text=None).\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        graf5.update_layout(yaxis_tickformat='.0f')

    # gráfico nombramientos por año
        graf6=px.bar(nombramientos,x='Año',y='Concursos',title='<b>Concursos nombrados por año</b>',color_discrete_sequence=[color_6]).\
                    update_yaxes(visible=visible_y_axis,title_text=None).\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        graf6.update_layout(yaxis_tickformat='.0f')

    # gráfico Evolución de dias_concursos por Año
        graf7=px.line(finalizados,x='Año',y='Porcentaje',title='<b>Porcentaje concurso ADP desiertos por año</b>').\
                update_yaxes(visible=visible_y_axis,title_text=None).\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        graf7.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_line_4)
        graf7.update_layout(yaxis_tickformat='.2%')

        with st.container():
            col1,col2,col3=st.columns(3,gap='small')
            with col1:    
                st.plotly_chart(graf1,use_container_width=True)
            with col2:
                st.plotly_chart(graf2,use_container_width=True)
            with col3:
                st.plotly_chart(graf3,use_container_width=True)
                st.markdown('Se consideran solo concursos con nómina enviada')
            col4,col5,col6=st.columns(3,gap='small')
            with col4:
                st.plotly_chart(graf5,use_container_width=True)
            with col5:
                st.plotly_chart(graf7,use_container_width=True)
            with col6:
                st.plotly_chart(graf6,use_container_width=True)
    #----------------------------------------------------------------------------------------------------------------------
    # filtro postulaciones ADP
    if seleccion_adp=='Postulaciones':
        df_postulaciones_adp=tb_postulaciones_adp()
        
        with st.container():
            col1,col2,col3,col4,col5=st.columns(5,gap="large")
            with col1:
                option_1 = st.selectbox('Nivel Jerárquico',Nivel)
            with col2:
                option_2 = st.selectbox('Región Postulantes',Region)
            with col3:
                option_3 = st.selectbox('Ministerio',Ministerios)
            with col4:
                option_4 = st.selectbox('Servicio',select_servicio(df_concursos,option_3))   
            with col5:
                option_5 = st.selectbox('Sexo Postulantes',sexo_list)
        

        if option_1=='Todos' and option_2=='Todos' and option_3=='Todos' and option_4=='Todos' and option_5=='Todos': #1
            postulaciones=df_postulaciones_adp.groupby('Año').agg({'postulaciones':'sum'}).reset_index()
            postulaciones_x_ministerio=df_postulaciones_adp.groupby('Ministerio').agg({'postulaciones':'sum'}).reset_index()
        
        if option_1=='Todos' and option_2=='Todos' and option_3=='Todos' and option_4=='Todos' and option_5!='Todos': #2
            postulaciones=df_postulaciones_adp[(df_postulaciones_adp['Sexo']==option_5)].groupby('Año').agg({'postulaciones':'sum'}).reset_index()
            postulaciones_x_ministerio=df_postulaciones_adp[(df_postulaciones_adp['Sexo']==option_5)].groupby('Ministerio').agg({'postulaciones':'sum'}).reset_index()
        
        if option_1=='Todos' and option_2!='Todos' and option_3=='Todos' and option_4=='Todos' and option_5!='Todos': #3
            postulaciones=df_postulaciones_adp[(df_postulaciones_adp['Region_Homologada']==option_2) & (df_postulaciones_adp['Sexo']==option_5)].groupby('Año').agg({'postulaciones':'sum'}).reset_index()
            postulaciones_x_ministerio=df_postulaciones_adp[(df_postulaciones_adp['Region_Homologada']==option_2) & (df_postulaciones_adp['Sexo']==option_5)].groupby('Ministerio').agg({'postulaciones':'sum'}).reset_index()
        
        if option_1!='Todos' and option_2=='Todos' and option_3!='Todos' and option_4=='Todos' and option_5=='Todos': #4
            postulaciones=df_postulaciones_adp[(df_postulaciones_adp['Nivel']==option_1) & (df_postulaciones_adp['Ministerio']==option_3)].groupby('Año').agg({'postulaciones':'sum'}).reset_index()
            postulaciones_x_ministerio=df_postulaciones_adp[(df_postulaciones_adp['Nivel']==option_1) & (df_postulaciones_adp['Ministerio']==option_3)].groupby('Ministerio').agg({'postulaciones':'sum'}).reset_index()

        if option_1=='Todos' and option_2=='Todos' and option_3!='Todos' and option_4=='Todos' and option_5=='Todos': #5
            postulaciones=df_postulaciones_adp[(df_postulaciones_adp['Ministerio']==option_3)].groupby('Año').agg({'postulaciones':'sum'}).reset_index()
            postulaciones_x_ministerio=df_postulaciones_adp[(df_postulaciones_adp['Ministerio']==option_3)].groupby('Ministerio').agg({'postulaciones':'sum'}).reset_index()

        if option_1=='Todos' and option_2=='Todos' and option_3!='Todos' and option_4=='Todos' and option_5!='Todos': #6
            postulaciones=df_postulaciones_adp[(df_postulaciones_adp['Ministerio']==option_3) & (df_postulaciones_adp['Sexo']==option_5)].groupby('Año').agg({'postulaciones':'sum'}).reset_index()
            postulaciones_x_ministerio=df_postulaciones_adp[(df_postulaciones_adp['Ministerio']==option_3) & (df_postulaciones_adp['Sexo']==option_5)].groupby('Ministerio').agg({'postulaciones':'sum'}).reset_index()

        if option_1!='Todos' and option_2=='Todos' and option_3!='Todos' and option_4=='Todos' and option_5!='Todos': #7
            postulaciones=df_postulaciones_adp[(df_postulaciones_adp['Nivel']==option_1) & (df_postulaciones_adp['Ministerio']==option_3) & (df_postulaciones_adp['Sexo']==option_5)].groupby('Año').agg({'postulaciones':'sum'}).reset_index()
            postulaciones_x_ministerio=df_postulaciones_adp[(df_postulaciones_adp['Nivel']==option_1) & (df_postulaciones_adp['Ministerio']==option_3) & (df_postulaciones_adp['Sexo']==option_5)].groupby('Ministerio').agg({'postulaciones':'sum'}).reset_index()

        if option_1!='Todos' and option_2=='Todos' and option_3=='Todos' and option_4=='Todos' and option_5!='Todos': #8
            postulaciones=df_postulaciones_adp[(df_postulaciones_adp['Nivel']==option_1) & (df_postulaciones_adp['Sexo']==option_5)].groupby('Año').agg({'postulaciones':'sum'}).reset_index()
            postulaciones_x_ministerio=df_postulaciones_adp[(df_postulaciones_adp['Nivel']==option_1) & (df_postulaciones_adp['Sexo']==option_5)].groupby('Ministerio').agg({'postulaciones':'sum'}).reset_index()

        if option_1=='Todos' and option_2=='Todos' and option_3!='Todos' and option_4!='Todos' and option_5=='Todos': #9
            postulaciones=df_postulaciones_adp[(df_postulaciones_adp['Ministerio']==option_3) & (df_postulaciones_adp['Servicio']==option_4)].groupby('Año').agg({'postulaciones':'sum'}).reset_index()
            postulaciones_x_ministerio=df_postulaciones_adp[(df_postulaciones_adp['Ministerio']==option_3) & (df_postulaciones_adp['Servicio']==option_4)].groupby('Ministerio').agg({'postulaciones':'sum'}).reset_index()
        
        if option_1!='Todos' and option_2=='Todos' and option_3!='Todos' and option_4!='Todos' and option_5=='Todos': #10
            postulaciones=df_postulaciones_adp[(df_postulaciones_adp['Nivel']==option_1) & (df_postulaciones_adp['Ministerio']==option_3) & (df_postulaciones_adp['Servicio']==option_4)].groupby('Año').agg({'postulaciones':'sum'}).reset_index()
            postulaciones_x_ministerio=df_postulaciones_adp[(df_postulaciones_adp['Nivel']==option_1) & (df_postulaciones_adp['Ministerio']==option_3) & (df_postulaciones_adp['Servicio']==option_4)].groupby('Ministerio').agg({'postulaciones':'sum'}).reset_index()
        
        if option_1!='Todos' and option_2=='Todos' and option_3!='Todos' and option_4!='Todos' and option_5!='Todos': #11
            postulaciones=df_postulaciones_adp[(df_postulaciones_adp['Nivel']==option_1) & (df_postulaciones_adp['Ministerio']==option_3) & (df_postulaciones_adp['Servicio']==option_4) & (df_postulaciones_adp['Sexo']==option_5)].groupby('Año').agg({'postulaciones':'sum'}).reset_index()
            postulaciones_x_ministerio=df_postulaciones_adp[(df_postulaciones_adp['Nivel']==option_1) & (df_postulaciones_adp['Ministerio']==option_3) & (df_postulaciones_adp['Servicio']==option_4) & (df_postulaciones_adp['Sexo']==option_5)].groupby('Ministerio').agg({'postulaciones':'sum'}).reset_index()

        #st.dataframe(postulaciones.head(10))
        #st.dataframe(postulaciones_x_ministerio.head(10))
        # ----------------------------------------------------------------------------------------------------------------
        # rename de variable ID_Postulacion
        postulaciones=postulaciones.rename(columns={'postulaciones': 'Postulaciones'})
        postulaciones_x_ministerio=postulaciones_x_ministerio.rename(columns={'postulaciones': 'Postulaciones'})
        # ----------------------------------------------------------------------------------------------------------------

        graf1=px.line(postulaciones,x='Año',y='Postulaciones',title='<b>Evolución de postulaciones ADP por año</b>').\
                update_yaxes(visible=visible_y_axis,title_text=None).\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        graf1.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_line)
        graf1.update_layout(yaxis_tickformat='.0f')


        # gráfico postulaciones por ministerio
        graf2=px.bar(postulaciones_x_ministerio,x='Ministerio',y='Postulaciones',title='<b>Postulaciones por Ministerio</b>',\
                     color_discrete_sequence=[color_6]).\
                    update_yaxes(visible=visible_y_axis,title_text=None).\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        graf2.update_layout(yaxis_tickformat='.0f')

        with st.container():
            col1,col2=st.columns(2,gap='small')
            with col1:
                st.plotly_chart(graf1,use_container_width=True)
            with col2:
                st.plotly_chart(graf2,use_container_width=True)
            st.dataframe(df_postulaciones_adp.head(10))
        

        #if option_1=='Todos' and option_2=='Todos' and option_3=='Todos' and option_4=='Todos' and option_5=='Todos': #1

    #----------------------------------------------------------------------------------------------------------------------
    # filtro nombramientos ADP
    if seleccion_adp=='Nombramientos':
        nombramiento_adp=tabla_nombramientos_adp()
        with st.container():
            col1,col2,col3,col4,col5=st.columns(5,gap="large")
            with col1:
                option_1 = st.selectbox('Nivel Jerárquico',Nivel)
            with col2:
                option_2 = st.selectbox('Región',Region,disabled=False)
            with col3:
                option_3 = st.selectbox('Ministerio',Ministerios)
            with col4:
                option_4 = st.selectbox('Servicio',select_servicio(df_concursos,option_3))   
            with col5:
                option_5 = st.selectbox('Sexo ADP',sexo_list) 


        #st.dataframe(nombramiento_adp.head(10))

        if option_1=='Todos' and option_2=='Todos' and option_3=='Todos' and option_4=='Todos' and option_5=='Todos':#1
            tb_nombramiento_adp=nombramiento_adp.groupby(['Año']).agg({'postulaciones':'sum'}).reset_index()
            tb_nombramiento_adp_ministerio=nombramiento_adp.groupby(['Ministerio']).agg({'postulaciones':'sum'}).reset_index()
            tb_nombramiento_sexo=nombramiento_adp.groupby(['Año','Sexo']).agg({'postulaciones':'sum'}).reset_index()   
            tb_nombramiento_sexo_ministerio=nombramiento_adp[nombramiento_adp.Sexo=='Mujer'].groupby(['Ministerio']).agg({'postulaciones':'sum'}).reset_index()   
        
        if option_1!='Todos' and option_2=='Todos' and option_3=='Todos' and option_4=='Todos' and option_5=='Todos':#2
            tb_nombramiento_adp=nombramiento_adp[nombramiento_adp['Nivel']==option_1].groupby(['Año']).agg({'postulaciones':'sum'}).reset_index()
            tb_nombramiento_adp_ministerio=nombramiento_adp[nombramiento_adp['Nivel']==option_1].groupby(['Ministerio']).agg({'postulaciones':'sum'}).reset_index()
            tb_nombramiento_sexo=nombramiento_adp[nombramiento_adp['Nivel']==option_1].groupby(['Año','Sexo']).agg({'postulaciones':'sum'}).reset_index()   
            tb_nombramiento_sexo_ministerio=nombramiento_adp[(nombramiento_adp.Sexo=='Mujer') & (nombramiento_adp['Nivel']==option_1)].groupby(['Ministerio']).agg({'postulaciones':'sum'}).reset_index()
        
        if option_1!='Todos' and option_2!='Todos' and option_3=='Todos' and option_4=='Todos' and option_5=='Todos':#3
            tb_nombramiento_adp=nombramiento_adp[(nombramiento_adp['Nivel']==option_1) & (nombramiento_adp['RegionCargo']==option_2)].groupby(['Año']).agg({'postulaciones':'sum'}).reset_index()
            tb_nombramiento_adp_ministerio=nombramiento_adp[(nombramiento_adp['Nivel']==option_1) & (nombramiento_adp['RegionCargo']==option_2)].groupby(['Ministerio']).agg({'postulaciones':'sum'}).reset_index()
            tb_nombramiento_sexo=nombramiento_adp[(nombramiento_adp['Nivel']==option_1) & (nombramiento_adp['RegionCargo']==option_2)].groupby(['Año','Sexo']).agg({'postulaciones':'sum'}).reset_index()   
            tb_nombramiento_sexo_ministerio=nombramiento_adp[(nombramiento_adp.Sexo=='Mujer') & (nombramiento_adp['Nivel']==option_1) & (nombramiento_adp['RegionCargo']==option_2)].groupby(['Ministerio']).agg({'postulaciones':'sum'}).reset_index()
            tb_nombramiento_sexo_ministerio=nombramiento_adp[(nombramiento_adp.Sexo=='Mujer') & (nombramiento_adp['Nivel']==option_1) & (nombramiento_adp['RegionCargo']==option_2)].groupby(['Ministerio']).agg({'postulaciones':'sum'}).reset_index()
        
        if option_1!='Todos' and option_2!='Todos' and option_3!='Todos' and option_4=='Todos' and option_5=='Todos':#4
            tb_nombramiento_adp=nombramiento_adp[(nombramiento_adp['Nivel']==option_1) & (nombramiento_adp['RegionCargo']==option_2) & (nombramiento_adp['Ministerio']==option_3)].groupby(['Año']).agg({'postulaciones':'sum'}).reset_index()
            tb_nombramiento_adp_ministerio=nombramiento_adp[(nombramiento_adp['Nivel']==option_1) & (nombramiento_adp['RegionCargo']==option_2) & (nombramiento_adp['Ministerio']==option_3)].groupby(['Ministerio']).agg({'postulaciones':'sum'}).reset_index()
            tb_nombramiento_sexo=nombramiento_adp[(nombramiento_adp['Nivel']==option_1) & (nombramiento_adp['RegionCargo']==option_2) & (nombramiento_adp['Ministerio']==option_3)].groupby(['Año','Sexo']).agg({'postulaciones':'sum'}).reset_index()   
            tb_nombramiento_sexo_ministerio=nombramiento_adp[(nombramiento_adp.Sexo=='Mujer') & (nombramiento_adp['Nivel']==option_1) & (nombramiento_adp['RegionCargo']==option_2) & (nombramiento_adp['Ministerio']==option_3)].groupby(['Ministerio']).agg({'postulaciones':'sum'}).reset_index()
            tb_nombramiento_sexo_ministerio=nombramiento_adp[(nombramiento_adp.Sexo=='Mujer') & (nombramiento_adp['Nivel']==option_1) & (nombramiento_adp['RegionCargo']==option_2) & (nombramiento_adp['Ministerio']==option_3)].groupby(['Ministerio']).agg({'postulaciones':'sum'}).reset_index()




        if option_1!='Todos' and option_2=='Todos' and option_3!='Todos' and option_4=='Todos' and option_5=='Todos':#2
            tb_nombramiento_adp=nombramiento_adp[(nombramiento_adp['Nivel']==option_1) & (nombramiento_adp['Ministerio']==option_3)].groupby(['Año']).agg({'postulaciones':'sum'}).reset_index()
            tb_nombramiento_sexo=nombramiento_adp[(nombramiento_adp['Nivel']==option_1) & (nombramiento_adp['Ministerio']==option_3)].groupby(['Año','Sexo']).agg({'postulaciones':'sum'}).reset_index()

        #st.dataframe(tb_nombramiento_adp.head(10))
        tb_nombramiento_adp=tb_nombramiento_adp.rename(columns={'postulaciones': 'Nombramientos'})
        #st.dataframe(tb_nombramiento_adp.head(10))
        tb_nombramiento_adp_ministerio=tb_nombramiento_adp_ministerio.rename(columns={'postulaciones': 'Total Nombramientos'})    
        tb_nombramiento_sexo=pd.merge(tb_nombramiento_sexo,tb_nombramiento_adp,how='left',on='Año')
        tb_nombramiento_sexo['Porcentaje']=tb_nombramiento_sexo['postulaciones']/tb_nombramiento_sexo['Nombramientos']
        tb_nombramiento_sexo_ministerio=pd.merge(tb_nombramiento_sexo_ministerio,tb_nombramiento_adp_ministerio,how='left',on='Ministerio')
        tb_nombramiento_sexo_ministerio['Porcentaje']=tb_nombramiento_sexo_ministerio['postulaciones']/tb_nombramiento_sexo_ministerio['Total Nombramientos']

        


        graf1=px.bar(tb_nombramiento_adp,x='Año',y='Nombramientos',title='<b>Nombramientos a cargos ADP por año</b>',color_discrete_sequence=[color_6]).\
                    update_yaxes(visible=visible_y_axis,title_text=None).\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        graf1.update_layout(yaxis_tickformat='.0f')

        graf3=px.bar(tb_nombramiento_sexo_ministerio,x='Ministerio',y='Porcentaje',\
                     title='<b>Porcentaje de mujeres con nombramientos a cargos ADP por Ministerio</b>',\
                        color_discrete_sequence=['orange']).\
                            update_yaxes(visible=visible_y_axis,title_text=None).\
                            update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-90)
        graf3.update_layout(yaxis_tickformat='.2%')
        
        #grafico 2: Distribución de Postulaciones por tipo de aviso
        # Se crean distintos DataFrames para "Aviso" y "postulacion en linea"
        df_hombre = tb_nombramiento_sexo[tb_nombramiento_sexo['Sexo'] == 'Hombre']
        df_mujer = tb_nombramiento_sexo[tb_nombramiento_sexo['Sexo'] == 'Mujer']
        
        # crea line plot usando plotly express
        graf2 = px.line(
            title='<b>Nombramientos desagregados por sexo</b>',
            labels={'Año': 'Año', 'Porcentaje': 'Porcentaje'},  # cambia etiquetas de ejes
        )
        
        # Cambiar el formato del eje y a porcentaje (0.1 se mostrará como 10%)
        graf2.update_layout(yaxis_tickformat='.2')
        
        # agrega lineas para categoria "Aviso" y "postulacion en linea"
        graf2.add_trace(
            go.Scatter(x=df_hombre['Año'], y=df_hombre['Porcentaje'], mode='lines+markers',line_shape='spline',marker=dict(size=8, color=sexo_color_map_2['Hombre']), name='Hombre'))#,line_color=sexo_color_map['Mujeres'])
        graf2.add_trace(go.Scatter(x=df_mujer['Año'], y=df_mujer['Porcentaje'], mode='lines+markers',line_shape='spline',marker=dict(size=8, color=sexo_color_map_2['Mujer']), name='Mujer'))#,line_color=sexo_color_map['Hombres']))
    
        # Actualizar la ubicación de la leyenda
        graf2.update_layout(
            legend=dict(x=0.5, xanchor='center', y=-0.2, yanchor='top', traceorder='normal', itemsizing='trace'))  # Ubicar debajo del eje x en dos columnas
        
        # actualiza el eje x para nostrar todas las etiquetas de años
        graf2.update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        graf2.update_layout(yaxis_tickformat='.2%', legend_title_text='Sexo', legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="right", x=1))


        graf4=px.bar(tb_nombramiento_adp_ministerio,x='Ministerio',y='Total Nombramientos',\
                      title='<b>Nombramientos a cargos ADP en Ministerios</b>',color_discrete_sequence=[color_6])
        graf4.update_yaxes(visible=visible_y_axis,title_text=None)
        graf4.update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-90)
        graf4.update_layout(yaxis_tickformat='.0f')

        #st.dataframe(tb_nombramiento_adp_ministerio.head(10))

        with st.container():
            col1,col2=st.columns(2,gap='small')
            with col1:
                st.plotly_chart(graf1,use_container_width=True)
            with col2:
                st.plotly_chart(graf2,use_container_width=True)

        with st.container():
            col1,col2=st.columns(2,gap='small')
            with col1: 
                st.plotly_chart(graf4,use_container_width=True)
            with col2:
                st.plotly_chart(graf3,use_container_width=True)
        
        # with st.container():
        #     col1,col2=st.columns(2,gap='small')
        #     with col1:
        #         st.dataframe(tb_nombramiento_sexo_ministerio)
        #     with col2:
        #         st.dataframe(tb_nombramiento_adp_ministerio)

        
        
#----------------------------------------------------------------------------------------------------------------------
if a=='Empleo Público':
   
    df_concursos_eepp=df_conc_ep()
    df_concursos_eepp['Year_Convocatoria']=pd.to_datetime(df_concursos_eepp['Fecha Inicio']).dt.year
    
    estamento_mapping = {
    'Directiva': 'Directivos',
    'Profesional Ley 15.076/19.664': 'Profesionales'}
    df_concursos_eepp['Estamento'] = df_concursos_eepp['Estamento'].replace(estamento_mapping)
    df_concursos_eepp['Estamento'].fillna('Otros', inplace=True)

    df_rentas=df_concursos_eepp[df_concursos_eepp['Renta Bruta']!=0]
    # aca esta la fecha de actualizacion!!!!
    #------------------------------------------------------------------------------------
    date=df_concursos_eepp.FechaActualizacion.max().strftime('%d/%m/%Y')
    #------------------------------------------------------------------------------------
    
    st.title('Estadísticas Portal Empleos Públicos')
    st.text(f'Fecha Actualización: {date}')

    unique_estamento = df_concursos_eepp['Estamento'].unique()
    Estamento = pd.DataFrame({'Estamento': unique_estamento})
    nuevo_registro = pd.DataFrame({'Estamento': ['Todos']})
    Estamento = pd.concat([nuevo_registro, Estamento])
    Estamento = Estamento.reset_index(drop=True)
    Estamento = Estamento['Estamento'].tolist()

    unique_calidad = df_concursos_eepp['Tipo de Vacante'].unique()
    Calidad = pd.DataFrame({'Calidad Jurídica': unique_calidad})
    nuevo_registro = pd.DataFrame({'Calidad Jurídica': ['Todos']})
    Calidad = pd.concat([nuevo_registro, Calidad])
    Calidad = Calidad.reset_index(drop=True)
    Calidad = Calidad['Calidad Jurídica'].tolist()

    unique_ministerios = df_concursos_eepp['Ministerio'].unique()
    Ministerios = pd.DataFrame({'Ministerio': unique_ministerios})
    nuevo_registro = pd.DataFrame({'Ministerio': ['Todos']})
    Ministerios = pd.concat([nuevo_registro, Ministerios])
    Ministerios = Ministerios.reset_index(drop=True)
    Ministerios = Ministerios['Ministerio'].tolist()

    #---------------------------------------------------------------
    if seleccion_eepp=='Convocatorias': #, "Postulaciones","Seleccionados"] 

        with st.container():
            col1,col2,col3,col4,col5=st.columns(5,gap="small")
            with col1:
                option_1 = st.selectbox('Estamento',Estamento)
            with col2:
                option_2 = st.selectbox('Calidad Juridíca',Calidad)
            with col3:    
                option_3 = st.selectbox('Región',Region)
            with col4:
                option_4 = st.selectbox('Ministerio',Ministerios)
            with col5:
                columnas=['Ministerio','Institucion']
                option_5 = st.selectbox('Servicio',select_servicio(df_concursos_eepp[columnas].rename(columns={'Institucion': 'Servicio'}),option_4))

        if option_1=='Todos' and option_2=='Todos' and option_3=='Todos' and option_4=='Todos' and option_5=='Todos': #1
            convocatorias=df_concursos_eepp.groupby('Year_Convocatoria').agg({'idConcurso':'count'}).reset_index()
            convocatorias=convocatorias.rename(columns={'idConcurso': 'Convocatorias'})
            
            convocatorias_x_tipo=df_concursos_eepp.groupby(['Year_Convocatoria','Tipo postulacion']).agg({'idConcurso':'count'}).reset_index()
            convocatorias_x_tipo=convocatorias_x_tipo.rename(columns={'idConcurso': 'Convocatorias_x_tipo'})
            
            convocatorias_x_tipo=pd.merge(convocatorias_x_tipo,convocatorias,on='Year_Convocatoria',how='left')
            convocatorias_x_tipo['Porcentaje_1']=np.round(convocatorias_x_tipo.Convocatorias_x_tipo/convocatorias_x_tipo.Convocatorias,2)*100

            vacantes=df_concursos_eepp.groupby('Year_Convocatoria').agg({'Nº de Vacantes':'sum'}).reset_index()
            vacantes=vacantes.rename(columns={'Nº de Vacantes': 'Vacantes'})
            
            vacantes_x_tipo=df_concursos_eepp.groupby(['Year_Convocatoria','Tipo postulacion']).agg({'Nº de Vacantes':'sum'}).reset_index()
            vacantes_x_tipo=vacantes_x_tipo.rename(columns={'Nº de Vacantes': 'Vacantes_x_tipo'})
            
            vacantes_x_tipo=pd.merge(vacantes_x_tipo,vacantes,on='Year_Convocatoria',how='left')
            
            vacantes_x_tipo['Porcentaje_2']=np.round(vacantes_x_tipo.Vacantes_x_tipo/vacantes_x_tipo.Vacantes,2)*100

            rentas=df_rentas
            rentas_x_min=df_rentas.groupby(['Year_Convocatoria','Ministerio']).agg({'Renta Bruta':'mean'}).reset_index()
            rentas_x_estamento=df_rentas.groupby(['Year_Convocatoria','Estamento']).agg({'Renta Bruta':'mean'}).reset_index()

            df_desiertos=df_concursos_eepp
            desiertos=df_desiertos[df_desiertos.Estado.isin(['Empleo Desierto','Concurso Desierto'])].groupby('Year_Convocatoria').agg({'idConcurso':'count'}).reset_index()
            desiertos=desiertos.rename(columns={'idConcurso': 'Desiertos','Year_Convocatoria':'Año'})

        else:
            if option_1!='Todos' and option_2=='Todos' and option_3=='Todos' and option_4=='Todos' and option_5=='Todos': #2
                filtro=(df_concursos_eepp.Estamento==option_1)
                filtro_rentas=(df_rentas.Estamento==option_1)
            if option_1=='Todos' and option_2!='Todos' and option_3=='Todos' and option_4=='Todos' and option_5=='Todos': #3
                filtro=(df_concursos_eepp['Tipo de Vacante']==option_2)
                filtro_rentas=(df_rentas['Tipo de Vacante']==option_2)
            if option_1=='Todos' and option_2=='Todos' and option_3!='Todos' and option_4=='Todos' and option_5=='Todos': #4
                filtro=(df_concursos_eepp['Region_Homologada']==option_3)
                filtro_rentas=(df_rentas['Region_Homologada']==option_3)
            if option_1=='Todos' and option_2=='Todos' and option_3=='Todos' and option_4!='Todos' and option_5=='Todos': #5
                filtro=(df_concursos_eepp['Ministerio']==option_4)
                filtro_rentas=(df_rentas['Ministerio']==option_4)
            if option_1=='Todos' and option_2=='Todos' and option_3=='Todos' and option_4=='Todos' and option_5!='Todos': #6
                filtro=(df_concursos_eepp['Institucion']==option_5)
                filtro_rentas=(df_rentas['Institucion']==option_5)
            if option_1!='Todos' and option_2!='Todos' and option_3=='Todos' and option_4=='Todos' and option_5=='Todos': #7
                filtro=(df_concursos_eepp['Estamento']==option_1) & (df_concursos_eepp['Tipo de Vacante']==option_2)
                filtro_rentas=(df_rentas['Estamento']==option_1) & (df_rentas['Tipo de Vacante']==option_2)
            if option_1!='Todos' and option_2=='Todos' and option_3!='Todos' and option_4=='Todos' and option_5=='Todos': #8
                filtro=(df_concursos_eepp['Estamento']==option_1) & (df_concursos_eepp['Region_Homologada']==option_3)
                filtro_rentas=(df_rentas['Estamento']==option_1) & (df_rentas['Region_Homologada']==option_3)
            if option_1!='Todos' and option_2=='Todos' and option_3=='Todos' and option_4!='Todos' and option_5=='Todos': #9
                filtro=(df_concursos_eepp['Estamento']==option_1) & (df_concursos_eepp['Ministerio']==option_4)
                filtro_rentas=(df_rentas['Estamento']==option_1) & (df_rentas['Ministerio']==option_4)
            if option_1!='Todos' and option_2=='Todos' and option_3=='Todos' and option_4=='Todos' and option_5!='Todos': #10
                filtro=(df_concursos_eepp['Estamento']==option_1) & (df_concursos_eepp['Institucion']==option_5)
                filtro_rentas=(df_rentas['Estamento']==option_1) & (df_rentas['Institucion']==option_5)
            if option_1!='Todos' and option_2!='Todos' and option_3!='Todos' and option_4=='Todos' and option_5=='Todos': #11
                filtro=(df_concursos_eepp['Estamento']==option_1) & (df_concursos_eepp['Tipo de Vacante']==option_2) & (df_concursos_eepp['Region_Homologada']==option_3)
                filtro_rentas=(df_rentas['Estamento']==option_1) & (df_rentas['Tipo de Vacante']==option_2) & (df_rentas['Region_Homologada']==option_3)
            if option_1!='Todos' and option_2=='Todos' and option_3!='Todos' and option_4=='Todos' and option_5=='Todos': #12
                filtro=(df_concursos_eepp['Estamento']==option_1) & (df_concursos_eepp['Tipo de Vacante']==option_2) & (df_concursos_eepp['Region_Homologada']==option_3)
                filtro_rentas=(df_rentas['Estamento']==option_1) & (df_rentas['Tipo de Vacante']==option_2) & (df_rentas['Region_Homologada']==option_3)
            if option_1!='Todos' and option_2!='Todos' and option_3=='Todos' and option_4!='Todos' and option_5=='Todos': #13
                filtro=(df_concursos_eepp['Estamento']==option_1) & (df_concursos_eepp['Tipo de Vacante']==option_2) & (df_concursos_eepp['Ministerio']==option_4)
                filtro_rentas=(df_rentas['Estamento']==option_1) & (df_rentas['Tipo de Vacante']==option_2) & (df_rentas['Ministerio']==option_4)
            if option_1!='Todos' and option_2=='Todos' and option_3!='Todos' and option_4=='Todos' and option_5!='Todos': #14
                filtro=(df_concursos_eepp['Estamento']==option_1) & (df_concursos_eepp['Region_Homologada']==option_3) & (df_concursos_eepp['Institucion']==option_5)
                filtro_rentas=(df_rentas['Estamento']==option_1) & (df_rentas['Region_Homologada']==option_3) & (df_rentas['Institucion']==option_5)
            if option_1!='Todos' and option_2=='Todos' and option_3=='Todos' and option_4!='Todos' and option_5!='Todos': #15
                filtro=(df_concursos_eepp['Estamento']==option_1) & (df_concursos_eepp['Ministerio']==option_4) & (df_concursos_eepp['Institucion']==option_5)
                filtro_rentas=(df_rentas['Estamento']==option_1) & (df_rentas['Ministerio']==option_4) & (df_rentas['Institucion']==option_5)
            if option_1!='Todos' and option_2=='Todos' and option_3!='Todos' and option_4!='Todos' and option_5=='Todos': #16
                filtro=(df_concursos_eepp['Estamento']==option_1) & (df_concursos_eepp['Region_Homologada']==option_3) & (df_concursos_eepp['Ministerio']==option_4)
                filtro_rentas=(df_rentas['Estamento']==option_1) & (df_rentas['Region_Homologada']==option_3) & (df_rentas['Ministerio']==option_4)
            if option_1=='Todos' and option_2!='Todos' and option_3!='Todos' and option_4!='Todos' and option_5=='Todos': #17
                filtro=(df_concursos_eepp['Tipo de Vacante']==option_2) & (df_concursos_eepp['Region_Homologada']==option_3) & (df_concursos_eepp['Ministerio']==option_4)
                filtro_rentas=(df_rentas['Tipo de Vacante']==option_2) & (df_rentas['Region_Homologada']==option_3) & (df_rentas['Ministerio']==option_4)
            if option_1=='Todos' and option_2=='Todos' and option_3!='Todos' and option_4!='Todos' and option_5!='Todos': #18
                filtro=(df_concursos_eepp['Region_Homologada']==option_3) & (df_concursos_eepp['Ministerio']==option_4) & (df_concursos_eepp['Institucion']==option_5)
                filtro_rentas=(df_rentas['Region_Homologada']==option_3) & (df_rentas['Ministerio']==option_4) & (df_rentas['Institucion']==option_5)
            if option_1=='Todos' and option_2!='Todos' and option_3=='Todos' and option_4!='Todos' and option_5!='Todos': #19
                filtro=(df_concursos_eepp['Tipo de Vacante']==option_2) & (df_concursos_eepp['Ministerio']==option_4) & (df_concursos_eepp['Institucion']==option_5)
                filtro_rentas=(df_rentas['Tipo de Vacante']==option_2) & (df_rentas['Ministerio']==option_4) & (df_rentas['Institucion']==option_5)
            if option_1=='Todos' and option_2!='Todos' and option_3!='Todos' and option_4=='Todos' and option_5!='Todos': #20
                filtro=(df_concursos_eepp['Tipo de Vacante']==option_2) & (df_concursos_eepp['Region_Homologada']==option_3) & (df_concursos_eepp['Institucion']==option_5)
                filtro_rentas=(df_rentas['Tipo de Vacante']==option_2) & (df_rentas['Region_Homologada']==option_3) & (df_rentas['Institucion']==option_5)
            if option_1=='Todos' and option_2=='Todos' and option_3=='Todos' and option_4!='Todos' and option_5!='Todos': #21
                filtro=(df_concursos_eepp['Ministerio']==option_4) & (df_concursos_eepp['Institucion']==option_5)
                filtro_rentas=(df_rentas['Ministerio']==option_4) & (df_rentas['Institucion']==option_5)
            if option_1=='Todos' and option_2=='Todos' and option_3!='Todos' and option_4=='Todos' and option_5!='Todos': #22
                filtro=(df_concursos_eepp['Region_Homologada']==option_3) & (df_concursos_eepp['Institucion']==option_5)
                filtro_rentas=(df_rentas['Region_Homologada']==option_3) & (df_rentas['Institucion']==option_5)
            if option_1=='Todos' and option_2=='Todos' and option_3!='Todos' and option_4!='Todos' and option_5=='Todos': #23
                filtro=(df_concursos_eepp['Region_Homologada']==option_3) & (df_concursos_eepp['Ministerio']==option_4)
                filtro_rentas=(df_rentas['Region_Homologada']==option_3) & (df_rentas['Ministerio']==option_4)
            if option_1=='Todos' and option_2!='Todos' and option_3=='Todos' and option_4!='Todos' and option_5=='Todos': #24
                filtro=(df_concursos_eepp['Tipo de Vacante']==option_2) & (df_concursos_eepp['Ministerio']==option_4)
                filtro_rentas=(df_rentas['Tipo de Vacante']==option_2) & (df_rentas['Ministerio']==option_4)
            if option_1=='Todos' and option_2!='Todos' and option_3!='Todos' and option_4=='Todos' and option_5=='Todos': #25
                filtro=(df_concursos_eepp['Tipo de Vacante']==option_2) & (df_concursos_eepp['Region_Homologada']==option_3)
                filtro_rentas=(df_rentas['Tipo de Vacante']==option_2) & (df_rentas['Region_Homologada']==option_3)
            if option_1=='Todos' and option_2!='Todos' and option_3=='Todos' and option_4=='Todos' and option_5!='Todos': #26
                filtro=(df_concursos_eepp['Tipo de Vacante']==option_2) & (df_concursos_eepp['Institucion']==option_5)
                filtro_rentas=(df_rentas['Tipo de Vacante']==option_2) & (df_rentas['Institucion']==option_5)
            if option_1=='Todos' and option_2!='Todos' and option_3!='Todos' and option_4!='Todos' and option_5!='Todos': #27
                filtro=(df_concursos_eepp['Tipo de Vacante']==option_2) & (df_concursos_eepp['Region_Homologada']==option_3) & (df_concursos_eepp['Ministerio']==option_4) & (df_concursos_eepp['Institucion']==option_5)
                filtro_rentas=(df_rentas['Tipo de Vacante']==option_2) & (df_rentas['Region_Homologada']==option_3) & (df_rentas['Ministerio']==option_4) & (df_rentas['Institucion']==option_5)
            if option_1!='Todos' and option_2=='Todos' and option_3!='Todos' and option_4!='Todos' and option_5!='Todos': #28
                filtro=(df_concursos_eepp['Estamento']==option_1) & (df_concursos_eepp['Region_Homologada']==option_3) & (df_concursos_eepp['Ministerio']==option_4) & (df_concursos_eepp['Institucion']==option_5)
                filtro_rentas=(df_rentas['Estamento']==option_1) & (df_rentas['Region_Homologada']==option_3) & (df_rentas['Ministerio']==option_4) & (df_rentas['Institucion']==option_5)
            if option_1!='Todos' and option_2!='Todos' and option_3=='Todos' and option_4!='Todos' and option_5!='Todos': #29
                filtro=(df_concursos_eepp['Estamento']==option_1) & (df_concursos_eepp['Tipo de Vacante']==option_2) & (df_concursos_eepp['Ministerio']==option_4) & (df_concursos_eepp['Institucion']==option_5)
                filtro_rentas=(df_rentas['Estamento']==option_1) & (df_rentas['Tipo de Vacante']==option_2) & (df_rentas['Ministerio']==option_4) & (df_rentas['Institucion']==option_5)
            if option_1!='Todos' and option_2!='Todos' and option_3!='Todos' and option_4=='Todos' and option_5!='Todos': #30
                filtro=(df_concursos_eepp['Estamento']==option_1) & (df_concursos_eepp['Tipo de Vacante']==option_2) & (df_concursos_eepp['Region_Homologada']==option_3) & (df_concursos_eepp['Institucion']==option_5)
                filtro_rentas=(df_rentas['Estamento']==option_1) & (df_rentas['Tipo de Vacante']==option_2) & (df_rentas['Region_Homologada']==option_3) & (df_rentas['Institucion']==option_5)
            if option_1!='Todos' and option_2!='Todos' and option_3!='Todos' and option_4!='Todos' and option_5=='Todos': #31
                filtro=(df_concursos_eepp['Estamento']==option_1) & (df_concursos_eepp['Tipo de Vacante']==option_2) & (df_concursos_eepp['Region_Homologada']==option_3) & (df_concursos_eepp['Ministerio']==option_4)
                filtro_rentas=(df_rentas['Estamento']==option_1) & (df_rentas['Tipo de Vacante']==option_2) & (df_rentas['Region_Homologada']==option_3) & (df_rentas['Ministerio']==option_4)
            if option_1!='Todos' and option_2!='Todos' and option_3!='Todos' and option_4!='Todos' and option_5!='Todos': #32
                filtro=(df_concursos_eepp['Estamento']==option_1) & (df_concursos_eepp['Tipo de Vacante']==option_2) & (df_concursos_eepp['Region_Homologada']==option_3) & (df_concursos_eepp['Ministerio']==option_4) & (df_concursos_eepp['Institucion']==option_5)
                filtro_rentas=(df_rentas['Estamento']==option_1) & (df_rentas['Tipo de Vacante']==option_2) & (df_rentas['Region_Homologada']==option_3) & (df_rentas['Ministerio']==option_4) & (df_rentas['Institucion']==option_5)
            
            convocatorias=df_concursos_eepp[filtro].groupby('Year_Convocatoria').agg({'idConcurso':'count'}).reset_index()
            convocatorias=convocatorias.rename(columns={'idConcurso': 'Convocatorias'})

            df_desiertos=df_concursos_eepp[filtro]
            desiertos=df_desiertos[df_desiertos.Estado.isin(['Empleo Desierto','Concurso Desierto'])].groupby('Year_Convocatoria').agg({'idConcurso':'count'}).reset_index()
            
            convocatorias_x_tipo=df_concursos_eepp[filtro].groupby(['Year_Convocatoria','Tipo postulacion']).agg({'idConcurso':'count'}).reset_index()
            convocatorias_x_tipo=convocatorias_x_tipo.rename(columns={'idConcurso': 'Convocatorias_x_tipo'})
            convocatorias_x_tipo=pd.merge(convocatorias_x_tipo,convocatorias,on='Year_Convocatoria',how='left')
            convocatorias_x_tipo['Porcentaje_1']=np.round(convocatorias_x_tipo.Convocatorias_x_tipo/convocatorias_x_tipo.Convocatorias,2)*100

            vacantes=df_concursos_eepp[filtro].groupby('Year_Convocatoria').agg({'Nº de Vacantes':'sum'}).reset_index()
            vacantes=vacantes.rename(columns={'Nº de Vacantes': 'Vacantes'})
            
            vacantes_x_tipo=df_concursos_eepp[filtro].groupby(['Year_Convocatoria','Tipo postulacion']).agg({'Nº de Vacantes':'sum'}).reset_index()
            vacantes_x_tipo=vacantes_x_tipo.rename(columns={'Nº de Vacantes': 'Vacantes_x_tipo'})
            vacantes_x_tipo=pd.merge(vacantes_x_tipo,vacantes,on='Year_Convocatoria',how='left')
            vacantes_x_tipo['Porcentaje_2']=np.round(vacantes_x_tipo.Vacantes_x_tipo/vacantes_x_tipo.Vacantes,2)*100

            rentas=df_rentas[filtro_rentas].groupby('Year_Convocatoria').agg({'Renta Bruta':'mean'}).reset_index()
            rentas_x_min=df_rentas[filtro_rentas].groupby(['Year_Convocatoria','Ministerio']).agg({'Renta Bruta':'mean'}).reset_index()
            rentas_x_estamento=df_rentas[filtro_rentas].groupby(['Year_Convocatoria','Estamento']).agg({'Renta Bruta':'mean'}).reset_index()

        convocatorias_vacantes=pd.merge(convocatorias_x_tipo,vacantes_x_tipo,how='left',on=['Year_Convocatoria','Tipo postulacion'])
        convocatorias_vacantes['Vacantes_x_Convocatoria']=np.round(convocatorias_vacantes.Vacantes_x_tipo/convocatorias_vacantes.Convocatorias_x_tipo,2)
        
        # cambio nombre year_convocatoria x Año
        convocatorias_vacantes=convocatorias_vacantes.rename(columns={'Year_Convocatoria': 'Año'})
        convocatorias_x_tipo=convocatorias_x_tipo.rename(columns={'Year_Convocatoria': 'Año'})
        convocatorias=convocatorias.rename(columns={'Year_Convocatoria': 'Año'})
        desiertos=desiertos.rename(columns={'idConcurso': 'Desiertos','Year_Convocatoria':'Año'})
        vacantes_x_tipo=vacantes_x_tipo.rename(columns={'Year_Convocatoria': 'Año'})
        vacantes=vacantes.rename(columns={'Year_Convocatoria': 'Año'})

        #----------------------------------------------------------------------------------------------------------------------------
        desiertos=pd.merge(desiertos,convocatorias,on='Año',how='left')
        desiertos['Porcentaje']=np.round(desiertos.Desiertos/desiertos.Convocatorias,2)
        
        # fin del else
        #----------------------------------------------------------------------------------------------------------------------------

        tipo_convocatoria={'Aviso':color_line_2,'Postulacion en linea':color_bar}
        convocatorias_x_tipo['Color'] = convocatorias_x_tipo['Tipo postulacion'].map(tipo_convocatoria)

        #----------------------------------------------------------------------------------------------------------------------------
        #----------------------------------------------------------------------------------------------------------------------------
        #grafico 2: Distribución de Postulaciones por tipo de aviso
        # Se crean distintos DataFrames para "Aviso" y "postulacion en linea"
        df_aviso = convocatorias_vacantes[convocatorias_x_tipo['Tipo postulacion'] == 'Aviso']
        df_linea = convocatorias_vacantes[convocatorias_x_tipo['Tipo postulacion'] == 'Postulacion en linea']
        
        # crea line plot usando plotly express
        graf2 = px.line(
            title='<b>Vacantes promedio por convocatorias</b>',
            labels={'Año': 'Año', 'Vacantes_x_Convocatoria': 'Vacantes por convocatoria'},  # cambia etiquetas de ejes
        )
        
        # Cambiar el formato del eje y a porcentaje (0.1 se mostrará como 10%)
        graf2.update_layout(yaxis_tickformat='.2')
        
        # agrega lineas para categoria "Aviso" y "postulacion en linea"
        graf2.add_trace(
            go.Scatter(x=df_aviso['Año'], y=df_aviso['Vacantes_x_Convocatoria'], mode='lines+markers',line_shape='spline',marker=dict(size=8, color=tipo_postulacion_color_map['Aviso']), name='Aviso'))#,line_color=sexo_color_map['Mujeres'])
        graf2.add_trace(go.Scatter(x=df_linea['Año'], y=df_linea['Vacantes_x_Convocatoria'], mode='lines+markers',line_shape='spline',marker=dict(size=8, color=tipo_postulacion_color_map['Postulacion en linea']), name='Postulacion en linea'))#,line_color=sexo_color_map['Hombres']))
    
        # Actualizar la ubicación de la leyenda
        graf2.update_layout(
            legend=dict(x=0.5, xanchor='center', y=-0.2, yanchor='top', traceorder='normal', itemsizing='trace'))  # Ubicar debajo del eje x en dos columnas
        
        # actualiza el eje x para nostrar todas las etiquetas de años
        graf2.update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        graf2.update_layout(yaxis_tickformat='.2f', legend_title_text='Tipo de postulación', legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="right", x=1))
        
        #----------------------------------------------------------------------------------------------------------------------------
        # # grafico Postulación Promedio por Año
        # graf3=px.line(df_postulaciones_promedio,x='Año',y='Tasa Postulación Promedio - Concursos en Línea',title='<b>Evolución de postulaciones promedio por convocatoria por año</b>').\
        #         update_yaxes(visible=visible_y_axis,title_text=None).\
        #                 update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        
        # graf3.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_line)
        #----------------------------------------------------------------------------------------------------------------------------
        # grafico Convocatorias por Año
        graf4=px.bar(convocatorias,x='Año',y='Convocatorias',title='<b>Evolución de convocatorias por año</b>',color_discrete_sequence=[color_bar]).\
                update_yaxes(visible=visible_y_axis,title_text=None,type='linear', dtick=5000).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        graf4.update_layout(yaxis_tickformat='.0f')
        # Se puede cambiar type de 'linear' a 'log' dtick es el intervalo
        #----------------------------------------------------------------------------------------------------------------------------
        graf7=px.bar(convocatorias_x_tipo, x='Año', y='Convocatorias_x_tipo',title='<b>Cantidad  de convocatorias por forma de publicación por año</b>',
                    color='Tipo postulacion',color_discrete_map=tipo_postulacion_color_map,labels={'idConcurso': 'Cantidad de Convocatorias'}).\
                    update_yaxes(visible=visible_y_axis,title_text=None,type='linear', dtick=5000).\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        graf7.update_layout(yaxis_tickformat='.0f', legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="right", x=1))
        # Personaliza el eje Y
        graf7.update_yaxes(
            type='linear',  # Puedes cambiar 'linear' a 'log' u otro tipo de escala si lo deseas
            dtick=5000  # Establece el intervalo en el eje Y, en este caso, cada 10 unidades
            )
        #----------------------------------------------------------------------------------------------------------------------------
        graf8= px.bar(convocatorias_x_tipo, x="Año", y="Porcentaje_1",title='<b>Distribución (%) de tipo de convocatorias por año</b>', color='Tipo postulacion',color_discrete_map=tipo_postulacion_color_map, text_auto=True).\
                update_yaxes(visible=False,title_text=None,type='linear').\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45).\
                            update_layout(yaxis_tickformat='.0f', legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="right", x=1))
        
        #----------------------------------------------------------------------------------------------------------------------------
    
        # grafico Vacantes Concursadas por Año
        graf5=px.bar(vacantes,x='Año',y='Vacantes',title='<b>Vacantes ofrecidas por año</b>',color_discrete_sequence=[color_bar_2]).\
                update_yaxes(visible=visible_y_axis,title_text=None).\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        graf5.update_layout(yaxis_tickformat='.0f')
        #----------------------------------------------------------------------------------------------------------------------------
        # grafico Porcentaje de convocatorias con postulación en linea por año
        #graf6=px.line(convocatorias_x_tipo,x='Year_Convocatoria',y='Porcentaje_2',title='<b>Distribución (%) de convocatorias con postulación en línea por año</b>').\
        #        update_yaxes(visible=visible_y_axis,title_text=None).\
        #                update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        # 
        #graf6.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_bar)
        #graf6.update_layout(yaxis_tickformat='.0%')
        #----------------------------------------------------------------------------------------------------------------------------
        graf9=px.histogram(rentas, x="Renta Bruta",title='<b>Histograma de rentas brutas ofrecidas</b>')
        graf10=px.line(rentas_x_min, x="Year_Convocatoria", y="Renta Bruta", color='Ministerio',markers='o',title='<b>Evolución de rentas brutas ofrecidas por año</b>')
        graf10.update_layout(yaxis_tickformat='.0f', legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="right", x=1))

        graf11=px.line(rentas_x_estamento, x="Year_Convocatoria", y="Renta Bruta", color='Estamento',markers='o',title='<b>Rentas brutas promedio por estamento por año</b>')
        graf11.update_layout(yaxis_tickformat='.0f', legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="right", x=1))
        graf11.update_yaxes(visible=visible_y_axis,title_text=None).\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        #----------------------------------------------------------------------------------------------------------------------------
        #graf12=px.bar(desiertos,x='Año',y='Desiertos',title='<b>Concursos desiertos por año</b>',color_discrete_sequence=[color_line_4]).\
        #        update_yaxes(visible=visible_y_axis,title_text=None).\
        #                update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        #graf12.update_layout(yaxis_tickformat='.0f')
        
        #gráfico desiertos EEPP
        graf12=px.line(desiertos,x='Año',y='Porcentaje',title='<b>Porcentaje convocatorias desiertos en EEPP</b>').\
                update_yaxes(visible=visible_y_axis,title_text=None).\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
        graf12.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_line_4)
        graf12.update_layout(yaxis_tickformat='.2%')

        #----------------------------------------------------------------------------------------------------------------------------
        col1,col2,col3=st.columns(3,gap='small')
        with col1:
            st.plotly_chart(graf4,use_container_width=True)
            st.markdown('Nota: Solo se consideran convocatorias efectuadas en portal de EEPP')
        with col2:
            st.plotly_chart(graf8,use_container_width=True)
        with col3:
            st.plotly_chart(graf12,use_container_width=True)
        
        
        col4, col5, col6=st.columns(3,gap='small')
        with col4:
                st.plotly_chart(graf5,use_container_width=True)
        with col5:
                st.plotly_chart(graf2,use_container_width=True)
        with col6:
                st.plotly_chart(graf11,use_container_width=True)

    if seleccion_eepp=='Postulaciones':
        @st.cache_data
        def postulciones_eepp():
            df_post_eepp=pq.read_table('datos/tb_postulaciones_eepp.parquet').to_pandas()
            df_post_eepp=pd.merge(df_post_eepp,all_region,on='Region',how='left')
            df_post_eepp=df_post_eepp.drop(columns=['Region'])
            return df_post_eepp

        df_postulaciones_eepp=postulciones_eepp()

        with st.container():
            col6,col7,col8,col9=st.columns(4,gap="small")
            with col6:    
                option_S1 = st.selectbox('Región',Region)
            with col7:
                option_S2 = st.selectbox('Ministerio',Ministerios)
            with col8:
                columnas=['Ministerio','Servicio']
                option_S3 = st.selectbox('Servicio',select_servicio(df_postulaciones_eepp[columnas],option_S2))
            with col9:
                option_S4 = st.selectbox('Sexo',sexo_list)

        

        if option_S1=='Todos' and option_S2=='Todos' and option_S3=='Todos' and option_S4=='Todos': #1
            postulaciones=df_postulaciones_eepp.groupby('Año').agg({'postulaciones':'sum'}).reset_index()
            postulaciones_x_ministerio=df_postulaciones_eepp.groupby('Ministerio').agg({'postulaciones':'sum'}).reset_index()
            st.dataframe(df_postulaciones_eepp.head(20))
        else:
            if option_S1=='Todos' and option_S2=='Todos' and option_S3=='Todos' and option_S4!='Todos': #2
                filtro=(df_postulaciones_eepp.Sexo==option_S4)
            if option_S1=='Todos' and option_S2=='Todos' and option_S3!='Todos' and option_S4=='Todos': #3
                filtro=(df_postulaciones_eepp['Servicio']==option_S3)
            if option_S1=='Todos' and option_S2=='Todos' and option_S3!='Todos' and option_S4!='Todos': #4
                filtro=(df_postulaciones_eepp['Sexo']==option_S4) & (df_postulaciones_eepp['Servicio']==option_S3)
            if option_S1=='Todos' and option_S2!='Todos' and option_S3=='Todos' and option_S4=='Todos': #5
                filtro=(df_postulaciones_eepp['Ministerio']==option_S2)
            if option_S1=='Todos' and option_S2!='Todos' and option_S3=='Todos' and option_S4!='Todos': #6
                filtro=(df_postulaciones_eepp['Sexo']==option_S4) & (df_postulaciones_eepp['Ministerio']==option_S2)
            if option_S1=='Todos' and option_S2!='Todos' and option_S3!='Todos' and option_S4=='Todos': #7
                filtro=(df_postulaciones_eepp['Ministerio']==option_S2) & (df_postulaciones_eepp['Servicio']==option_S3)
            if option_S1=='Todos' and option_S2!='Todos' and option_S3!='Todos' and option_S4!='Todos': #8
                filtro=(df_postulaciones_eepp['Ministerio']==option_S2) & (df_postulaciones_eepp['Servicio']==option_S3) & (df_postulaciones_eepp['Sexo']==option_S4)
            if option_S1!='Todos' and option_S2=='Todos' and option_S3=='Todos' and option_S4=='Todos': #9
                filtro=(df_postulaciones_eepp['Region_Homologada']==option_S1)
            if option_S1!='Todos' and option_S2=='Todos' and option_S3=='Todos' and option_S4!='Todos': #10
                filtro=(df_postulaciones_eepp['Region_Homologada']==option_3) & (df_postulaciones_eepp['Sexo']==option_S4)    
            if option_S1!='Todos' and option_S2=='Todos' and option_S3!='Todos' and option_S4=='Todos': #11
                filtro=(df_postulaciones_eepp['Region_Homologada']==option_3) & (df_postulaciones_eepp['Ministerio']==option_S2) 
            if option_S1!='Todos' and option_S2!='Todos' and option_S3=='Todos' and option_S4=='Todos': #12
                filtro=(df_postulaciones_eepp['Region_Homologada']==option_3) & (df_postulaciones_eepp['Ministerio']==option_S2)
            if option_S1!='Todos' and option_S2=='Todos' and option_S3!='Todos' and option_S4!='Todos': #13
                filtro=(df_postulaciones_eepp['Region_Homologada']==option_3) & (df_concursos_eepp['Servicio']==option_S3)
            if option_S1!='Todos' and option_S2!='Todos' and option_S3=='Todos' and option_S4!='Todos': #14
                filtro=(df_postulaciones_eepp['Ministerio']==option_S2) & (df_postulaciones_eepp['Servicio']==option_S3) & (df_postulaciones_eepp['Sexo']==option_S4)
            if option_S1!='Todos' and option_S2!='Todos' and option_S3!='Todos' and option_S4=='Todos': #15
                filtro=(df_postulaciones_eepp['Region_Homologada']==option_S1) & (df_postulaciones_eepp['Ministerio']==option_S2) & (df_postulaciones_eepp['Servicio']==option_S3)                
            if option_S1!='Todos' and option_S2!='Todos' and option_S3!='Todos' and option_S4!='Todos': #16
                filtro=(df_postulaciones_eepp['Region_Homologada']==option_S1) & (df_postulaciones_eepp['Ministerio']==option_S2) & (df_postulaciones_eepp['Servicio']==option_S3) & (df_postulaciones_eepp['Sexo']==option_S4)
             
            st.dataframe(df_postulaciones_eepp[filtro].head(20))
    #if seleccion_eepp=='Seleccionados': 
#----------------------------------------------------------------------------------------------------------------------

if a=='Prácticas Chile':

    df_postulaciones=pd.read_csv('PCH/postulaciones_x_año.csv',encoding='utf-8')    
    df_convocatorias=pd.read_csv('PCH/Convocatorias_x_año.csv')
    #df_seleccionados=pd.read_csv('PCH/Seleccionado_x_año.csv',sep=";",encoding='utf-8')
    df_seleccionados=pd.read_excel('PCH/Seleccionado_x_año.xlsx')
    
    date='31 de Marzo de 2023'
    
    st.title('Estadísticas Portal Prácticas Chile')
    st.subheader(date)
    # markdown style
    
    st.markdown("""
    <style>
    .normal-font {
        font-size:30px;
        fott-type:roboto
    }
    </style>
    """, unsafe_allow_html=True)
    
    #----------------------------------------------------------------------------------------------------------------------------
    # grafico Evolución de Postulaciones por Año
    graf1=px.line(df_postulaciones,x='año',y='Postulaciones',title='<b>Evolución de postulaciones por año</b>').\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1)
    graf1.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_line)
    graf1.update_layout(yaxis_tickformat='.0f')
    #----------------------------------------------------------------------------------------------------------------------------
    
    # grafico Convocatorias por Año
    graf2=px.bar(df_convocatorias,x='Año',y='Convocatorias',title='<b>Evolución de convocatorias por año</b>',color_discrete_sequence=[color_bar]).\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1)
    #----------------------------------------------------------------------------------------------------------------------------
    # grafico Seleccionados por Año
    # Create the line plot
    graf3 = px.line(df_seleccionados, x='year', y='Seleccionados', title='<b>Evolución de cantidad estudiantes seleccionados/as por año</b>')\
        .update_yaxes(visible=visible_y_axis, title_text=None)\
        .update_xaxes(title_text=None,tickmode='linear', dtick=1)
    
    graf3.update_traces(mode='lines+markers', marker=dict(size=8), line_shape='spline', line_color=color_line)
    #----------------------------------------------------------------------------------------------------------------------------
    
    
    col1,col2,col3=st.columns(3,gap='small')
    with col1:
        st.markdown('<p class="normal-font">Prácticas Chile es un programa gestionado por el Servicio Civil, que busca promover y atraer talento joven al Estado, y que permite a estudiantes de carreras universitarias y técnicas realizar sus prácticas en ministerios y servicios públicos, poniendo al servicio del país sus conocimientos y habilidades. </p>', unsafe_allow_html=True)
    with col2:
        st.plotly_chart(graf1,use_container_width=True)
    with col3:
        st.plotly_chart(graf2,use_container_width=True)
    
    
    col4, col5=st.columns(2,gap='small')
    with col4:
            st.plotly_chart(graf3,use_container_width=True)
    with col4:
            st.text('')

#----------------------------------------------------------------------------------------------------------------------
if a=='Directores para Chile':
    df_DEEM=pd.read_csv('DEEM/tblConcursos.csv',encoding='utf-8',sep=';')        
    df_DEEM=df_DEEM.rename(columns={'Comuna/Ciudad': 'Comuna'})
    df_DEEM['Estado_Concurso']=np.where(df_DEEM['Estado']=='Desvinculado','Nombrado',df_DEEM['Estado'])
    estados_proceso=['Admisibilidad','Ev.Externa', 'Entrevista', 'Nómina', 'Convocatoria']
    df_DEEM['Estado_Final']=np.where(df_DEEM['Estado']=='Desvinculado','Nombrado',np.where(df_DEEM['Estado'].isin(estados_proceso),'En Proceso',df_DEEM['Estado']))
    date=max(df_DEEM.FechaCorte)

    df_DEEM=pd.merge(df_DEEM,all_region,on='Region',how='left')

    def select_comuna(df, option_1):
        if option_1 == 'Todos':
            unique_comuna = df['Comuna'].unique()
            Comuna = pd.DataFrame({'Comuna': unique_comuna})
            nuevo_registro = pd.DataFrame({'Comuna': ['Todos']})
            Comuna = pd.concat([nuevo_registro, Comuna]).Comuna.tolist()
        else:
            unique_comuna = df.query(f'Region_Homologada == "{option_1}"')['Comuna'].unique()
            Comuna = pd.DataFrame({'Comuna': unique_comuna})
            nuevo_registro = pd.DataFrame({'Comuna': ['Todos']})
            Comuna = pd.concat([nuevo_registro, Comuna]).Comuna.tolist()
        
        return Comuna
    
    st.title('Estadísticas Portal Directores para Chile')
    st.subheader(date)
    
    # markdown style
    st.markdown("""
    <style>
    .normal-font {
        font-size:30px;
        fott-type:roboto
    }
    </style>
    """, unsafe_allow_html=True)

    # unique_region = df_DEEM['Region'].unique()
    # Region = pd.DataFrame({'Region': unique_region})
    # nuevo_registro = pd.DataFrame({'Region': ['Todos']})
    # Region = pd.concat([nuevo_registro, Region])
    # Region = Region.reset_index(drop=True)
    # Region = Region['Region'].tolist()

    unique_comuna = df_DEEM['Comuna'].unique()
    Comuna = pd.DataFrame({'Comuna': unique_comuna})
    nuevo_registro = pd.DataFrame({'Comuna': ['Todos']})
    Comuna = pd.concat([nuevo_registro, Comuna])
    Comuna = Comuna.reset_index(drop=True)
    Comuna = Comuna['Comuna'].tolist()

    unique_estado = df_DEEM['Estado_Concurso'].unique()
    Estado = pd.DataFrame({'Estado': unique_estado})
    nuevo_registro = pd.DataFrame({'Estado': ['Todos']})
    Estado = pd.concat([nuevo_registro, Estado])
    Estado = Estado.reset_index(drop=True)
    Estado = Estado['Estado'].tolist()

    columnas=['Region','Comuna']

    with st.container():
        col1,col2=st.columns(2,gap="small")
        with col1:
            option_1 = st.selectbox('Región',Region)
        with col2:
            option_2 = st.selectbox('Comuna',select_comuna(df_DEEM,option_1))
    #----------------------------------------------------------------------------------------------------------------------------
    if option_1=='Todos' and option_2=='Todos': 
            df_convocatorias=df_DEEM.groupby('AgnoFechaInicioConvocatoria').agg({'idConcurso':'count'}).reset_index()
            df_estados = df_DEEM.groupby(['AgnoFechaInicioConvocatoria','Estado_Concurso']).agg({'idConcurso': 'count'}).reset_index()
            df_estados_finales = df_DEEM.groupby(['AgnoFechaInicioConvocatoria','Estado_Final']).agg({'idConcurso': 'count'}).reset_index()
    if option_1!='Todos' and option_2=='Todos':  #2
            df_convocatorias=df_DEEM[(df_DEEM.Region_Homologada==option_1)].groupby('AgnoFechaInicioConvocatoria').agg({'idConcurso':'count'}).reset_index()
            df_estados = df_DEEM[(df_DEEM.Region_Homologada==option_1)].groupby(['AgnoFechaInicioConvocatoria','Estado_Concurso']).agg({'idConcurso': 'count'}).reset_index()
            df_estados_finales = df_DEEM[(df_DEEM.Region_Homologada==option_1)].groupby(['AgnoFechaInicioConvocatoria','Estado_Final']).agg({'idConcurso': 'count'}).reset_index()
    if option_1=='Todos' and option_2!='Todos':  #3
            df_convocatorias=df_DEEM[(df_DEEM.Comuna==option_2)].groupby('AgnoFechaInicioConvocatoria').agg({'idConcurso':'count'}).reset_index()
            df_estados = df_DEEM[(df_DEEM.Comuna==option_2)].groupby(['AgnoFechaInicioConvocatoria','Estado_Concurso']).agg({'idConcurso': 'count'}).reset_index()
            df_estados_finales = df_DEEM[(df_DEEM.Comuna==option_2)].groupby(['AgnoFechaInicioConvocatoria','Estado_Final']).agg({'idConcurso': 'count'}).reset_index()
    if option_1!='Todos' and option_2!='Todos': #4
            df_convocatorias=df_DEEM[(df_DEEM.Region_Homologada==option_1) & (df_DEEM.Comuna==option_2)].groupby('AgnoFechaInicioConvocatoria').agg({'idConcurso':'count'}).reset_index()
            df_estados = df_DEEM[(df_DEEM.Comuna==option_2) & (df_DEEM.Region_Homologada==option_1)].groupby(['AgnoFechaInicioConvocatoria','Estado_Concurso']).agg({'idConcurso': 'count'}).reset_index()
            df_estados_finales = df_DEEM[(df_DEEM.Region_Homologada==option_1) & (df_DEEM.Comuna==option_2)].groupby(['AgnoFechaInicioConvocatoria','Estado_Final']).agg({'idConcurso': 'count'}).reset_index()
    #----------------------------------------------------------------------------------------------------------------------------

    
    df_convocatorias=df_convocatorias.rename(columns={'AgnoFechaInicioConvocatoria':'Año','idConcurso':'Convocatorias'})
    df_estados=df_estados.rename(columns={'AgnoFechaInicioConvocatoria':'Año','idConcurso':'Convocatorias'})
    #----------------------------------------------------------------------------------------------------------------------------
    # grafico Convocatorias por Año
    graf1=px.bar(df_convocatorias,x='Año',y='Convocatorias',title='<b>Convocatorias de directores de escuelas por año</b>',color_discrete_sequence=[color_bar]).\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1)

    # grafico Desiertos y Anulados por Año
    
    graf3=px.bar(df_estados[df_estados['Estado_Concurso'].isin(['Desierto','Anulado'])], x="Año", y="Convocatorias",color='Estado_Concurso',color_discrete_map=estados_edu_color_map ,title="Concursos Desiertos o Anulados").\
             update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1).\
                        update_layout(legend=dict(x=0.5, xanchor='center', y=-0.1, yanchor='top', traceorder='normal', itemsizing='trace',orientation='h'))  # Ubicar debajo del eje x en dos columnas
    
    graf4 = px.pie(df_estados_finales, values='idConcurso', names='Estado_Final',color='Estado_Final',color_discrete_map=estados_edu_color_map).\
                update_layout(legend=dict(x=0.5, xanchor='center', y=-0.1, yanchor='top', traceorder='normal', itemsizing='trace',orientation='h'))
    #estados_edu_color_map
    #----------------------------------------------------------------------------------------------------------------------------
    
    with st.container():
        col1,col2,col3=st.columns(3,gap='small')
        with col1:
            st.plotly_chart(graf1,use_container_width=True)
        with col2:
            st.plotly_chart(graf3,use_container_width=True)
            #st.markdown('gráfico 3')
            #st.dataframe(df_estados[df_estados['Estado_Concurso'].isin(['Desierto','Anulado'])])
        with col3:
           st.plotly_chart(graf4,use_container_width=True)


    
    
    # grafico Seleccionados por Año
    # Create the line plot
    #graf3 = px.line(df_seleccionados, x='year', y='Seleccionados', title='<b>Evolución de cantidad estudiantes seleccionados/as por año</b>')\
    #    .update_yaxes(visible=visible_y_axis, title_text=None)\
    #    .update_xaxes(title_text=None,tickmode='linear', dtick=1)
    #
    #graf3.update_traces(mode='lines+markers', marker=dict(size=8), line_shape='spline', line_color=color_line)
    #----------------------------------------------------------------------------------------------------------------------------
    

    
    
    #col4, col5=st.columns(2,gap='small')
    #with col4:
    #        st.plotly_chart(graf3,use_container_width=True)
    #with col4:
    #        st.text('')
        

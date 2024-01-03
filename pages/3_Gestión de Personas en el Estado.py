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
import glob # necesario para la unificacion de archivos csv
import seaborn as sns

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
color_line='#4A4A4A' #dark grey
color_line_2='#E0701E' #orange
color_line_3='#006FB3' #blue
color_bar='#006FB3' #blue
color_bar_2='#0A132D' #dark blue
color_bar_3='#E0701E' #orange
# Asignar colores de acuerdo a una paleta de colores a cada sexo
sexo_color_map = {'Mujeres': 'orange', 'Hombres': 'blue'} 
metodologia_color_map={'E-Learning': '#00D1C4', 'Híbrida': '#C5D100','Presencial':'#983300','Otra':'#7000D1'}# Mapeo de colores por tipo de metodologia
modo_compra_color_map={'Sin costo': '#19D100', 'Convenio Marco': '#004EB4','Contratación Directa':'#FA0695','Licitación Pública/ Privada':'#D18800','Compra Ágil':'#942201','Compra Coordinada':'#009964'}# Mapeo de colores por tipo de metodologia

respuestas_difusion_color_map={'Si Realiza algún tipo de Difusión de Código': '#19D100', 'No Realiza algún tipo de Difusión de Código': '#004EB4','Sin Respuesta':'#FF0000'}# Mapeo de colores por tipo respuesta
gobierno_color_map={'MB2': '#000789', 'SP1': '#5f6368','SP2':'#0072f0','GB1':'#67f0f2'}# Mapeo de colores por tipo respuesta

with st.sidebar:
    a=st.radio('Gestión de Personas: ',['Capacitación en el Estado','Integridad','Egresos ADP','Normas de Gestión de Personas','Prevención de Maltrato y Acoso Laboral'])




if a=='Capacitación en el Estado':

    def select_servicio(df, option):
        if option == 'Todos':
            unique_servicio = df['Servicio'].unique()
            Servicio = pd.DataFrame({'Servicio': unique_servicio})
            nuevo_registro = pd.DataFrame({'Servicio': ['Todos']})
            Servicio = pd.concat([nuevo_registro, Servicio]).Servicio.tolist()
        else:
            unique_servicio = df.query(f'Ministerio == "{option}"')['Servicio'].unique()
            Servicio = pd.DataFrame({'Servicio': unique_servicio})
            nuevo_registro = pd.DataFrame({'Servicio': ['Todos']})
            Servicio = pd.concat([nuevo_registro, Servicio]).Servicio.tolist()

        return Servicio

    st.title('Capacitación en el Estado')
    # consolidar los archivos csv en un solo dataframe
    # Ruta de los archivos CSV (ajusta la ruta según tu directorio)
    ruta_archivos = 'GestionPersonas/actividades_ejecutadas*.csv'
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
    df_actividades_ejecutadas_sispubli['Modalidad_de_Compra']=np.where(df_actividades_ejecutadas_sispubli['Modalidad_de_Compra']=='No Aplica (Sin Costo)','Sin costo',df_actividades_ejecutadas_sispubli['Modalidad_de_Compra'])
    
    Metodología_de_Aprendizaje_mapping = {'Video Conferencia':'E-Learning',
        'E-Learning/Video Conferencia':'E-Learning',
        'Presencial/E-Learning':'Híbrida',
        'Presencial/Video Conferencia':'Híbrida'}
    df_actividades_ejecutadas_sispubli['Metodología_de_Aprendizaje'] = df_actividades_ejecutadas_sispubli['Metodología_de_Aprendizaje'].replace(Metodología_de_Aprendizaje_mapping)


    df_Ministerios=pd.read_excel('GestionPersonas/Minsiterios_Homologados.xlsx')

    df_actividades_ejecutadas_sispubli=pd.merge(df_actividades_ejecutadas_sispubli,df_Ministerios,how='left',on='Ministerio')
    df_actividades_ejecutadas_sispubli.drop(columns='Ministerio',inplace=True)
    df_actividades_ejecutadas_sispubli=df_actividades_ejecutadas_sispubli.rename(columns={'Min_Homologado':'Ministerio'})

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

    # para 4 variables que toman 2 valores las combinaciones son 16

    if option_1=='Todos' and option_2=='Todos' and option_3=='Todos' and option_4=='Todos': #1
        Actividades=df_actividades_ejecutadas_sispubli.groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli.groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli.groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()
        Metodologia_Actividades=df_actividades_ejecutadas_sispubli.groupby(['Año','Metodología_de_Aprendizaje']).agg({'id_actividad':'sum'}).reset_index()
        Metodologia_Participantes=df_actividades_ejecutadas_sispubli.groupby(['Año','Metodología_de_Aprendizaje']).agg({'Numero_de_Participantes':'sum'}).reset_index()
        Modalidad_Actividades=df_actividades_ejecutadas_sispubli.groupby(['Año','Modalidad_de_Compra']).agg({'id_actividad':'sum'}).reset_index()
    if option_1=='Todos' and option_2!='Todos' and option_3=='Todos'and option_4=='Todos': #2
        Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2)].groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2)].groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2)].groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()
        Metodologia_Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2)].groupby(['Año','Metodología_de_Aprendizaje']).agg({'id_actividad':'sum'}).reset_index()
        Metodologia_Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2)].groupby(['Año','Metodología_de_Aprendizaje']).agg({'Numero_de_Participantes':'sum'}).reset_index()
    if option_1=='Todos' and option_2!='Todos' and option_3!='Todos' and option_4=='Todos': #3
        Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3)].groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3)].groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3)].groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()
    if option_1=='Todos' and option_2!='Todos' and option_3!='Todos' and option_4!='Todos': #4
        Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()
    if option_1!='Todos' and option_2=='Todos' and option_3=='Todos' and option_4=='Todos': #5
        Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1)].groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1)].groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1)].groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()
    if option_1!='Todos' and option_2!='Todos' and option_3=='Todos' and option_4=='Todos': #6
        Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1)].groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1)].groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1)].groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()
    if option_1!='Todos' and option_2!='Todos' and option_3!='Todos' and option_4=='Todos': #7
        Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1) & (df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3)].groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1) & (df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3)].groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1) & (df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3)].groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()
    if option_1!='Todos' and option_2!='Todos' and option_3!='Todos' and option_4!='Todos': #8
        Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3)].groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3)].groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3)].groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()
    if option_1=='Todos' and option_2=='Todos' and option_3!='Todos' and option_4!='Todos': #9
        Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()
    if option_1!='Todos' and option_2=='Todos' and option_3!='Todos' and option_4!='Todos': #10
        Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()
    if option_1=='Todos' and option_2=='Todos' and option_3=='Todos' and option_4!='Todos': #11
        Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()
    if option_1!='Todos' and option_2!='Todos' and option_3=='Todos' and option_4!='Todos': #12
        Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1) & (df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1) & (df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1) & (df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()
    if option_1=='Todos' and option_2=='Todos' and option_3!='Todos' and option_4=='Todos': #13
        Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3)].groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3)].groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3)].groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()
    if option_1=='Todos' and option_2!='Todos' and option_3=='Todos' and option_4!='Todos': #14
        Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()
    if option_1!='Todos' and option_2=='Todos' and option_3=='Todos' and option_4!='Todos': #15
        Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1) & (df_actividades_ejecutadas_sispubli.Metodología_de_Aprendizaje==option_4)].groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()
    if option_1!='Todos' and option_2=='Todos' and option_3!='Todos' and option_4=='Todos': #16
        Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3)].groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3)].groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Ministerio==option_1) & (df_actividades_ejecutadas_sispubli.Modalidad_de_Compra==option_3)].groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()

    
    Actividades=Actividades.rename(columns={'id_actividad':'Actividades'})
    Inversion=Inversion.rename(columns={'Gasto_monto_Item001':'Inversion'})
    Participantes=Participantes.rename(columns={'Numero_de_Participantes':'Participantes'})
    Metodologia_Actividades=Metodologia_Actividades.rename(columns={'id_actividad':'Actividades'})
    Modalidad_Actividades=Modalidad_Actividades.rename(columns={'id_actividad':'Actividades'})


    graf1=px.bar(Actividades,x='Año',y='Actividades',title='<b>Cantidad de capacitaciones realizadas por año</b>',color_discrete_sequence=[color_bar]).\
                 update_yaxes(visible=visible_y_axis,title_text=None).\
                      update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    graf1.update_layout(yaxis_tickformat='.0f')
    

    graf2=px.line(Inversion,x='Año',y='Inversion',title='<b>Inversión en capacitación realizadas por año [MM$]</b>').\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    graf2.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_line)
    graf2.update_layout(yaxis_tickformat='.0f')

    graf3=px.bar(Participantes,x='Año',y='Participantes',title='<b>Cantidad total de participantes a capacitaciones por año</b>',color_discrete_sequence=[color_bar_3]).\
                 update_yaxes(visible=visible_y_axis,title_text=None).\
                      update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    graf3.update_layout(yaxis_tickformat='.0f')

    #df_treemap=df_actividades_ejecutadas_sispubli.groupby(['Ministerio','Servicio','Modalidad_de_Compra','Metodologia_de_Aprendizaje']).agg({'Gasto_monto_Item001':'sum'}).reset_index()
    #df_treemap=df_treemap.rename(columns={'Gasto_monto_Item001':'Inversion'})
    #df_treemap['Todos']='Todos'
    

    graf4 = px.bar(Metodologia_Actividades, x="Año", y="Actividades",color='Metodología_de_Aprendizaje',color_discrete_map=metodologia_color_map, title="Cantidad de capacitaciones por metodología de aprendizaje")

    #graf5=go.Figure(data=[go.Pie(labels=Modalidad_Actividades.Modalidad_de_Compra,values=Modalidad_Actividades.Actividades,hole=0.5,color='Modalidad_de_Compra',color_discrete_map=modo_compra_color_map)])    
    
    graf5 = go.Figure(data=[
    go.Pie(
        labels=Modalidad_Actividades['Modalidad_de_Compra'],
        values=Modalidad_Actividades['Actividades'],
        hole=0.5,
        marker_colors=[modo_compra_color_map[modalidad] for modalidad in Modalidad_Actividades['Modalidad_de_Compra']]
    )
])



    graf5.update_layout(title_text="Distribución de capacitaciones por modalidad de compra")

    inversion_promedio=np.round(Inversion['Inversion'].sum()/Participantes['Participantes'].sum(),0)
    total_actividades=Actividades['Actividades'].sum()
    total_participantes=Participantes['Participantes'].sum()
    total_inversion=np.round(Inversion['Inversion'].sum()/1_000_000,0)

    with st.container():
        col2,col3,col4,col5=st.columns(4,gap='small')
        #with col1:
        #    st.markdown(f"<h2 style='text-align: center; color: grey;'>Entre el 2016 y {df_actividades_ejecutadas_sispubli.Año.max()} la cantidad de capacitaciones realizadas es</h2>", unsafe_allow_html=True)
        with col2:
            valor_col2=f"{total_actividades:,}"#.replace(",", ".")
            st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col2}</h1>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: grey;'>Total actividades de capacitación realizadas</h2>", unsafe_allow_html=True)
        with col3:
            valor_col3=f"{total_participantes:,}"#.replace(",", ".")
            st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col3}</h1>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: grey;'>Total de participantes</h2>", unsafe_allow_html=True)
        
        with col4:
            valor_col4=f"{total_inversion:,}"#.replace(",", ".")
            st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col4}</h1>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: grey;'>Total inversión en capacitación [$MM]</h2>", unsafe_allow_html=True)
        with col5:
            valor_col5=f"{inversion_promedio:,}"#.replace(",", ".")
            st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col5}</h1>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: grey;'>Inversión Promedio por participante</h2>", unsafe_allow_html=True)



    with st.container():
        col1,col2,col3=st.columns(3,gap='small')
        with col1:    
            st.plotly_chart(graf1,use_container_width=True)
        with col2:
            st.plotly_chart(graf3,use_container_width=True)
        with col3:
            st.plotly_chart(graf2,use_container_width=True)
    with st.container():
        col4,col5=st.columns(2,gap='small')
        with col4:
            st.plotly_chart(graf4,use_container_width=True)
        with col5:
            st.plotly_chart(graf5,use_container_width=True)




    #st.text(df_actividades_ejecutadas_sispubli.Año.unique())
#---------------------------------------------------------------------------------------------------
if a=='Integridad':
    st.title('Integridad en el Estado')

    df_integridad=pd.read_csv('GestionPersonas/bbdd_integridad.csv',sep=',')
    #mt_organismos_integridad=pd.read_excel('GestionPersonas/mt_organismos_integridad.xlsx',sheet_name='Hoja1')   
    #df_integridad=pd.merge(df_integridad,mt_organismos_integridad,how='left',left_on='Servicio',right_on='INSTITUCIÓN')

    unique_ministerios = df_integridad['Ministerio'].unique()
    Ministerios = pd.DataFrame({'Ministerio': unique_ministerios})
    nuevo_registro = pd.DataFrame({'Ministerio': ['Todos']})
    Ministerios = pd.concat([nuevo_registro, Ministerios])
    Ministerios = Ministerios.reset_index(drop=True)
    Ministerios = Ministerios['Ministerio'].tolist()

    def select_servicio(df, option):
        if option == 'Todos':
            unique_servicio = df['Servicio'].unique()
            Servicio = pd.DataFrame({'Servicio': unique_servicio})
            nuevo_registro = pd.DataFrame({'Servicio': ['Todos']})
            Servicio = pd.concat([nuevo_registro, Servicio]).Servicio.tolist()
        else:
            unique_servicio = df.query(f'Ministerio == "{option}"')['Servicio'].unique()
            Servicio = pd.DataFrame({'Servicio': unique_servicio})
            nuevo_registro = pd.DataFrame({'Servicio': ['Todos']})
            Servicio = pd.concat([nuevo_registro, Servicio]).Servicio.tolist()
        return Servicio
    


    #-------------------------------------------------------------------------------------------------------

    with st.container():
        option_1 = st.selectbox('Ministerio',Ministerios)
        # col1,col2=st.columns(2,gap="large")
        # with col1:
        #    option_1 = st.selectbox('Ministerio',Ministerios)
        # with col2:
        #     grafico_1=st.selectbox("Selecciona como quieres ver el dato",["Gráfico","Tabla"],key="1")
    #-------------------------------------------------------------------------------------------------------
    # datos difusión codigos de etica y grafico
    if option_1=='Todos':
        df_difusion=df_integridad[df_integridad['Pregunta']=='Difusión de Código de Etica']
    else:
        df_difusion=df_integridad[(df_integridad['Pregunta']=='Difusión de Código de Etica') & (df_integridad['Ministerio']==option_1)]
    
    df_difusion['Resp_1']=np.where(df_difusion.Respuesta=='Si Realiza algún tipo de Difusión de Código',1,0)
    df_difusion['Resp_2']=np.where(df_difusion.Respuesta=='No Realiza algún tipo de Difusión de Código',1,0)
    df_difusion['Resp_3']=np.where(df_difusion.Respuesta=='Sin Respuesta',1,0)

    tabla_difusion=df_difusion.groupby(['Ministerio']).agg({'Resp_1':'sum','Resp_2':'sum','Resp_3':'sum'}).reset_index()
    tabla_difusion_melted = pd.melt(tabla_difusion, id_vars=['Ministerio'], value_vars=['Resp_1', 'Resp_2', 'Resp_3'], var_name='Respuesta', value_name='Valor')
  
    tabla_difusion_melted['Respuesta'] = np.where(
        tabla_difusion_melted['Respuesta'] == 'Resp_1', 'Si Realiza algún tipo de Difusión de Código',
        np.where(tabla_difusion_melted['Respuesta'] == 'Resp_2', 'No Realiza algún tipo de Difusión de Código', 'Sin Respuesta')
    )
    
    df_difusion_all=df_integridad[df_integridad['Pregunta']=='Difusión de Código de Etica']
    df_difusion_all['Resp_1']=np.where(df_difusion_all.Respuesta=='Si Realiza algún tipo de Difusión de Código',1,0)
    df_difusion_all['Resp_2']=np.where(df_difusion_all.Respuesta=='No Realiza algún tipo de Difusión de Código',1,0)
    df_difusion_all['Resp_3']=np.where(df_difusion_all.Respuesta=='Sin Respuesta',1,0)

    tabla_difusion_all=df_difusion_all.groupby(['Ministerio']).agg({'Resp_1':'sum','Resp_2':'sum','Resp_3':'sum'}).reset_index()
    tabla_difusion_melted_all = pd.melt(tabla_difusion_all, id_vars=['Ministerio'], value_vars=['Resp_1', 'Resp_2', 'Resp_3'], var_name='Respuesta', value_name='Valor')
  
    tabla_difusion_melted_all['Respuesta'] = np.where(
        tabla_difusion_melted_all['Respuesta'] == 'Resp_1', 'Si Realiza algún tipo de Difusión de Código',
        np.where(tabla_difusion_melted_all['Respuesta'] == 'Resp_2', 'No Realiza algún tipo de Difusión de Código', 'Sin Respuesta')
    )
    tabla_difusion_melted_group=tabla_difusion_melted.groupby('Ministerio')['Valor'].sum().reset_index()
    tabla_difusion_melted_group=tabla_difusion_melted_group.rename(columns={'Valor':'Total'})
    tabla_difusion_melted=pd.merge(tabla_difusion_melted,tabla_difusion_melted_group,how='left',on='Ministerio')
    tabla_difusion_melted['Porcentaje']=np.round(tabla_difusion_melted['Valor']/tabla_difusion_melted['Total'],2)*100

    graf1 = go.Figure(data=[
    go.Pie(
        labels=tabla_difusion_melted_all['Respuesta'],
        values=tabla_difusion_melted_all['Valor'],
        hole=0.5,
        marker_colors=[respuestas_difusion_color_map[Respuesta] for Respuesta in tabla_difusion_melted_all['Respuesta']]
        )
    ])
    graf1.update_layout(
    title_text="Distribución de difusión de códigos de ética",
    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="right", x=0.7)
    )


    graf2=px.bar(tabla_difusion_melted,x='Ministerio',y='Porcentaje',color='Respuesta',
                 color_discrete_map=respuestas_difusion_color_map,
                 title="Servicios que difunden sus códigos de ética por Ministerio")
    #graf2.update_layout(yaxis_tickformat='.0f',legend=dict(orientation="h"),
    #                    xaxis_title="Ministerio",yaxis_title="Valor",title_x=0.5,
    #                    margin=dict(l=0, r=0, b=0, t=40))
    graf2.update_layout(showlegend=False,xaxis_title=None)

    #-------------------------------------------------------------------------------------------------------
    with st.container():
        st.subheader("Instituciones que difunden su Código de Ética")
        col1,col2=st.columns([0.3, 0.7])
        with col1:
            st.plotly_chart(graf1,use_container_width=True)
        with col2:
            grafico_2=st.selectbox("Selecciona como quieres ver el dato",["Gráfico","Tabla"],key="1")
            if grafico_2=="Gráfico":
                st.plotly_chart(graf2,use_container_width=True)
            else:
                st.dataframe(df_integridad[df_integridad['Pregunta']=='Difusión de Código de Etica'],width=1300)
                st.download_button(label="Descargar datos",data=df_integridad[df_integridad['Pregunta']=='Difusión de Código de Etica'].to_csv().encode("utf-8"),file_name=f"Difusion Cod Etica.csv",mime="text/csv")
                
    #st.dataframe(tabla_difusion_melted.head(20))
    #st.dataframe(tabla_difusion_melted_group.head(20))    
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
if a=='Egresos ADP':
    @st.cache_data
    def egresos_adp():
        df_1=pd.read_excel('ADP/egresos_adp.xlsx',sheet_name='Graf I Nivel Datastudio')
        df_2=pd.read_excel('ADP/egresos_adp.xlsx',sheet_name='Graf II Nivel Datastudio')
        df_1_2=pd.read_excel('ADP/egresos_adp.xlsx',sheet_name='Graf I y II Nivel Datastudio')
        df_egresos_adp=pd.concat([df_1,df_2,df_1_2])
        return df_egresos_adp

    df_egresos_adp=egresos_adp()

    st.title('Egresos ADP')
    texto_egresos_adp_1="""Como una manera de contribuir a la transparencia en la gestión pública, el Servicio Civil pone a disposición de la ciudadanía las cifras de renuncias voluntarias y no voluntarias del Sistema de Alta Dirección Pública, desde el 11 de marzo de 2022 a la fecha, que son informadas vía oficio a nuestra institución."""
    texto_egresos_adp_2="""Consideraciones"""
    with st.expander(texto_egresos_adp_2):
        st.write("""
            1 Los porcentajes de vacancias son calculados en base a la cantidad de cargos directivos al inicio de cada gobierno.\n
            2 Las vacancias son consideradas en la fecha en la cual se hace efectiva la renuncia y no la fecha de recepción del documento.\n
            3 Las cifras de los años 2010 y 2014 no son comparables con los períodos siguientes, pues son previas a la dictación de la Ley N°20.955, de 2016, que perfeccionó el Sistema de Alta Dirección Pública.
        """)
    #gráfico porcentaje postulaciones por año y sexo segun seleccion portal
    valor_min=0
    valor_max=94
    
    graf1=px.line(df_egresos_adp[(df_egresos_adp['Nivel']=='I') & (df_egresos_adp['Motivo']=='Total')],x='Semana',y='% Egreso Acumulado',\
                  title='<b>Porcentaje de renuncias no voluntarias, voluntarias y no renovaciones de jefaturas de servicio ADP</b>',\
                    color='Gobierno',color_discrete_map=gobierno_color_map).\
                        update_yaxes(visible=True,title_text=None).\
                            update_xaxes(title_text='Semana de Gobierno',tickmode='linear', dtick=4,tickangle=-45,autorange=False, range=[valor_min, valor_max])
    graf1.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline')
    graf1.update_layout(yaxis_tickformat='.0%')

    graf2=px.line(df_egresos_adp[(df_egresos_adp['Nivel']=='I') & (df_egresos_adp['Motivo']=='No Voluntario')],x='Semana',y='% Egreso Acumulado',\
                  title='<b>Porcentaje de renuncias no voluntarias de jefaturas de servicio</b>',\
                    color='Gobierno',color_discrete_map=gobierno_color_map).\
                        update_yaxes(visible=True,title_text=None).\
                            update_xaxes(title_text='Semana de Gobierno',tickmode='linear', dtick=4,tickangle=-45,autorange=False, range=[valor_min, valor_max])
    graf2.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline')
    graf2.update_layout(yaxis_tickformat='.0%')

    graf3=px.line(df_egresos_adp[(df_egresos_adp['Nivel']=='II') & (df_egresos_adp['Motivo']=='Total')],x='Semana',y='% Egreso Acumulado',\
                  title='<b>Porcentaje de renuncias no voluntarias, voluntarias y no renovaciones de jefaturas de servicio ADP</b>',\
                    color='Gobierno',color_discrete_map=gobierno_color_map).\
                        update_yaxes(visible=True,title_text=None).\
                            update_xaxes(title_text='Semana de Gobierno',tickmode='linear', dtick=4,tickangle=-45,autorange=False, range=[valor_min, valor_max])
    graf3.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline')
    graf3.update_layout(yaxis_tickformat='.0%')

    graf4=px.line(df_egresos_adp[(df_egresos_adp['Nivel']=='II') & (df_egresos_adp['Motivo']=='No Voluntario')],x='Semana',y='% Egreso Acumulado',\
                  title='<b>Porcentaje de renuncias no voluntarias de jefaturas de servicio</b>',\
                    color='Gobierno',color_discrete_map=gobierno_color_map).\
                        update_yaxes(visible=True,title_text=None).\
                            update_xaxes(title_text='Semana de Gobierno',tickmode='linear',dtick=4,tickangle=-45,autorange=False, range=[valor_min, valor_max])
    graf4.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline')
    graf4.update_layout(yaxis_tickformat='.0%')

    graf5=px.line(df_egresos_adp[(df_egresos_adp['Nivel']=='Todos') & (df_egresos_adp['Motivo']=='Total')],x='Semana',y='% Egreso Acumulado',\
                  title='<b>Porcentaje de renuncias no voluntarias, voluntarias y no renovaciones en cargos de primer y segundo nivel ADP</b>',\
                    color='Gobierno',color_discrete_map=gobierno_color_map).\
                        update_yaxes(visible=True,title_text=None).\
                            update_xaxes(title_text='Semana de Gobierno',tickmode='linear', dtick=4,tickangle=-45,autorange=False, range=[valor_min, valor_max])
    graf5.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline')
    graf5.update_layout(yaxis_tickformat='.0%')

    graf6=px.line(df_egresos_adp[(df_egresos_adp['Nivel']=='Todos') & (df_egresos_adp['Motivo']=='No Voluntario')],x='Semana',y='% Egreso Acumulado',\
                  title='<b>Porcentaje de renuncias no voluntarias en cargos de primer y segundo nivel ADP</b>',\
                    color='Gobierno',color_discrete_map=gobierno_color_map).\
                        update_yaxes(visible=True,title_text=None).\
                            update_xaxes(title_text='Semana de Gobierno',tickmode='linear',dtick=4,tickangle=-45,autorange=False, range=[valor_min, valor_max])
    graf6.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline')
    graf6.update_layout(yaxis_tickformat='.0%')

    columnas_df_egresos=['Gobierno','Año','Semana','Motivo','Cargos','Egresos','% Egreso Acumulado','Nivel']

    st.subheader("Estadísticas egresos de jefaturas de primer nivel ADP")
    with st.container():
        col1,col2=st.columns(2,gap='small')
        with col1:
            st.plotly_chart(graf1,use_container_width=True)
        with col2:
            st.plotly_chart(graf2,use_container_width=True)

    st.subheader("Estadísticas egresos de jefaturas de segundo nivel ADP")
    with st.container():
        col1,col2=st.columns(2,gap='small')
        with col1:
            st.plotly_chart(graf3,use_container_width=True)
        with col2:
            st.plotly_chart(graf4,use_container_width=True)
    
    st.subheader("Estadísticas egresos de jefaturas de primer y segundo nivel ADP")
    with st.container():
        col1,col2=st.columns(2,gap='small')
        with col1:
            st.plotly_chart(graf5,use_container_width=True)
        with col2:
            st.plotly_chart(graf6,use_container_width=True)

    with st.container():
        st.subheader("Base de Egresos del Sistema de Alta Dirección Pública")
        st.text('Muestra primeras 20 líneas de la base de datos')
        st.dataframe(df_egresos_adp[columnas_df_egresos].head(20), width=1300)
        st.download_button(label="Descargar datos",data=egresos_adp().to_csv().encode("utf-8"),file_name=f"Egresos ADP.csv",mime="text/csv")
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
if a=='Normas de Gestión de Personas':
    st.title('Indicadores de Normas de Aplicación General en Gestión y Desarrollo de Personas')

    def Normas_Gestion_Personas():
        Normas_GP=pd.read_excel('GestionPersonas/Normas_GP.xlsx',sheet_name='BBDD')  
        return Normas_GP

    df_normas_gp=Normas_Gestion_Personas()

    unique_ministerios = df_normas_gp.Ministerio.unique()
    Ministerios = pd.DataFrame({'Ministerio': unique_ministerios})
    nuevo_registro = pd.DataFrame({'Ministerio': ['Todos']})
    Ministerios = pd.concat([nuevo_registro, Ministerios])
    Ministerios = Ministerios.reset_index(drop=True)
    Ministerios = Ministerios['Ministerio'].tolist()

    def select_servicio_ngp(df, option):
        if option == 'Todos':
            unique_servicio = df['Servicio'].unique()
            Servicio = pd.DataFrame({'Servicio': unique_servicio})
            nuevo_registro = pd.DataFrame({'Servicio': ['Todos']})
            Servicio = pd.concat([nuevo_registro, Servicio]).Servicio.tolist()
        else:
            unique_servicio = df.query(f'Ministerio == "{option}"')['Servicio'].unique()
            Servicio = pd.DataFrame({'Servicio': unique_servicio})
            nuevo_registro = pd.DataFrame({'Servicio': ['Todos']})
            Servicio = pd.concat([nuevo_registro, Servicio]).Servicio.tolist()
        return Servicio

    #filtros
    with st.container():
        col1,col2=st.columns(2,gap="large")
        with col1:
           option_7 = st.selectbox('Ministerio',Ministerios,key="7")
        with col2:
           option_8 = st.selectbox('Institución / Servicio',select_servicio_ngp(df_normas_gp,option_7),key="8")


    if option_7=='Todos' and option_8=='Todos':
        Norma_1=df_normas_gp.query('ID_Norma==1').groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_2=df_normas_gp.query('ID_Norma==2').groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_3=df_normas_gp.query('ID_Norma==3').groupby(['Año']).agg({'Norma_3_Ingresos_con_Procedimiento':'sum','Norma_3_Ingresos_totales':'sum'}).reset_index()
        Norma_4=df_normas_gp.query('ID_Norma==4').groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_5=df_normas_gp.query('ID_Norma==5').groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_6=df_normas_gp.query('ID_Norma==6').groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_7=df_normas_gp.query('ID_Norma==7').groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_8=df_normas_gp.query('ID_Norma==8').groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_9=df_normas_gp.query('ID_Norma==9').groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_10=df_normas_gp.query('ID_Norma==10').groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_11=df_normas_gp.query('ID_Norma==11').groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        

    if option_7!='Todos' and option_8=='Todos':
        Norma_1=df_normas_gp.query('ID_Norma==1')[df_normas_gp['Ministerio']==option_7].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_2=df_normas_gp.query('ID_Norma==2')[df_normas_gp['Ministerio']==option_7].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_3=df_normas_gp.query('ID_Norma==3')[df_normas_gp['Ministerio']==option_7].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_4=df_normas_gp.query('ID_Norma==4')[df_normas_gp['Ministerio']==option_7].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_5=df_normas_gp.query('ID_Norma==5')[df_normas_gp['Ministerio']==option_7].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_6=df_normas_gp.query('ID_Norma==6')[df_normas_gp['Ministerio']==option_7].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_7=df_normas_gp.query('ID_Norma==7')[df_normas_gp['Ministerio']==option_7].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_8=df_normas_gp.query('ID_Norma==8')[df_normas_gp['Ministerio']==option_7].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_9=df_normas_gp.query('ID_Norma==9')[df_normas_gp['Ministerio']==option_7].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_10=df_normas_gp.query('ID_Norma==10')[df_normas_gp['Ministerio']==option_7].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_11=df_normas_gp.query('ID_Norma==11')[df_normas_gp['Ministerio']==option_7].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()

   

    if option_7!='Todos' and option_8!='Todos':
        Norma_1=df_normas_gp.query('ID_Norma==1')[(df_normas_gp['Ministerio']==option_7) & (df_normas_gp['Servicio']==option_8)].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_2=df_normas_gp.query('ID_Norma==2')[(df_normas_gp['Ministerio']==option_7) & (df_normas_gp['Servicio']==option_8)].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_3=df_normas_gp.query('ID_Norma==3')[(df_normas_gp['Ministerio']==option_7) & (df_normas_gp['Servicio']==option_8)].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_4=df_normas_gp.query('ID_Norma==4')[(df_normas_gp['Ministerio']==option_7) & (df_normas_gp['Servicio']==option_8)].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_5=df_normas_gp.query('ID_Norma==5')[(df_normas_gp['Ministerio']==option_7) & (df_normas_gp['Servicio']==option_8)].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_6=df_normas_gp.query('ID_Norma==6')[(df_normas_gp['Ministerio']==option_7) & (df_normas_gp['Servicio']==option_8)].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_7=df_normas_gp.query('ID_Norma==7')[(df_normas_gp['Ministerio']==option_7) & (df_normas_gp['Servicio']==option_8)].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_8=df_normas_gp.query('ID_Norma==8')[(df_normas_gp['Ministerio']==option_7) & (df_normas_gp['Servicio']==option_8)].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_9=df_normas_gp.query('ID_Norma==9')[(df_normas_gp['Ministerio']==option_7) & (df_normas_gp['Servicio']==option_8)].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_10=df_normas_gp.query('ID_Norma==10')[(df_normas_gp['Ministerio']==option_7) & (df_normas_gp['Servicio']==option_8)].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_11=df_normas_gp.query('ID_Norma==11')[(df_normas_gp['Ministerio']==option_7) & (df_normas_gp['Servicio']==option_8)].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()

  

    if option_7=='Todos' and option_8!='Todos':
        Norma_1=df_normas_gp.query('ID_Norma==1')[df_normas_gp['Servicio']==option_8].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_2=df_normas_gp.query('ID_Norma==2')[df_normas_gp['Servicio']==option_8].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_3=df_normas_gp.query('ID_Norma==3')[df_normas_gp['Servicio']==option_8].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_4=df_normas_gp.query('ID_Norma==4')[df_normas_gp['Servicio']==option_8].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_5=df_normas_gp.query('ID_Norma==5')[df_normas_gp['Servicio']==option_8].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_6=df_normas_gp.query('ID_Norma==6')[df_normas_gp['Servicio']==option_8].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_7=df_normas_gp.query('ID_Norma==7')[df_normas_gp['Servicio']==option_8].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_8=df_normas_gp.query('ID_Norma==8')[df_normas_gp['Servicio']==option_8].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_9=df_normas_gp.query('ID_Norma==9')[df_normas_gp['Servicio']==option_8].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_10=df_normas_gp.query('ID_Norma==10')[df_normas_gp['Servicio']==option_8].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()
        Norma_11=df_normas_gp.query('ID_Norma==11')[df_normas_gp['Servicio']==option_8].groupby(['Año']).agg({'SSPP_Considerado':'sum','Cumplimiento':'sum'}).reset_index()

  

    Norma_1['Metrica']=np.where(Norma_1['SSPP_Considerado']==0,0,Norma_1['Cumplimiento']/Norma_1['SSPP_Considerado'])
    Norma_2['Metrica']=np.where(Norma_2['SSPP_Considerado']==0,0,Norma_2['Cumplimiento']/Norma_2['SSPP_Considerado'])
    Norma_3['Metrica']=np.where(Norma_3['Norma_3_Ingresos_totales']==0,0,Norma_3['Norma_3_Ingresos_con_Procedimiento']/Norma_3['Norma_3_Ingresos_totales'])
    Norma_4['Metrica']=Norma_4['Cumplimiento']
    Norma_5['Metrica']=np.where(Norma_5['SSPP_Considerado']==0,0,Norma_5['Cumplimiento']/Norma_5['SSPP_Considerado'])
    Norma_6['Metrica']=Norma_6['Cumplimiento']
    Norma_7['Metrica']=np.where(Norma_7['SSPP_Considerado']==0,0,Norma_7['Cumplimiento']/Norma_7['SSPP_Considerado'])
    Norma_8['Metrica']=np.where(Norma_8['SSPP_Considerado']==0,0,Norma_8['Cumplimiento']/Norma_8['SSPP_Considerado'])
    Norma_9['Metrica']=Norma_9['Cumplimiento']
    Norma_10['Metrica']=np.where(Norma_10['SSPP_Considerado']==0,0,Norma_10['Cumplimiento']/Norma_10['SSPP_Considerado'])
    Norma_11['Metrica']=np.where(Norma_11['SSPP_Considerado']==0,0,Norma_11['Cumplimiento']/Norma_11['SSPP_Considerado'])

    with st.container():
        col1,col2,col3=st.columns(3,gap='small')
        with col1:
            col_1_1,col_1_2,col_1_3,col_1_4,col_1_5=st.columns(5,gap='small')
            texto_Norma_1="""Porcentaje de Jefaturas de Gestión de Personas que se encuentran en un 2do o 3er Nivel Jerárquico"""
            valor_col_1_1 =f"{Norma_1.query('Año==2018').Metrica.iloc[0]:.2%}"
            valor_col_1_2 =f"{Norma_1.query('Año==2019').Metrica.iloc[0]:.2%}"
            valor_col_1_3 =f"{Norma_1.query('Año==2020').Metrica.iloc[0]:.2%}"
            valor_col_1_4 =f"{Norma_1.query('Año==2021').Metrica.iloc[0]:.2%}"
            valor_col_1_5 =f"{Norma_1.query('Año==2022').Metrica.iloc[0]:.2%}"

            with col_1_1:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_1_1}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2018</h3>", unsafe_allow_html=True)
            with col_1_2:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_1_2}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2019</h3>", unsafe_allow_html=True)
            with col_1_3:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_1_3}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2020</h3>", unsafe_allow_html=True)
            with col_1_4:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_1_4}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2021</h3>", unsafe_allow_html=True)
            with col_1_5:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_1_5}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2022</h3>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: grey;'>{texto_Norma_1}</h2>", unsafe_allow_html=True)

        with col2:
            col_2_1,col_2_2,col_2_3,col_2_4,col_2_5=st.columns(5,gap='small')
            texto_Norma_2="""Porcentaje de Servicios Públicos que tienen una Política de Gestión de Personas con estándares del Servicio Civil"""
            valor_col_2_1=f"{Norma_2.query('Año==2018').Metrica.iloc[0]:.2%}"
            valor_col_2_2=f"{Norma_2.query('Año==2019').Metrica.iloc[0]:.2%}"
            valor_col_2_3=f"{Norma_2.query('Año==2020').Metrica.iloc[0]:.2%}"
            valor_col_2_4=f"{Norma_2.query('Año==2021').Metrica.iloc[0]:.2%}"
            valor_col_2_5=f"{Norma_2.query('Año==2022').Metrica.iloc[0]:.2%}"
            with col_2_1:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_2_1}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2018</h3>", unsafe_allow_html=True)
            with col_2_2:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_2_2}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2019</h3>", unsafe_allow_html=True)
            with col_2_3:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_2_3}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2020</h3>", unsafe_allow_html=True)
            with col_2_4:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_2_4}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2021</h3>", unsafe_allow_html=True)
            with col_2_5:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_2_5}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2022</h3>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: grey;'>{texto_Norma_2}</h2>", unsafe_allow_html=True)
        
        with col3:
            col_3_1,col_3_2,col_3_3,col_3_4,col_3_5=st.columns(5,gap='small')
            texto_Norma_3="""Porcentaje de ingresos a la Contrata y/o Código del Trabajo cubiertos por procesos de Reclutamiento y Selección"""
            valor_col_3_1=f"{Norma_3.query('Año==2018').Metrica.iloc[0]:.2%}"
            valor_col_3_2=f"{Norma_3.query('Año==2019').Metrica.iloc[0]:.2%}"
            valor_col_3_3=f"{Norma_3.query('Año==2020').Metrica.iloc[0]:.2%}"
            valor_col_3_4=f"{Norma_3.query('Año==2021').Metrica.iloc[0]:.2%}"
            valor_col_3_5=f"{Norma_3.query('Año==2022').Metrica.iloc[0]:.2%}"
            with col_3_1:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_3_1}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2018</h3>", unsafe_allow_html=True)
            with col_3_2:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_3_2}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2019</h3>", unsafe_allow_html=True)
            with col_3_3:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_3_3}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2020</h3>", unsafe_allow_html=True)
            with col_3_4:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_3_4}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2021</h3>", unsafe_allow_html=True)
            with col_3_5:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_3_5}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2022</h3>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: grey;'>{texto_Norma_3}</h2>", unsafe_allow_html=True)
    
    with st.container():
        col4,col5,col6=st.columns(3,gap='small')
        with col4:
            col_4_1,col_4_2,col_4_3,col_4_4,col_4_5=st.columns(5,gap='small')
            texto_Norma_4="""Total de Vacantes de planta que se concursaron para los diferentes tipos de concursos"""
            valor_col_4_1=f"{Norma_4.query('Año==2018').Metrica.iloc[0]:,}"
            valor_col_4_2=f"{Norma_4.query('Año==2019').Metrica.iloc[0]:,}"
            valor_col_4_3=f"{Norma_4.query('Año==2020').Metrica.iloc[0]:,}"
            valor_col_4_4=f"{Norma_4.query('Año==2021').Metrica.iloc[0]:,}"
            valor_col_4_5=f"{Norma_4.query('Año==2022').Metrica.iloc[0]:,}"
            with col_4_1:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_4_1}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2018</h3>", unsafe_allow_html=True)
            with col_4_2:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_4_2}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2019</h3>", unsafe_allow_html=True)
            with col_4_3:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_4_3}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2020</h3>", unsafe_allow_html=True)
            with col_4_4:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_4_4}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2021</h3>", unsafe_allow_html=True)
            with col_4_5:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_4_5}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2022</h3>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: grey;'>{texto_Norma_4}</h2>", unsafe_allow_html=True)

        with col5:
            col_5_1,col_5_2,col_5_3,col_5_4,col_5_5=st.columns(5,gap='small')
            texto_Norma_5="""Porcentaje de Servicios Públicos que declaran haber realizado Inducción en un plazo menor a 30 días"""
            valor_col_5_1=f"{Norma_5.query('Año==2018').Metrica.iloc[0]:.2%}"
            valor_col_5_2=f"{Norma_5.query('Año==2019').Metrica.iloc[0]:.2%}"
            valor_col_5_3=f"{Norma_5.query('Año==2020').Metrica.iloc[0]:.2%}"
            valor_col_5_4=f"{Norma_5.query('Año==2021').Metrica.iloc[0]:.2%}"
            valor_col_5_5=f"{Norma_5.query('Año==2022').Metrica.iloc[0]:.2%}"
            with col_5_1:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_5_1}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2018</h3>", unsafe_allow_html=True)
            with col_5_2:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_5_2}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2019</h3>", unsafe_allow_html=True)
            with col_5_3:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_5_3}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2020</h3>", unsafe_allow_html=True)
            with col_5_4:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_5_4}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2021</h3>", unsafe_allow_html=True)
            with col_5_5:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_5_5}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2022</h3>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: grey;'>{texto_Norma_5}</h2>", unsafe_allow_html=True)

        with col6:
            col_6_1,col_6_2,col_6_3,col_6_4,col_6_5=st.columns(5,gap='small')
            texto_Norma_6="""Total de estudiantes seleccionados"""
            valor_col_6_1=f"{Norma_6.query('Año==2018').Metrica.iloc[0]:,}"
            valor_col_6_2=f"{Norma_6.query('Año==2019').Metrica.iloc[0]:,}"
            valor_col_6_3=f"{Norma_6.query('Año==2020').Metrica.iloc[0]:,}"
            valor_col_6_4=f"{Norma_6.query('Año==2021').Metrica.iloc[0]:,}"
            valor_col_6_5=f"{Norma_6.query('Año==2022').Metrica.iloc[0]:,}"
            with col_6_1:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_6_1}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2018</h3>", unsafe_allow_html=True)
            with col_6_2:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_6_2}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2019</h3>", unsafe_allow_html=True)
            with col_6_3:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_6_3}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2020</h3>", unsafe_allow_html=True)
            with col_6_4:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_6_4}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2021</h3>", unsafe_allow_html=True)
            with col_6_5:
                st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_6_5}</h3>", unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center; color: grey;'>2022</h3>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: grey;'>{texto_Norma_6}</h2>", unsafe_allow_html=True)
        
        with st.container():
            col7,col8,col9=st.columns(3,gap='small')
            with col7:
                col_4_1,col_4_2,col_4_3,col_4_4,col_4_5=st.columns(5,gap='small')
                texto_Norma_4="""Total de Vacantes de planta que se concursaron para los diferentes tipos de concursos"""
                valor_col_4_1=f"{Norma_4.query('Año==2018').Metrica.iloc[0]:,}"
                valor_col_4_2=f"{Norma_4.query('Año==2019').Metrica.iloc[0]:,}"
                valor_col_4_3=f"{Norma_4.query('Año==2020').Metrica.iloc[0]:,}"
                valor_col_4_4=f"{Norma_4.query('Año==2021').Metrica.iloc[0]:,}"
                valor_col_4_5=f"{Norma_4.query('Año==2022').Metrica.iloc[0]:,}"
                with col_4_1:
                    st.markdown(f"<h5 style='text-align: center; color: grey;'>{valor_col_4_1}</h5>", unsafe_allow_html=True)
                    st.markdown("<h5 style='text-align: center; color: grey;'>2018</h5>", unsafe_allow_html=True)
                with col_4_2:
                    st.markdown(f"<h5 style='text-align: center; color: grey;'>{valor_col_4_2}</h5>", unsafe_allow_html=True)
                    st.markdown("<h5 style='text-align: center; color: grey;'>2019</h5>", unsafe_allow_html=True)
                with col_4_3:
                    st.markdown(f"<h5 style='text-align: center; color: grey;'>{valor_col_4_3}</h5>", unsafe_allow_html=True)
                    st.markdown("<h5 style='text-align: center; color: grey;'>2020</h5>", unsafe_allow_html=True)
                with col_4_4:
                    st.markdown(f"<h5 style='text-align: center; color: grey;'>{valor_col_4_4}</h5>", unsafe_allow_html=True)
                    st.markdown("<h5 style='text-align: center; color: grey;'>2021</h5>", unsafe_allow_html=True)
                with col_4_5:
                    st.markdown(f"<h5 style='text-align: center; color: grey;'>{valor_col_4_5}</h5>", unsafe_allow_html=True)
                    st.markdown("<h7 style='text-align: center; color: grey;'>2022</h7>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='text-align: center; color: grey;'>{texto_Norma_4}</h4>", unsafe_allow_html=True)

            with col8:
                col_5_1,col_5_2,col_5_3,col_5_4,col_5_5=st.columns(5,gap='small')
                texto_Norma_5="""Porcentaje de Servicios Públicos que declaran haber realizado Inducción en un plazo menor a 30 días"""
                valor_col_5_1=f"{Norma_5.query('Año==2018').Metrica.iloc[0]:.2%}"
                valor_col_5_2=f"{Norma_5.query('Año==2019').Metrica.iloc[0]:.2%}"
                valor_col_5_3=f"{Norma_5.query('Año==2020').Metrica.iloc[0]:.2%}"
                valor_col_5_4=f"{Norma_5.query('Año==2021').Metrica.iloc[0]:.2%}"
                valor_col_5_5=f"{Norma_5.query('Año==2022').Metrica.iloc[0]:.2%}"
                with col_5_1:
                    st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_5_1}</h3>", unsafe_allow_html=True)
                    st.markdown("<h3 style='text-align: center; color: grey;'>2018</h3>", unsafe_allow_html=True)
                with col_5_2:
                    st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_5_2}</h3>", unsafe_allow_html=True)
                    st.markdown("<h3 style='text-align: center; color: grey;'>2019</h3>", unsafe_allow_html=True)
                with col_5_3:
                    st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_5_3}</h3>", unsafe_allow_html=True)
                    st.markdown("<h3 style='text-align: center; color: grey;'>2020</h3>", unsafe_allow_html=True)
                with col_5_4:
                    st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_5_4}</h3>", unsafe_allow_html=True)
                    st.markdown("<h3 style='text-align: center; color: grey;'>2021</h3>", unsafe_allow_html=True)
                with col_5_5:
                    st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_5_5}</h3>", unsafe_allow_html=True)
                    st.markdown("<h3 style='text-align: center; color: grey;'>2022</h3>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align: center; color: grey;'>{texto_Norma_5}</h2>", unsafe_allow_html=True)

            with col9:
                col_6_1,col_6_2,col_6_3,col_6_4,col_6_5=st.columns(5,gap='small')
                texto_Norma_6="""Total de estudiantes seleccionados"""
                valor_col_6_1=f"{Norma_6.query('Año==2018').Metrica.iloc[0]:,}"
                valor_col_6_2=f"{Norma_6.query('Año==2019').Metrica.iloc[0]:,}"
                valor_col_6_3=f"{Norma_6.query('Año==2020').Metrica.iloc[0]:,}"
                valor_col_6_4=f"{Norma_6.query('Año==2021').Metrica.iloc[0]:,}"
                valor_col_6_5=f"{Norma_6.query('Año==2022').Metrica.iloc[0]:,}"
                with col_6_1:
                    st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_6_1}</h3>", unsafe_allow_html=True)
                    st.markdown("<h3 style='text-align: center; color: grey;'>2018</h3>", unsafe_allow_html=True)
                with col_6_2:
                    st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_6_2}</h3>", unsafe_allow_html=True)
                    st.markdown("<h3 style='text-align: center; color: grey;'>2019</h3>", unsafe_allow_html=True)
                with col_6_3:
                    st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_6_3}</h3>", unsafe_allow_html=True)
                    st.markdown("<h3 style='text-align: center; color: grey;'>2020</h3>", unsafe_allow_html=True)
                with col_6_4:
                    st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_6_4}</h3>", unsafe_allow_html=True)
                    st.markdown("<h3 style='text-align: center; color: grey;'>2021</h3>", unsafe_allow_html=True)
                with col_6_5:
                    st.markdown(f"<h3 style='text-align: center; color: grey;'>{valor_col_6_5}</h3>", unsafe_allow_html=True)
                    st.markdown("<h3 style='text-align: center; color: grey;'>2022</h3>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='text-align: center; color: grey;'>{texto_Norma_6}</h2>", unsafe_allow_html=True)
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
if a=='Prevención de Maltrato y Acoso Laboral':
    st.title('Prevención de Maltrato y Acoso Laboral')
#---------------------------------------------------------------------------------------------------
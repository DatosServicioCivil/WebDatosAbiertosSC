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
color_line='#4A4A4A' #dark grey
color_line_2='#E0701E' #orange
color_line_3='#006FB3' #blue
color_bar='#006FB3' #blue
color_bar_2='#0A132D' #dark blue
color_bar_3='#E0701E' #orange
# Asignar colores de acuerdo a una paleta de colores a cada sexo
sexo_color_map = {'Mujeres': 'orange', 'Hombres': 'blue'} 

with st.sidebar:
    a=st.radio('Gestión de Personas: ',['Normas de Gestión de Personas','Capacitación en el Estado','Integridad','Prevención de Maltrato y Acoso Laboral','Egresos ADP'])



#---------------------------------------------------------------------------------------------------
if a=='Normas de Gestión de Personas':
    st.title('Normas de Gestion de Personas en el Estado')
#---------------------------------------------------------------------------------------------------
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
    df_actividades_ejecutadas_sispubli['Metodología_de_Aprendizaje']=np.where(df_actividades_ejecutadas_sispubli['Metodología_de_Aprendizaje']=='Video Conferencia','E-Learning',\
                                                                              np.where(df_actividades_ejecutadas_sispubli['Metodología_de_Aprendizaje']=='E-Learning/Video Conferencia','E-Learning',\
                                                                                       np.where(df_actividades_ejecutadas_sispubli['Metodología_de_Aprendizaje']=='Presencial/E-Learning','Híbrida',\
                                                                                                np.where(df_actividades_ejecutadas_sispubli['Metodología_de_Aprendizaje']=='Presencial/Video Conferencia','Híbrida',\
                                                                                                    df_actividades_ejecutadas_sispubli['Metodología_de_Aprendizaje']))))


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
    if option_1=='Todos' and option_2!='Todos' and option_3=='Todos'and option_4=='Todos': #2
        Actividades=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2)].groupby('Año').agg({'id_actividad':'count'}).reset_index()
        Inversion=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2)].groupby('Año').agg({'Gasto_monto_Item001':'sum'}).reset_index()
        Participantes=df_actividades_ejecutadas_sispubli[(df_actividades_ejecutadas_sispubli.Servicio==option_2)].groupby('Año').agg({'Numero_de_Participantes':'sum'}).reset_index()
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

    df_treemap=df_actividades_ejecutadas_sispubli.groupby(['Ministerio','Servicio','Modalidad_de_Compra','Metodología_de_Aprendizaje']).agg({'Gasto_monto_Item001':'sum'}).reset_index()
    df_treemap=df_treemap.rename(columns={'Gasto_monto_Item001':'Inversion'})
    df_treemap['Todos']='Todos'
    

    graf4 = px.bar(Actividades, x="Año", y="Actividades",color='Metodología_de_Aprendizaje', title="Cantidad de capacitaciones por metodología de aprendizaje")
    graf4.show()

    #graf4 = go.Figure()
    #graf4.add_trace(go.Treemap(
    #ids=df_treemap.Ministerio,
    #labels=df_treemap.Ministerio,   
    #parents=df_treemap.Todos,  # Usar 'Todos' como el nodo raíz
    #maxdepth=-1,
    #root_color="lightgrey",
    #values=df_treemap.Inversion))

    #graf4.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    #graf4 = px.treemap(df_treemap, path=['Todos','Ministerio', 'Servicio', 'Modalidad_de_Compra','Metodología_de_Aprendizaje'], values='Inversion')
    #graf4.update_traces(root_color="lightgrey")
    #graf4.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    #graf4.show()




    inversion_promedio=np.round(Inversion['Inversion'].sum()/Participantes['Participantes'].sum(),0)
    total_actividades=Actividades['Actividades'].sum()
    total_participantes=Participantes['Participantes'].sum()
    total_inversion=np.round(Inversion['Inversion'].sum()/1_000_000,0)

    with st.container():
        col1,col2,col3,col4,col5=st.columns(5,gap='small')
        with col1:
            st.markdown(f"<h2 style='text-align: center; color: grey;'>Entre el 2016 y {df_actividades_ejecutadas_sispubli.Año.max()} la cantidad de capacitaciones realizadas es</h2>", unsafe_allow_html=True)
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
        st.plotly_chart(graf4,use_container_width=True)



    #st.text(df_actividades_ejecutadas_sispubli.Año.unique())
#---------------------------------------------------------------------------------------------------
if a=='Integridad':
    st.title('Integridad en el Estado')
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
if a=='Prevención de Maltrato y Acoso Laboral':
    st.title('Prevención de Maltrato y Acoso Laboral')
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
if a=='Egresos ADP':
    st.title('Egresos ADP')
#---------------------------------------------------------------------------------------------------
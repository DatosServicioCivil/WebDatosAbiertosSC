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


Nivel=['Nivel I', 'Nivel II']
Ministerios=['Ministerio de Hacienda', 'Ministerio de Educación','Ministerio de Economía, Fomento y Turismo', 'Ministerio de Salud',
       'Ministerio del Trabajo y Previsión Social','Ministerio de Agricultura', 'Ministerio del Deporte',
       'Ministerio de Minería', 'Ministerio de Energía','Ministerio de Defensa Nacional', 'Ministerio de Obras Públicas',
       'Ministerio de Justicia y Derechos Humanos','Ministerio del Interior y Seguridad Pública',
       'Ministerio de las Culturas, las artes y el Patrimonio','Ministerio de Desarrollo Social y Familia','Ministerio de Vivienda y Urbanismo',
       'Ministerio de Ciencia, Tecnología, Conocimiento e Innovación','Ministerio de Relaciones Exteriores',
       'Ministerio del Medio Ambiente','Ministerio de Transportes y Telecomunicaciones','Ministerio de la Mujer y la Equidad de Género',
       'Ministerio Secretaría General de Gobierno', 'Autónomo','Administración Central',]
Region=['Región de Metropolitana de Santiago','Región de Magallanes y de la Antártica Chilena',
       'Región del Libertador General Bernardo OHiggins','Región del Maule', 'Región del Biobío', 'Región de Los Ríos',
       'Región de  Valparaíso', 'Región de Los Lagos','Región de Arica y Parinacota', 'Región de la Araucanía',
       'Región de Antofagasta', 'Región de  Atacama','Región de  Coquimbo',
       'Región de Aysén del General Carlos Ibañez del Campo','Región de Tarapacá', 'Región del Ñuble']


with st.sidebar:
    a=st.radio('Reclutamiento y Selección: ',['Alta Dirección Pública','Empleo Público','Prácticas Chile'])

if a=='Alta Dirección Pública':
    with st.container():
       st.radio('Seleccionar: ',["Concursos", "Postulaciones","Nombramientos"],horizontal=True)
if a=='Empleo Público':
    with st.container():
       st.radio('Seleccionar: ',["Convocatorias", "Postulaciones","Seleccionados"],horizontal=True)
if a=='Prácticas Chile':
    with st.container():
       st.radio('Seleccionar: ',["Convocatorias", "Postulaciones","Seleccionados"],horizontal=True)


if a=='Alta Dirección Pública':
    with st.container():
        col1,col2,col3=st.columns(3,gap="large")
        with col1:
           option_1 = st.selectbox('Nivel Jerárquico',Nivel)
        with col2:
           option_2 = st.selectbox('Región',Region)
        with col3:
           option_3 = st.selectbox('Ministerio',Ministerios)
#----------------------------------------------------------------------------------------------------------------------
if a=='Empleo Público':

    import pandas as pd
    import streamlit as st
    import plotly.express as px 
    import plotly.graph_objects as go
    
    df_postulaciones=pd.read_csv('EEPP/postulaciones_x_año.csv',encoding='utf-8')    
    df_postulaciones_sexo=pd.read_csv('EEPP/porcentaje_postulaciones_sexo_e.csv',sep=";")
    df_postulaciones_promedio=pd.read_csv('EEPP/Postulacion_Promedio_x_Año.csv')
    df_convocatorias=pd.read_csv('EEPP/Convocatorias_x_año.csv')
    df_vacantes=pd.read_csv('EEPP/Vacantes.csv')
    df_ConvEnLinea=pd.read_csv('EEPP/ConvEnLineaxAño.csv',sep=";")
    
    date='31 de Marzo de 2023'
    
    st.title('Estadísticas Portal Empleos Públicos')
    st.subheader(date)
    
    # define si se ven los ejes Y
    visible_y_axis=True
    
    #https://framework.digital.gob.cl/colors.html
    color_line='#2D717C'
    color_bar='#6633CC'
    #----------------------------------------------------------------------------------------------------------------------------
    # grafico Evolución de Postulaciones por Año
    graf1=px.line(df_postulaciones,x='año',y='postulaciones',title='<b>Evolución de postulaciones por año</b>').\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    graf1.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_line)
    graf1.update_layout(yaxis_tickformat='.0f')
    #----------------------------------------------------------------------------------------------------------------------------
    #grafico 2: Distribución de Postulaciones por Sexo
    # Create separate DataFrames for "Mujeres" and "Hombres"
    df_mujeres = df_postulaciones_sexo[df_postulaciones_sexo.Sexo == 'Mujeres']
    df_hombres = df_postulaciones_sexo[df_postulaciones_sexo.Sexo == 'Hombres']
    
    # Asignar colores de acuerdo a una paleta de colores a cada sexo
    sexo_color_map = {'Mujeres': 'orange', 'Hombres': 'blue'}  # Mapeo de colores por sexo
    
    
    # Create the line plot using Plotly Express
    graf2 = px.line(
        title='<b>Evolución de postulaciones por año y sexo</b>',
        labels={'year': 'Año', 'Porcentaje': 'Porcentaje'},  # Customize axis labels
    )
    
    # Cambiar el formato del eje y a porcentaje (0.1 se mostrará como 10%)
    graf2.update_layout(yaxis_tickformat='.0%')
    
    # Add lines for "Mujeres" and "Hombres"
    graf2.add_trace(
        go.Scatter(x=df_mujeres['year'], y=df_mujeres['Porcentaje'], mode='lines+markers',line_shape='spline',marker=dict(size=8), name='Mujeres',line_color=sexo_color_map['Mujeres'])
    )
    graf2.add_trace(go.Scatter(x=df_hombres['year'], y=df_hombres['Porcentaje'], mode='lines+markers',line_shape='spline',marker=dict(size=8), name='Hombres',line_color=sexo_color_map['Hombres']))
    
    # Actualizar la ubicación de la leyenda
    graf2.update_layout(
        legend=dict(x=0.5, xanchor='center', y=-0.2, yanchor='top', traceorder='normal', itemsizing='trace')  # Ubicar debajo del eje x en dos columnas
    )
    
    # actualiza el eje x para nostrar todas las etiquetas de años
    graf2.update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    
    #----------------------------------------------------------------------------------------------------------------------------
    # grafico Postulación Promedio por Año
    graf3=px.line(df_postulaciones_promedio,x='Año',y='Tasa Postulación Promedio - Concursos en Línea',title='<b>Evolución de postulaciones promedio por convocatoria por año</b>').\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    
    graf3.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_line)
    #----------------------------------------------------------------------------------------------------------------------------
    # grafico Convocatorias por Año
    graf4=px.bar(df_convocatorias,x='Año',y='Convocatorias',title='<b>Evolución de convocatorias por año</b>',color_discrete_sequence=[color_bar]).\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    graf4.update_layout(yaxis_tickformat='.0f')
    #----------------------------------------------------------------------------------------------------------------------------
    # grafico Vacantes Concursadas por Año
    graf5=px.bar(df_vacantes,x='Año',y='Vacantes',title='<b>Evolución de vacantes ofrecidas por año</b>',color_discrete_sequence=[color_bar]).\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    graf5.update_layout(yaxis_tickformat='.0f')
    #----------------------------------------------------------------------------------------------------------------------------
    # grafico Porcentaje de Convocatorias en Linea por Año
    graf6=px.line(df_ConvEnLinea,x='year',y='Porcentaje Convocatorias Postulacion en Linea',title='<b>Evolución de convocatorias en línea por año</b>').\
            update_yaxes(visible=visible_y_axis,title_text=None).\
                    update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
    
    graf6.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline', line_color=color_bar)
    graf6.update_layout(yaxis_tickformat='.0%')
    #----------------------------------------------------------------------------------------------------------------------------
    
    
    
    col1,col2,col3=st.columns(3,gap='small')
    with col1:
        st.plotly_chart(graf1,use_container_width=True)
    with col2:
        st.plotly_chart(graf2,use_container_width=True)
    with col3:
        st.plotly_chart(graf4,use_container_width=True)
    
    
    col4, col5, col6=st.columns(3,gap='small')
    with col4:
            st.plotly_chart(graf3,use_container_width=True)
    with col5:
            st.plotly_chart(graf5,use_container_width=True)
    with col6:
            st.plotly_chart(graf6,use_container_width=True)
    
    

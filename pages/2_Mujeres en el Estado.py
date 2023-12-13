import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from PIL import Image
import plotly.express as px
import numpy as np
import time
import streamlit.components.v1 as components
import pyarrow.parquet as pq

st.set_page_config(layout='wide')

# carga archivos parquet postulaciones ADP
@st.cache_data
def df_post_adp():
    df_post_adp_1=pq.read_table('ADP/df_postulaciones_adp_1.parquet').to_pandas()
    df_post_adp_2=pq.read_table('ADP/df_postulaciones_adp_2.parquet').to_pandas()
    df_post_adp_3=pq.read_table('ADP/df_postulaciones_adp_3.parquet').to_pandas()
    df_post_adp_4=pq.read_table('ADP/df_postulaciones_adp_4.parquet').to_pandas()
    df_postulaciones_adp=pd.concat([df_post_adp_1,df_post_adp_2,df_post_adp_3,df_post_adp_4])
    return df_postulaciones_adp

# carga archivos parquet concursos EEPP
@st.cache_data
def df_conc_ep():
    df_2=pq.read_table('EEPP/df_concursos_eepp_Postulacion en linea.parquet').to_pandas()
    df_conc_ep=df_2
    return df_conc_ep

# carga archivos parquet concursos DEEM
@st.cache_data
def df_post_deem():
    df=pq.read_table('DEEM/df_postulaciones_dee.parquet').to_pandas()
    df_post_deem=df
    return df_post_deem

# carga archivos parquet concursos DEEM
@st.cache_data
def df_tabla_deem():
    df=pq.read_table('DEEM/df_concursos_dee.parquet').to_pandas()
    df_tab_deem=df
    return df_tab_deem

@st.cache_data
def tabla_postulaciones():
    tb_1=pq.read_table('ADP/tb_postulaciones_adp.parquet').to_pandas()
    tb_2=pq.read_table('DEEM/tb_postulaciones_dee.parquet').to_pandas()
    tb_3=pq.read_table('EEPP/tb_postulaciones_eepp.parquet').to_pandas()
    tb_postulaciones=pd.concat([tb_1,tb_2,tb_3])
    return tb_postulaciones

# se asocia concursos, cargos, nivel a postulaciones
df_concursos=pq.read_table('ADP/df_concursos.parquet').to_pandas()
df_postulaciones_adp=df_post_adp()

df_post_adp=pd.merge(df_postulaciones_adp,df_concursos,how='left',on='CD_Concurso')

# Camculo porcentajes mujeres nombradas en ADP
Porcentaje_Mujeres_Nombradas_ADP_I_N=df_post_adp[(df_post_adp['NOMBRADO']=='SI') & (df_post_adp['GENERO']=='F') & (df_post_adp['Nivel']=='I')]['ID_Postulacion'].count()\
    /df_post_adp[(df_post_adp['NOMBRADO']=='SI') & (df_post_adp['Nivel']=='I')]['ID_Postulacion'].count()

Porcentaje_Mujeres_Nombradas_ADP_II_N=df_post_adp[(df_post_adp['NOMBRADO']=='SI') & (df_post_adp['GENERO']=='F') & (df_post_adp['Nivel']=='II')]['ID_Postulacion'].count()\
    /df_post_adp[(df_post_adp['NOMBRADO']=='SI') & (df_post_adp['Nivel']=='II')]['ID_Postulacion'].count()

# informacion de convocatorias de EEPP
df_concursos_eepp=df_conc_ep()
df_concursos_eepp['Año']=pd.to_datetime(df_concursos_eepp['Fecha Final Proceso']).dt.year

Porcentaje_Mujeres_Seleccionadas_Jefaturas_EEPP=df_concursos_eepp[(df_concursos_eepp['Tipo Base']=='Jefe Departamento')]['SeleccionadoMujeres'].sum()\
    /df_concursos_eepp[(df_concursos_eepp['Tipo Base']=='Jefe Departamento')]['Seleccionados'].sum()

#Calculo porcentaje mujeres nombradas deem
df_tabla_deem=df_tabla_deem()
Porcentaje_Mujeres_Nombradas_DEEM=df_tabla_deem[(df_tabla_deem['Estado']=='Nombrado') & (df_tabla_deem['SexoNombrado']=='Femenino')]['idConcurso'].count()\
                                                / df_tabla_deem[(df_tabla_deem['Estado']=='Nombrado') & (df_tabla_deem['SexoNombrado']!='Sin Inform Portal-GeeDem') & (df_tabla_deem['SexoNombrado']!='')]['idConcurso'].count()

# tablas de postulaciones y porcentajes por sexo
tb_postulaciones=tabla_postulaciones()
tb_postulaciones_sexo_año=tb_postulaciones[tb_postulaciones.Sexo.isin(['Hombre','Mujer'])].groupby(['Año','Sexo','portal'])['postulaciones'].sum().reset_index()



# This function sets the logo and company name inside the sidebar
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="./imagenes/logo.png", width=150, height=150)
st.image(my_logo)

sexo_color_map = {'Mujer': 'orange', 'Hombre': 'blue','Todos':'grey'}  # Mapeo de colores por sexo
visible_y_axis=False

# Set Page Header
st.header("Mujeres en el Estado")
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


texto_mas_mujeres="""Más Mujeres: Conoce los principales indicadores del Servicio Civil que 
potencian y aumentan el liderazgo y presencia laboral de las mujeres en el Estado"""
valor_col2=Porcentaje_Mujeres_Nombradas_ADP_I_N
valor_col3=Porcentaje_Mujeres_Nombradas_ADP_II_N
valor_col4=Porcentaje_Mujeres_Seleccionadas_Jefaturas_EEPP
valor_col5=Porcentaje_Mujeres_Nombradas_DEEM
with st.container():
    col1,col2,col3,col4,col5=st.columns(5,gap='small')
    with col1:
        st.markdown(f"<h3 style='text-align: center; color: grey;'>{texto_mas_mujeres}</h3>", unsafe_allow_html=True)
    with col2:
        #image = Image.open('imagenes/job_offer.png')
        #st.image(image)
        valor_col2=f"{valor_col2:.2%}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col2}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>% Mujeres seleccionadas cargos I nivel ADP</h3>", unsafe_allow_html=True)
    with col3:
        valor_col3=f"{valor_col3:.2%}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col3}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>% Mujeres seleccionadas cargos II nivel ADP</h3>", unsafe_allow_html=True)
    with col4:
        #image = Image.open('imagenes/mannager_selection.png')
        #st.image(image)
        valor_col4=f"{valor_col4:.2%}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col4}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>% Mujeres seleccionadas cargos Jefaturas</h3>", unsafe_allow_html=True)
    with col5:
        #image = Image.open('imagenes/mannager_selection.png')
        #st.image(image)
        valor_col5=f"{valor_col5:.2%}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col5}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>% Mujeres seleccionadas cargos DEEM</h3>", unsafe_allow_html=True)




with st.container():
    col1,col2=st.columns(2,gap='small')
    with col1:    
        option_1 = st.selectbox('Tipo de oferta laboral', ['Todas','ADP', 'DEEM', 'EEPP'])
    with col2:
        option_2=st.selectbox("Selecciona como quieres ver el dato",["Gráfico","Tabla"])

if option_1:
    tb_postulaciones_sexo_año = tb_postulaciones_sexo_año.groupby(['Año', 'Sexo'])['postulaciones'].sum().reset_index()
if option_1=='ADP':
    tb_postulaciones_sexo_año = tb_postulaciones_sexo_año[tb_postulaciones_sexo_año['portal']=='ADP'].groupby(['Año', 'Sexo'])['postulaciones'].sum().reset_index()
if option_1=='DEEM':
    tb_postulaciones_sexo_año = tb_postulaciones_sexo_año[tb_postulaciones_sexo_año['portal']=='DEEM'].groupby(['Año', 'Sexo'])['postulaciones'].sum().reset_index()
if option_1=='EEPP':
    tb_postulaciones_sexo_año = tb_postulaciones_sexo_año[tb_postulaciones_sexo_año['portal']=='EEPP'].groupby(['Año', 'Sexo'])['postulaciones'].sum().reset_index()

#gráfico postulaciones por año y sexo segun seleccion portal
graf1=px.bar(tb_postulaciones_sexo_año,x='Año',y='postulaciones',title='<b>Postulaciones por año desagregado por sexo</b>',color='Sexo',color_discrete_map=[sexo_color_map]).\
                    update_yaxes(visible=visible_y_axis,title_text=None).\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
graf1.update_layout(yaxis_tickformat='.0f')

with st.container():
    st.plotly_chart(graf1,use_container_width=True)



st.dataframe(df_concursos.head(10))
st.markdown("<hr>", unsafe_allow_html=True)
st.dataframe(df_postulaciones_adp.head(10))

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

#--------------------------- colores
color_line='#4A4A4A' #dark grey
color_line_2='#E0701E' #orange
color_line_3='#006FB3' #blue
color_line_4='#A7ED74' #verde montaña
color_bar='#006FB3' #blue
color_bar_2='#0A132D' #dark blue
color_5="#B2FFFF" #celeste
color_6="#7CB2B2" #celeste orcuro
# se define color para sexo
#------------------------------------------------------------------------------------------------
sexo_color_map = {'Mujer': 'orange', 'Hombre': 'blue','Todos':'grey'}  # Mapeo de colores por sexo

# # carga archivos parquet postulaciones ADP
# #--------------------------------------------------------------------------------------------------
# @st.cache_data
# def df_post_adp():
#     df_postulaciones_adp = pd.read_parquet('ADP/tb_postulaciones_adp.parquet')
#     return df_postulaciones_adp

# # carga archivos parquet concursos EEPP
# #--------------------------------------------------------------------------------------------------

@st.cache_data
def df_conc_eepp():
    df_conc_ep = pd.read_parquet('EEPP/df_concursos_eepp.parquet')
    return df_conc_ep

# # carga archivos parquet DEEM
# #--------------------------------------------------------------------------------------------------
# carga archivos parquet postulaciones DEEM
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

# union postulaciones
#--------------------------------------------------------------------------------------------------
@st.cache_data
def tabla_postulaciones():
    tb_1=pq.read_table('ADP/tb_postulaciones_adp.parquet').to_pandas()
    tb_2=pq.read_table('DEEM/tb_postulaciones_dee.parquet').to_pandas()
    tb_3=pq.read_table('EEPP/tb_postulaciones_eepp.parquet').to_pandas()
    tb_postulaciones=pd.concat([tb_1,tb_2,tb_3])
    return tb_postulaciones


@st.cache_data
def tabla_postulaciones_adp():
    tb_1=pq.read_table('ADP/tb_postulaciones_adp.parquet').to_pandas()
    tb_postulaciones_adp=tb_1
    return tb_postulaciones_adp

@st.cache_data
def tabla_nombramientos_adp():
    tb_1=pq.read_table('ADP/tb_nombramientos_adp.parquet').to_pandas()
    tb_nombramientos_adp=tb_1
    return tb_nombramientos_adp

@st.cache_data
def tabla_postulaciones_eepp():
    tb_2=pq.read_table('DEEM/tb_postulaciones_dee.parquet').to_pandas()
    tb_postulaciones_eepp=tb_2
    return tb_postulaciones_eepp

@st.cache_data
def tabla_postulaciones_dee():
    tb_3=pq.read_table('EEPP/tb_postulaciones_eepp.parquet').to_pandas()
    tb_postulaciones_dee=tb_3
    return tb_postulaciones_dee

#--------------------------------------------------------------------------------------------------


# carga datos de postulaciones y nombramientos en ADP
tb_postulaciones_adp=tabla_postulaciones_adp()
nombramiento_adp=tabla_nombramientos_adp()

# Calculo porcentajes mujeres nombradas en ADP
Porcentaje_Mujeres_Nombradas_ADP_I_N=tb_postulaciones_adp[(tb_postulaciones_adp['Estado']=='SI') & (tb_postulaciones_adp['Sexo']=='Mujer') & (tb_postulaciones_adp['Nivel']=='I')]['postulaciones'].sum()\
    /tb_postulaciones_adp[(tb_postulaciones_adp['Estado']=='SI') & (tb_postulaciones_adp['Nivel']=='I')]['postulaciones'].sum()
Porcentaje_Mujeres_Nombradas_ADP_II_N=tb_postulaciones_adp[(tb_postulaciones_adp['Estado']=='SI') & (tb_postulaciones_adp['Sexo']=='Mujer') & (tb_postulaciones_adp['Nivel']=='II')]['postulaciones'].sum()\
    /tb_postulaciones_adp[(tb_postulaciones_adp['Estado']=='SI') & (tb_postulaciones_adp['Nivel']=='II')]['postulaciones'].sum()

# carga datos de postulaciones en EEPP
df_concursos_eepp=df_conc_eepp()
tb_postulaciones_eepp=tabla_postulaciones_eepp()

Porcentaje_Mujeres_Seleccionadas_Jefaturas_EEPP=df_concursos_eepp[(df_concursos_eepp['Tipo Base']=='Jefe Departamento')]['selec_Mujeres'].sum()\
    /df_concursos_eepp[(df_concursos_eepp['Tipo Base']=='Jefe Departamento')]['Total_Seleccionados'].sum()


# carga datos de postulaciones en ADP
df_concursos_dee=df_tabla_deem()
tb_postulaciones_dee=tabla_postulaciones_dee()
#Calculo porcentaje mujeres nombradas deem
#Porcentaje_Mujeres_Nombradas_DEEM=df_concursos_dee[(df_concursos_dee['Estado']=='Nombrado') & (df_concursos_dee['SexoNombrado']=='Mujer')]['postulaciones'].count()\
#                                                / df_concursos_dee[(df_concursos_dee['Estado']=='Nombrado') & ((df_concursos_dee['SexoNombrado']!='Sin Inform Portal-GeeDem') | (df_concursos_dee['SexoNombrado']!='Sin Inform Portal-GeeDem'))]['postulaciones'].count()
Porcentaje_Mujeres_Nombradas_DEEM=df_concursos_dee[(df_concursos_dee['Estado']=='Nombrado') & (df_concursos_dee['Cargo']=='Director(a)') & (df_concursos_dee['SexoNombrado']=='Femenino')]['idConcurso'].count()\
                                                / df_concursos_dee[(df_concursos_dee['Estado']=='Nombrado') & (df_concursos_dee['SexoNombrado']!='Sin Inform Portal-GeeDem') & (df_concursos_dee['SexoNombrado']!='')]\
                                                ['idConcurso'].count()


# Porcentajes de Postulaciones de Mujeres
#------------------------------------------------------------------------------------------------
Porcentaje_Postulaciones_Mujeres_ADP_I_N=tb_postulaciones_adp[(tb_postulaciones_adp['Sexo']=='Mujer') & (tb_postulaciones_adp['Nivel']=='I')]['postulaciones'].sum()\
    /tb_postulaciones_adp[(tb_postulaciones_adp['Nivel']=='I')]['postulaciones'].sum()

Porcentaje_Postulaciones_Mujeres_ADP_II_N=tb_postulaciones_adp[(tb_postulaciones_adp['Sexo']=='Mujer') & (tb_postulaciones_adp['Nivel']=='II')]['postulaciones'].sum()\
    /tb_postulaciones_adp[(tb_postulaciones_adp['Nivel']=='II')]['postulaciones'].sum()

Porcentaje_Postulaciones_Mujeres_EEPP=df_concursos_eepp[(df_concursos_eepp['Tipo Base']=='Jefe Departamento')]['Post_Mujeres'].sum()\
    /df_concursos_eepp[(df_concursos_eepp['Tipo Base']=='Jefe Departamento')]['Total_Postulaciones'].sum()

#Porcentaje_Postulaciones_Mujeres_DEEM=tb_postulaciones_dee[(tb_postulaciones_dee['Sexo']=='Mujer')]['postulaciones'].sum()\
#                                                / tb_postulaciones_dee['postulaciones'].sum()

Porcentaje_Postulaciones_Mujeres_DEEM=df_concursos_dee[(df_concursos_dee['Cargo']=='Director(a)')]['NumMujeres'].sum()\
                                                / df_concursos_dee[(df_concursos_dee['Cargo']=='Director(a)')]['Número Postulaciones'].sum()\




# tablas de postulaciones y porcentajes por sexo
#------------------------------------------------------------------------------------------------
# Concatenar DataFrames
tb_postulaciones = tabla_postulaciones()
# Filtrar por Sexo
tb_postulaciones = tb_postulaciones[tb_postulaciones['Sexo'].isin(['Hombre', 'Mujer'])]
#------------------------------------------------------------------------------------------------

# This function sets the logo and company name inside the sidebar
def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="./imagenes/logo.png", width=150, height=150)
st.image(my_logo)

#--------------------------------------
# variable para visualizar eje y
visible_y_axis=False
#------------------------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------------------------

texto_mas_mujeres="""Más Mujeres: Conoce los principales indicadores del Servicio Civil que 
potencian y aumentan el liderazgo y presencia laboral de las mujeres en el Estado"""
valor_col2=Porcentaje_Mujeres_Nombradas_ADP_I_N
valor_col_2_2=Porcentaje_Postulaciones_Mujeres_ADP_I_N
valor_col3=Porcentaje_Mujeres_Nombradas_ADP_II_N
valor_col_3_2=Porcentaje_Postulaciones_Mujeres_ADP_II_N
valor_col4=Porcentaje_Mujeres_Seleccionadas_Jefaturas_EEPP
valor_col_4_2=Porcentaje_Postulaciones_Mujeres_EEPP
valor_col5=Porcentaje_Mujeres_Nombradas_DEEM
valor_col_5_2=Porcentaje_Postulaciones_Mujeres_DEEM
with st.container():
    col1,col2,col3,col4,col5=st.columns(5,gap='small')
    with col1:
        st.markdown(f"<h3 style='text-align: center; color: grey;'>{texto_mas_mujeres}</h3>", unsafe_allow_html=True)
    with col2:
        valor_col2=f"{valor_col2:.2%}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col2}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>% Mujeres seleccionadas cargos I nivel ADP</h3>", unsafe_allow_html=True)
        valor_col_2_2=f"{valor_col_2_2:.2%}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col_2_2}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>% Postulaciones de mujeres a cargos I nivel ADP</h3>", unsafe_allow_html=True)
    with col3:
        valor_col3=f"{valor_col3:.2%}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col3}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>% Mujeres seleccionadas cargos II nivel ADP</h3>", unsafe_allow_html=True)
        valor_col_3_2=f"{valor_col_3_2:.2%}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col_3_2}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>% Postulaciones de mujeres a cargos II nivel ADP</h3>", unsafe_allow_html=True)
    with col4:
        valor_col4=f"{valor_col4:.2%}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col4}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>% Mujeres seleccionadas cargos Jefaturas</h3>", unsafe_allow_html=True)
        valor_col_4_2=f"{valor_col_4_2:.2%}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col_4_2}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>% Postulaciones de Mujeres a cargos Jefaturas</h3>", unsafe_allow_html=True)
    with col5:
        valor_col5=f"{valor_col5:.2%}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col5}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>% Mujeres seleccionadas cargos DEEM</h3>", unsafe_allow_html=True)
        valor_col_5_2=f"{valor_col_5_2:.2%}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{valor_col_5_2}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>% Postulaciones de Mujeres a cargos DEEM</h3>", unsafe_allow_html=True)
    
#------------------------------------------------------------------------------------------------

with st.container():
    col1,col2=st.columns(2,gap='small')
    with col1:    
        option_1 = st.selectbox('Tipo de oferta laboral', ['Todos','ADP', 'DEE', 'EEPP'],key='1')
    with col2:
        option_2=st.selectbox("Selecciona como quieres ver el dato",["Gráfico","Tabla"],key='2')

if option_1=='Todos':
    tb_postulaciones_año = tb_postulaciones.groupby(['Año'])['postulaciones'].sum().reset_index()
    tb_postulaciones_sexo_año = tb_postulaciones.groupby(['Año', 'Sexo'])['postulaciones'].sum().reset_index()
    Postulaciones_Mujeres=tb_postulaciones[tb_postulaciones['Sexo']=='Mujer']['postulaciones'].sum()
    Porcentaje_Postulaciones_Mujeres=Postulaciones_Mujeres/tb_postulaciones['postulaciones'].sum()
else:
    tb_postulaciones_año = tb_postulaciones[tb_postulaciones['portal']==option_1].groupby(['Año'])['postulaciones'].sum().reset_index()
    tb_postulaciones_sexo_año = tb_postulaciones[tb_postulaciones['portal']==option_1].groupby(['Año', 'Sexo'])['postulaciones'].sum().reset_index()
    Postulaciones_Mujeres=tb_postulaciones[(tb_postulaciones['Sexo']=='Mujer') & (tb_postulaciones['portal']==option_1)]['postulaciones'].sum()
    Porcentaje_Postulaciones_Mujeres=Postulaciones_Mujeres/tb_postulaciones[(tb_postulaciones['portal']==option_1)]['postulaciones'].sum()


# cambio de nombre de columnas
tb_postulaciones_año=tb_postulaciones_año.rename(columns={'postulaciones':'Total Postulaciones'})
tb_postulaciones_sexo_año=tb_postulaciones_sexo_año.rename(columns={'postulaciones':'Postulaciones'})
# union de tablas por left join 
tb_postulaciones_sexo_año=pd.merge(tb_postulaciones_sexo_año,tb_postulaciones_año,how='left',on='Año')
tb_postulaciones_sexo_año['Porcentaje']=(tb_postulaciones_sexo_año['Postulaciones']/tb_postulaciones_sexo_año['Total Postulaciones'])


#-------------------------------------------------------------------------------------------------------------
#gráfico postulaciones por año y sexo segun seleccion portal
graf1=px.bar(tb_postulaciones_sexo_año,x='Año',y='Postulaciones',title='<b>Postulaciones por año desagregado por sexo</b>',color='Sexo',color_discrete_map=sexo_color_map).\
                     update_yaxes(visible=True,title_text=None).\
                         update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
graf1.update_layout(yaxis_tickformat='.0f')

#gráfico porcentaje postulaciones por año y sexo segun seleccion portal
graf2=px.line(tb_postulaciones_sexo_año,x='Año',y='Porcentaje',title='<b>Porcentaje postulaciones por año desagregado por sexo</b>',color='Sexo',color_discrete_map=sexo_color_map).\
                     update_yaxes(visible=True,title_text=None).\
                         update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
graf2.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline')#, line_color=color_line)
graf2.update_layout(yaxis_tickformat='.0%')



with st.container():
    col1,col2,col3=st.columns([0.2,0.4,0.4],gap='small')
    with col1:
        Postulaciones_Mujeres=f"{Postulaciones_Mujeres:,}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{Postulaciones_Mujeres}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>Total de postulaciones de mujeres en portales del Servicio Civil</h3>", unsafe_allow_html=True)
        Porcentaje_Postulaciones_Mujeres=f"{Porcentaje_Postulaciones_Mujeres:.2%}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{Porcentaje_Postulaciones_Mujeres}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>% Postulaciones de mujeres en portales del Servicio Civil</h3>", unsafe_allow_html=True)
    with col2:
        st.plotly_chart(graf2,use_container_width=True)
    with col3:
        st.plotly_chart(graf1,use_container_width=True)


with st.container():
    col1,col2=st.columns(2,gap='small')
    with col1:    
        option_3 = st.selectbox('Nivel Jerárquico', ['Todos','I', 'II'],key='3')
    with col2:
        option_4=st.selectbox("Selecciona como quieres ver el dato",["Gráfico","Tabla"],key='4')

if option_3=='Todos':
    tb_nombramiento_adp_ministerio=nombramiento_adp.groupby(['Ministerio']).agg({'postulaciones':'sum'}).reset_index()
    tb_nombramiento_sexo_ministerio=nombramiento_adp[(nombramiento_adp.Sexo=='Mujer')].groupby(['Ministerio']).agg({'postulaciones':'sum'}).reset_index()
    nombramiento_adp=nombramiento_adp
else:
    tb_nombramiento_adp_ministerio=nombramiento_adp[nombramiento_adp['Nivel']==option_3].groupby(['Ministerio']).agg({'postulaciones':'sum'}).reset_index()
    tb_nombramiento_sexo_ministerio=nombramiento_adp[(nombramiento_adp.Sexo=='Mujer') & (nombramiento_adp['Nivel']==option_3)].groupby(['Ministerio']).agg({'postulaciones':'sum'}).reset_index()
    nombramiento_adp=nombramiento_adp[nombramiento_adp['Nivel']==option_3]

tb_nombramiento_adp_ministerio=tb_nombramiento_adp_ministerio.rename(columns={'postulaciones': 'Total Nombramientos'})    
tb_nombramiento_sexo_ministerio=pd.merge(tb_nombramiento_sexo_ministerio,tb_nombramiento_adp_ministerio,how='left',on='Ministerio')
tb_nombramiento_sexo_ministerio['Porcentaje']=tb_nombramiento_sexo_ministerio['postulaciones']/tb_nombramiento_sexo_ministerio['Total Nombramientos']

Mujeres_Nombradas_ADP=nombramiento_adp[(nombramiento_adp.Sexo=='Mujer')]['postulaciones'].sum()
Porcentaje_Mujeres_Nombradas_ADP=Mujeres_Nombradas_ADP/nombramiento_adp['postulaciones'].sum()

graf3=px.bar(tb_nombramiento_sexo_ministerio,x='Ministerio',y='Porcentaje',\
             title='<b>Porcentaje de nombramientos a cargos ADP por Ministerio</b>',color_discrete_sequence=['orange']).\
        update_yaxes(visible=visible_y_axis,title_text=None).\
                        update_xaxes(title_text=None,tickmode='linear', dtick=1,tickangle=-45)
graf3.update_layout(yaxis_tickformat='.2%')

# Add a horizontal line at 50%
line_value = 0.5
graf3.add_shape(
    dict(
        type='line',
        x0=0,  # Starting x-coordinate
        x1=len(tb_nombramiento_sexo_ministerio['Ministerio']) - 1,  # Ending x-coordinate
        y0=line_value,  # Constant y-coordinate
        y1=line_value,  # Constant y-coordinate
        line=dict(color='red', width=2,dash='dot')  # Line color and width
    )
)



with st.container():
    col1,col2=st.columns([0.2,0.8],gap='small')
    with col1:
        Mujeres_Nombradas_ADP=f"{Mujeres_Nombradas_ADP:,}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{Mujeres_Nombradas_ADP}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>Total de mujeres nombradas en cargos ADP</h3>", unsafe_allow_html=True)
        Porcentaje_Mujeres_Nombradas_ADP=f"{Porcentaje_Mujeres_Nombradas_ADP:.2%}"
        st.markdown(f"<h1 style='text-align: center; color: grey;'>{Porcentaje_Mujeres_Nombradas_ADP}</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey;'>% de mujeres nombradas en cargos ADP en portales del Servicio Civil</h3>", unsafe_allow_html=True)
    with col2:
        st.plotly_chart(graf3,use_container_width=True)


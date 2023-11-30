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
@st.cache_data
def org():
    df1 = pd.read_csv("EEPP/df_concursos_eepp_Aviso.csv", sep=";", encoding="utf-8")
    df2 = pd.read_csv("EEPP/df_concursos_eepp_Postulacion en linea.csv", sep=";", encoding="utf-8")
    df=pd.concat([df1,df2],axis=0)
    organismos=df["Institucion"].unique()
    return organismos



@st.cache_data
def reg():
    df_reg=pd.read_excel("Regiones/all_region_values.xlsx",sheet_name="Sheet1")
    region=df_reg["Region_Homologada"].unique()
    return region

@st.cache_data
def df_eepp():
    df1 = pd.read_csv("EEPP/df_concursos_eepp_Aviso.csv", sep=";", encoding="utf-8")
    df2 = pd.read_csv("EEPP/df_concursos_eepp_Postulacion en linea.csv", sep=";", encoding="utf-8")
    df=pd.concat([df1,df2],axis=0)
    df_reg=pd.read_excel("Regiones/all_region_values.xlsx",sheet_name="Sheet1")
    df=pd.merge(df,df_reg,left_on="Región",right_on="Region",how="left")
    return df

@st.cache_data
def df_adp_concursos():
    df_adp = pd.read_csv("ADP/df_concursos.csv", sep=";", encoding="utf-8")
    df_reg=pd.read_excel("Regiones/all_region_values.xlsx",sheet_name="Sheet1")
    df_adp=pd.merge(df_adp,df_reg,on="Region",how="left")
    return df_adp


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
            select_region1=st.selectbox("Selecciona región N°1",reg())
        with col2:
            select_region2=st.selectbox("Selecciona región N°2",reg(),placeholder="Seleccionar región")
        if select_region1==select_region2:
            st.error("No se pueden seleccionar dos regiones iguales")
            st.stop()
        # Add horizontal line
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("Convocatorias EEPP")
        col1,col2=st.columns(2)
        with col1:
            #st.write("Selecciona año")
            Año=st.selectbox("Selecciona año",periodo_años)
        #fecha2=st.date_input("Fecha 2",value=pd.to_datetime("2021-09-01"))
        with col2:
            #st.write("Selecciona como quieres ver el dato")
            grafico=st.selectbox("Selecciona como quieres ver el dato",["Gráfico","Tabla"])

        if grafico=="Gráfico":
            df=df_eepp()
            df["Año"]=pd.DatetimeIndex(df["Fecha Inicio"]).year
            df['Mes']=pd.DatetimeIndex(df["Fecha Inicio"]).month
            df=df[(df["Año"]==Año) & (df["Region_Homologada"].isin([select_region1,select_region2]))]
            df=df.groupby(["Región","Mes"]).agg({"idConcurso":"count"}).reset_index()    
            df=df.rename(columns={"idConcurso":"Convocatorias","Region_Homologada":"Región"})
            graf1 = px.bar(df, x="Mes", y="Convocatorias",title=f'<b>Convocatoria EEPP {Año}</b>',
                color='Región', barmode='group',
                height=400)
            graf1.update_xaxes(title_text='Mes',tickmode='linear', dtick=1)
            st.plotly_chart(graf1,use_container_width=True)
        
        elif grafico=="Tabla":
            df=df_eepp()
            df["Año"]=pd.DatetimeIndex(df["Fecha Inicio"]).year
            df['Mes']=pd.DatetimeIndex(df["Fecha Inicio"]).month
            df=df[(df["Año"]==Año) & (df["Region_Homologada"].isin([select_region1,select_region2]))]
            df=df.groupby(["Año","Region_Homologada","Mes"]).agg({"idConcurso":"count"}).reset_index()    
            df=df.rename(columns={"idConcurso":"Convocatorias","Region_Homologada":"Región"})
            st.dataframe(df,hide_index=True,width=600)
            st.download_button(label="Descargar datos",data=df.to_csv().encode("utf-8"),file_name=f"Convocatorias EEPP {Año}.csv",mime="text/csv")

        st.subheader("Postulaciones EEPP")
        col1,col2=st.columns(2)
        with col1:
            #st.write("Selecciona año")
            Año_2=st.selectbox("Selecciona año",periodo_años,key="2")
        #fecha2=st.date_input("Fecha 2",value=pd.to_datetime("2021-09-01"))
        with col2:
            #st.write("Selecciona como quieres ver el dato")
            grafico_2=st.selectbox("Selecciona como quieres ver el dato",["Gráfico","Tabla"],key="3")

        if grafico_2=="Gráfico":
            df=df_eepp()
            df["Año"]=pd.DatetimeIndex(df["Fecha Inicio"]).year
            df['Mes']=pd.DatetimeIndex(df["Fecha Inicio"]).month
            df=df[(df["Año"]==Año_2) & (df["Region_Homologada"].isin([select_region1,select_region2]))]
            df=df.groupby(["Region_Homologada","Mes"]).agg({"Número Postulaciones":"sum"}).reset_index()    
            df=df.rename(columns={"Número Postulaciones":"Postulaciones","Region_Homologada":"Región"})
            graf2 = px.line(df, x="Mes", y="Postulaciones",
                            title=f'<b>Postulaciones EEPP {Año_2}</b>',
                            color='Región')
            graf2.update_xaxes(title_text='Mes',tickmode='linear', dtick=1)
            graf2.update_traces(mode='lines+markers', marker=dict(size=8),line_shape='spline')
            st.plotly_chart(graf2,use_container_width=True)


        st.subheader("Concursos ADP")
        col1,col2=st.columns(2)
        with col1:
            Año_3=st.selectbox("Selecciona año",periodo_años,key="4")
        #fecha2=st.date_input("Fecha 2",value=pd.to_datetime("2021-09-01"))
        with col2:
            #st.write("Selecciona como quieres ver el dato")
            grafico_3=st.selectbox("Selecciona como quieres ver el dato",["Gráfico","Tabla"],key="5")

        if grafico_3=="Gráfico":
            df_adp=df_adp_concursos()
            df_adp["Mes"] = pd.to_datetime(df_adp["Fecha_Convocatoria"], format="%Y-%m-%d").dt.month
            df_adp=df_adp[(df_adp["Year_Convocatoria"]==Año_3) & (df_adp["Region_Homologada"].isin([select_region1,select_region2]))]
            df_adp=df_adp.groupby(["Region_Homologada","Mes"]).agg({"CD_Concurso":"count"}).reset_index()    
            df_adp=df_adp.rename(columns={"CD_Concurso":"Concursos","Region_Homologada":"Región","Year_Convocatoria":"Año"})
            graf3 = px.bar(df_adp, x="Mes", y="Concursos",title=f'<b>Concursos ADP {Año}</b>',
                color='Región', barmode='group',
                height=400)
            graf3.update_xaxes(title_text='Mes',tickmode='linear', dtick=1)
            st.plotly_chart(graf3,use_container_width=True)
 
        elif grafico_3=="Tabla":
            df_adp=df_adp_concursos()
            df_adp["Mes"] = pd.to_datetime(df_adp["Fecha_Convocatoria"], format="%Y-%m-%d").dt.month
            df_adp=df_adp[(df_adp["Year_Convocatoria"]==Año_3) & (df["Region_Homologada"].isin([select_region1,select_region2]))]
            df_adp=df_adp.groupby(["Region_Homologada","Mes","Nivel"]).agg({"CD_Concurso":"count"}).reset_index()    
            df_adp=df_adp.rename(columns={"CD_Concurso":"Concursos","Region_Homologada":"Región","Year_Convocatoria":"Año"})
            st.dataframe(df_adp,hide_index=True,width=600)
            st.download_button(label="Descargar datos",data=df.to_csv().encode("utf-8"),file_name=f"Concursos ADP {Año_2}.csv",mime="text/csv")
            

    if seleccion=="Por organismo":
        
        st.subheader("Seleccionar organismos a comparar")
        col1,col2=st.columns(2)
        with col1:
            select_organismo1=st.selectbox("Selecciona organismo N°1",org())
        with col2:
            select_organismo2=st.selectbox("Selecciona organismo N°2",org())
        if select_organismo1==select_organismo2:
            st.error("No se pueden seleccionar dos organismos iguales")
            st.stop()
        # Add horizontal line
        st.markdown("<hr>", unsafe_allow_html=True)

        col1,col2,col3=st.columns(3)
        with col1:
            tipo=st.selectbox("Selecciona el tipo de información a comparar",tipo_info_organismos)
        with col2:
            Año=st.selectbox("Selecciona año",periodo_años)
        #fecha2=st.date_input("Fecha 2",value=pd.to_datetime("2021-09-01"))
        with col3:
            grafico=st.selectbox("Selecciona como quieres ver el dato",["Gráfico","Tabla"])
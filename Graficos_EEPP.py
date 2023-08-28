import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go


#--funcion para traer datos y guardar en cache----
@st.cache_data
def get_data_1():
    df_postulaciones=pd.read_csv('datos/EEPP/postulaciones_x_año.csv',encoding='utf-8')
    return df_postulaciones
df_postulaciones=get_data_1()

def get_data_2():
    df_postulaciones_sexo=pd.read_csv('datos/EEPP/Porcentaje_Postulaciones_Sexo_e.csv')
    return df_postulaciones_sexo
df_postulaciones_sexo=get_data_2()

def get_data_3():
    df_postulaciones_promedio=pd.read_csv('datos/EEPP/Postulacion_Promedio_x_Año.csv')
    return df_postulaciones_promedio
df_postulaciones_promedio=get_data_3()

def get_data_4():
    df_convocatorias=pd.read_csv('datos/EEPP/Convocatorias_x_año.csv')
    return df_convocatorias
df_convocatorias=get_data_4()
    
def get_data_5():
    df_vacantes=pd.read_csv('datos/EEPP/Vacantes.csv')
    return df_vacantes
df_vacantes=get_data_5()

def get_data_6():
    df_ConvEnLinea=pd.read_csv('datos/EEPP/ConvEnLineaxAño.csv')
    return df_ConvEnLinea
df_ConvEnLinea=get_data_6()
    
    


date='31 de Agosto de 2023'

st.title('Estadísticas Portal Empleos Públicos')
st.subheader(date)

# define si se ven los ejes Y
visible_y_axis=False
#----------------------------------------------------------------------------------------------------------------------------
# grafico Evolución de Postulaciones por Año
graf1=px.bar(df_postulaciones,x='año',y='postulaciones',title='<b>Evolución de Postulaciones por Año</b>',text_auto=True).\
        update_yaxes(visible=visible_y_axis).\
                update_xaxes(title_text=None)

#----------------------------------------------------------------------------------------------------------------------------
#grafico 2: Distribución de Postulaciones por Sexo
# Load your data
df_postulaciones_sexo = pd.read_csv('datos/EEPP/Porcentaje_Postulaciones_Sexo_e.csv', encoding='utf-8', sep=";").\
                          update_yaxes(visible=visible_y_axis)#.update_xaxes(title_text=None)      

# Create separate DataFrames for "Mujeres" and "Hombres"
df_mujeres = df_postulaciones_sexo[df_postulaciones_sexo.Sexo == 'Mujeres']
df_hombres = df_postulaciones_sexo[df_postulaciones_sexo.Sexo == 'Hombres']

# Create the line plot using Plotly Express
graf2 = px.line(
    title='<b>Distribución de Postulaciones por Sexo</b>',
    labels={'year': 'Año', 'Porcentaje': 'Porcentaje'},  # Customize axis labels
)

# Add lines for "Mujeres" and "Hombres"
graf2.add_trace(
    go.Scatter(x=df_mujeres['year'], y=df_mujeres['Porcentaje'], mode='lines', name='Mujeres')
)
graf2.add_trace(go.Scatter(x=df_hombres['year'], y=df_hombres['Porcentaje'], mode='lines', name='Hombres'))

#----------------------------------------------------------------------------------------------------------------------------
# grafico Postulación Promedio por Año
graf3=px.bar(df_postulaciones,x='Año',y='Tasa Postulación Promedio - Concursos en Línea',title='<b>Evolución de postulaciones promedio por convocatoria por año</b>',text_auto=True).\
        update_yaxes(visible=visible_y_axis).\
                update_xaxes(title_text=None)




col1,col2,col3=st.columns(3)
with col1:
    st.plotly_chart(graf1,use_container_width=True)

with col2:
    st.plotly_chart(graf2,use_container_width=True)

with col3:
    st.plotly_chart(graf3,use_container_width=True)

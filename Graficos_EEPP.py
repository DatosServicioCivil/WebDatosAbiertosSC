import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go

st.set_page_config(layout='wide')

df_postulaciones=pd.read_csv('EEPP/postulaciones_x_año.csv',encoding='utf-8')    
df_postulaciones_sexo=pd.read_csv('EEPP/porcentaje_postulaciones_sexo_e.csv',sep=";")
df_postulaciones_promedio=pd.read_csv('EEPP/Postulacion_Promedio_x_Año.csv')
df_convocatorias=pd.read_csv('EEPP/Convocatorias_x_año.csv')
df_vacantes=pd.read_csv('EEPP/Vacantes.csv')
df_ConvEnLinea=pd.read_csv('EEPP/ConvEnLineaxAño.csv')

date='31 de Agosto de 2023'

st.title('Estadísticas Portal Empleos Públicos')
st.subheader(date)

# define si se ven los ejes Y
visible_y_axis=True
#----------------------------------------------------------------------------------------------------------------------------
# grafico Evolución de Postulaciones por Año
graf1=px.line(df_postulaciones,x='año',y='postulaciones',title='<b>Evolución de Postulaciones por Año</b>').\
        update_yaxes(visible=visible_y_axis).\
                update_xaxes(title_text=None)

#----------------------------------------------------------------------------------------------------------------------------
#grafico 2: Distribución de Postulaciones por Sexo
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
    go.Scatter(x=df_mujeres['year'], y=df_mujeres['Porcentaje'], mode='lines',line_shape='spline', name='Mujeres')
)
graf2.add_trace(go.Scatter(x=df_hombres['year'], y=df_hombres['Porcentaje'], mode='lines',line_shape='spline', name='Hombres'))

#----------------------------------------------------------------------------------------------------------------------------
# grafico Postulación Promedio por Año
graf3=px.line(df_postulaciones_promedio,x='Año',y='Tasa Postulación Promedio - Concursos en Línea',title='<b>Evolución de postulaciones promedio por convocatoria por año</b>').\
        update_yaxes(visible=visible_y_axis).\
                update_xaxes(title_text=None)




col1,col2,col3=st.columns(3,gap='small')
with col1:
    st.plotly_chart(graf1,use_container_width=True)

with col2:
    st.plotly_chart(graf2,use_container_width=True)

with col3:
    st.plotly_chart(graf3,use_container_width=True)

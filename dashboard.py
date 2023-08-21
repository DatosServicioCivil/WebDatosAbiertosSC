#---defino librerias----------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#--- Hide streamlit style-----
hide_st_style="""
<style>
    footer {visibility:hidden}
    header {visibility:hidden}  
</style>
"""

#st.markdown(hide_st_style)



#https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

st.set_page_config(page_title="Web Datos Abiertos Servicio Civil",\
                   layout='wide',\
                    initial_sidebar_state='expanded')

#--funcion para traer datos y guardar en cache----
@st.cache_data
def get_data():
        df=pd.read_csv('concursos_adp.csv')
        df=df[(df['Estado']!='Sin Efecto') & (df['Estado']!= 'SIN EFECTO')]
        df['Ministerio'] = df['Ministerio'].str.replace(r'(Ministerio de |Ministerio del )\s*', '', regex=True)
        df['Ministerio'] = df['Ministerio'].str.replace(r'(Ministerio )\s*', '', regex=True)
        df['Ministerio'] = df['Ministerio'].str.replace(r'(Culturas, las artes y el Patrimonio)\s*', 'Cultura', regex=True)
        df['Ministerio'] = df['Ministerio'].str.replace(r'(Ciencia, Tecnología, Conocimiento e Innovación)\s*', 'Ciencia', regex=True)
        return df

df=get_data()

visible_y_axis=False

st.markdown('#')
st.title(':flag-cl: Web Datos Abiertos Servicio Civil')


st.write(('El **Servicio Civil** pone a disposición de la ciudadania esta aplicación de **Datos Abiertos,** como una forma de rendir cuentas y generar dialogo horizontal y transparente'))




with st.sidebar:
        
        st.title('Filtros')
        Filtro_Nivel=st.multiselect(label='Nivel jerárquico',
                                    options=df['Nivel'].dropna().unique(),
                                    default=df['Nivel'].dropna().unique())
        Filtro_Adscrito=st.multiselect(label='Tipo de cargo',
                                    options=df['Adscrito'].dropna().unique(),
                                    default=df['Adscrito'].dropna().unique())
        #Filtro_Año=st.multiselect(label='año',
        #                            options=df['año'].dropna().unique(),
        #                            default=df['año'].dropna().unique())
        radio_filtro_ministerio=st.radio('Deseas filtrar por ministerio?',('No','Si'),horizontal=True)
        if radio_filtro_ministerio=='Si':
            Filtro_Ministerio=st.multiselect(label='Ministerio',
                                        options=df['Ministerio'].dropna().unique(),
                                        default=df['Ministerio'].dropna().unique())


if radio_filtro_ministerio=='No':
        df_select=df.query('Nivel==@Filtro_Nivel & Adscrito==@Filtro_Adscrito')
else:
        df_select=df.query('Nivel==@Filtro_Nivel & Adscrito==@Filtro_Adscrito & Ministerio==@Filtro_Ministerio')

tabla_grafico_1=df_select.groupby(['año']).agg(Concursos=('CD_Concurso','count')).reset_index()


if radio_filtro_ministerio=='Si' and len(Filtro_Ministerio)==1:
        tabla_grafico_2=df_select[df_select['Ministerio'].isin(Filtro_Ministerio)].groupby(['Servicio']).agg(Concursos=('CD_Concurso','count')).reset_index()
        graf2 = px.bar(tabla_grafico_2, y='Concursos', x='Servicio', text='Concursos',title=f'<b>Publicados por servicio</b>',).\
                update_yaxes(range=[0, max(tabla_grafico_2['Concursos']) * 1.1],visible=visible_y_axis).\
                        update_traces(texttemplate='%{text:.2s}', textposition='outside').\
                                update_layout(uniformtext_minsize=8, uniformtext_mode='hide').\
                                        update_xaxes(title_text=None)

else:
        tabla_grafico_2=df_select.groupby(['Ministerio']).agg(Concursos=('CD_Concurso','count')).reset_index()              
        graf2 = px.bar(tabla_grafico_2, y='Concursos', x='Ministerio', text='Concursos',title='<b>Publicados por ministerio</b>',).\
                update_yaxes(range=[0, max(tabla_grafico_2['Concursos']) * 1.1],visible=visible_y_axis).\
                        update_traces(texttemplate='%{text:.2s}', textposition='outside').\
                                update_layout(uniformtext_minsize=8, uniformtext_mode='hide').\
                                        update_xaxes(title_text=None)

tabla_detalle=df_select.groupby(['año','Nivel','Adscrito','Ministerio']).agg(Concursos=('CD_Concurso','count')).reset_index()

total_concursos_publicados=int(df.CD_Concurso.count())
cantidad_cargos_publicados=int(df.Cargo.nunique())
servicios=int(df.Servicio.nunique())
total_nombrados = df[df.Estado.isin(["CON NOMBRAMIENTO", "FINALIZADO", "Finalizado con nombramiento"])].CD_Concurso.count()

kpi1,kpi2,kpi3,kpi4=st.columns(4,gap='large')
with kpi1:
        st.image('imagenes/reclutamiento_seleccion.png',use_column_width='auto')
        st.metric(label='Concursos publicados:',value=total_concursos_publicados)
with kpi2:
        st.image('imagenes/cargo.jpeg',use_column_width='auto')
        st.metric(label='Cargos publicados:',value=cantidad_cargos_publicados)
with kpi3:
        st.image('imagenes/ministerio.png',use_column_width='auto')
        st.metric(label='Servicios con publicaciones:',value=servicios)
with kpi4:
        st.image('imagenes/seleccionado.png',use_column_width='auto')
        st.metric(label='Total ADP nombrados/as:',value=total_nombrados)
st.markdown('---')
st.markdown('##')
st.title(':bar_chart: Gráficos concursos publicados')

#my_pal = {año: "red" if año in [2006, 2010, 2014, 2018, 2022] else "blue" for año in tabla_grafico_1['año'].unique()}
inicio_gobierno = [2006, 2010, 2014, 2018, 2022]


graf1=px.bar(tabla_grafico_1,x='año',y='Concursos',title='<b>Publicados por año</b>',text_auto=True).\
        update_yaxes(visible=visible_y_axis).\
                update_xaxes(title_text=None).\
                        update_traces(marker=dict(color=['red' if year in inicio_gobierno else 'blue' for year in tabla_grafico_1['año']]))

col1,col2=st.columns(2,gap='large')
with col1:
        st.plotly_chart(graf1,use_container_width=True)
        st.write(f'En el 2004 el sistema de Alta Dirección Publica empieza funcionar. En su primer año convoca a concurso 16 cargos. En sus 20 años de fncionamiento el sistema a convocado **{total_concursos_publicados}** concursos tanto de primer como segundo nivel jerárquico.')
with col2:
        st.plotly_chart(graf2,use_container_width=True)

st.markdown('##')
st.title(':1234: Detalle concursos publicados')
st.dataframe(df_select.sort_values(by='año',ascending=True))






# streamlit run /Users/cristiangonzalezavalos/Desktop/Magister/streamlit/dashboard.py


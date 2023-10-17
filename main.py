from plotly import express as px
import numpy as np
import pandas as pd
import pyreadstat
import zipfile
import os
import re

if not os.path.exists('Data/'):
    os.mkdir('Data/')
    for _, _, f in os.walk('RawData/'):
        for file in f:
            f_name = 'RawData/' + file
            z_file = zipfile.ZipFile(f_name, 'r')
            year = '20' + ''.join(re.findall(f'\d+', f_name))
            z_file.extractall(f'Data/sav/{year}/')

if not os.path.exists('Data/data.csv') and os.path.exists('Data/sav/'):
    fix = {'l_format': 'l_formato', 'p_format': 'p_formato', 'r_format': 'r_formato', 'perslecl': 'persleclrp'}
    db = pd.DataFrame(
        columns=['p34_4', 'p32_6esp', 'p36_2', 'n_ren_ele', 'p25', 'p9', 'control', 'p10', 'p12_5', 'p6_2', 'p6_6esp',
                 'mat_lec', 'p12_7', 'p11_6esp', 'p7', 'p13', 'p22', 'p33_4', 'p30', 'p12_4', 'p32', 'p_formato',
                 'p12_3', 'p23_2', 'p9_5esp', 'p6_1', 'p26', 'p1', 'p6_5', 'p16', 'p11', 'p6_4', 'p18_5', 'factor',
                 'p29', 'p34_4_1', 'p18_4', 'p19', 'p35', 'p21_5esp', 'p18_2', 'p14_1', 'perslec', 'p17', 'p15_5esp',
                 'p8_1', 'viv_sel', 'p34_1', 'p2', 'p20_1', 'p3_1', 'p24', 'p27', 'p34_3_1', 'h_lec', 'p20_2',
                 'l_formato', 'p12_8', 'p15', 'folio', 'p12_6', 'p36_1', 'p12_2', 'r_formato', 'p36_4', 'p3_3', 'p34_2',
                 'p36_3', 'year', 'p33_2', 'anio', 'p12_9esp', 'p4', 'p12_1', 'p21', 'persleclrp', 'p6_3', 'p7_3',
                 'p23_1', 'p17_6esp', 'p12_9', 'p33_1', 'p28', 'p28_7esp', 'p33_3', 'hog_mud', 'periodo', 'p3_4', 'cd',
                 'cond_activ', 'p18_1', 'p3_2', 'p8_2', 'p13_3', 'p18_3', 'edad', 'p14_2', 'entidad', 'nivel', 'p31',
                 'sexo', 'p19_3', 'p5_6esp', 'p34_3', 'p3_5', 'p6_6', 'p25_6esp', 'p5', 'num_hog'])
    for _, dirname, _ in os.walk('Data/sav/'):
        for year in dirname:
            for _, _, files in os.walk(f'Data/sav/{year}'):
                for file in files:
                    f_name = f'Data/sav/{year}/{file}'
                    ndb, _ = pyreadstat.read_sav(f_name)
                    ndb.columns = ndb.columns.str.lower()
                    ndb.columns = ndb.columns.map(lambda x: fix.get(x, x))
                    ndb['year'] = year
                    db = pd.concat([db, ndb], join='inner')
    db.to_csv('Data/data.csv')

db = pd.read_csv('Data/data.csv')

db['sexo'] = db['sexo'].apply(lambda x: 'Hombre' if x == 1 else 'Mujer')

if not os.path.exists('Plots/'):
    os.mkdir('Plots/')

fig = px.histogram(db, x='sexo', color='year', barmode='group', title='Sexo de Encuestados por Año')
fig.update_layout(yaxis_title='Número de Personas', xaxis_title='Sexo')
fig.write_html('Plots/Sexo de Encuestados por Año.html')

fig = px.histogram(db, x='edad', color='year', barmode='overlay', title='Edad de Encuestados por Año')
fig.update_layout(yaxis_title='Número de Personas', xaxis_title='Año')

for trace in fig.data:
    avg = np.average(trace['x'])
    std = np.std(trace['x'])
    fig.add_vline(x=avg, line_dash='dash', line_color=trace['marker']['color'])
    fig.add_vline(x=avg+std, line_color=trace['marker']['color'])
    fig.add_vline(x=avg-std, line_color=trace['marker']['color'])

fig.write_html('Plots/Edad de Encuestados por Año.html')

fig = px.histogram(db, x='year', title='Encuestados por Año')
fig.update_layout(yaxis_title='Número de Personas', xaxis_title='Año')
fig.write_html('Plots/Encuestados por Año.html')

fig = px.histogram(db, x='p3_5', color='year', barmode='group', title='Lectura por Año', histnorm='percent')
fig.update_layout(yaxis_title='% de Personas', xaxis_title='Libros Leídos')

for trace in fig.data:
    avg = np.average(trace['x'])
    std = np.std(trace['x'])
    fig.add_vline(x=avg, line_dash='dash', line_color=trace['marker']['color'])
    fig.add_vline(x=avg+std, line_color=trace['marker']['color'])
    fig.add_vline(x=avg-std, line_color=trace['marker']['color'])

fig.write_html('Plots/Lectura por Año.html')


fig = px.histogram(db, x='sexo', y='p3_5', color='sexo', title='Lectura por Sexo', histfunc='avg')
fig.update_layout(yaxis_title='Promedio de Libros Leídos', xaxis_title='Libros Leídos')

fig.write_html('Plots/Lectura por Sexo.html')

fig = px.histogram(db, y='p3_5', x='year', color='sexo', barmode='group', title='Lectura por Sexo y Año', histfunc='avg')
fig.update_layout(yaxis_title='Promedio de Libros Leídos', xaxis_title='Año')

fig.write_html('Plots/Lectura por Sexo y Año.html')


fig = px.histogram(db, y='p3_5', x=['p6_2', 'p6_3', 'p6_4', 'p6_5'], barmode='group', title='Lectura por Genero de Libro', histnorm='percent')
fig.update_layout(yaxis_title='% de Personas', xaxis_title='Libros Leídos')

newnames = {
    'p6_2': 'Escolar',
    'p6_3': 'Autoayuda/Religioso',
    'p6_4': 'Literatura',
    'p6_5': 'Cultura General'
}

fig.for_each_trace(lambda t: t.update(name=newnames[t.name]))

fig.write_html('Plots/Lectura por Genero de Libro.html')

fig = px.histogram(db, y='p3_5', x='edad', color='year', barmode='overlay', title='Lectura por Edad y Año', histfunc='avg')
fig.update_layout(yaxis_title='Promedio de Libros Leídos', xaxis_title='Edad')

fig.write_html('Plots/Lectura por Edad y Año.html')

fig = px.histogram(db, y='p3_5', x='edad', barmode='overlay', title='Lectura por Edad', histfunc='avg')
fig.update_layout(yaxis_title='Promedio de Libros Leídos', xaxis_title='Edad')

fig.write_html('Plots/Lectura por Edad.html')

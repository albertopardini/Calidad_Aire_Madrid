import pandas as pd
import plotly.express as px


# Ruta al archivo CSV en Colab
rutaArchivo = 'calidad_aire_datos_mes.csv'

calidadAireDatosMes = pd.read_csv(rutaArchivo, thousands='.', decimal=',',sep=';')

# Mostrar las primeras filas del conjunto de datos
#print(calidadAireDatosMes)

# Especificar las columnas desde 'h01' hasta 'h24'
columns_to_check = [f'h{i:02d}' for i in range(1, 25)]

# Borrar las filas donde cualquiera de las columnas especificadas tenga un valor nulo
calidadAireDatosMes = calidadAireDatosMes.dropna(subset=columns_to_check)
#calidadAireDatosMes

# Especificar las columnas a eliminar
columns_to_drop = ['provincia', 'punto_muestreo'] + [f'v{i:02d}' for i in range(1, 25)]
# Eliminar las columnas especificadas
calidadAireDatosMes = calidadAireDatosMes.drop(columns=columns_to_drop)

# Seleccionar las columnas desde 'h0' hasta 'h24'
columnasHoras = calidadAireDatosMes.filter(like='h')
minimoPorFila = columnasHoras.min(axis=1).round(2)
maximoPorFila = columnasHoras.max(axis=1).round(2)
promedioPorFila = columnasHoras.mean(axis=1).round(2)

# Agrega al dataframe la columna 'prom_dia' y 'max_dia'
calidadAireDatosMes ['min_dia'] = minimoPorFila
calidadAireDatosMes ['max_dia'] = maximoPorFila
calidadAireDatosMes ['prom_dia'] = promedioPorFila

# Definir un diccionario para mapear los códigos de magnitud a sus descripciones
magnitud_descripcion = {
    1:'Dióxido de azufre',
    6:'Monóxido de carbono',
    7:'Monóxido de nitrógeno',
    8:'Dióxido de nitrógeno',
    9:'Partículas en suspensión < PM2.5',
    10:'Partículas en suspensión< PM10',
    11:'Partículas en suspensión< PM1',
    12:'Óxidos de nitrógeno',
    14:'Ozono',
    20:'Tolueno',
    22:'Black Carbon',
    30:'Benceno',
    42:'Hidrocarburos totales',
    44:'Hidrocarburos no metánicos',
    431:'MetaParaXileno'
}

# Crear la columna 'magnitud_descrip' utilizando el diccionario
calidadAireDatosMes['magnitud_descrip'] = calidadAireDatosMes['magnitud'].map(magnitud_descripcion)

# Mostrar las primeras filas del DataFrame actualizado
#print(calidadAireDatosMes.head())

# Definir un diccionario para mapear los códigos de municipios a sus nombres de estación.
nombre_estacion = {
    5:'ALCALA DE HENARES',
    6:'ALCOBENDAS',
    7:'ALCORCON',
    9:'ALGETE',
    13:'ARANJUEZ',
    14:'ARGANDA DEL REY',
    16:'ATAZAR, EL',
    45:'COLMENAR VIEJO',
    47:'COLLADO VILLALBA',
    49:'COSLADA',
    58:'FUENLABRADA',
    65:'GETAFE',
    67:'GUADALIX DE LA SIERRA',
    74:'LEGANES',
    80:'MAJADAHONDA',
    92:'MOSTOLES',
    102:'ORUSCO DE TAJUÑA',
    106:'PARLA',
    115:'POZUELO DE ALARCÓN',
    120:'PUERTO DE COTOS',
    123:'RIVAS-VACIAMADRID',
    127:'ROZAS, LAS',
    133:'SAN MARTÍN DE VALDEIGLESIAS',
    134:'SAN SEBASTIAN DE LOS REYES',
    148:'TORREJÓN DE ARDOZ',
    161:'VALDEMORO',
    171:'VILLA DEL PRADO',
    180:'VILLAREJO DE SALVANÉS'
}

# Crear la columna 'nombre_estacion' utilizando el diccionario
calidadAireDatosMes['nombre_estacion'] = calidadAireDatosMes['municipio'].map(nombre_estacion)

# Mostrar las primeras filas del DataFrame actualizado
#print(calidadAireDatosMes.tail())

magnitudDiaEstacion=calidadAireDatosMes[['dia','min_dia','max_dia','prom_dia','magnitud_descrip','nombre_estacion']].sort_values(by='dia',ascending=True)
print(magnitudDiaEstacion)

magnitudEstacionMinMaxProm = magnitudDiaEstacion.groupby(['magnitud_descrip', 'nombre_estacion']).agg({'min_dia': 'min', 'max_dia': 'max', 'prom_dia': 'mean'}).round(2)
print(magnitudEstacionMinMaxProm)

# Crea el gráfico animado de barras
fig = px.bar(calidadAireDatosMes, x="magnitud_descrip", y="max_dia",color="magnitud_descrip",
             animation_frame="dia",animation_group="magnitud_descrip",
             range_y=[0,350],
             title='MADRID - CONTAMINANTES EN EL AIRE - OCTUBRE 2024')
fig.update_layout(
    title={
        'text': 'MADRID - CONCENTRACION MAXIMA CONTAMINANTES EN AIRE - OCT/24',
        'x': 0.5,  # Centra el título en el gráfico
        'font': {'size': 22, 'color': 'black', 'family': 'Arial', 'weight': 'bold'}},
    xaxis_title={"text":"Sustancias","standoff":40,'font': {'size': 18, 'color': 'black', 'family': 'Arial', 'weight': 'bold'}},
    yaxis_title={"text":"Concentración [µg/m³]","standoff":20,'font': {'size': 18, 'color': 'black', 'family': 'Arial', 'weight': 'bold'}},
    hovermode="x unified"
)

fig.show()
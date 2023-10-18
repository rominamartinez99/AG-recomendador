import csv
import random


def info_completa_csv(filename):
    datos = []
    with open(filename, 'r', newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        next(lector_csv)  # Omitir la línea de encabezados
        
        for fila in lector_csv:
            if len(fila) > 0:
                grupo = [campo.strip() for campo in fila]
                datos.append(grupo)
    return datos

def generar_poblacion_inicial_con_CSV(filename):
    datos = []
    grupo = []
    with open(filename, 'r', newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        next(lector_csv)  # Omitir la línea de encabezados
        for fila in lector_csv:
            if len(fila) > 0:
                primera_columna = fila[0].split(';')[0].strip()
                grupo.append(primera_columna)
                if len(grupo) == 5:
                    aptitud = calcular_aptitud_general(grupo,info_completa)
                    grupo.append(aptitud)
                    datos.append(grupo)
                    grupo = []  # Reiniciar el grupo
    return datos

def cruzamiento_simple_padres(padre1, padre2):
    hijo = []
    hijo.append(padre1[0])
    hijo.append(padre1[1])
    hijo.append(padre1[2])
    hijo.append(padre2[3])
    hijo.append(padre2[4])
    return hijo
    
def nueva_poblacion_por_cruzamiento(poblacion_elegida):
    descendencia = []
    for i in range(0, len(poblacion_elegida)-1, 2):
        nuevo_hijo = cruzamiento_simple_padres(poblacion_elegida[i], poblacion_elegida[i+1])
        aptitud_hijo = calcular_aptitud_general(nuevo_hijo,info_completa)
        nuevo_hijo.append(aptitud_hijo)
        descendencia.append(nuevo_hijo)
    nuevo_hijo = cruzamiento_simple_padres(poblacion_elegida[0], poblacion_elegida[len(poblacion_elegida)-1])
    descendencia.append(nuevo_hijo)
    aptitud_hijo = calcular_aptitud_general(nuevo_hijo,info_completa)
    nuevo_hijo.append(aptitud_hijo)
    return descendencia 

info_completa = info_completa_csv('titles1.csv')

def calcular_aptitud(id_titulo,info_completa): #TODO Completar el resto de los atributos
	valor_aptitud = 0
	for elemento in info_completa:
		if(elemento[0] == id_titulo):
			if (elemento[2]==tipo):
				valor_aptitud += 10
			else:
				valor_aptitud -= 10
				
			#if usuario['genero'] in info_show['genres'].values[0]:
			#	valor_aptitud += 15
			#else:
			#	valor_aptitud -= 15
			
			# Verificar si la información del show coincide con los criterios del usuario
			#if info_show['type'].values[0] == usuario['tipo']:
			#	valor_aptitud += 10
			#else:
			#	valor_aptitud -= 10


			# Aplicar la función de limpieza a la calificación
			#imdb_score_cleaned = limpiar_calificaciones(info_show['imdb_score'].values[0])
			#if float(imdb_score_cleaned) >= usuario['calificacion']:
			#	valor_aptitud += 5
			#else:
			#	valor_aptitud -= 5		
	return valor_aptitud

def calcular_aptitud_general(recomendacion,info_completa):
	valor_aptitud = 0
	for i in range (5): 
			id_titulo = recomendacion[i]
			valor_aptitud = valor_aptitud + calcular_aptitud(id_titulo, info_completa)
	return valor_aptitud
	
def seleccion_por_ranking(poblacion_actual):
    poblacion_ordenada = sorted(poblacion_actual, key=lambda x: x[5], reverse=True)
    #Construir la nueva población con la cantidad de apariciones elegidas para cada uno de los mejores
    nueva_poblacion = []

    #Apariciones del primero
    for i in range(100):  # Hasta acá hay 200
        nueva_poblacion.append(poblacion_ordenada[i])
        nueva_poblacion.append(poblacion_ordenada[i])

    for i in range(100, len(poblacion_ordenada) - 100):
        nueva_poblacion.append(poblacion_actual[i])

    return nueva_poblacion


def mutar_poblacion(poblacion_actual): #TODO
	return 1
	
#Ejecucion del Algoritmo Genetico

#TODO: input del usuario
tipo = 'SHOW'
prob_mut = 0 #A definir
vueltas = 0 #A definir

poblacion = generar_poblacion_inicial_con_CSV('titles1.csv')

for i in range (vueltas):
    nueva_poblacion = seleccion_por_ranking(poblacion)
    descendencia = nueva_poblacion_por_cruzamiento(nueva_poblacion)
    poblacion = descendencia
    r = random(0,1)
    if (r <= prob_mut):
		poblacion = mutacion(poblacion)

poblacion_final = sorted(poblacion, key=lambda x: x[5], reverse=True)
#TODO: buscar por ID los títulos para imprimir
print("Su recomendación es", poblacion_final[0])

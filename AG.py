import csv
import random

archivo = 'titles14.csv'
archivo_actores = 'credits1.csv'

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

def obtener_actores_por_pelicula(archivo_actores):
	datos_agrupados = {}
	with open(archivo_actores, 'r', newline='', encoding='utf-8') as archivo_csv:
		lector_csv = csv.reader(archivo_csv)
		next(lector_csv)  # Omitir la línea de encabezados

		# Recorre las filas del CSV
		for fila in lector_csv:
			titulo = fila[1]
			actores = fila[2]

			# Si la columna A no está en el diccionario, crea una nueva entrada
			if titulo not in datos_agrupados:
				datos_agrupados[titulo] = []

			# Agrega el valor de la columna B a la lista correspondiente en el diccionario
			datos_agrupados[titulo].append(actores)

	# Convierte el diccionario a una lista de listas
	resultado = [[clave, valores] for clave, valores in datos_agrupados.items()]
	return resultado

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
                    aptitud = calcular_aptitud_general(grupo, info_completa)
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
    for i in range(0, len(poblacion_elegida) - 1, 2):
        nuevo_hijo = cruzamiento_simple_padres(poblacion_elegida[i], poblacion_elegida[i+1])
        aptitud_hijo = calcular_aptitud_general(nuevo_hijo, info_completa)
        nuevo_hijo.append(aptitud_hijo)
        descendencia.append(nuevo_hijo)
    nuevo_hijo = cruzamiento_simple_padres(poblacion_elegida[0], poblacion_elegida[len(poblacion_elegida) - 1])
    descendencia.append(nuevo_hijo)
    aptitud_hijo = calcular_aptitud_general(nuevo_hijo, info_completa)
    nuevo_hijo.append(aptitud_hijo)
    return descendencia

info_completa = info_completa_csv(archivo)
lista_actores = obtener_actores_por_pelicula(archivo_actores)

def calcular_aptitud(id_titulo, info_completa):
    valor_aptitud = 0
    for elemento in info_completa:
        if elemento[0] == id_titulo:
            if elemento[2] == tipo:  # Show o movie
                valor_aptitud += 20
                if tipo == "SHOW":
                    if float(elemento[6]) <= duracion:
                        valor_aptitud += 15
                    else:
                        valor_aptitud -= 10
                else:
                    if float(elemento[4]) <= duracion:
                        valor_aptitud += 15
                    else:
                        valor_aptitud -= 10
            else:
                valor_aptitud -= 10

            if int(elemento[3]) >= anio:  # Año de estreno
                valor_aptitud += 5
            else:
                valor_aptitud -= 5
            if genero in elemento[5]:
                valor_aptitud += 15
            else:
                valor_aptitud -= 15
            if elemento[7]:
                if float(elemento[7]) >= puntuacion:
                    valor_aptitud += 3
                else:
                    valor_aptitud -= 3
            if elemento[8]:
                elemento[8] = elemento[8].replace(",", ".")
                if float(elemento[8]) >= puntuacion:
                    valor_aptitud += 3
                else:
                    valor_aptitud -= 3

    if actor != "-":
        for elemento in lista_actores:
            if elemento[0] == id_titulo:
                if actor in elemento[1]:
                    valor_aptitud += 15
                else:
                    valor_aptitud -= 10
    return valor_aptitud



def calcular_aptitud_general(recomendacion, info_completa):
    valor_aptitud = 0
    for i in range(5):
        id_titulo = recomendacion[i]
        valor_aptitud += calcular_aptitud(id_titulo, info_completa)
    return valor_aptitud

def seleccion_por_ranking(poblacion_actual):
    poblacion_ordenada = sorted(poblacion_actual, key=lambda x: x[5], reverse=True)
    # Construir la nueva población con la cantidad de apariciones elegidas para cada uno de los mejores
    nueva_poblacion = []

    #Apariciones del primero
    for i in range(100):  #Hasta acá hay 200
        nueva_poblacion.append(poblacion_ordenada[i])
        nueva_poblacion.append(poblacion_ordenada[i])

    for i in range(100, len(poblacion_ordenada) - 100):
        nueva_poblacion.append(poblacion_actual[i])

    return nueva_poblacion

def mutar_poblacion(poblacion):
    aux = poblacion
    cromosoma_a_cambiar = random.randint(0,len(poblacion)-1)
    posicion_a_cambiar = random.randint(0,4)
    cromosoma_a_copiar = random.randint(0,len(poblacion)-1)
    posicion_a_copiar = random.randint(0,4)
    nueva_peli = aux[cromosoma_a_copiar][posicion_a_copiar]
    aux[cromosoma_a_cambiar][posicion_a_cambiar] = nueva_peli
    return aux


def imprimir_recomendacion(poblacion):
	poblacion_final = sorted(poblacion, key=lambda x: x[5], reverse=True)
	for i in range(5):
		for elemento in info_completa:
			if (elemento[0] == poblacion_final[0][i]):
				print(i+1,')',elemento[1],'\n')
				
def get_user_data():
    # Opciones predefinidas en inglés
    genres = ['documentation', 'war', 'drama', 'crime', 'history', 'animation', 'sport', 'horror', 'fantasy', 'european', 'reality', 'romance', 'western', 'comedy', 'music', 'family', 'thriller', 'scifi', 'action']
    ratings = ["0-3", "4-7", "8-10"]
    content_types = ["MOVIE", "SHOW"]

    # Traducción de géneros y tipos al español
    generos_en_espanol = ['Documental', 'Guerra', 'Drama', 'Crimen', 'Historia', 'Animacion', 'Deporte', 'Terror', 'Fanatasia', 'Europeas', 'Realidad', 'Romance', 'Western', 'Comedia', 'Musical', 'Familia', 'Thriller', 'Ciencia Ficcion', 'Accion']
    tipo_en_espanol = ["Pelicula", "Serie"]
    print("¡Bienvenido al recomendador de contenido del grupo 3 de IA!")
    # Preguntar al usuario en español sobre el género
    print("A continuación deberás elegir algunos datos para que podamos buscar el mejor contenido en base a tus preferencias.")
    print("Opciones de género:")
    for i, genero in enumerate(generos_en_espanol, 1):
        print(f"{i}. {genero}")
    
    while True:
        try:
            genre_id = int(input("Elige el ID del género que deseas: "))
            if 1 <= genre_id <= len(generos_en_espanol):
                break
            else:
                print("ID incorrecto. Introduce un ID válido.")
        except ValueError:
            print("Entrada no válida. Introduce un número entero válido.")

    chosen_genre = genres[genre_id - 1]
		
    # Preguntar al usuario en español sobre la calificación
    
    while True:
        try:
            rating_id = int(input("Elige el número de calificación mínima que prefieres del 1 al 10: "))
            if 1 <= rating_id <= 10:
                break
            else:
                print("Número incorrecto. Introduce un número del 1 al 10.")
        except ValueError:
            print("Entrada no válida. Introduce un número entero válido.")

    chosen_rating = rating_id

    while True:
        try:
            min_year = int(input("Elige el año de estreno a partir del cual te interesa el contenido: "))
            if 1900 <= min_year <= 2023:
                break
            else:
                print("Entrada no válida. Ingrese un año válido (ejemplo: 1995).")
        except ValueError:
            print("Entrada no válida. Ingrese un año válido (ejemplo: 1995).")

    chosen_year = min_year

    # Preguntar al usuario en español sobre el tipo de contenido
    print("\nOpciones de tipo de contenido:")
    for i, content_type in enumerate(tipo_en_espanol, 1):
        print(f"{i}. {content_type}")

    while True:
        try:
            content_type_id = int(input("Elige el ID del tipo de contenido: "))
            if 1 <= content_type_id <= len(tipo_en_espanol):
                break
            else:
                print("ID incorrecto. Introduce un ID válido.")
        except ValueError:
            print("Entrada no válida. Introduce un número entero válido.")

    chosen_content_type = content_types[content_type_id - 1]

    while True:
        try:
            if chosen_content_type == "SHOW":
                duracion = int(input("Elige la cantidad máxima de temporadas deseada: "))
            else:
                duracion = int(input("Elige la cantidad máxima de minutos de duración deseada: "))

            if duracion > 0:
                break  # Si es un número válido, sal del bucle
            else:
                print("Por favor, ingrese un número entero mayor a cero. Intente nuevamente.")
        except ValueError:
            print("Entrada no válida. Ingrese un número entero mayor a cero.")

    actor = input("Ingresa el nombre y/o apellido de un actor o actriz deseado. Si no tenes preferencia, ingresá un guión '-':")
    # Devolver las opciones elegidas en un diccionario
    user_data = {
        "genre": chosen_genre,
        "rating": chosen_rating,
        "content_type": chosen_content_type,
        "year": chosen_year,
        "actor": actor,
        "duracion": duracion
    }

    return user_data

# Ejecución del Algoritmo Genético

#Input del usuario
datos_usuario = get_user_data()
print("\nDatos ingresados correctamente. ¡Estamos buscando lo mejor para vos!")

tipo = datos_usuario["content_type"]
genero = datos_usuario["genre"]
puntuacion = float(datos_usuario["rating"])
anio = datos_usuario["year"]
actor = datos_usuario["actor"]
duracion = datos_usuario["duracion"]

#tipo = 'MOVIE'
#genero = 'romance'
#puntuacion = 6.0
prob_mut = 0.5
vueltas = 100

#Generar poblacion inicial
poblacion = generar_poblacion_inicial_con_CSV(archivo)

#Ciclos - criterio de paro
for i in range(vueltas):
    #Operador seleccion
    nueva_poblacion = seleccion_por_ranking(poblacion)
    #Operador cruzamiento
    descendencia = nueva_poblacion_por_cruzamiento(nueva_poblacion)
    poblacion = descendencia
    #Operador mutacion
    r = random.uniform(0,1)
    if r <= prob_mut:
        poblacion = mutar_poblacion(poblacion)

#Mejor individuo
print("\nTe recomendamos:")
imprimir_recomendacion(poblacion)

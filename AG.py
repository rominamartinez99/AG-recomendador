import csv
import random

archivo = 'titles13.csv'

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

def calcular_aptitud(id_titulo, info_completa):
    valor_aptitud = 0
    for elemento in info_completa:
        if (elemento[0] == id_titulo):
            if (elemento[2] == tipo):
                valor_aptitud += 10
            else:
                valor_aptitud -= 10
            if (genero in elemento[5]):
                valor_aptitud += 15
            else:
                valor_aptitud -= 15
            if(elemento[7]):
                if (float(elemento[7]) >= puntuacion):
                    valor_aptitud += 5
                else:
                    valor_aptitud -= 5
            if(elemento[8]):
                elemento[8] = elemento[8].replace(",", ".")
                if (float(elemento[8]) >= puntuacion):
                    valor_aptitud += 5
                else:
                    valor_aptitud -= 5
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
    content_types = ["SHOW", "MOVIE"]

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
            if min_year >= 0:
                break
            else:
                print("Número incorrecto. Introduce un número mayor a cero.")
        except ValueError:
            print("Entrada no válida. Introduce un número entero mayor a cero.")

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

    # Devolver las opciones elegidas en un diccionario
    user_data = {
        "genre": chosen_genre,
        "rating": chosen_rating,
        "content_type": chosen_content_type,
        "year": chosen_year
    }

    return user_data

datos_usuario = get_user_data()
print("\nDatos ingresados correctamente, estamos buscando lo mejor para vos!.")

# Ejecución del Algoritmo Genético

#Input del usuario

tipo = datos_usuario["content_type"]
genero = datos_usuario["genre"]
puntuacion = datos_usuario["rating"]
anio = datos_usuario["year"]

#tipo = 'MOVIE'
#genero = 'romance'
#puntuacion = 6.0
prob_mut = 0.5
vueltas = 10


poblacion = generar_poblacion_inicial_con_CSV(archivo)

for i in range(vueltas):
    nueva_poblacion = seleccion_por_ranking(poblacion)
    descendencia = nueva_poblacion_por_cruzamiento(nueva_poblacion)
    poblacion = descendencia
    r = random.uniform(0,1)
    if r <= prob_mut:
        poblacion = mutar_poblacion(poblacion)

print("\nTe recomendamos:")
imprimir_recomendacion(poblacion)


print(calcular_aptitud('ts300399',info_completa)) #tiene ceros
print(calcular_aptitud('tm82169',info_completa)) #tiene comas
print(calcular_aptitud('tm191099',info_completa)) #tiene puntos

import sys
from lifestore_file import lifestore_searches as searches # [id_search, id product]
from lifestore_file import lifestore_sales as sales # [id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)]
from lifestore_file import lifestore_products as products # [id_product, name, price, category, stock]
from collections import Counter
import numpy as np
import pandas as pd
# 1) productos más vendidos y rezagados [cat = menores ventas, menores búsquedas]
## 1.1) Listado de los 5 productos mas vendidos y otra con los 10 más buscados
## 1.2) Por categoría, listado de los 5 productos menos vendidos, y los 10 menos buscados
# 2) productos por reseña [cat = mayores ventas, mayores búsquedas]
## 2.1) 2 listados, 5 prod c/una, una de los mejores reseñados y el de los peores, considera devolucion de productos
# 3) Sugerir:
## 3.1) productos a retirar del mercado
## 3.2) estrategia de reduccion de inventario acumulado [cat= datos de ingresos y ventas]

"""
Primera tutoria -- Sesion de dudas

MEJORES PRÁCTICAS:
 >>> Dejar el archivo (.py) de las listas exclusivo para eso. [OK]
 >>> Crear otro archivo con el código e instrucciones para el proyecto (main.py) [OK]

 Formateo en prints:
 print('El precio es: ', producto[columna_del_precio])
 print('El precio de ', producto[tal], 'es de ', producto[precio])
 print(f'El precio de {producto} es de {precio}')

 * para evitar prints tan largos, pueden guardarse en variables los accesos a los datos
"""
# Sistema de usuarios que pueda funcionar en versiones 2 ó 3 de Python. Tiene límite de intentos.
user_db = {}
fails = 0
user_logged = False

while user_logged == False:
    if fails == 3:
        sys.exit('\nHa excedido el número de intentos. Vuelva a ejecutar este programa.')
    if sys.version_info.major == 2:
        user = raw_input('\nCrea o ingresa tu nombre de usuario: \n')
        if user in user_db.keys():
            password = raw_input(f'\nIngresa tu contraseña {user}: \n')
            if password == user_db[user]:
                print(f'\nBienvenido(a) {user}\n')
                user_logged = True
            else:
                print('\nContraseña incorrecta. Intenta de nuevo\n')
                fails += 1
        else:
            password = raw_input('\nRegistra una contraseña para tu usuario: \n')
            user_db[user] = password

    elif sys.version_info.major == 3:
        user = input('\nCrea o ingresa tu nombre de usuario si ya tienes uno: \n')
        if user in user_db.keys():
            password = input(f'\nIngresa tu contraseña {user}: \n')
            if password == user_db[user]:
                print(f'\nBienvenido(a) {user}\n')
                user_logged = True
            else:
                print('\nContraseña incorrecta. Intenta de nuevo\n')
                fails += 1
        else:
            password = input('\n¡Te has registrado! Crea una contraseña para tu usuario: \n')
            user_db[user] = password
            print('\nContraseña registrada con éxito\n')

# Booleano iniciador
done = False

while True: # Ejecuta hasta que el booleano cambie de estado
    try:
    #while fails <= 3: # Ejecuta hasta que los fallos acumulados sean menores o iguales a 3
        # Programa para Python 2.x
        if sys.version_info.major == 2:
            query = raw_input("""\n¿Qué consulta desea realizar?\n 
            \nSi desea revisar los datos tabulares de búsquedas de productos, ingrese '1'\n
            \nSi desea revisar los datos tabulares de ventas de productos, ingrese '2'\n
            \nSi desea revisar las especificaciones de los productos a la venta, ingrese '3'\n
            \nPara consultar los productos con mayores o menores ventas ingrese '4' \n
            \nPara consultar los productos con mayores o menores búsquedas ingrese '5'\n
            \nPara consultar los productos con mejores o peores reseñas, ingrese '6'\n
            \nPara consultar detalles sobre ingresos y ventas, ingrese '7'\n
            \nSi desea cerrar este programa, ingrese '0'\n
            """)
            if query == '0':
                done = True
            elif query == '1':
                details = raw_input('\n¿Desea un listado detallado con nombre del producto y su ID? s/n\n')
                if details == 's':
                    for search in searches: # [id_search, id product] ... products -> [id_product, name, price, category, stock]
                        print(f'La búsqueda #{search[0]} corresponde al producto {"".join([product[1] for product in products if product[0] == search[1]])} de ID {search[1]}')
                elif details == 'n':
                    for search in searches:
                        print(*search)
                else:
                    print('Entrada inválida. Intente de nuevo')
                    fails += 1
                
                # Reajustar consulta
                query = raw_input("""\n¿Qué otra consulta desea realizar?\n 
                \nSi desea revisar los datos tabulares de búsquedas de productos otra vez, ingrese '1'\n
                \nSi desea revisar los datos tabulares de ventas de productos, ingrese '2'\n
                \nSi desea revisar las especificaciones de los productos a la venta, ingrese '3'\n
                \nPara consultar los productos con mayores o menores ventas ingrese '4' \n
                \nPara consultar los productos con mayores o menores búsquedas ingrese '5'\n
                \nPara consultar los productos con mejores o peores reseñas, ingrese '6'\n
                \nPara consultar detalles sobre ingresos y ventas, ingrese '7'\n
                \nSi desea cerrar este programa, ingrese '0'\n
                """)
            elif query == '2':
                details = raw_input('\n¿Desea un listado detallado con nombre del producto y su ID? s/n\n')
                if details == 's':
                    for sale in sales: # [id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)] ... products -> [id_product, name, price, category, stock]
                        print(f'La venta #{sale[0]} corresponde al producto {"".join([product[1] for product in products if product[0] == sale[1]])} de ID {sale[1]}')
                elif details == 'n':
                    for sale in sales:
                        print(*sale)
                else:
                    print('Entrada inválida. Intente de nuevo')
                    fails += 1
                
                # Reajustar consulta
                query = raw_input("""\n¿Qué otra consulta desea realizar?\n 
                \nSi desea revisar los datos tabulares de búsquedas de productos, ingrese '1'\n
                \nSi desea revisar los datos tabulares de ventas de productos otra vez, ingrese '2'\n
                \nSi desea revisar las especificaciones de los productos a la venta, ingrese '3'\n
                \nPara consultar los productos con mayores o menores ventas ingrese '4' \n
                \nPara consultar los productos con mayores o menores búsquedas ingrese '5'\n
                \nPara consultar los productos con mejores o peores reseñas, ingrese '6'\n
                \nPara consultar detalles sobre ingresos y ventas, ingrese '7'\n
                \nSi desea cerrar este programa, ingrese '0'\n
                """)
            elif query == '3':
                details = raw_input('\n¿Desea un listado detallado de los productos? s/n\n')
                if details == 's': # [id_product, name, price, category, stock]
                    for product in products:
                        print(f'El producto {product[1]}, de ID {product[0]}, en la categoría {product[3]}, tiene un precio de {product[2]} y un total de {product[4]} unidad(es) en existencia')
                elif details == 'n':
                    for product in products:
                        print(*product)
                else:
                    print('Entrada inválida. Intente de nuevo')
                    fails += 1
                
                # Reajustar consulta
                query = raw_input("""\n¿Qué otra consulta desea realizar?\n 
                \nSi desea revisar los datos tabulares de búsquedas de productos, ingrese '1'\n
                \nSi desea revisar los datos tabulares de ventas de productos, ingrese '2'\n
                \nSi desea revisar las especificaciones de los productos a la venta otra vez, ingrese '3'\n
                \nPara consultar los productos con mayores o menores ventas ingrese '4' \n
                \nPara consultar los productos con mayores o menores búsquedas ingrese '5'\n
                \nPara consultar los productos con mejores o peores reseñas, ingrese '6'\n
                \nPara consultar detalles sobre ingresos y ventas, ingrese '7'\n
                \nSi desea cerrar este programa, ingrese '0'\n
                """)
            elif query == '4': # Para consultar los productos con mayores o menores ventas ingrese '4'

                # 1) Conformar lista anidada [ID_prod, name, category, sales]

                # 1.1) Poblar lista nueva con las listas de [ID_prod, name, category]
                i = 0 # contador para iterar
                product_id_sales = []
                for product in products:
                    product_id_sales.append(product) # Agrega toda la lista de cada producto de la base de datos
                    product_id_sales[i].pop(2) # Remueve ['price'] y actualiza los índices a la derecha del elemento removido
                    product_id_sales[i].pop(3) # Remueve ['stock'] >> Se volvió índice 3 por la actualización anterior
                    i += 1 # actualiza contador

                # 2) Obtener las ventas que tuvo cada producto por categorías (se necesitará más adelante)
                sales_by_category = Counter(i[2] for i in product_id_sales) # donde i es cada entrada (lista) y 2 el índice ['category']

                # 1.2) Bucle para añadir la cantidad de ventas, 0 o la que le corresponda al producto
                for product in product_id_sales: # repasa cada entrada (lista) de la lista anteriormente poblada
                    if product[0] not in sales_by_category.keys(): # Si el id_product NO ESTÁ en el diccionario de conteo de ventas
                        product.append(0) # agrega entonces 0 ventas
                    else: 
                        for id_product in sales_by_category.keys(): # repasa todos los id_product del conteo de ventas
                            if id_product == product[0]: # si el id_product del conteo de ventas es igual al de la entrada (lista) en turno
                                product.append(dict(sales_by_category)[id_product]) # concatena el valor que le corresponde a la key 'id_product' en el diccionario
            
                # 1.3) Ordenar la lista completa de menores a mayores ventas
                sorted(product_id_sales, key=lambda x: x[3]) # donde X es cada entrada (lista) y 3 el índice ['sales']

                

                # 3) Recibir input del usuario sobre cómo quiere visualizar los resultados

                # Ciclo para permanecer en elección de categorias
                in_categories == True

                while in_categories == True:

                    # 3.1) Almacenar la categoría a consultar
                    categ = input("""\n¿Qué categoría desea consultar?\n 
                    \nTodas, ingrese '0' \n
                    \nAudífonos, ingrese '1'\n
                    \nBocinas, ingrese '2'\n
                    \nDiscos duros, ingrese '3'\n
                    \nMemorias USB, ingrese '4' \n
                    \nPantallas, ingrese '5'\n
                    \nProcesadores, ingrese '6'\n
                    \nTarjetas de video, ingrese '7'\n
                    \nTarjetas madre, ingrese '8'\n
                    \nPara retroceder a otras opciones, ingrese '9'\n
                    """)

                    # 3.1.1) Verifica que la entrada sea número entero
                    if isinstance(categ, int): # Devuelve True si el input es 'integer'

                        if categ == '9':
                            in_categories = False

                        # 3.2) Con el punto 3.1.1) validado, procede a almacenar la cantidad de items a mostrar. 
                        amount = input("""A continuación se mostrarán los productos ordenados por ventas.\n 
                        Por favor, indique el número de items más vendidos y menos vendidos que desea ver.\n 
                        Para verlos todos ingrese '0'\n
                        """)

                        # 3.2.1) Verifica que la entrada sea número entero
                        if isinstance(amount, int): # Devuelve True si el input es 'integer'

                            # 3.3) Todas las categorias
                            if categ == '0':

                                # 3.3.1) Entrada 0 -> Todos los items
                                if amount == '0':
                                    for i in product_id_sales:
                                        print(f'El producto {i[1].split(",")[0]}, de ID {i[0]} y categoría {i[2]}, vendió {i[3]} unidades')

                                # 3.3.2) Número que excede el número de ventas ingresado. Error.
                                elif amount not in range(1, sum(sales_by_category.values())): # rango de 1 a la suma de las ventas por categoría
                                    amount = raw_input(f'\nError: hay un máximo de {sum(sales_by_category.values())} entradas. Ajuste su petición.\n')
                                    fails += 1
                                
                                # 3.3.3) Si no es 0 y sí se encuentra en el rango anterior
                                else:
                                    print('\n Productos menos vendidos:\n')
                                    for s in product_id_sales[:amount]: # Slicing hasta la cantidad especificada por el usuario
                                        print(f'El producto {s[1].split(",")[0]}, de ID {s[0]} y de categoría {s[2]}, vendió {s[3]} unidades')
                                    print('\n Productos más vendidos:\n')
                                    for s in product_id_sales[-amount:]: # slocing de los ultimos n elementos especificados por el usuario
                                        print(f'El producto {s[1].split(",")[0]}, de ID {s[0]} y de categoría {s[2]}, vendió {s[3]} unidades')

                            elif categ == '1':
                                print('\nResultados en categoría "Audífonos":\n')
                                for i in product_id_sales:
                                    if i[2] == 'audifonos':
                                        print(f'El producto {i[1].split(",")[0]}, de ID {i[0]}, vendió {i[3]} unidades')
                            elif categ == '2':
                                print('\nResultados en categoría "Bocinas":\n')
                                for i in product_id_sales:
                                    if i[2] == 'bocinas':
                                        print(f'El producto {i[1].split(",")[0]}, de ID {i[0]}, vendió {i[3]} unidades')
                            elif categ == '3':
                                print('\nResultados en categoría "Discos duros":\n')
                                for i in product_id_sales:
                                    if i[2] == 'discos duros':
                                        print(f'El producto {i[1].split(",")[0]}, de ID {i[0]}, vendió {i[3]} unidades')
                            elif categ == '4':
                                print('\nResultados en categoría "Memorias USB":\n')
                                for i in product_id_sales:
                                    if i[2] == 'memorias usb':
                                        print(f'El producto {i[1].split(",")[0]}, de ID {i[0]}, vendió {i[3]} unidades')
                            elif categ == '5':
                                print('\nResultados en categoría "Pantallas":\n')
                                for i in product_id_sales:
                                    if i[2] == 'pantallas':
                                        print(f'El producto {i[1].split(",")[0]}, de ID {i[0]}, vendió {i[3]} unidades')
                            elif categ == '6':
                                print('\nResultados en categoría "Procesadores":\n')
                                for i in product_id_sales:
                                    if i[2] == 'procesadores':
                                        print(f'El producto {i[1].split(",")[0]}, de ID {i[0]}, vendió {i[3]} unidades')
                            elif categ == '7':
                                print('\nResultados en categoría "Tarjetas de video":\n')
                                for i in product_id_sales:
                                    if i[2] == 'tarjetas de video':
                                        print(f'El producto {i[1].split(",")[0]}, de ID {i[0]}, vendió {i[3]} unidades')
                            elif categ == '8':
                                print('\nResultados en categoría "Tarjetas madre":\n')
                                for i in product_id_sales:
                                    if i[2] == 'tarjetas madre':
                                        print(f'El producto {i[1].split(",")[0]}, de ID {i[0]}, vendió {i[3]} unidades')
                        
                        # Error para entrada incorrecta en 3.2.1)
                        else:
                            print('Entrada inválida. Intente de nuevo con un número enlistado.')
                            fails += 1
                    else: # Caso para respuesta invalida en 3.1.1)
                        print('Entrada inválida. Intente de nuevo con un número enlistado.')
                        fails += 1
            elif query == '5': # consultar los productos con mayores o menores búsqueda
                """ Por categoría, generar un listado con los 5 productos con menores
                ventas y uno con los 10 productos con menores búsquedas
                """
                # 1) Conformar lista anidada [ID_prod, name, category, searches]

                # 1.1) Poblar lista nueva con las listas de [ID_prod, name, category]
                i = 0 # contador para iterar
                product_id_sales = []
            elif query == '6': # consultar los productos con mejores o peores reseñas
                """ CONSIGNA -> Mostrar dos listados de 5 productos c/una, un listado
                para los productos con las mejores reseñas y otro para las peores,
                considerando los productos con devolución (omitir productos sin reseñas)
                """
            # elif query == '7': # consultar detalles sobre ingresos y ventas

            else:
                print('Entrada inválida. Intente de nuevo')
                fails += 1
        
        # Programa para Python 3.x
        elif sys.version_info.major == 3:
            while True:
                try:
                    query = int(input("""\n¿Qué consulta desea realizar?\n 
                    Si desea revisar los datos tabulares de búsquedas de productos, ingrese '1'\n
                    Si desea revisar los datos tabulares de ventas de productos, ingrese '2'\n
                    Si desea revisar las especificaciones de los productos a la venta, ingrese '3'\n
                    Para consultar los productos con mayores o menores ventas ingrese '4' \n
                    Para consultar los productos con mayores o menores búsquedas ingrese '5'\n
                    Para consultar los productos con mejores o peores reseñas, ingrese '6'\n
                    Para consultar detalles sobre ingresos y ventas, ingrese '7'\n
                    Si desea cerrar este programa, ingrese '0'\n"""))

                    if query not in range(0,8):
                        print('Esa opción no es válida')

                    else:
                        break

                except:
                    print('Esa opción no es válida')

            if query == 0:
                break
            elif query == 1:
                details = input('\n¿Desea un listado detallado con nombre del producto y su ID? s/n\n')
                if details == 's':
                    for search in searches: # [id_search, id product] ... products -> [id_product, name, price, category, stock]
                        print(f'La búsqueda #{search[0]} corresponde al producto {"".join([product[1] for product in products if product[0] == search[1]])} de ID {search[1]}')
                elif details == 'n':
                    for search in searches:
                        print(*search)
                else:
                    print('Entrada inválida. Intente de nuevo')
                    fails += 1
                
                # Reajustar consulta
                # query = input("""\n¿Qué otra consulta desea realizar?\n 
                # Si desea revisar los datos tabulares de búsquedas de productos otra vez, ingrese '1'\n
                # Si desea revisar los datos tabulares de ventas de productos, ingrese '2'\n
                # Si desea revisar las especificaciones de los productos a la venta, ingrese '3'\n
                # Para consultar los productos con mayores o menores ventas ingrese '4' \n
                # Para consultar los productos con mayores o menores búsquedas ingrese '5'\n
                # Para consultar los productos con mejores o peores reseñas, ingrese '6'\n
                # Para consultar detalles sobre ingresos y ventas, ingrese '7'\n
                # Si desea cerrar este programa, ingrese '0'\n
                # """)
            elif query == 2:
                details = input('\n¿Desea un listado detallado con nombre del producto y su ID? s/n\n')
                if details == 's':
                    for sale in sales: # [id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)] ... products -> [id_product, name, price, category, stock]
                        print(f'La venta #{sale[0]} corresponde al producto {"".join([product[1] for product in products if product[0] == sale[1]])} de ID {sale[1]}')
                elif details == 'n':
                    for sale in sales:
                        print(*sale)
                else:
                    print('Entrada inválida. Intente de nuevo')
                    fails += 1
                
                # Reajustar consulta
                # query = input("""\n¿Qué otra consulta desea realizar?\n 
                # Si desea revisar los datos tabulares de búsquedas de productos, ingrese '1'\n
                # Si desea revisar los datos tabulares de ventas de productos otra vez, ingrese '2'\n
                # Si desea revisar las especificaciones de los productos a la venta, ingrese '3'\n
                # Para consultar los productos con mayores o menores ventas ingrese '4' \n
                # Para consultar los productos con mayores o menores búsquedas ingrese '5'\n
                # Para consultar los productos con mejores o peores reseñas, ingrese '6'\n
                # Para consultar detalles sobre ingresos y ventas, ingrese '7'\n
                # Si desea cerrar este programa, ingrese '0'\n
                # """)
            elif query == 3:
                details = input('\n¿Desea un listado detallado de los productos? s/n\n')
                if details == 's': # [id_product, name, price, category, stock]
                    for product in products:
                        print(f'El producto {product[1]}, de ID {product[0]}, en la categoría {product[3]}, tiene un precio de ${product[2]} y un total de {product[4]} unidad(es) en existencia')
                elif details == 'n':
                    for product in products:
                        print(*product)
                else:
                    print('Entrada inválida. Intente de nuevo')
                    fails += 1
                
                # # Reajustar consulta
                # query = input("""\n¿Qué otra consulta desea realizar?\n 
                # Si desea revisar los datos tabulares de búsquedas de productos, ingrese '1'\n
                # Si desea revisar los datos tabulares de ventas de productos, ingrese '2'\n
                # Si desea revisar las especificaciones de los productos a la venta otra vez, ingrese '3'\n
                # Para consultar los productos con mayores o menores ventas ingrese '4' \n
                # Para consultar los productos con mayores o menores búsquedas ingrese '5'\n
                # Para consultar los productos con mejores o peores reseñas, ingrese '6'\n
                # Para consultar detalles sobre ingresos y ventas, ingrese '7'\n
                # Si desea cerrar este programa, ingrese '0'\n
                # """)
            elif query == 4: # Para consultar los productos con mayores o menores ventas

                # 1) Conformar lista anidada [ID_prod, name, category, sales]

                # 1.1) Poblar lista nueva con las listas de [ID_prod, name, category]
                i = 0 # contador para iterar
                product_id_sales = [] # RESULTADO -> [id_product, name, category]
                for product in products:
                    product_id_sales.append(product) # Agrega toda la lista de cada producto de la base de datos
                    product_id_sales[i].pop(2) # Remueve ['price'] y actualiza los índices a la derecha del elemento removido
                    product_id_sales[i].pop(3) # Remueve ['stock'] >> Se volvió índice 3 por la actualización anterior
                    i += 1 # actualiza contador
                
                # 2) Obtener las ventas que tuvo cada producto por categorías (se necesitará más adelante)
                # sales_by_category = Counter(i[2] for i in product_id_sales) # donde i es cada entrada (lista) y 2 el índice ['category']
                products_with_sales = Counter(i[1] for i in sales) # donde i[1] es id_product

                # 1.2) Bucle para añadir la cantidad de ventas, 0 o la que le corresponda al producto
                for product in product_id_sales: # repasa cada entrada (lista) de la lista anteriormente poblada
                    if product[0] not in products_with_sales.keys(): # Si el id_product NO ESTÁ en el diccionario de conteo de ventas
                        product.append(0) # agrega entonces 0 ventas
                    else: 
                        for id_product in products_with_sales.keys(): # repasa todos los id_product del conteo de ventas
                            if id_product == product[0]: # si el id_product del conteo de ventas es igual al de la entrada (lista) en turno
                                product.append(dict(products_with_sales)[id_product]) # concatena el valor que le corresponde a la key 'id_product' en el diccionario
                
                # 1.3) Ordenar la lista completa de menores a mayores ventas
                sorted(product_id_sales, key=lambda x: x[3]) # donde X es cada entrada (lista) y 3 el índice ['sales']

                # 3) Recibir input del usuario sobre cómo quiere visualizar los resultados

                # Ciclo para permanecer en elección de categorias
                
                while True: # Ciclo para forzar a elegir un número entero que esté en el rango [0,9]
                    try:
                        # 3.1) Almacenar la categoría a consultar
                        categ = int(input("""\n¿Qué categoría desea consultar?\n 
                        Todas, ingrese '0' \n
                        Audífonos, ingrese '1'\n
                        Bocinas, ingrese '2'\n
                        Discos duros, ingrese '3'\n
                        Memorias USB, ingrese '4' \n
                        Pantallas, ingrese '5'\n
                        Procesadores, ingrese '6'\n
                        Tarjetas de video, ingrese '7'\n
                        Tarjetas madre, ingrese '8'\n
                        Para retroceder a otra opción, ingrese '9'\n
                        """))

                        if categ not in range(0,10):
                            print('Entrada inválida. Intente de nuevo con un número enlistado.')
                        else:
                            break
                    except:
                        print('Entrada inválida. Intente de nuevo con un número enlistado.')

                if categ == 9:
                    continue
                    
                while True:
                    try:
                        # 3.2) Con el punto 3.1.1) validado, procede a almacenar la cantidad de items a mostrar. 
                        amount = int(input("""A continuación se mostrarán los productos ordenados por ventas.\n 
                        Por favor, indique el número de items más vendidos y menos vendidos que desea ver.\n 
                        Para verlos todos ingrese '0'\n
                        """))
                        if amount not in range(0, sum(products_with_sales.values())):
                            print(f'\nError: hay un máximo de {sum(products_with_sales.values())} entradas. Ajuste su petición.\n')
                        else:
                            break
                    except:
                        print('Entrada inválida. Intente de nuevo con un número enlistado.')
                
                if categ == 0:
                    if amount == 0:
                        for i in product_id_sales:
                            print(f'El producto {i[1].split(",")[0]}, de ID {i[0]} y categoría {i[2]}, vendió {i[3]} unidades')

                    else: # Si 'amount' no es 0 y sí se encuentra en rango
                        print('Productos menos vendidos:\n')
                        for s in product_id_sales[:amount]: # Slicing hasta la cantidad especificada por el usuario
                            print(f'El producto {s[1].split(",")[0]}, de ID {s[0]} y de categoría {s[2]}, vendió {s[3]} unidades')
                        print('Productos más vendidos:\n')
                        for s in product_id_sales[-amount:]: # slocing de los ultimos n elementos especificados por el usuario
                            print(f'El producto {s[1].split(",")[0]}, de ID {s[0]} y de categoría {s[2]}, vendió {s[3]} unidades')

                elif categ == 1:
                    print('\nResultados en categoría "Audífonos":\n')
                    for i in product_id_sales:
                        if i[2] == 'audifonos':
                            print(f'Los audifonos {i[1].split(",")[0]}, de ID {i[0]}, vendió {i[3]} unidades')

                elif categ == 2:
                    print('\nResultados en categoría "Bocinas":\n')
                    for i in product_id_sales:
                        if i[2] == 'bocinas':
                            print(f'Las bocinas {i[1].split(",")[0]}, de ID {i[0]}, vendió {i[3]} unidades')

                elif categ == 3:
                    print('\nResultados en categoría "Discos duros":\n')
                    for i in product_id_sales:
                        if i[2] == 'discos duros':
                            print(f'El DD {i[1].split(",")[0]}, de ID {i[0]}, vendió {i[3]} unidades')

                elif categ == 4:
                    print('\nResultados en categoría "Memorias USB":\n')
                    for i in product_id_sales:
                        if i[2] == 'memorias usb':
                            print(f'La USB {i[1].split(",")[0]}, de ID {i[0]}, vendió {i[3]} unidades')

                elif categ == 5:
                    print('\nResultados en categoría "Pantallas":\n')
                    for i in product_id_sales:
                        if i[2] == 'pantallas':
                            print(f'La pantalla {i[1].split(",")[0]}, de ID {i[0]}, vendió {i[3]} unidades')

                elif categ == 6:
                    print('\nResultados en categoría "Procesadores":\n')
                    for i in product_id_sales:
                        if i[2] == 'procesadores':
                            print(f'El procesador {i[1].split(",")[0]}, de ID {i[0]}, vendió {i[3]} unidades')

                elif categ == 7:
                    print('\nResultados en categoría "Tarjetas de video":\n')
                    for i in product_id_sales:
                        if i[2] == 'tarjetas de video':
                            print(f'La tarjeta de video {i[1].split(",")[0]}, de ID {i[0]}, vendió {i[3]} unidades')

                elif categ == 8:
                    print('\nResultados en categoría "Tarjetas madre":\n')
                    for i in product_id_sales:
                        if i[2] == 'tarjetas madre':
                            print(f'La tarjeta madre {i[1].split(",")[0]}, de ID {i[0]}, vendió {i[3]} unidades')
                
            elif query == 5: # consultar los productos con mayores o menores búsquedas
                # Recibir input del usuario sobre cómo quiere visualizar las BÚSQUEDAS

                while True: # Escoger categoría: ciclo para forzar a elegir un número entero que esté en el rango [0,9]
                    try:
                        categ = int(input("""\n¿Qué categoría desea consultar?\n 
                        Todas, ingrese '0' \n
                        Audífonos, ingrese '1'\n
                        Bocinas, ingrese '2'\n
                        Discos duros, ingrese '3'\n
                        Memorias USB, ingrese '4' \n
                        Pantallas, ingrese '5'\n
                        Procesadores, ingrese '6'\n
                        Tarjetas de video, ingrese '7'\n
                        Tarjetas madre, ingrese '8'\n
                        Para retroceder a otra opción, ingrese '9'\n"""))

                        if categ not in range(0,10):
                            print('Entrada inválida. Intente de nuevo con un número enlistado.')
                        else:
                            break
                    except:
                        print('Entrada inválida. Intente de nuevo con un número enlistado.')
                
                if categ == 9:
                    continue

                # 1) Conformar lista anidada [ID_prod, name, category, searches]

                # 1.1) Poblar lista nueva con las listas de [ID_prod, name, category]
                i = 0 # contador para iterar
                product_id_categ = []
                for product in products:
                    product_id_categ.append(product) # Agrega toda la lista de cada producto de la base de datos
                    product_id_categ[i].pop(2) # Remueve ['price'] y actualiza los índices a la derecha del elemento removido
                    product_id_categ[i].pop(3) # Remueve ['stock'] >> Se volvió índice 3 por la actualización anterior
                    i += 1 # actualiza contador
                
                # 2) Obtener las BUSQUEDAS que tuvo cada producto por categoría (se necesitará más adelante)
                products_with_searches = Counter(i[1] for i in searches) # donde i[1] es id_product

                # 1.2) Bucle para añadir la cantidad de BÚSQUEDAS, 0 o la que le corresponda al producto
                for product in product_id_categ: # repasa cada entrada (lista) de la lista anteriormente poblada
                    if product[0] not in products_with_searches.keys(): # Si el id_product NO ESTÁ en el diccionario de conteo de BUSQUEDAS
                        product.append(0) # agrega entonces 0 BUSQUEDAS

                    else: 
                        for id_product in products_with_searches.keys(): # repasa todos los id_product del conteo de ventas
                            if id_product == product[0]: # si el id_product del conteo de BÚSQUEDAS es igual al de la entrada (lista) en turno
                                product.append(dict(products_with_searches)[id_product]) # concatena el valor que le corresponde a la key 'id_product' en el diccionario
                
                # 1.3) Ordenar la lista completa de menores a mayores BUSQUEDAS
                sorted(product_id_categ, key=lambda x: x[3]) # donde X es cada entrada (lista) y 3 el índice ['sales']
                    
                while True: # Escoger cantidad
                    try:
                        # 3.2) Con el punto 3.1.1) validado, procede a almacenar la cantidad de items a mostrar. 
                        amount = int(input("""A continuación se mostrarán los productos ordenados por ventas.\n 
                        Por favor, indique el número de items más vendidos y menos vendidos que desea ver.\n 
                        Para verlos todos ingrese '0'\n"""))

                        if amount not in range(0, sum(products_with_searches.values())):
                            print(f'\nError: hay un máximo de {sum(products_with_searches.values())} entradas. Ajuste su petición.\n')
                        else:
                            break
                    except:
                        print('Entrada inválida. Intente de nuevo con un número enlistado.')
                
                if categ == 0:
                    if amount == 0:
                        for i in product_id_categ:
                            print(f'El producto {i[1].split(",")[0]}, de ID {i[0]} y categoría {i[2]}, se buscó {i[3]} veces')

                    else: # Si 'amount' no es 0 y sí se encuentra en rango
                        print('Productos menos buscados:\n')
                        for s in product_id_categ[:amount]: # Slicing hasta la cantidad especificada por el usuario
                            print(f'El producto {s[1].split(",")[0]}, de ID {s[0]} y de categoría {s[2]}, se buscó {s[3]} veces')
                        print('Productos más buscados:\n')
                        for s in product_id_categ[-amount:]: # slocing de los ultimos n elementos especificados por el usuario
                            print(f'El producto {s[1].split(",")[0]}, de ID {s[0]} y de categoría {s[2]}, se buscó {s[3]} veces')

                elif categ == 1:
                    print('\nResultados en categoría "Audífonos":\n')
                    for i in product_id_categ:
                        if i[2] == 'audifonos':
                            print(f'Los audifonos {i[1].split(",")[0]}, de ID {i[0]}, se buscó {i[3]} veces')

                elif categ == 2:
                    print('\nResultados en categoría "Bocinas":\n')
                    for i in product_id_categ:
                        if i[2] == 'bocinas':
                            print(f'Las bocinas {i[1].split(",")[0]}, de ID {i[0]}, se buscó {i[3]} veces')

                elif categ == 3:
                    print('\nResultados en categoría "Discos duros":\n')
                    for i in product_id_categ:
                        if i[2] == 'discos duros':
                            print(f'El DD {i[1].split(",")[0]}, de ID {i[0]}, se buscó {i[3]} veces')

                elif categ == 4:
                    print('\nResultados en categoría "Memorias USB":\n')
                    for i in product_id_categ:
                        if i[2] == 'memorias usb':
                            print(f'La USB {i[1].split(",")[0]}, de ID {i[0]}, se buscó {i[3]} veces')

                elif categ == 5:
                    print('\nResultados en categoría "Pantallas":\n')
                    for i in product_id_categ:
                        if i[2] == 'pantallas':
                            print(f'La pantalla {i[1].split(",")[0]}, de ID {i[0]}, se buscó {i[3]} veces')

                elif categ == 6:
                    print('\nResultados en categoría "Procesadores":\n')
                    for i in product_id_categ:
                        if i[2] == 'procesadores':
                            print(f'El procesador {i[1].split(",")[0]}, de ID {i[0]}, se buscó {i[3]} veces')

                elif categ == 7:
                    print('\nResultados en categoría "Tarjetas de video":\n')
                    for i in product_id_categ:
                        if i[2] == 'tarjetas de video':
                            print(f'La tarjeta de video {i[1].split(",")[0]}, de ID {i[0]}, se buscó {i[3]} veces')

                elif categ == 8:
                    print('\nResultados en categoría "Tarjetas madre":\n')
                    for i in product_id_categ:
                        if i[2] == 'tarjetas madre':
                            print(f'La tarjeta madre {i[1].split(",")[0]}, de ID {i[0]}, se buscó {i[3]} veces')
            
            elif query == 6: # consultar los productos con mejores o peores reseñas
                # Recibir input del usuario sobre cómo quiere visualizar las RESEÑAS

                while True: # Escoger categoría: ciclo para forzar a elegir un número entero que esté en el rango [0,9]
                    try:
                        # 3.1) Almacenar la categoría a consultar
                        categ = int(input("""\n¿Qué categoría desea consultar?\n 
                        Todas, ingrese '0' \n
                        Audífonos, ingrese '1'\n
                        Bocinas, ingrese '2'\n
                        Discos duros, ingrese '3'\n
                        Memorias USB, ingrese '4' \n
                        Pantallas, ingrese '5'\n
                        Procesadores, ingrese '6'\n
                        Tarjetas de video, ingrese '7'\n
                        Tarjetas madre, ingrese '8'\n
                        Para retroceder a otra opción, ingrese '9'\n"""))

                        if categ not in range(0,10):
                            print('Entrada inválida. Intente de nuevo con un número enlistado.')
                        else:
                            break
                    except:
                        print('Entrada inválida. Intente de nuevo con un número enlistado.')
                    
                if categ == 9:
                    continue
                

                # 1) Conformar lista anidada [ID_prod, name, category, score]
                # sales -> [id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)]
                # Borrar -> id_sale, date, refund

                # 1.1) Poblar lista nueva con las listas de [ID_prod, name, category]
                i = 0 # contador para iterar
                product_id_categ = []
                for sale in sales:
                    product_id_categ.append(sale) # Agrega toda la lista de cada producto de la base de datos
                    product_id_categ[i].pop(0) # Remueve ['id_sale'] y actualiza los índices a la derecha del elemento removido
                    product_id_categ[i].pop(2) # Remueve ['date'] y actualiza los índices a la derecha del elemento removido
                    product_id_categ[i].pop(3) # Remueve ['refund'] >> Se volvió índice 3 por la actualización anterior
                    i += 1 # actualiza contador
                
                # 1.3) Ordenar la lista completa de menores a mayores BUSQUEDAS
                sorted(product_id_categ, key=lambda x: x[3]) # donde X es cada entrada (lista) y 2 el índice ['score']
                    
                while True: # Escoger cantidad
                    try:
                        amount = int(input("""A continuación se mostrarán los productos ordenados por ventas.\n 
                        Por favor, indique el número de items más vendidos y menos vendidos que desea ver.\n 
                        Para verlos todos ingrese '0'\n"""))

                        if amount not in range(0, len(product_id_categ)+1):
                            print(f'\nError: hay un máximo de {len(product_id_categ)} entradas. Ajuste su petición.\n')
                        else:
                            break
                    except:
                        print('Entrada inválida. Intente de nuevo con un número enlistado.')

                # 1) product_id_categ -> [ID_prod, name, category, score]
                
                if categ == 0:
                    if amount == 0:
                        for i in product_id_categ:
                            print(f'El producto {i[1].split(",")[0]}, de ID {i[0]} y categoría {i[2]}, recibió una calificación de {i[3]}')

                    else: # Si 'amount' no es 0 y sí se encuentra en rango
                        print('Productos peor reseñado:\n')
                        for s in product_id_categ[:amount]: # Slicing hasta la cantidad especificada por el usuario
                            print(f'El producto {s[1].split(",")[0]}, de ID {s[0]} y de categoría {s[2]}, recibió una calificación de {s[3]}')
                        print('Productos mejor reseñado:\n')
                        for s in product_id_categ[-amount:]: # slocing de los ultimos n elementos especificados por el usuario
                            print(f'El producto {s[1].split(",")[0]}, de ID {s[0]} y de categoría {s[2]}, recibió una calificación de {s[3]}')

                elif categ == 1:
                    print('\nResultados en categoría "Audífonos":\n')
                    for i in product_id_categ:
                        if i[2] == 'audifonos':
                            print(f'Los audifonos {i[1].split(",")[0]}, de ID {i[0]}, recibieron una calificación de {i[3]}')

                elif categ == 2:
                    print('\nResultados en categoría "Bocinas":\n')
                    for i in product_id_categ:
                        if i[2] == 'bocinas':
                            print(f'Las bocinas {i[1].split(",")[0]}, de ID {i[0]}, recibieron una calificación de {i[3]}')

                elif categ == 3:
                    print('\nResultados en categoría "Discos duros":\n')
                    for i in product_id_categ:
                        if i[2] == 'discos duros':
                            print(f'El DD {i[1].split(",")[0]}, de ID {i[0]}, recibió una calificación de {i[3]}')

                elif categ == 4:
                    print('\nResultados en categoría "Memorias USB":\n')
                    for i in product_id_categ:
                        if i[2] == 'memorias usb':
                            print(f'La USB {i[1].split(",")[0]}, de ID {i[0]}, recibió una calificación de {i[3]}')

                elif categ == 5:
                    print('\nResultados en categoría "Pantallas":\n')
                    for i in product_id_categ:
                        if i[2] == 'pantallas':
                            print(f'La pantalla {i[1].split(",")[0]}, de ID {i[0]}, recibió una calificación de {i[3]}')

                elif categ == 6:
                    print('\nResultados en categoría "Procesadores":\n')
                    for i in product_id_categ:
                        if i[2] == 'procesadores':
                            print(f'El procesador {i[1].split(",")[0]}, de ID {i[0]}, recibió una calificación de {i[3]}')

                elif categ == 7:
                    print('\nResultados en categoría "Tarjetas de video":\n')
                    for i in product_id_categ:
                        if i[2] == 'tarjetas de video':
                            print(f'La tarjeta de video {i[1].split(",")[0]}, de ID {i[0]}, recibió una calificación de {i[3]}')

                elif categ == 8:
                    print('\nResultados en categoría "Tarjetas madre":\n')
                    for i in product_id_categ:
                        if i[2] == 'tarjetas madre':
                            print(f'La tarjeta madre {i[1].split(",")[0]}, de ID {i[0]}, recibió una calificación de {i[3]}')
            
            elif query == 7: # consultar detalles sobre ingresos y ventas
                print('Terminame')
            else:
                print('Entrada inválida. Intente de nuevo')
                fails += 1
    except:
        sys.exit('\nFin del programa -- 2021 Ian Miguel Figueroa Schulte -- Hasta pronto.')

# Interrumpe el programa cuando los fallos acumulados alcancen o rebasen 3
if fails >= 3: 
    sys.exit('\nHa excedido el número de intentos. Vuelva a ejecutar este programa.')

sys.exit('\nFin del programa -- 2021 Ian Miguel Figueroa Schulte -- Hasta pronto.')

# Cuenta las veces que cada elemento único de la columna # aparece en la lista, para cada sublista x
# idprod_sales -> diccionario {id_prod : sales}
idprod_sales = Counter(x[1] for x in sales)
# RESULTADO = Más vendido, con 50 ventas, 54 -> "SSD Kingston A400, 120GB, SATA III, 2.5'', 7mm"
# RESULTADO = Menos vendidos, con 1 venta, [10, 13, 17, 22, 28, 40, 45, 46, 50, 60, 66, 67, 84, 89, 94]

# sublista de ventas = idprod_and_name -> [id_product, name]
idprod_and_name = [x[:2] for x in products]
# sublista de ventas = idprod_name_sales -> [id_product, name, sales]
idprod_name_sales = [] # lista vacia
counter1 = 0 # contador para iterar
for i in idprod_and_name: # para cada producto [ID, name] en la lista
    for key in idprod_sales.keys(): # para cada ID de producto contenido en la lista
        if i[0] == key: # si la id_product es igual al ID de producto
            idprod_name_sales.append(i) # agrega el producto
            idprod_name_sales[counter1].append(idprod_sales[key]) # agrega en el producto de índice counter1-ésimo el valor (cantidad de ventas) de la key (producto) del diccionario
            counter1 += 1

# ordenar lista anterior de menos a más ventas
sortd_id_name_sale = sorted(idprod_name_sales,key=lambda x: x[2])

# imprime cada sublista por renglon, sin corchetes ni comas
for s in idprod_name_sales:
    print(*s)

print('-------------------')

for s in sortd_id_name_sale:
    print(*s)

print('-------------------')

### Productos más buscados
## RESULTADOS 
## Más buscado, con 263 registros, 54 -> SSD Kingston A400, 120GB, SATA III, 2.5'', 7mm
## Menos buscados, con 1 registro, [10, 45]
# Lista con ID_prod y conteo -> diccionario
idprod_searched = Counter(x[1] for x in searches)
print(idprod_searched)

print('-------------------')

# lista que incluya nombre
idprod_name_searched = [] # lista vacia
counter2 = 0 # contador para iterar
for i in idprod_name_sales: # para cada producto [ID, name] en la lista
    for key in idprod_searched.keys(): # para cada ID de producto contenido en la lista
        if i[0] == key: # si la id_product es igual al ID de producto
            idprod_name_searched.append(i[:2]) # agrega el producto sin las ventas
            idprod_name_searched[counter2].append(idprod_searched[key]) # agrega en el producto de índice counter2-ésimo el valor (cantidad de busquedas) de la key (producto) del diccionario
            counter2 += 1

for s in idprod_name_searched:
    print(*s)

print('-------------------')

# lista ordenada de menor a mayor en busquedas
sortd_searches = sorted(idprod_name_searched,key=lambda x: x[2])

for s in sortd_searches:
    print(*s)

print('-------------------')

### Reseñas
## RESULTADOS
##
# Lista de mejores reseñados [rate -> x[2] = 5], sin devolver [refund -> x[4] = 0]
best_rated = []
#items_in_list = 0

for i in sales:
        if len(best_rated) == 5:
            break
        elif i[2] == 5:
            if i[4] == 0:
                best_rated.append(i)
                #items_in_list += 1
                #items_in_list += 1
                #counter3 += 1

print("LISTA DE MEJORES CALIFICADOS \n")
print(best_rated)

# Lista de peores reseñados [rate -> x[2] = 1], considera devoluciones [refund -> x[4] = 1]
worst_rated = []

for i in sales:
        if len(worst_rated) == 5:
            break
        elif i[2] == 1:
            if i[4] == 0:
                worst_rated.append(i)
            else:
                if i[4] == 1:
                    worst_rated.append(i)

print('-------------------')

print("LISTA DE PEORES CALIFICADOS \n")
print(worst_rated)

# UNUSED----------------------------
#print(product_and_name)

#sum(x.count)

#print(lifestore_sales.co)

#for sale in lifestore_sales:
#    for val in sale:

#def contar(lst, obj):
#
#   if lst == []:
#        return 0
#    if lst[1] == obj:
#        return 1 + count[lst[1:], obj]
#    elif type(lst[0]) == list:
#        return count(lst[0], obj) + count(lst[1:], obj)
#    else:
#        return 0 + count(lis[1:], obj)

# # def contar_ventas(lst, prod):

#     cont = 0
#     for i in lst:
#         for j in i:
#             if i[1] == prod:
#                 cont += 1
    
#     return cont

# print("Conteo = ", contar_ventas(lifestore_sales,))
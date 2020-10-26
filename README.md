# Entrega: Implementación de algoritmo básico
Este repositorio contiene la implementación de los diferentes algoritmos junto con los extras realizados. Asimismo, este fichero explica el trabajo realizado, la estructura del repositorio y las instrucciones para su ejecución.

Autor: **Pedro Arias Pérez**

Link: [pariaspe/graph-searching](https://github.com/pariaspe/graph-searching)


## Índice
- [1. Descripción](#1-descripción)
- [2. Estructura de Carpetas](#2-estructura-de-carpetas)
- [3. Base](#3-base)
- [4. Extras](#4-extras)
    - [4.1. Extra 1](#extra-1-visualización-y-resumen)
    - [4.2. Extra 2](#extra-2-algoritmo-interactivo)
    - [4.3. Extra 3](#extra-3-dijkstra-y-a*)
    - [4.4. Extra 4](#extra-4-comparación-entre-algoritmos-uniformes)
    - [4.5. Extra 5](#extra-5-comparación-entre-todos-los-algoritmos)
    - [4.6. Extra 6](#extra-6-mapa-laberinto)

---

## 1. Descripción
Para la práctica se han realizado los siguientes hitos:

- **Base**:
    1. BFS.
    2. Algoritmo greedy (DFS).


- **Extra**:
    1. Mejora de visualización y resumen de ejecución.
    2. Algoritmo interactivo.
    3. Dijkstra y A*.
    4. Comparación de algoritmos uniformes.
    5. Comparación entre todos los algoritmos.
    6. Mapa laberinto.


## 2. Estructura de carpetas
El esquema de organización del reposition es el siguiente:
```
.
+-- doc (img...)
+-- base
    +-- bfs
        +-- main.py
    +-- dfs
        +-- main.py
+-- extra
    +-- bfs
        +-- bfs.py
    +-- dfs
        +-- dfs.py
    +-- dijkstra
        +-- dijkstra.py
    +-- astar
        +-- astar.py
    +-- utils.py
    +-- compare.py
    +-- comparison.txt
    +-- comparison2.txt
+-- maps
    +-- lab1
        +-- lab1.csv
        +-- lab1.jpg
        +-- README.md
    +-- map1 (csv...)
         :
         :
    +-- map11 (csv..)
+-- README.md
```

## 3. Base
El algoritmo greedy que he hecho es un DFS. Destacar sobre ambos algoritmos las siguientes consideraciones:

Sobre **BFS**:
- He modificado levemente el código para que no haya que cambiar la ruta del mapa al cambiar el equipo.

Sobre **DFS**:
- He modificado mínimamente el código reorganizando el código en clases (creando la clase "mapa" `CharMap`) y en métodos ejecutados según una secuencia de control establecida en `main()`.
- El algoritmo es a derechas y utiliza una FIFO para almacenar los nodos e ir recorriendo el mapa.

## 4. Extras
### Extra 1: Visualización y Resumen
Se le ha dado formato al texto que se imprime por la terminal. De esa forma, haciendo uso de caracteres ANSI se puede mejorar la visualizaciṕn sin necesidad de una usar una librería externa.
Para ello se ha reestructurado el código en distintas clases, creando varias nuevas, que se encuentran en el fichero utils.py. Los distintos algoritmos utilizan métodos y clases de este fichero.

Código de colores:
- 0: libre -> blanco
- 1: obstáculo -> negro
- 2: visitado -> azul
- 3: start -> verde
- 4: goal -> rojo
- actual -> azul con X intermitente
- nueva -> cian

Además, tras la ejecuciónse muestra un pequeño resumen que recoge parámetros importantes del algoritmo, como la longitud de la ruta encontrada, el número de celdas accedidas o el tiempo de ejecución.

```
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%           RESULTS            %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Route 	 Cells 	
Length	Checked	  Time
--------------------------------
  72	    398	   0.05704
```


Ficheros necesarios: `extra/utils.py` + `extra/[alg]/[alg].py` (ej: bfs.py, dfs.py)

Ejemplo de ejecución:
```
$ cd extra/bfs
$ python3 bfs.py
```

![extra-1](doc/extra-1.png)

### Extra 2: Algoritmo interactivo
Todos los algoritmos admiten argumentos a la hora de ejecutarlos mediante la línea de comandos. Estos argumentos permiten modificar el funcionamiento base de los algoritmos.
Estas opciones se pueden visualizar con el argumento `-h`.

```
$ cd extra/dfs
$ python3 dfs.py -h
usage: dfs.py [-h] [-m MAP] [-s N N] [-e N N] [-i] [-k] [-o OUTPUT]

Depth First Search Algorithm.

optional arguments:
  -h, --help           show this help message and exit
  -m MAP, --map MAP    change map folder
  -s N N, --start N N  change start point
  -e N N, --end N N    change end point
  -i                   interactive mode (choose map, start, end...)
  -k                   set counter clockwise (left-handed)
  -o OUTPUT            output mode (choose from none, base, colored)
```

**Opciones**

| argument | option | example |
| --- | ------- | ------- |
| -h, --help | display help message and exit | `python3 dfs.py -h` |
| -m MAP, --map MAP | use map MAP | `python3 dfs.py -m map5` |
| -s X Y, --start X Y | use [X][Y] as start point | `python3 dfs.py -s 2 2` |
| -e X Y, --end X Y | use [X][Y] as end point | `python3 dfs.py -e 10 7` |
| -i | enter interactive mode | `python3 dfs.py -i` |
| -k | set counter-clockwise | `python3 dfs.py -k` |
| -o [none, base, colored] | use OUTPUT mode | `python3 dfs.py -o base` |


**OJO**: La opción `-k` solo está disponible para el algoritmo DFS.

![modo-interactivo](doc/extra-2.png)

### Extra 3: Dijkstra y A*
También se han implementado dos algoritmos con información de costes. Para ello, ha sido necesario extender alguna clase del fichero `utils.py` para añadirles información de costes a los nodos. Las principales diferencias son:
- Nueva clase nodo `NodeCost` que extiende la clase `Node` añadiendo información sobre el coste.
- Nueva clase mapa `CharMapCost` que utiliza los nodos con coste (`NodeCost`) y tiene dos listas, una de nodos visitados y otra de nodos por visitar.
- Nuevo método para calcular el coste con la distancia euclídea (norma dos).

Por lo demás, el algoritmo es similar al BFS, utilizando como nodo central en cada iteración del bucle el nodo con menor coste de la lista de nodos por visitar. Una vez visitado, este nodo se añade a la lista de visitados y se elimina de la lista de nodos por visitar. La ruta final se calcula sobre la lista de nodos visitados.

La diferencia entre Dijkstra y A* es en el cálculo del coste.
- Dijkstra: `cost = dist(current, start)`
- A*: `cost = dist(current, start) + dist(current, goal)`

### Extra 4: Comparación entre algoritmos uniformes
Para comparar los algoritmos se ha creado un fichero (`compare.py`) que ejecuta los algoritmos sobre los distintos mapas y muestra los parámetros más relevantes como el número de accesos a casillas del mapa, el tamaño de la ruta encontrada por el algoritmo o el tiempo de ejecución.
Para ejecutar esta comparación entre algoritmos uniformes, es tan sencillo como lanzar el fichero `compare.py` con la opción `-u`:
```
$ cd extra
$ python3 compare.py -u
```

La salida de esta ejecución se volcado al archivo de texto `comparison.txt` donde se puede comprobar los resultados obtenidos. La comparación aquí expuesta se ha realizado sobre todos los mapas que se han facilitado con el material para la práctica. La intención es tener un espectro de pruebas amplio que permita obtener unos resultados generales, y que no dependan de la configuración específica de un mapa en particular.

```
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%           TOTAL              %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    	Route    Cells 	
Alg.	Length  Checked    Time
--------------------------------
BFS	 410	  13492	1.72058
DFSR	1176	 10641	1.43472
DFSL	1242	  4933	0.86646

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%          RANKINGS            %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

                LESS
     SHORTEST  CHECKS  FASTEST
--------------------------------
map1	BFS	 DFSr	BFS
map2	BFS	 DFSl	DFSl
map3	BFS	 DFSl	DFSl
map4	BFS	 DFSl	DFSl
map5	BFS	 DFSr	DFSr
map6	BFS	 DFSl	DFSl
map7	BFS	 DFSl	DFSl
map8	BFS	 DFSl	DFSr
map9	BFS	 DFSl	DFSl
map10   BFS	 DFSl	DFSl
map11   BFS	 DFSr	DFSr
--------------------------------

	SHORTEST ROUTE
--------------------------------
1º: BFS (11)

	LESS CELLS CHECKED
--------------------------------
1º: DFSl (8)
2º: DFSr (3)

	FASTEST ALGORITHM
--------------------------------
1º: DFSl (7)
2º: DFSr (3)
3º: BFS (1)
```

Sobre estas estadísticas se quiere hacer una reflexión sobre las fortalezas y debilidades de los algoritmos analizados. La comparación es principalmente sobre BFS frente a DFS, aunque también hacemos una distinción entre DFS a derechas (DFSr) o a izquierdas (DFSl).

En primer lugar, y como era obvio esperar, el camino más corto se obtiene siempre con el algoritmo BFS. Un algoritmo exhaustivo va a encontrar siempre que exista el camino óptimo (más corto). Por tanto, un algoritmo greedy podrá como mucho empatar y encontrar el mismo camino. Sin embargo, como podemos observar esto no ocurre en ninguna ocasión. Además, en los datos estadísticos totales mostrados, se puede observar como la ruta total acumulada encontrada es de 410 en BFS frente a los ~1.200 en DFS, prácticamente el triple.

Encontrar el camino óptimo supone acceder a un mayor número de celdas que un algoritmo greedy. Esto también coincide con lo esperado, pues un algoritmo en anchura (como también se conoce a los algoritmos exhaustivos) recorre más casillas del mapa que uno en profundidad. Esto se puede observar en los datos estadísticos totales, donde BFS duplica a DFS en número de casillas accedidas (+13k frente a ~7.5k).

Con respecto al tiempo de ejecución, se observa que los algoritmos en profundidad suelen ser más rápidos que los algoritmos en anchura. Solo en uno de los once mapas el algoritmo más rápido es un BFS. Esto se puede deber a que el mapa en cuestion (`map1`) es un mapa muy pequeño, por lo que las diferencias entre algoritmos no son grandes. Esto coincide con que, como se acaba de mencionar, los algoritmos en anchura acceden a un número muy superior de casillas que repercute en el tiempo de ejecución. Observando los tiempos de ejecución en los mapas de muestra podemos ver como el algoritmo BFS casi dobla en tiempo a los algoritmos DFS (1.72s frente a ~1.1s).

Por último, es interesante mencionar que en los mapas seleccionados para esta comparación se observa una cierta tendencia de izquierdas, pues los resultados obtenidos con el algoritmo DFS a izquierzas (DFSl) son ligeramente mejores a los obtenidos con un DFS a derechas (DFSr).

Como conclusión, si se dispone del suficiente tiempo para planificar el movimiento sería más interesante utilizar un algoritmo como BFS, pues eso supondría que el robot realizase la ruta más corta lo que influye en aspectos tan importantes como la autonomía energética del robot.
Sin embargo, si se dispone de un tiempo de planificación límitado, sería más interesante utilizar un algoritmo como DFS, pues lo tiempos podrían llegar a reducirse a la mitad, como se ha observado en esta pequeña prueba experimental.

### Extra 5: Comparación entre todos los algoritmos
Esta segunda comparación se realiza entre todos los algoritmos implementados: BFS, DFS (a izquierdas y a derechas), Dijkstra y A*. La comparación ejecuta los once mapas disponibles. Para ejecutarla solo es necesario lanzar el fichero `compare.py`:

```
$ cd extra
$ python3 compare.py
```

La salida de esta ejecución se volcado al archivo de texto `comparison2.txt` donde se puede comprobar los resultados obtenidos. Parte de este fichero se copia a continuación.

```
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%           TOTAL              %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    	Route 	 Cells 	
Alg.	Length	Checked	  Time
--------------------------------
BFS	  410	13492	1.66053
DFSR	1176	10641	1.46119
DFSL	1242	 4933	0.88823
DIJK	 462	 8104	0.81826
ASTAR	444	 6294	0.67656

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%          RANKINGS            %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

                LESS
     SHORTEST  CHECKS  FASTEST
--------------------------------
map1	BFS, DIJK, ASTAR	DFSr	ASTAR
map2	BFS, DIJK, ASTAR	ASTAR	ASTAR
map3	BFS	DFSl	DFSl
map4	BFS	DFSl	DFSl
map5	BFS	DFSr	DFSr
map6	BFS, ASTAR	ASTAR	ASTAR
map7	BFS	DFSl	ASTAR
map8	BFS, DIJK	DFSl	ASTAR
map9	BFS, ASTAR	DFSl	ASTAR
map10	BFS, ASTAR	DFSl	DFSl
map11	BFS, DIJK, ASTAR	ASTAR	ASTAR
--------------------------------

	SHORTEST ROUTE
--------------------------------
1º: BFS (4)
2º: BFS, DIJK, ASTAR (3)
3º: BFS, ASTAR (3)

	LESS CELLS CHECKED
--------------------------------
1º: DFSl (6)
2º: ASTAR (3)
3º: DFSr (2)

	FASTEST ALGORITHM
--------------------------------
1º: ASTAR (7)
2º: DFSl (3)
3º: DFSr (1)
```

Como se puede observar en los resultados globales, el algoritmo que mejor resultados obtiene es A*. Este algoritmo ha sido siete veces el más rápido y en seis ocasiones a encontrado la ruta más corta.

Por otro lado, viendo los resultados acumulados en los once mapas, es el segundo con la ruta más corta (444) después de BFS, que como ya se ha comentado encuentra siempre la ruta más corta si existe. En cuanto al número de accesos y de tiempo de ejecución es el mejor, seguido por DFS en número de accesos (~6300 frente a ~6500) y seguido por Dijkstra en tiempo de ejecución (0.676s frente a 0.818s).

Dijkstra también obtiene bueno resultados, aunque no tan buenos como A*. Entre las diferencias entre ambos, destacar que Dijkstra (al igual que los algoritmos sin costes) no utiliza la posición de la meta por lo que se podría ejecutar en un caso en el que esta fuera desconocida.

### Extra 6: Mapa Laberinto
Los mapas existentes son todos bastante abiertos, así que por comprobar como se comportan los algoritmos en un mapa más enrevesado he creado un laberinto.
Los ficheros de este nuevo mapa se encuentran en el directorio `lab1`.

- Punto de inicio: 2, 2
- Punto de final: 15, 15

![lab1](maps/lab1/lab1.jpg)

Comparando los algoritmos, se obtienen los siguientes resultados:
```
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%		lab1		          %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    	Route 	 Cells 	
Alg.	Length	Checked	  Time
--------------------------------
BFS	  60	563	0.03255
DFSr	 72	398	0.03306
DFSl	 74	375	0.03218
DIJK	 62	563	0.03328
ASTAR	64	447	0.02620

Shortest -------> BFS (60)
Less checks ----> DFSl (375)
Fastest --------> ASTAR (0.0262)

```

Los resultados obtenidos son similares a los expuestos en los apartados anteriores. El camino más corto es el encontrado por el BFS (60), seguido por Dijkstra (62) y por A* (64). Los algoritmos que encuentran la ruta más corta son también los más lentos (BFS con 0.032 y Dijkstra 0.033), aunque obtienen resultados similares al resto.

El mejor resultado es el obtenido por A*, siendo visiblemente más rápido que el resto de algoritmos (0.026).

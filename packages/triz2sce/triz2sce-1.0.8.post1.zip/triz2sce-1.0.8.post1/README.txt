Triz2sce
********

English instructions below.

Triz2sce versión 1.0.8 190323 (c) 2018 Pedro Fernández

Triz2sce.py es un script de Python 3.x que transforma un fichero generado con la utilidad para mapear aventuras Trizbort en un código fuente compatible con el compilador del DAAD.
No es un diseñador visual de aventuras ni una aplicación para su desarrollo completo. Está concebido como herramienta para hacer prototipos iniciales de aventuras con rapidez y facilidad y, a su vez, como herramienta de apoyo a autores nóveles, ideal para su uso en talleres de aprendizaje.

Uso:
====

Usar "Python triz2sce.py -h" en una linea de comandos o powershell para ver las opciones.

El script requiere como argumentos un fichero de entrada (que debe ser un mapa generado por la utilidad Trizbort en formato XML, con soporte para la versión 1.7.0) y, opcionalmente, el nombre de un fichero de salida, que será un código fuente en formato .SCE compatible con la versión 2.40-2.42 del compilador del DAAD. Si no se especifica se creará un fichero con el mismo nombre y la extensión .SCE

La opción -p1 generará un listado SCE con los mensajes del sistema en primera persona. Por defecto éstos se crearán en segunda persona.
La opción -e generará un listado SCE con los textos y el vocabulario en inglés. Por defecto se crearán en español.

- Trizbort:

 - http://www.trizbort.com/

- DAAD

 - http://wiki.caad.es/DAAD
 - http://www.caad.es/fichas/daad.html
 - http://www.rockersuke.com/if/ebbp/
 - http://8-bit.info/infinite-imaginations-aventuras-ad/


Hasta el momento parece convertir correctamente:

- Habitaciones, incluyendo sus descripciones y estableciendo la localidad de comienzo.
- Conexiones comunes por puntos cardinales (N,S,E,O,NE,NO,SE,SO).
- Conexiones up/down o in/out.
- Conexiones de una sola dirección.
- Objetos incluidos en las habitaciones.

Triz2sce añade por su cuenta una barra de estado con el nombre de la localidad actual y el número de turnos transcurridos en la aventura.
También añade un listado automático de salidas y soporte para respuestas por defecto a los comandos "SALIDAS", "MIRAR", "EXAMINAR", "AYUDA", "METER", "SACAR" y "VACIAR". Esto gastará un número variable de mensajes en la sección /MTX y las banderas 100 y 101.

Triz2sce usa los textos del cuadro de diálogo "map settings" (menu "tools") como pantalla de presentación, créditos y texto de introducción a la aventura (añadiendo frases por defecto en caso de que estuviesen vacíos).

A su vez usará el campo "subtitle" de cada localidad como texto para su descripción corta en la barra de estado (máximo 26 caracteres). Si no lo hubiera usará el campo "name" y si éste fuera el elegido por defecto "Cave" lo cambiará por "Localidad xx". A su vez usará el campo "description" para la descripción larga de la localidad en la ventana de texto de la aventura (usando de nuevo un texto por defecto "Descripción localidad xx" si no encontrase ninguno).

Igualmente triz2sce leerá, si los hubiera, los atributos [m], [f], [1], [2], [w] y [c] en el nombre de los objetos, entendiéndolos como masculino, fememnino, singular, plural, ropa y contenedor, y añadirá el artículo indeterminado correspondiente (un, uno, una, unas) al comienzo del texto de los objetos en la sección /OTX. Tanto si los hay como si no, entenderá la primera palabra del texto como la palabra de vocabulario para ese objeto y el texto completo como texto para su uso en listados.

Y por el momento triz2sce no puede manejarse con:

- Textos personalizados en los extremos de las conexiones, así como el resto de características personalizables de dichas conexiones en Trizbort (puertas, oscuridad) que al fin y al cabo tampoco tienen un soporte universal en los distintos formatos de fichero a los que Trizbort puede exportar.
- Conexiones con puntos intermedios en los espacios del mapa. Cualquier cosa que no sea una conexión directa entre una habitación y otra la ignorará.

Bugs conocidos:
===============

- Debido al comportamiento ligeramente distinto del intérprete inglés, intentar meter un objeto contenedor dentro de sí mismo (o de un objeto inexistente) en una obra inglesa, en lugar de un mensaje de error hace que el jugador deje el objeto en la localidad actual.

- Debido a que los condactos para meter y/o sacar objetos de contenedores usan un único mensaje del sistema, es probable que haya disonancias con el número (singular/plural) del objeto.

HISTORIA
========

- **1.0.8 190323**

 - Pleno soporte para objetos ropa y contenedores.
 - Chequeos adicionales para evitar nombres no válidos de objetos (cadenas nulas, espacios en blanco).

- **1.0.7** 181208

 - Arreglado: el script se colgaba si se cambiaba la posición por defecto de los objetos en una localidad sin añadir ningún objeto.

- **1.0.6** 181205

 - Arreglado: el objeto dummy creado si el mapa no incluye objetos no tenía todos los atributos necesarios.

- **1.0.5** 180916

 - Arreglado: extensión erronea al crear el fichero de salida.

- **1.0.4** 180915

 - Parche para que el contador de turnos pase de 65535 a 0 en lugar de 65200 y algo.

- **1.0.3** 180822 

 - El fichero de salida es ahora un argumento opcional.
 - Añadida opción para la creación de plantillas de DAAD en inglés.

- **1.0.1** 180420

 - Añadida forma imperativa pronominal al verbo "poner"
 - Añadido soporte al atributo [w] (que entenderá como "wearable")

- **1.0** 180404

 - Primer lanzamiento.

- **Beta 0.9.1** 180402

 - Filtra acentos en el campo "author" antes de pasarlo a mayúsculas (las mayúsculas acentuadas no son admimtidas por el compilador del DAAD).
 - Añadida el verbo "AYUDA" al vocabulario e implementada su correspondiente acción.

- **Beta 0.9** 180331

 - Añadida barra de estado que muestra el atributo "subtitle" de la localidad y el nº de turnos ejecutados durante el juego.
 - Añadido soporte para el verbo "EXAMINAR" con respuesta por defecto.
 - El texto de los objetos de la sección /OTX añade artículos indeterminados (un, unos, una, unas) en función de los atributos de los objetos.

- **Beta 0.6** 180315

 - Listado de salidas deja de ser opcional (el aprendiz puede aprender a retirarlo manualmente con facilidad, lo que es más acorde con el carácter de herramienta de aprendizaje de triz2sce)
 - Se usan los textos del cuadro de diálogo "map settings" (menú tools) de trizbort como pantalla de presentación y créditos de la aventura.

- **Beta 0.5** 181103

 - Números de vocabulario diferentes para las acciones EXAMINAR y MIRAR
 - Corregido bug por el que se producía un error al intentar convertir mapas sin objetos (a base de añadir un objeto dummy)
 - Añadido listado automático de salidas (opcional) que, ojo, gasta los flags 100 y 101

Triz2sce english doc
********************

Triz2sce version 1.0.8 190323 (c) 2018 Pedro Fernández

Triz2sce is a Python 3.x script that transforms a file generated with the text-adventure mapping tool Trizbort into a source code compatible with the DAAD compiler.
It's not meant to be either an adventure visual designer or a complete development tool. It's conceived as a fast and easy text-adventura prototyping tool, and also as a supporting tool for novel authors, specially suitable for learning workshops.

Usage:
======

Type "Python triz2sce.py -h" in a command line or powershell window to see the options.

The script requires as an argument a file (wwhich must be a map generated with the Trizbort utility in XML format) and, optionally, the name of an output file which will be a SCE formatted source code compatible with version 2.40-2.42 of the DAAD compiler. If it's not specified, a file with the same name and a .SCE extension will be created. 

Option -p1 will create a SCE listing with first-person system messages. Default is second-person.
Option -e will create a SCE listing with english texts and vocabulary. Default is spanish.

- Trizbort:

 - http://www.trizbort.com/

- DAAD

 - http://wiki.caad.es/DAAD
 - http://www.caad.es/fichas/daad.html (download)

So far it seems to convert correctly:

- Rooms, including descriptions and setting the initial location.
- Common cardinal points connections (N,S,E,W,NE,NW,SE,SW).
- Up/down and in/out connections.
- One way connections
- Objects included in locations.

Trizio2sce adds on its own a status line with the current location name and the number of used turns.
It also adds an automatic exits listing and support for default answers to the "EXITS", "LOOK", "EXAMINE", "HELP" and "EMPTY" commands. This will use a variable amount of messages in the /MTX section and flags 100 and 101.

It will also use each location "subtitle" field as a text for its short description at the status line (max. 26 characters). If it wasn't provided it will use the "name" field and if this was the default text "Cave" it will be changed to "Loaction xx". In turn, the "description" field will form the long room description in the adventure text window (again using a default "Location xx description" if there wasn't any)

Equally, triz2sce will read, if any, the [m], [f], [1], [2], [w] and [c] attributes in the objects' name, understanding them as male, female, singular, plural, wearable and container, and will add the corresponding indefinite article at he start of the object text in the /OTX section. In any case it will use the first word in the text as its vocabulary word and the whole text as text for listings.

And for the moment trizio2sce cannot handle:

- Personalized texts at the connections extremes.
- Connections with intermediate points along the map. Anything other than a direct connection between a room and another will be ignored.

Known bugs:
===========

- Due to the slighty different behavior of the english interpreter, trying to put a container object inside itself (or into a non-existent object) in an english work, instead of displaying an error message will make player drop the object at current location.

- Number (singular/plural) discordances are to be expected due to the fact that putting in and out condacts use just one system message for both cases.

HISTORY
=======

- **1.0.8** 190323

 - Full support for wearable and container objects.
 - Extra checks for non valid object names (null strings, blank spaces).
 
- **1.0.7** 181208

 - Fixed: Changing default position of objects in a room made script crash if no object were added.

- **1.0.6** 181205

 - Fixed: Dummy object created if map does not include any object lacked some needed atributes.

- **1.0.5** 180916

 - Fixed: wrong extension when creating output file.

- **1.0.4** 180915

 - Fix the turns counter so it skips from 65535 to 0 instead of 65200 something.

- **1.0.3** 180822 

 - Output file is now an optional argument
 - Added option to create english DAAD templates.


Este repositorio contiene utilidades para descargar y parsear las actas de votaciones 
nominales del Congreso de la Nación.


parse_all_votaciones.sh
=======================

Es un shell script que invoca a parse_votaciones.py para todos los PDFs de un directorio

## Uso

Ejemplo

	$ ./parse_all_votaciones actas_2001-may2013 csv

votaciones-parser
=================

Parser de actas de votaciones legislativas.

## Requisitos

    Python (>= 2.7)
    pdftotext


## Uso 

Ejemplo:

    $ ./parse_votaciones.py 130OP19_01_R22.pdf 130OP19_01_R22.csv

Para ver las opciones de uso:

    $ ./parse_votaciones.py -h

    parse_votaciones.py [-h] [--outformat {csv,json}] [--keep-textfile]
                           infile [outfile]

    positional arguments:
      infile                archivo PDF a procesar
      outfile               archivo de salida con la informacion procesada

    optional arguments:
      -h, --help            show this help message and exit
      --outformat {csv,json}
                            formato de salida (CSV o JSON)
      --keep-textfile       mantiene el archivo generado por pdftotext

## License

Junto con este proyecto, deberías recibir un archivo denominado ``LICENSE`` con los términos de la licencia.



Descargar votaciones
====================

Descargar PDFs de votaciones nominales.

## Requisitos

    Python (>= 2.7)
    BeautifulSoup (4.1.3)


## Como usar

Ejemplo:

    $ python get_votaciones.py --url http://www.diputados.gov.ar/secadmin/ds_electronicos/periodo/2013/index.html --folder votaciones_2013

    Otras URL de ejemplo:
    http://www.diputados.gov.ar/secadmin/ds_electronicos/periodo/2012/index.html
    http://www.diputados.gov.ar/secadmin/ds_electronicos/periodo/2009/index.html
    etc.

Para ver las opciones de uso:

    $ python  get_votaciones.py --help

    Descargar PDFs de votaciones nominales

    optional arguments:
      -h, --help       show this help message and exit
      --folder FOLDER  Carpeta destino para PDF descargados
      --keep-links     Conservar links de PDF en un archivo llamado links.txt
      --url URL        URL del período de votaciones nominales Ej.: http://www.di
                       putados.gov.ar/secadmin/ds_electronicos/periodo/2013/index.
                       html

## License

Junto con este proyecto, deberías recibir un archivo denominado ``LICENSE`` con los términos de la licencia.


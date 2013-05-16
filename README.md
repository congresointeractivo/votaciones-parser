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


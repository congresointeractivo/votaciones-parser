#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import argparse
import urllib
import json

# ArgumentParser configuration

parser = argparse.ArgumentParser(description='Parsea PDF de votaciones.')

parser.add_argument('infile', type=argparse.FileType('r'),
        help='archivo PDF a procesar')
parser.add_argument('outfile', nargs='?', default=sys.stdout,
        type=argparse.FileType('w'),
        help='archivo de salida (stdout si se omite)')
parser.add_argument('--keep-textfile', action='store_true',
        help='mantiene el archivo generado por pdftotext')
parser.add_argument('--pretty-print', action='store_true',
        help='imprime una versión legible')
parser.add_argument('--outformat', choices=['csv', 'json'], default='json',
        help='formato de salida')


def call_pdftotext(filename):
    ''' Uses pdftotext to create a text file based on the given filename of a
    pdf file. Returns the name of the text file.
    '''
    subprocess.call('pdftotext -nopgbrk -layout %s' % filename, shell=True)
    return infilename[:-3] + 'txt'


def deactivate_readflag(line):
    ''' Returns True if the readflag must be deactivated.
    Returns False if not.
    '''
    return line.strip()[0] == '[' \
        or line.find('Página') != -1 \
        or line.find('Observaciones') != -1


def activate_readflag(line):
    ''' Returns True if the readflag must be activated. Returns False if not.'''
    return line.find('Apellido y Nombre') != -1


def split_data(line):
    ''' Splits the line and returns a list with non-empty data.
    >>> split_data("Base Mayoría: Votos Emitidos      Tipo de Mayoría:  ...")
    ["Base Mayoría: Votos Emitidos","Tipo de Mayoría: Más de la mitad", ... )
    '''
    return [e.strip() for e in line.strip().split('  ') if e]


def split_data_with_number(text):
    '''>>> split_data_with_number("19ava Sesión Ordinaria")
    [19, "Sesión Ordinaria"]
    '''
    data = text.split()
    s = ''
    for i in range(len(data[0])):
        if data[0][i].isdigit():
            s += data[0][i]
    return int(s), ' '.join(data[1:])


def output_json(textfile, outfile):
    PERIODO = 'periodo'
    SESION = 'sesion'
    REUNION = 'reunion'
    TIPOPERIODO = 'tipo_periodo'
    TIPOSESION = 'tipo_sesion'
    TIPOREUNION = 'tipo_reunion'
    TITULO = 'titulo'
    ACTA = 'acta'
    VERSION = 'version'
    FECHA = 'fecha'
    HORA = 'hora'
    BASE = 'base_mayoria'
    TIPO = 'tipo_mayoria'
    QUORUM = 'quorum'
    MIEMBROS = 'miembros'
    RESULTADO = 'resultado'
    PRESIDENTE = 'presidente'
    VOTOS = 'votos'
    OBSERVACIONES = 'observaciones'

   # process input file and write to output file
    line = textfile.readline()

    # parse file header
    acta = {}

    while line.find('Período') == -1:
        line = textfile.readline().strip()
    periodo_str, sesion_str, reunion_str = line.split(' - ')
    acta[PERIODO], acta[TIPOPERIODO] = split_data_with_number(periodo_str)
    acta[SESION], acta[TIPOSESION] = split_data_with_number(sesion_str)
    acta[REUNION], acta[TIPOREUNION] = split_data_with_number(reunion_str)

    acta[TITULO] = textfile.readline().strip()

    line = textfile.readline().strip()
    nro_acta, version, fecha, hora = split_data(line)
    acta[ACTA] = int(nro_acta.split(' ')[-1])
    acta[FECHA] = fecha.split(' ')[-1]
    acta[HORA] = hora.split(' ')[-1]
    acta[VERSION] = version

    while line.find('Base Mayoría') == -1:
        line = textfile.readline()
    base, tipo, quorum = split_data(line)
    acta[BASE] = base.split(':')[-1].strip()
    acta[TIPO] = tipo.split(':')[-1].strip()
    acta[QUORUM] = quorum.split(':')[-1].strip()

    while line.find('Miembros del cuerpo') == -1:
        line = textfile.readline()
    miembros, basura, resultado = split_data(line)
    acta[MIEMBROS] = int(miembros.split(':')[-1])
    acta[RESULTADO] = resultado

    while line.find('Presidente') == -1:
        line = textfile.readline()
    acta[PRESIDENTE] = line.split(':')[-1].strip()

    # parse individual votes

    acta[VOTOS] = []

    line = textfile.readline()
    readflag = False
    while line and line.find('Observaciones') == -1:

        # ignore blank lines
        if not line.strip():
            line = textfile.readline()
            continue

        if deactivate_readflag(line):
            readflag = False

        if readflag:
            data = split_data(line)
            if len(data) == 4:
                acta[VOTOS].append(data)

        if activate_readflag(line):
            readflag = True

        line = textfile.readline()

    # parse observations
    if line:
        observaciones = []
        line = textfile.readline()
        while line and line.find('Modificación') == -1:
            if not line.strip():
                line = textfile.readline()
                continue
            observaciones.append(line)
            line = textfile.readline()
        acta[OBSERVACIONES] = ''.join(observaciones)

    # write json file
    if pretty_print:
        json.dump(acta, fp=outfile, indent=4, separators=(',', ': '),
            encoding='utf-8', ensure_ascii=False)
    else:
        json.dump(acta, fp=outfile, encoding='utf-8', ensure_ascii=False)


def output_csv(textfile, outfile):
    line = textfile.readline()

    readflag = False
    while line:

        # ignore blank lines
        if not line.strip():
            line = textfile.readline()
            continue

        if deactivate_readflag(line):
            readflag = False

        if readflag:
            data = split_data(line)
            if len(data) == 4:
                # Apellido y Nombre, Bloque, Provincia, Voto
                outfile.write(','.join(data) + '\n')

        if activate_readflag(line):
            readflag = True

        line = textfile.readline()


if __name__ == '__main__':

    # parse program arguments
    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    outformat = args.outformat
    pretty_print = args.pretty_print
    keep_textfile = args.keep_textfile
    infilename = infile.name

    # pdftotext call
    textfilename = call_pdftotext(infilename)

    # Fix filenames
    textfilename = urllib.unquote(textfilename.encode("utf-8"))

    textfile = open(textfilename, 'r')

    if outformat == 'json':
        output_json(textfile, outfile)
    elif outformat == 'csv':
        output_csv(textfile, outfile)

    # close files
    infile.close()
    outfile.close()
    textfile.close()
    if not keep_textfile:
        os.remove(textfilename)

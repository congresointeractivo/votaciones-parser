#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, subprocess, argparse


# ArgumentParser configuration

parser = argparse.ArgumentParser(description='Parsea PDF de votaciones.')

parser.add_argument('infile', type=argparse.FileType('r'), \
        help='archivo PDF a procesar')
parser.add_argument('outfile', nargs='?', default=sys.stdout,  type=argparse.FileType('w'),\
        help='archivo de salida con la informacion procesada (stdout si se omite)')
parser.add_argument('--outformat', choices=['csv','json'], default='csv',\
        help='formato de salida (CSV o JSON)')
parser.add_argument('--keep-textfile', action='store_true',\
        help='mantiene el archivo generado por pdftotext')


# parse actual arguments

args = parser.parse_args()
infile = args.infile
outfile = args.outfile
outformat = args.outformat
keep_textfile = args.keep_textfile
infilename = args.infile.name


# pdftotext call

subprocess.call('pdftotext -nopgbrk -layout %s' % infilename, shell=True)
textfilename = infilename[:-3] + 'txt'


# parse the text file generated with pdftotext 
# (currently outputs csv format)

def deactivate_readflag(line):
    return line.strip()[0]=="[" \
        or line.find("Página") != -1 \
        or line.find("Observaciones") != -1

def activate_readflag(line):
    return line.find("Apellido y Nombre") != -1

if __name__ == '__main__':
    textfile = open(textfilename, 'r')
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
            data = [e.strip() for e in line.strip().split("  ") if e]
            if len(data) == 4: 
                # Apellido y Nombre, Bloque, Provincia, Voto
                outfile.write( ','.join(data) + '\n' )
        
        if activate_readflag(line):
            readflag = True
        
        line = textfile.readline()
    
    textfile.close()
    
    if not keep_textfile:
        os.remove(textfilename)
    
    infile.close()
    outfile.close()


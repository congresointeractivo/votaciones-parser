#!/bin/bash
if [ ! "$1" ]; then
  echo "El primer parámetro debe ser la carpeta en la que están los PDFs"
  exit
fi 
if [ ! "$2" ]; then
  echo "El segundo parámetro debe ser la carpeta en la que se guardaran los archivos procesados"
  exit
fi 

INDIR="$1"
OUTDIR="$2"

for file in `ls "$INDIR"`
do
	echo "Procesando $INDIR/$file..."
	python parse_votaciones.py "$INDIR/$file" "$OUTDIR/$file.json"
done

#!/bin/bash
while true; do
  clear
  echo "VIRAL DNA v3.0"
  echo "1) Escanear URL"
  echo "2) Salir"
  read -p "Opción: " o
  case $o in
    1) read -p "URL: " u; python3 CORE/viral_scanner.py "$u"; read ;;
    2) exit ;;
  esac
done

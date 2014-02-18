from time import sleep
from quick2wire.gpio import pins,In,Out

import argparse

def shiftOut(latchPin,dataPin,clockPin,bitOrden,datos):
  print('llamada al shiftOut')
  
  # indico que voy a comenzar a enviar nuevos valores
  latchPin.value = 0

  # según el orden, saco una lista
  if bitOrden == 'LSBFIRST': #0,1,2,3,4,5,6,7
    orden = list(range(8)) 
  if bitOrden == 'MSBFIRST': #7,6,5,4,3,2,1,0
    orden = list(range(7,-1,-1)) 

  # con el operador a nivel de bit, obtengo los bits uno a uno de los datos a enviar
  for i in orden:
    if 2**i & datos:
      print(1,end='')
      dataPin.value = 1
    else:
      print(0,end='')
      dataPin.value = 0

  print()

    # una vez que el data tiene el valor correcto, subo y bajo el reloj para que lo lea el shift register
    clock.value = 1
    clock.value = 0
  

  #indico que finalizo el envío de nuevos valores
  latchPin.value = 1

  # un pequeño retraso entre estados para mantener los leds en esa iluminacion
  sleep(0.5)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--tipoMovimiento',help='1 para izquierda<->derecha. 2 para simetría. Valor por defecto 1.')
  args = parser.parse_args()
  
  latchPin = pins.pin(1,direction=Out)
  clockPin = pins.pin(4,direction=Out)
  dataPin = pins.pin(5,direction=Out)

  pines = [latch,clock,data]

  for pin in pines:
    pin.open()

  try:
    if args.tipoMovimiento=='2':
      while True:
        for i in range(7,-1,-1):
          shiftOut(latchPin,dataPin,clockPin,'MSBFIRST',2**i)
    else:
      while True:
        for i,j in zip(range(8),range(7,-1,-1)):
          shiftOut(1,2,3,'MSBFIRST',2**i | 2**j)
        for i in range(8):
          shiftOut(latchPin,dataPin,clockPin,'MSBFIRST',2**i)          

  except KeyboardInterrupt:
    pass
  finally:
    for pin in pines:
      pin.close()

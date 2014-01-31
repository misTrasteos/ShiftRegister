short latchPin = 5; //patilla arduino para el latch
short clockPin = 6; //patilla arduino para la señal de reloj
short dataPin = 4; //patilla arduino por la que se envían los datos

void setup(){
  //se configuran todos los pines de salida
  pinMode(latchPin,OUTPUT);
  pinMode(clockPin,OUTPUT);
  pinMode(dataPin,OUTPUT);
}//setup

void loop(){
  // es un byte, de ocho bits. Cada uno representa el estado de un led
  // 000 00 000
  byte leds = 0; 
  
  // efecto hacia un lado
  // se limpia el bit anterior, y se ilumina el actual
  for(int i=0;i<8;i++){
    bitClear(leds,i-1);
    bitSet(leds, i);

    salida(leds);
  }//for

  // efecto hacia el otro lado
  // se limpia el bit siguiente, y se ilumina el actual  
  for(int i=8;i>=0;i--){
    bitClear(leds,i+1);
    bitSet(leds,i);
    
    salida(leds);
  }//for
}//loop

void salida(byte leds){
    // indicamos al integrado que le vamos a enviar en serie
    // el nuevo valor de cada salida
    // esto se consigue poniendo la patilla del latch a bajo
    digitalWrite(latchPin,LOW);
    
    //esta función de la API arduino
    // leds: la variable a enviar bit a bit
    // LSBFIRST: Less Significant Bit First
    // dataPin: en esta patilla enviamos los datos de la variable leds en serie
    // clockPin: patilla que sirve de señal de reloj para que el integrado lea los datos
    //        está sincronizada con dataPin
    shiftOut(dataPin, clockPin, LSBFIRST, leds);

    // indicamos al integrado que ya hemos enviado el nuevo estado
    digitalWrite(latchPin, HIGH); 

    // un pequeño margen para hacer vistoso el efecto.
    delay(150);
}//salida
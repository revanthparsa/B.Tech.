   // for incoming serial data

void setup() {
        Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
}

void loop() {

        // send data only when you receive data:
                  // read the incoming byte:
      

                // say what you got:
              
                //Serial.write("hello");
                Serial.print(Serial.readStringUntil('\n'));
                
                delay(100);
                
            
                
       
}


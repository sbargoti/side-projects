#include <MicroView.h>
#include <Servo.h>

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
Servo myservo;

void quickprint(String str)
{
        uView.clear(PAGE);
        uView.setFontType(1); 		// set font type 1
	uView.setCursor(11,0);		// points cursor to x=11 y=0
	uView.print(str);
        uView.display();
}

void slowprint(String str)
{
        quickprint(str);
        delay(500);
}

void setup()
{
	uView.begin();		// init and start MicroView
	uView.clear(PAGE);	// erase the memory buffer, when next uView.display() is called, the OLED will be cleared.
	Serial.begin(9600);

        
	inputString.reserve(5);
        
        myservo.attach(5);
        
        
        quickprint("setup");
        delay(1000);
        quickprint("s-complete");
}


int pos = 0;

void loop()
{
	//uView.setCursor(11,16);		// points cursor to x=11 y=16
	//uView.print("World");

	//uView.setCursor(11,35);		// points cursor to x=11 y=35
	//uView.setFontType(4);		// sets font to space invaders
	//uView.drawChar(21,32,48,WHITE, XOR);	//prints space invader character using XOR
        
        // quickprint("servo-mode");
        
        //Get pos from serial
//        for( pos=0; pos<180; pos+=1)
//        {
//          myservo.write(pos);
//          delay(15);
//        }
        
        // quickprint("servo-mode-complete");
        
	//uView.display();
	if (stringComplete) {
        //uView.setCursor(11,0);
    	//uView.print(inputString); 
    	//uView.display();
        pos = inputString.toInt();
        myservo.write(pos);
    	quickprint(inputString);
        //  clear the string:
    	inputString = "";
    	stringComplete = false;
  	}
	
}


/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read(); 
    // add it to the inputString:
    inputString += inChar;
//    slowprint(inputString);
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    } 
  }
}


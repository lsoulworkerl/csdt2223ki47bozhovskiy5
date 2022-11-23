// Some of this code was adapted from code in Instructables Arduino Keypad 4x4 Tutorial
// by Autodesk, which can be found at https://www.instructables.com/id/Arduino-Keypad-4x4-Tutorial/

/* Included libraries */
#include <Keypad.h>

/* Definitions */
#define CLK 10
#define SS 11
#define MOSI 12
#define MISO 13
#define FALSE 0
#define TRUE !FALSE

/* Function prototype */
void setBits(char keypressed);

/* Variables */
unsigned long prevTick = 0.0;
unsigned long lastTime = 0.0;
int clockState = LOW;
int prevClkState = LOW;
unsigned int clkCounter = 0;
unsigned int pressTime;
char keypressed;
int bitNum[4];
int bitSent[] = {FALSE, FALSE, FALSE, FALSE};
int bitsToSend = 0;
int ii;

/* Constants */
const byte numRows = 4; // number of keypad rows
const byte numCols = 4; // number of columns on the keypad

void setup()
{
  	Serial.begin(9600);
	// Set pins as inputs or outputs
  	pinMode(CLK, OUTPUT);
	pinMode(MOSI, OUTPUT);
    pinMode(MISO, INPUT);
	pinMode(SS, OUTPUT);
  
  	// Set initial output pin states
	digitalWrite(CLK, LOW);
	digitalWrite(MOSI, LOW);
  	digitalWrite(SS, HIGH);
  
  	Serial.println("please, write number");
    delay(10000);
  	if (Serial.available() > 0) {  //check data
        keypressed = Serial.read();
    }


} // end setup

void loop()
{
	// Clock code
  	if ((millis() - prevTick ) >= 1000) // 1000 milliseconds has passed
  	{
    	clockState = !clockState; // toggle clockState
    	digitalWrite(CLK, clockState);
      	prevTick = millis(); // restart timing from this point
      	clkCounter++;
    }
  
  	if(bitsToSend > 0)
    {
    	if (!(bitSent[bitsToSend - 1])) // if next bit not yet sent
        {  
            if((clkCounter - pressTime) > (-1 * bitsToSend + 5)) // if it is the correct time for this bit to be sent
            {
            	if((clockState == LOW) && ((millis() - lastTime) > 1000)) // if the clock is low and it's at least a second since the last bit was sent
                {
    	    		digitalWrite(SS, LOW); // notify slave that a message is coming
                  	digitalWrite(MOSI, bitNum[bitsToSend - 1]); // write current bit to MOSI line
          			bitSent[bitsToSend - 1] = TRUE; // record that the bit has been sent
          			bitsToSend--; // decrement bit number
                  	lastTime = millis(); // timestamp of when this bit was sent
                } // end if
            } // end if
        } // end
    }
  else {
    if(digitalRead(MISO) == HIGH) // check for acknowledgment of receipt from slave
    {
      if((millis() - lastTime) > 2000)
      {
        digitalWrite(SS, HIGH); // if message was sent and acknowledged, end transmission
        digitalWrite(MOSI, LOW); // reset MOSI to off
      }
    }
    setBits(keypressed); // use setBits function to convert the key to hexadecimal bits in the 'bitNum' array
    pressTime = clkCounter; // check clock count when key was pressed
    lastTime = millis(); // timestamp of when the key was pressed
    bitsToSend = 4; // set number of bits to be sent
    
    for(ii = 0 ; ii < 4 ; ii++) // change the 'bitSent' array to FALSE
    {
      bitSent[ii] = FALSE;
    } 	
    
  }
  	delay(10); // Delay a little bit to improve simulation performance

} // end loop


// The function which sets hexadecimal bits based on the char from keypad
void setBits(char keypressed)
{
  	switch(keypressed)
    {
    	case '0':
           	bitNum[3] = 0;
      		bitNum[2] = 0;
      		bitNum[1] = 0;
      		bitNum[0] = 0;
      		break;
    	case '1':
           	bitNum[3] = 0;
      		bitNum[2] = 0;
      		bitNum[1] = 0;
      		bitNum[0] = 1;
      		break;      
    	case '2':
           	bitNum[3] = 0;
      		bitNum[2] = 0;
      		bitNum[1] = 1;
      		bitNum[0] = 0;
      		break;      	
    	case '3':
           	bitNum[3] = 0;
      		bitNum[2] = 0;
      		bitNum[1] = 1;
      		bitNum[0] = 1;
      		break;      	
    	case '4':
           	bitNum[3] = 0;
      		bitNum[2] = 1;
      		bitNum[1] = 0;
      		bitNum[0] = 0;
      		break;      
    	case '5':
           	bitNum[3] = 0;
      		bitNum[2] = 1;
      		bitNum[1] = 0;
      		bitNum[0] = 1;
      		break;      
    	case '6':
           	bitNum[3] = 0;
      		bitNum[2] = 1;
      		bitNum[1] = 1;
      		bitNum[0] = 0;
      		break;
    	case '7':
           	bitNum[3] = 0;
      		bitNum[2] = 1;
      		bitNum[1] = 1;
      		bitNum[0] = 1;
      		break;
    	case '8':
           	bitNum[3] = 1;
      		bitNum[2] = 0;
      		bitNum[1] = 0;
      		bitNum[0] = 0;
      		break;      
    	case '9':
           	bitNum[3] = 1;
      		bitNum[2] = 0;
      		bitNum[1] = 0;
      		bitNum[0] = 1;
      		break;      
    	case 'A':
           	bitNum[3] = 1;
      		bitNum[2] = 0;
      		bitNum[1] = 1;
      		bitNum[0] = 0;
      		break;      
    	case 'B':
           	bitNum[3] = 1;
      		bitNum[2] = 0;
      		bitNum[1] = 1;
      		bitNum[0] = 1;
      		break;      
    	case 'C':
           	bitNum[3] = 1;
      		bitNum[2] = 1;
      		bitNum[1] = 0;
      		bitNum[0] = 0;
      		break;
    	case 'D':
           	bitNum[3] = 1;
      		bitNum[2] = 1;
      		bitNum[1] = 0;
      		bitNum[0] = 1;
      		break;      
    	case '*': // Takes the place of 'E'
           	bitNum[3] = 1;
      		bitNum[2] = 1;
      		bitNum[1] = 1;
      		bitNum[0] = 0;
      		break;      
    	case '#': // Takes the place of 'F'
           	bitNum[3] = 1;
      		bitNum[2] = 1;
      		bitNum[1] = 1;
      		bitNum[0] = 1;
      		break;
      	default:
      		// do nothing if not matching  
            ;
    }
} // end setBits function

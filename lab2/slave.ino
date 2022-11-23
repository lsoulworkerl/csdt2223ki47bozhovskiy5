/* Included libraries */
#include <LiquidCrystal.h>

/* Arduino pin definitions */
#define CLK 7
#define SS 8
#define MOSI 9
#define MISO 10

/* Variables */
int clkState = LOW;
int prevClkState = LOW;
int data = 0x00; // for storing received bits
int bitPos = 3; // current bit position
unsigned long timerStart;
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);


void setup()
{
    Serial.begin(9600);
	// set pins as inputs or outputs
  	pinMode(CLK, INPUT);
	pinMode(MOSI, INPUT);
    pinMode(MISO, OUTPUT);
	pinMode(SS, INPUT);
  
  	// set initial states of output pins
  	digitalWrite(MISO, LOW);
  
  	// set up the LCD's number of columns and rows:
  	lcd.begin(16, 2);
	lcd.setCursor(0, 1);  
}  	


void loop()
{
	clkState = digitalRead(CLK); // align clock with master's clock
  	if (clkState != prevClkState) // if clock has changed
    {
       	prevClkState = clkState;
      	if (digitalRead(SS) == LOW) // and if this slave is to receive a message
      	{
          	if (clkState == HIGH) // and if clock change was from low to high
            {
            	if (digitalRead(MOSI) == LOW) // if MOSI was low then record a 0 in current bit position
                { 
                    data <<= 1;
                    Serial.println(data, DEC);
                	data &= ~(0x01 << bitPos); // 'AND' existing bit with a 0 to make it 0
                  	bitPos--; // decrement to next bit position
                }
              	else // if MOSI was high then record a 1 in current bit position
                {
                  	data |= (0x01 << bitPos); // 'OR' existing bit with a 1 to make it 1
                  	bitPos--; // decrement to next bit position
                }
              	if (bitPos < 0) // if all 4 bits have been set
                {  	
                  	delay(500);
                  	digitalWrite(MISO, HIGH); // send an acknowledgment signal
                    delay(1000);
                  	digitalWrite(MISO, LOW);
                    bitPos = 3; // reset bit position
           			lcd.clear(); // clear previous data on lcd
  					lcd.print(data); // send data to lcd
                }
            }
        }
    }
 	
  
  	delay(10); // Delay a little bit to improve simulation performance

} // end loop

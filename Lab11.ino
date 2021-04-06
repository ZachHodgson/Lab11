int CLK=13; // clk signal
int timer1_counter;
String user_input;
volatile int data[2000];

void setup() {
  // put your setup code here, to run once:
  noInterrupts(); // disable all interrupts
  TCCR1A = 0;
  TCCR1B = 0;
  // preload timer 65536-16MHz/256/2Hz
  timer1_counter = 10000; // Adjust the value accordingly
  TCNT1 = timer1_counter; // preload timer
  TCCR1B |= (1 << CS12); // 256 pre-scaler
  TIMSK1 |= (1 << TOIE1); // enable timer overflow interrupt
  interrupts(); // enable all interrupts
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0){
    user_input == Serial.readStringUntil('\n');
    for(int i=0;i<2000;i++){
      data[i] = toInt(user_input);
    }
  }
  delay(500);
}

ISR(TIMER1_OVF_vect) // interrupt service routine
{
  TCNT1 = timer1_counter; // preload timer
  digitalWrite(CLK, digitalRead(CLK) ^ 1);
}

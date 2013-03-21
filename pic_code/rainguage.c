#include <16F877A.h>
#device ADC=10 //for 10 bit resolution
#fuses HS,NOWDT,PUT,NOPROTECT,NOLVP
#include "pic.h"
#use delay(clock=20000000)
#use rs232(baud=9600,xmit=PIN_C6,rcv=PIN_C7,bits=8,errors)
#use I2C(master, sda=PIN_C4, scl=PIN_C3)
#include "lcd_R.h"
#include "sht11.c"

void rain(void);
void soil(void);
double map(double value, float x_min, float x_max, float y_min, float y_max); 

unsigned int16 s;
float y,v,x=0.00;
int a,r;
void main()
{
 float restemp, truehumid;
 trisa0=1;
 trisa1=0;
 adcon1=0x0e;
 trisb=0x00;
 //trisd1=0;
 lcdinit();
 go(0);
 printc("  RAIN GUAGE  ");
 sht_init();

 while(1)
 {
   rain();	 
   setup_adc(ADC_CLOCK_INTERNAL);
   //printf("BGW:");
   printf("RAIN;%3.2f;",x);
   soil();
   sht_rd (restemp, truehumid);
   printf("Temp;%3.1f;", restemp, 223);
   printf("RH;%3.1f\n", truehumid);
   delay_ms(50);        //delay 500 ms between reading to prevent self heating of sensor
 }
}

/*
////////////////////////END OF MAIN PROGRAM //////////////////////////////////////
*/

void rain()
{
  a=input(PIN_A1);
  if(a)
  {
	x=x+0.2;  
	r++	  ;
    //printf("%d",r);
    //printf("RAIN = %3.2f",x);
    //delay_ms(500); 	
  }  
}
	
void soil()
{
  //setup_adc_ports(AN0_AN1_AN2_AN4_AN5_AN6_AN7_VSS_VREF);//to setup a0 as analog read and a3 as reference	
  set_adc_channel(0);
  delay_us(20);
  s=read_adc();
  //printf("VALUE=%lu\t",s);
  y= 0.0048 * s;
  //printf("SOIL=%f",y); 
  if(y > 0.00 && y < 0.25)
  {
  	  v = map(y, 0,0.25, 0,2.5);
      printf("VWC;%3.3f;",v); 
  }
  else if(y > 0.25 && y < 0.5)
  {
	  v = map(y, 0.25,0.5, 2.5,7.5);
      printf("VWC;%3.3f;",v); 
  } 
   else if(y > 0.5 && y < 0.75)
  {
	  v = map(y, 0.5,0.75, 7.5,10.0);
      printf("VWC;%3.3f;",v); 
  } 
   else if(y > 0.75 && y < 1.0)
  {
	  v = map(y, 0.75, 1.0 , 10.0 , 12.5);
      printf("VWC;%3.3f;",v); 
  } 
   else if(y > 1.0 && y < 1.25)
  {
	  v = map(y, 1.0,1.25, 12.5,15.0);
      printf("VWC;%3.3f;",v); 
  } 
   else if(y > 1.25 && y < 1.5)
  {
	  v = map(y, 1.25,1.5, 15.0,25.0);
      printf("VWC;%3.3f;",v); 
  } 
   else if(y > 1.5 && y < 1.75)
  {
	  v = map(y, 1.5, 1.75, 25.0 , 35.0);
      printf("VWC;%3.3f;",v); 
  } 
   else if(y > 1.75 && y < 2.0)
  {
	  v = map(y, 1.75, 2.0, 35.0 , 45.0);
      printf("VWC;%3.3f;",v); 
  } 
   else if(y > 2.0 && y < 2.5)
  {
	  v = map(y, 2.0 , 2.5, 45.0 , 50.0);
      printf("VWC;%3.3f;",v); 
  } 
 
}
 
 double map(double value, float x_min, float x_max, float y_min, float y_max)   
{                               
    return (y_min + (((y_max - y_min)/(x_max - x_min)) * (value - x_min)));
} 
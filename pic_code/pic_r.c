//#define max 65534
#include<16f877a.h>
#include<pic.h>
#USE DELAY (CLOCK=20000000)
#use rs232(baud=9600,parity=N,xmit=PIN_C6,rcv=PIN_C7,bits=8)
#include"lcd1JOVIN.h"
#include<string.h>

			
void main()
{
  trisb=0x00;
  trisa=0x00;
  lcdinit();
   while(1)
	{
	  go(0);
      printc("JOVIN");
      delay_ms(1000);     
    }	
}


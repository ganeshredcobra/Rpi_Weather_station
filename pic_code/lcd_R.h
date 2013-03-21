/*LCD HEDDER 4 bit 
CAUTION : Use pic.h hedder
		   : You have to configure output status of used pins from TRIS register
		   : Don't use location 0x20 it is used here for inner calculations 
		   :Don't use d0,d1,d2,d3,RS,E,selfscroll names in the program
Define the bits d0 to d3 ,RS, E and use the functions 

R is not used and it should be grounded
*/
#define 	d3	rb0//rb7	
#define 	d2	rb1//rb6
#define 	d1	rb2//rb5
#define 	d0	rb3//rb4
#define RS	rb7//rb3
#define E	rb6//rb2
#define selfscroll		// for strings > 16 char "selfscroll" or "newline" 
/*Functions avialable
For printing strings directly use printc("String"); insted of prints
//lcdinit();  -> initialises LCD to 2 row 5x7 cursor off right side mode
go(location)	-> goto specified address from 0.  64 is second line starting address
clrscr();		-> clear LCD screen
print(no) -> displays Nos in dec upto 999999.999 only
printc(char)	-> displays an ASCII char
prints(char*)	-> Base address of char array
scroll(char*,delay)		scroll a message with delay*10 ms
wave(char*,delay)		wave a message with delay*10 ms
command(no) -> no	Cursor	Blink
			NO=000011CB					1 for ON  & 0 for off
enb()		-> Give a high to low pulse in E pin
outc(no)		-> output nibble to dataline and call an enb()
*/

#byte in =0x20
#bit g0 =0x20.0
#bit g1 =0x20.1
#bit g2 =0x20.2
#bit g3 =0x20.3 
#bit g4 =0x20.4
#bit g5 =0x20.5
#bit g6 =0x20.6
#bit g7 =0x20.7

void enb(void)
{
	E=1;
	delay_us(1);
	E=0;
}//
void outc(int a)
{	in=a;
	d3=g3;
	d2=g2;
	d1=g1;
	d0=g0;
	delay_us(1);
	enb();
}//

lcdinit()  
{     
	
	delay_ms(2);	//wait time
		
	RS=0;
	outc(3);
	delay_ms(5);  
	outc(3);
	delay_us(50);
	outc(2);
	delay_us(50);
	outc(2);
	delay_us(50);
	outc(8);
	delay_us(50);	  
    
     outc(1);	//CURSOR MODE,RIGHT SH
     delay_us(50);
     outc(4);
     delay_us(50);
     outc(0);	//SCREEN,CUR-Off,
     delay_us(50);
     outc(0xC);
     delay_us(10);
     delay_us(50);	
     outc(0);	//CUR RIGHT SHIFT
     delay_us(50);
     outc(6);
     delay_us(50);
    outc(0);	//CLE LCD &MEM HM CUR
    delay_us(50);
    outc(1);
    delay_ms(2);
 //   printf("Init over");
     RS=1;
   
}//

void printc(char a)
{	
	outc (a>>4);
	delay_us(50);
	outc (a);
	delay_us(50);
}	//

void command(int dat)
{	
	RS=0;
	printc(dat);
	RS=1;
}	

void go(int p)
{	//p=p|0x80;
	RS=0;
	printc(p | 0x80);
	RS=1;
}//


print(float q)
{	
	float p ;
	int i=0,j=0,k=0,l=0,m=0,n=0,x;
	i =q/100000;
	if(i)
	{
	printc (i+0x30);
	}
	p=i;
	q = q - p*100000;
	j=q/10000;
	if(i || j)
	{
	printc(j+0x30);
	}
	p=j;
	q = q - p*10000;
	k=q/1000;
	if(i || j || k)
	{printc(k+0x30);}
	p=k;
	q = q - p*1000; 
	
	l=q / 100;
	if( i || j || k || l )
	{printc(l+0x30);}
	p=l;
	q = q - p *100;

	m=q/10;
	if(i || j || k || l || m)
	{printc (m+0x30);}
	q = q - m*10;
	n=q;
	printc(n+0x30);
	q = q -n; 

	q=q*1000;					//Aftrer Decimel	
	l=q / 100;
	p=l;
	q = q - p *100;
	m=q/10;
	q = q - m*10;
	n=q;
	if(n || m || l)
	{
	printc('.');
	printc(l+0x30);
	}
	if(n || m)
	{
	printc(m+0x30);
	}
	if(n)
	{
	printc(n+0x30>>4);
	}
	
}//	

	prints(char *c)
{	int k=0;
	while(*c!='\0')
	{
	//printf("%c",*c);
	printc(*c);
	c++;
	#ifdef selfscroll
	k++;
	if(k>15)
	{
	delay_ms(200);
	command(0x18);
	}
	#endif
	#ifdef newline
	k++;
	if(k==16 || k==48)
	go(64);
	if(k==32 || k== 64)
	go(0);
	#endif
	}
}//

clrscr()
{	
	RS=0;
	outc(0);	//CLE LCD &MEM HM CUR
    	delay_us(50);
    	outc(1);
    	delay_ms(2);
	RS=1;
}//

scroll(char *c,long int d)
{
	int i=15;
 for(i=15;i>0;i--)
	{
	go(i);
	prints(c);
	delay_ms(10*d);
	clrscr();
	}
	while(*c!='\0')
	{
	go(0);
	prints(c);
	c++;
	delay_ms(10*d);
	clrscr();
	}
}//

wave(char *c,long int d)
{	char *t;
	int i=15,k=0;
	t=c;
	while(*t!='\0')
	{k++;t++;}
 for(i=16-k;i>=0;i--)
	{
	go(i);
	prints(c);
	delay_ms(10*d);
	clrscr();
	if(i==0)
	break;
	}
	for(i=0;i<17-k;i++)
	{
	go(i);
	prints(c);
	delay_ms(10*d);
	clrscr();
	}//
	
}//

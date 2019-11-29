#include <stdio.h>
int w1 =5;
int w2 =4;
#define maxL  10000
       
int daMx[8]={-2,-1,1,2,2,1,-1,-2};
int daMy[8]={1,2,2,1,-1,-2,-2,-1};
int wR1,wR2;
int wraOne(int p1,int p2,int a,int b)
{
     a = p1+a;
     b = p2+b;    
    if (a<0 || b<0 || a>w1 || b>w2)
        {return -1;}
    wR1=a;
    wR2=b;
    return 1;
    }
    
int getNextPos(int a,int b,int n)
{
    return wraOne(a,b,daMx[n-1],daMy[n-1]);    
    }
int curPosx = 0;
int curPosy = 0;

int posListx[1000];
int posListy[1000];
int tryTimeList[1000];
int listL = 0;
int tryTime = 1;
long int co = 0;
int foundPos(int a,int b)
{
    for(int i=0;i<listL;i++)
        {
            if (posListx[i]==a&&posListy[i]==b)
                {return 1;}
            }
            return -1;
    }
int main()

{
 while (1)
     {
    co += 1;
    if (co %1000000==0)
        {printf("%ld,%d,(%d,%d),(%d,%d),(%d,%d),(%d,%d),(%d,%d)\n",co,listL,
        posListx[0],posListy[0],
        posListx[1],posListy[1],
        posListx[2],posListy[2],
        posListx[3],posListy[3],
        posListx[4],posListy[4]);}
    if (listL==(w1+1)*(w2+1)-1 && (curPosx*curPosy==2 ||curPosx*curPosy==-2))
        {
        printf("ok\n");
        for(int i=0;i<listL;i++)
            printf("(%d,%d) ", posListx[i],posListy[i]);
        printf("(%d,%d)\n",curPosx,curPosy);
        break;
        }
    if (tryTime == 9)
    {
        if (listL==0)
            {
                  printf("failed\n");
                    break;
                }
   
        curPosx = posListx[listL-1];
        curPosy = posListy[listL-1];
        tryTime = tryTimeList[listL-1];
            listL--;
        tryTime += 1;
        continue;
        }
    int r = getNextPos(curPosx,curPosy,tryTime);
    int a = wR1;
    int b = wR2;
    int r2 = foundPos(a,b);
    if ( r==-1 || r2==1)
        {
        tryTime += 1;
        continue;
        }
    posListx[listL] = curPosx;
    posListy[listL] = curPosy;
    tryTimeList[listL]=tryTime;
    listL++;
    curPosx=a;
    curPosy=b;
    tryTime = 1;
        }
    return 0;
    }

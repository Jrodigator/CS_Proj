# include <stdio.h>
# include <stdbool.h>
# include <math.h>

int addBinary(bool [5], bool [5]);

int main(){
   int i=0;
   int g =0;
   int sum[5];

   sum[0] =0;
   sum[1] =0;
   sum[2] =0;
   sum[3] =0;
   sum[4] =0;

   int b[5];
   b[0] =0;
   b[1] =1;
   b[2] =0;
   b[3] =0;
   b[4] =0;

   int set[5];
   set[0] =0;
   set[1] =1;
   set[2] =1;
   set[3] =0;
   set[4] =0;

   bool c[5] = {0,0,1,0,1};
   bool d[5] = {0,0,1,0,0};
   addBinary(c,d);

 }


int addBinary(bool a[5], bool b[5]){

    int i, c = 0;
    int sum[5];
    for(i = 0; i < 5 ; i++){
       sum[i] = ((a[i] ^ b[i]) ^ c); // c is carry
       c = ((a[i] & b[i]) | (a[i] & c)) | (b[i] & c);
    }

    sum[i] = c;
    int total = 0;
    int z=0;

    for(z=0; z<5; z++) {
       //printf("%d",sum[z]);
       total = total + (pow(2,(z)))*sum[z];

    }

    printf("%d", total);
    return c;
}
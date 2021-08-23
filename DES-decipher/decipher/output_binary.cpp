#include<bits/stdc++.h>
using namespace std;

int main(){
    FILE *fi, *fo;
    fo = fopen("output_binary.txt", "w");
    char temp[17];
    fi = fopen("cleanout.txt","r+");
    long int i=0;
    int modulus;
    char temp2[64];

    while(i<200000){
        fscanf(fi, "%s", temp);
        
        for(int j=0;j<16;j++){
            int val = temp[j]-102;
            // cout << val << endl;
            for (int k=0; k<4;k++){
                modulus = val%2;
                val = val/2;
                temp2[j*4+3-k] = modulus+48;
            }
            // fprintf(fo, "%s", temp2);
            // cout << sizeof(temp2) << endl;
            
        }
        for(int i=0;i<64;i++){
            // cout<<temp2[i]<<endl;
            fprintf(fo,"%c",temp2[i]);
        }
        // fprintf(fo, "%s\n", temp2);
        fprintf(fo, "\n");
        ++i;
    }
}
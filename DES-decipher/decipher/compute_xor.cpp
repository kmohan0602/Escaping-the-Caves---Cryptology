#include<iostream>
#include<fstream>
#include<string>
using namespace std;

int main(){
    ifstream fi;
    ofstream fo1, fo2, fo3,fo4;

    // int RFP[] = {
    //     8,40,16,48,24,56,32,64,
    //     7, 39,15,47,23,55,31,63,
    //     6,38,14,46,22,54,30,62,
    //     5,37,13,45, 21,53,29,61,
    //     4,36,12,44,20,52,28,60,
    //     3, 35, 11,43,19,51,27,59,
    //     2, 34, 10, 42,18, 50,26,58,
    //     1,33,9,41, 17, 49, 25,57,
    // };

    int RFP[]={
         57,49,41,33,25,17,9,1,
         59,51,43,35,27,19,11,3,
         61,53,45,37,29,21,13,5,
         63,55,47,39,31,23,15,7,
         58,50,42,34,26,18,10,2,
         60,52,44,36,28,20,12,4,
         62,54,46,38,30,22,14,6,
         64,56,48,40,32,24,16,8
        };

    int E[] = {
        32, 1, 2, 3, 4, 5,
        4, 5,6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17, 
        16, 17, 18, 19, 20, 21, 
        20, 21, 22, 23, 24, 25, 
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    };

    int INV_P[] = {
        9, 17, 23, 31,
        13, 28, 2, 18,
        24, 16, 30, 6,
        26, 20, 10, 1,
        8, 14, 25, 3,
        4, 29, 11, 19,
        32, 12, 22, 7,
        5, 27, 15, 21,
    };


    fi.open("output_binary.txt");
    fo1.open("xor_exp_out.txt");
    fo2.open("xor_s_out.txt");
    fo3.open("alpha1.txt");
    fo4.open("reverse_fp.txt");

    long int count = 0;
    string c1,c2;
    char temp_c1[8][8], temp_c2[8][8];
    char inv_c1[8][8], inv_c2[8][8];
    int output_xor[8][8];

    while(count < 100000){
        count++;
        getline(fi, c1);
        getline(fi,c2);

        for(int i=0;i<8;i++){
            for(int j=0; j<8;j++){
                temp_c1[i][j] = c1[i*8+j];
                temp_c2[i][j] = c2[i*8+j];
                // output_xor[i][j] = temp_c1[i][j] ^ temp_c2[i][j];
            }
        }

        for(int i=0;i<8;i++){
            for(int j=0;j<8;j++){
                int row = (RFP[i*8+j]-1)/8;
                int col = (RFP[i*8+j]-1)%8;
                inv_c1[i][j] = temp_c1[row][col];
                fo4 << inv_c1[i][j];
            }
        }
        fo4<<'\n';
        for(int i=0;i<8;i++){
            for(int j=0;j<8;j++){
                int row = (RFP[i*8+j]-1)/8;
                int col = (RFP[i*8+j]-1)%8;
                inv_c2[i][j] = temp_c2[row][col];
                fo4 << inv_c2[i][j];
            }
        }
        fo4<<'\n';

        //finding xor b/n pairs of output strings
        for(int i=0;i<8;i++)
        {
            for(int j=0;j<8;j++)
            {
                output_xor[i][j] = int(inv_c1[i][j]) ^ int(inv_c2[i][j]);
            }
        }
        
        //finding output of expansion of xor of output strings

        for(int i=0;i<8;i++)
        {
            for(int j=0;j<6;j++)
            {
                int row = (E[i*6+j]-1)/8;
                int col = (E[i*6+j]-1)%8;
                fo1<<output_xor[row][col];
                fo3<<inv_c1[row][col];
            }
        }
        fo1<<'\n';
        fo3<<'\n';
        // findig xor b/n L5 XOR & R6
        output_xor[4][5] = output_xor[4][5] ^ 1;

        //finding output from S-Boxes
        for(int i=0;i<8;i++)
        {
            for(int j=0;j<4;j++)
            {
                int row = (INV_P[i*4+j]-1)/8;
                int col = (INV_P[i*4+j]-1)%8;
                fo2<<output_xor[row+4][col];
            }
        }
        fo2<<'\n';
    }
}
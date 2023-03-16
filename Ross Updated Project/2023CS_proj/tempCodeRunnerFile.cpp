int binary_addition(bool a[5], bool b[5]) {
    bool c[5];
    bool o = 0;
    int i = 0;
    int k = 0;

    for (i = 5; i >= 0; i--) {
        if ((a[i] ^ b[i]) && !(o)) {
            c[4-i] = 1; 
            o = 0;
        }
        else if ((a[i] ^ b[i]) && (o)) {
            c[4-i] = 0;
            o = 1;
        }
        else if ((a[i] && b[i]) && !(o)) {
            c[4-i] = 0;
            o = 1;
        }
        else if ((a[i] && b[i] && o)) {
            c[4-i] = 1;
            o = 1;
        }
        else if (o) {
            c[4-i] = 1;
            o = 0;
        }
        else { 
            c[4-i] = 0;
            o = 1;
        }
    }
    //c[4] = o;
    int sum = 0;
    
    for (k = 0; k <= 4; k++) {
        sum += 2^(k) * c[k]; 
    }
    
    return sum;
}


bool a[5] = {0,0,1,0,1};
bool b[5] = {0,1,0,0,1};

sprintf(int_str, "%d", binary_addition(a, b));

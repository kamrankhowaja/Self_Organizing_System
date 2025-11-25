// to run gcc -o Part1 Part1.c ex-1/blackbox1.c -lm
// ./Part1
#include "ex-1/blackbox1.h"  
#include <stdio.h>
#include <stdlib.h>

void generate_csv(int n, double input[], double output_box_a[]) {
    FILE *file = fopen("output_data.csv", "w");
    if (file == NULL) {
        printf("Error opening file for writing\n");
        return;
    }
    fprintf(file, "Index,Input,Output_boxA\n");

    for (int i = 0; i < n; i++) {
        fprintf(file, "%d,%f,%f\n", i, input[i], output_box_a[i]);
    }
    fclose(file);
}

int main() {
    int n = 100;
    double input[n];
    double output_box_a[n];

    for (int i = 0; i < n; i++) {
        input[i] = (double)i;
    }

    for (int i = 0; i < n; i++) {
        output_box_a[i] = boxA(0.1,1.0, (i > 0) ? output_box_a[i - 1] : input[i]);
        boxB(0.5, (unsigned)n);
    }

    generate_csv(n, input, output_box_a);

    // for (int i = 0; i < n; i++) {
    //     printf("Output boxA[%d]: %f\n", i, output_box_a[i]);
    // }
    return 0;
}

// to run gcc -o Part1 Part1.c ex-1/blackbox1.c -lm
// ./Part1

#include "ex-1/blackbox1.h"  
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define TIME_STEP 0.1
#define NUM_POINTS 50000

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

void generate_boxA_data(int n){
    double time[n];
    double output_box_a[n];
    double previous_value = 0.0;
    
    time[0] = 0.0;
    for (int i = 0; i < n; i++) {
        if (i > 0) {
            time[i] = time[i-1] + TIME_STEP;
        }
        output_box_a[i] = boxA(TIME_STEP, time[i], previous_value);
        previous_value = output_box_a[i];
    }

    generate_csv(n, time, output_box_a);
    printf("Data for boxA generated and saved to output_data.csv\n");
}

void generate_boxB_data(int initial_state){

    printf("Generating data for boxB");
    boxB(initial_state, 100);
    printf("Data for boxB generated and printed to console\n");
}

int main() {
    int n = NUM_POINTS;
    int initial_state = 0.9999;
    generate_boxA_data(n);
    generate_boxB_data(initial_state);
    return 0;
}


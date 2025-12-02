// to run gcc -o Part1 Part1.c ex-1/blackbox1.c -lm
// ./Part1

#include "ex-1/blackbox1.h"  
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <unistd.h>

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

void generate_boxB_data(double initial_state){

    printf("Generating data for boxB\n");

    const char *tmp_name = "boxB_temp.txt";
    FILE *tmp = fopen(tmp_name, "w+");
    if (tmp == NULL) {
        printf("Failed to open temporary file for capturing output\n");
        return;
    }

    // Save current stdout fd
    fflush(stdout);
    int saved_stdout = dup(fileno(stdout));
    if (saved_stdout == -1) {
        printf("Failed to duplicate stdout\n");
        fclose(tmp);
        return;
    }

    // Redirect stdout to temporary file
    if (dup2(fileno(tmp), fileno(stdout)) == -1) {
        printf("Failed to redirect stdout\n");
        close(saved_stdout);
        fclose(tmp);
        return;
    }

    // Call boxB which prints to stdout (now redirected to tmp)
    boxB(initial_state, 100);

    // Restore stdout
    fflush(stdout);
    if (dup2(saved_stdout, fileno(stdout)) == -1) {
        printf("Failed to restore stdout\n");
    }
    close(saved_stdout);
    fclose(tmp);

    // Read captured output and write CSV
    tmp = fopen(tmp_name, "r");
    if (tmp == NULL) {
        printf("Failed to reopen temporary file for reading\n");
        return;
    }

    FILE *csv = fopen("boxB_output.csv", "w");
    if (csv == NULL) {
        printf("Failed to open CSV file for writing\n");
        fclose(tmp);
        return;
    }
    fprintf(csv, "time,value\n");

    char line[256];
    double t, v;
    while (fgets(line, sizeof(line), tmp)) {
        if (sscanf(line, "%lf %le", &t, &v) == 2) {
            fprintf(csv, "%f,%e\n", t, v);
        }
    }

    fclose(tmp);
    fclose(csv);
    remove(tmp_name);

    printf("Data for boxB generated and saved to boxB_output.csv\n");
}

int main() {
    int n = NUM_POINTS;
    double initial_state = 0.5;
    generate_boxA_data(n);
    generate_boxB_data(initial_state);
    return 0;
}


#include "ex-1/blackbox1.h"  // Include the blackbox header
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n = 10;  // Define the size of the time series
    double input[n];           // Array to store input values
    double output_box_a[n];    // Array to store outputs from boxA
    double output_box_b[n];    // Array to store outputs from boxB

    // Generate input values for the black boxes (you can modify the input pattern)
    for (int i = 0; i < n; i++) {
        input[i] = (double)i;  // Simple linear input, can change to suit your problem
    }

    // Generate outputs for boxA
    for (int i = 0; i < n; i++) {
        output_box_a[i] = boxA(0.1, input[i], (i > 0) ? output_box_a[i - 1] : 0.0);  // Call to boxA
    }
    // Print the outputs for both boxA and boxB
    for (int i = 0; i < n; i++) {
        printf("Output boxA[%d]: %f\n", i, output_box_a[i]);
    }

    return 0;
}
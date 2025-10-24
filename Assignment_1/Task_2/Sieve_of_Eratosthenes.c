#include<stdio.h>
#include<stdbool.h>
#include<stdlib.h>
#include<time.h>


int main() {

    long* n = (long*)malloc(sizeof(long));
    *n = 1000000;

    clock_t start = clock();

    unsigned long size = (unsigned long)(*n + 1) * sizeof(bool);
    bool* is_prime = (bool*)malloc(size);

    if (is_prime == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }

    // Step 1: Initialize the array
    for (int i = 0; i <= *n; i++) {
        is_prime[i] = true;
    }

    is_prime[0] = false;
    is_prime[1] = false;
    // Step 2: Sieve of Eratosthenes
    for (long p = 2; p <= *n; p++) {
        if (is_prime[p]) {
            for (long multiple = p * p; multiple <= *n; multiple += p) {
                is_prime[multiple] = false;
            }
            // printf("Prime found: %d\n", p);
        }
    }

    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Time taken to find all primes up to %ld: %f seconds\n", *n, time_taken);
    
    // Highest Prime number 
    for (long i = *n; i >= 2; i--) {
        if (is_prime[i]) {
            printf("Highest prime number up to %ld is: %ld \n", *n, i);
            break;
        }
    }
    
    free(is_prime);
    free(n);
    return 0;
}
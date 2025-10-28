#include<stdio.h>
#include<stdbool.h>
#include<stdlib.h>
#include<string.h>
#include<omp.h>

int main() {
    long n = 10000000000;
    long segment_size = 100000000;  // 100 million per segment
    
    double start = omp_get_wtime();
    
    printf("Starting Sieve of Eratosthenes for n = %ld\n", n);
    printf("======================================\n\n");
    
    // Step 1: Find all primes up to sqrt(n) using simple sieve
    printf("Phase 1: Finding small primes up to sqrt(n)...\n");
    long limit = 100000;  // sqrt(10^10) ≈ 100000
    bool* small_primes = (bool*)malloc((limit + 1) * sizeof(bool));
    
    for (long i = 0; i <= limit; i++) {
        small_primes[i] = true;
    }
    small_primes[0] = small_primes[1] = false;
    
    for (long p = 2; p * p <= limit; p++) {
        if (small_primes[p]) {
            for (long multiple = p * p; multiple <= limit; multiple += p) {
                small_primes[multiple] = false;
            }
        }
    }
    
    // Collect small primes
    long* primes = (long*)malloc(limit * sizeof(long));
    long prime_count = 0;
    for (long i = 2; i <= limit; i++) {
        if (small_primes[i]) {
            primes[prime_count++] = i;
        }
    }
    free(small_primes);
    
    printf("✓ Found %ld small primes\n\n", prime_count);
    
    // Calculate total segments
    long total_segments = (n + segment_size - 1) / segment_size;
    printf("Phase 2: Processing %ld segments in parallel...\n", total_segments);
    printf("Segment size: %ld\n", segment_size);
    printf("======================================\n\n");
    
    // Step 2: Segmented sieve in parallel with progress tracking
    long highest_prime = 2;
    long segments_completed = 0;
    
    #pragma omp parallel
    {
        bool* segment = (bool*)malloc(segment_size * sizeof(bool));
        long local_highest = 2;
        
        #pragma omp for schedule(dynamic)
        for (long seg_idx = 0; seg_idx < total_segments; seg_idx++) {
            long low = seg_idx * segment_size;
            long high = low + segment_size - 1;
            if (high > n) high = n;
            
            // Initialize segment
            long seg_length = high - low + 1;
            memset(segment, true, seg_length);
            
            // Sieve this segment
            for (long i = 0; i < prime_count; i++) {
                long p = primes[i];
                
                // Find first multiple of p in [low, high]
                long start = (low / p) * p;
                if (start < low) start += p;
                if (start == p) start += p;  // Don't mark p itself
                if (start < 2) start = 2 * p;
                
                for (long j = start; j <= high; j += p) {
                    segment[j - low] = false;
                }
            }
            
            // Find highest prime in this segment
            for (long i = high; i >= low && i >= 2; i--) {
                if (segment[i - low]) {
                    if (i > local_highest) {
                        local_highest = i;
                    }
                    break;
                }
            }
            
            // Update progress
            #pragma omp critical
            {
                segments_completed++;
                double progress = (100.0 * segments_completed) / total_segments;
                
                // Print milestone progress
                if (segments_completed % 10 == 0 || segments_completed == total_segments) {
                    double elapsed = omp_get_wtime() - start;
                    double segments_per_sec = segments_completed / elapsed;
                    double eta = (total_segments - segments_completed) / segments_per_sec;
                    
                    printf("Progress: %6.2f%% | Segments: %4ld/%ld | Elapsed: %6.1fs | ETA: %6.1fs | Range: %ld - %ld\n",
                           progress, segments_completed, total_segments, elapsed, eta, low, high);
                }
                
                // Print milestones (every billion)
                if (high >= 1000000000 && (high - segment_size) < 1000000000) {
                    printf("★ MILESTONE: Reached 1 billion!\n");
                }
                if (high >= 2000000000 && (high - segment_size) < 2000000000) {
                    printf("★ MILESTONE: Reached 2 billion!\n");
                }
                if (high >= 3000000000 && (high - segment_size) < 3000000000) {
                    printf("★ MILESTONE: Reached 3 billion!\n");
                }
                if (high >= 4000000000 && (high - segment_size) < 4000000000) {
                    printf("★ MILESTONE: Reached 4 billion!\n");
                }
                if (high >= 5000000000 && (high - segment_size) < 5000000000) {
                    printf("★ MILESTONE: Reached 5 billion!\n");
                }
                if (high >= 6000000000 && (high - segment_size) < 6000000000) {
                    printf("★ MILESTONE: Reached 6 billion!\n");
                }
                if (high >= 7000000000 && (high - segment_size) < 7000000000) {
                    printf("★ MILESTONE: Reached 7 billion!\n");
                }
                if (high >= 8000000000 && (high - segment_size) < 8000000000) {
                    printf("★ MILESTONE: Reached 8 billion!\n");
                }
                if (high >= 9000000000 && (high - segment_size) < 9000000000) {
                    printf("★ MILESTONE: Reached 9 billion!\n");
                }
                if (high >= 10000000000 && (high - segment_size) < 10000000000) {
                    printf("★ MILESTONE: Reached 10 billion!\n");
                }
            }
        }
        
        #pragma omp critical
        {
            if (local_highest > highest_prime) {
                highest_prime = local_highest;
            }
        }
        
        free(segment);
    }
    
    double end = omp_get_wtime();
    printf("\n======================================\n");
    printf("COMPLETED!\n");
    printf("Time taken to find all primes up to %ld: %.2f seconds\n", n, end - start);
    printf("Highest prime number up to %ld is: %ld\n", n, highest_prime);

    free(primes);
    return 0;

}
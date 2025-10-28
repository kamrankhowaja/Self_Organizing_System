import numpy as np
import time
from multiprocessing import Pool, cpu_count
import math
import sys

def sieve_small_primes(limit):
    """Find all primes up to limit using simple sieve"""
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    
    for p in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[p]:
            is_prime[p*p::p] = False
    
    return np.where(is_prime)[0]

def sieve_segment(args):
    """Sieve a single segment"""
    seg_idx, segment_size, n, primes = args
    
    low = seg_idx * segment_size
    high = min(low + segment_size - 1, n)
    seg_length = high - low + 1
    
    # Initialize segment
    segment = np.ones(seg_length, dtype=bool)
    
    # Sieve this segment
    for p in primes:
        # Find first multiple of p in [low, high]
        start = (low // p) * p
        if start < low:
            start += p
        if start == p:
            start += p  # Don't mark p itself
        if start < 2:
            start = 2 * p
        
        # Mark multiples as composite
        for j in range(start, high + 1, p):
            segment[j - low] = False
    
    # Find highest prime in this segment
    local_highest = 2
    for i in range(high, max(low - 1, 1), -1):
        if segment[i - low]:
            local_highest = i
            break
    
    return seg_idx, low, high, local_highest

def main():
    n = 10000000000
    
    # Get parameters from command line
    # Usage: python script.py [num_processes] [segment_size_in_millions]
    if len(sys.argv) > 1:
        num_processes = int(sys.argv[1])
    else:
        num_processes = cpu_count()
    
    if len(sys.argv) > 2:
        segment_size = int(sys.argv[2]) * 1000000  # Convert millions to actual number
    else:
        segment_size = 100000000  # Default 100 million
    
    print(f"Configuration:")
    print(f"  Target n: {n:,}")
    print(f"  Segment size: {segment_size:,} ({segment_size//1000000}M)")
    print(f"  Available CPU cores: {cpu_count()}")
    print(f"  Using processes: {num_processes}")
    
    # Calculate total segments
    total_segments = (n + segment_size - 1) // segment_size
    print(f"  Total segments: {total_segments}")
    print()
    
    start_time = time.time()
    
    print(f"Starting Sieve of Eratosthenes for n = {n:,}")
    print("=" * 70)
    print()
    
    # Phase 1: Find small primes
    print("Phase 1: Finding small primes up to sqrt(n)...")
    limit = 100000  # sqrt(10^10) ≈ 100000
    primes = sieve_small_primes(limit)
    prime_count = len(primes)
    
    phase1_time = time.time() - start_time
    print(f"✓ Found {prime_count:,} small primes in {phase1_time:.2f}s\n")
    
    print(f"Phase 2: Processing {total_segments} segments in parallel...")
    print("=" * 70)
    print()
    
    # Prepare arguments for parallel processing
    args_list = [(seg_idx, segment_size, n, primes) for seg_idx in range(total_segments)]
    
    # Process segments in parallel
    highest_prime = 2
    segments_completed = 0
    milestone_printed = set()
    
    # Adjust progress reporting frequency based on number of segments
    report_frequency = max(1, total_segments // 100)  # Report at most 100 times
    
    phase2_start = time.time()
    
    with Pool(processes=num_processes) as pool:
        for result in pool.imap_unordered(sieve_segment, args_list, chunksize=1):
            seg_idx, low, high, local_highest = result
            
            if local_highest > highest_prime:
                highest_prime = local_highest
            
            segments_completed += 1
            progress = (100.0 * segments_completed) / total_segments
            
            # Print progress
            if segments_completed % report_frequency == 0 or segments_completed == total_segments:
                elapsed = time.time() - phase2_start
                segments_per_sec = segments_completed / elapsed if elapsed > 0 else 0
                eta = (total_segments - segments_completed) / segments_per_sec if segments_per_sec > 0 else 0
                
                print(f"Progress: {progress:6.2f}% | Segments: {segments_completed:4d}/{total_segments} | "
                      f"Speed: {segments_per_sec:5.1f} seg/s | Elapsed: {elapsed:6.1f}s | ETA: {eta:6.1f}s")
            
            # Print milestones (every billion)
            milestones = [
                (1000000000, "1 billion"),
                (2000000000, "2 billion"),
                (3000000000, "3 billion"),
                (4000000000, "4 billion"),
                (5000000000, "5 billion"),
                (6000000000, "6 billion"),
                (7000000000, "7 billion"),
                (8000000000, "8 billion"),
                (9000000000, "9 billion"),
                (10000000000, "10 billion")
            ]
            
            for milestone_value, milestone_name in milestones:
                if high >= milestone_value and (high - segment_size) < milestone_value:
                    if milestone_value not in milestone_printed:
                        print(f"  ★ MILESTONE: Reached {milestone_name}!")
                        milestone_printed.add(milestone_value)
    
    end_time = time.time()
    total_time = end_time - start_time
    phase2_time = end_time - phase2_start
    
    print()
    print("=" * 70)
    print("COMPLETED!")
    print(f"Phase 1 (small primes): {phase1_time:.2f}s")
    print(f"Phase 2 (segmented sieve): {phase2_time:.2f}s")
    print(f"Total time: {total_time:.2f}s")
    print(f"Average speed: {segments_completed/phase2_time:.2f} segments/second")
    print(f"Highest prime number up to {n:,} is: {highest_prime:,}")
    print("=" * 70)

if __name__ == "__main__":
    print("Usage: python sieve.py [num_processes] [segment_size_in_millions]")
    print("Example: python sieve.py 16 50  # Use 16 processes, 50M segment size")
    print()
    main()
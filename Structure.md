# Multi-Core Hash Cracker

An optimized, memory-safe offline hash recovery tool written in Python. This tool implements parallel processing across multiple CPU cores to execute fast, high-performance dictionary and brute-force (mask) attacks without exhausting system memory.

---

## Features

* **True Multi-Core Concurrency:** Bypasses Python’s Global Interpreter Lock (GIL) using `ProcessPoolExecutor` to scale performance across all available CPU threads.
* **Constant Memory Footprint (O(1) RAM):** Uses lazy generators to process files stream-by-stream. Whether parsing a 50MB file or a 100GB data dump, RAM usage remains low and stable.
* **Adaptive Inter-Process Communication:** Bundles candidates into adjustable token batches (default: 25,000) to balance worker workload and minimize CPU overhead.
* **Queue Backpressure Management:** Dynamically throttles job submission once the worker queue fills up, preventing memory overflow.
* **Instant Early-Exit:** Safely drops background worker processes and cancels pending queues the exact millisecond a match is found.
* **Corrupted-Byte Tolerant:** Bypasses legacy or malformed binary encodings frequently hidden within public leak wordlists.

---

##  Supported Hashing Algorithms

The script natively wraps Python's standard cryptographic `hashlib` bindings:
* **MD5** / **SHA-1**
* **SHA-2 Family:** SHA-224, SHA-256, SHA-384, SHA-512
* **SHA-3 Family:** SHA3-224, SHA3-256, SHA3-384, SHA3-512

---

## Architecture Pipeline



[ Data Source ] --------> [ Pipeline Buffer ] -------> [ Queue Manager ] -------> [ Worker Pool ]
stream_wordlist()         batch_generator()          Capped Futures            check_batch() on Core 0
OR                   (Groups items              (Prevents RAM              check_batch() on Core 1
generate_combinations()      by 25,000)                overflow)                check_batch() on Core 2
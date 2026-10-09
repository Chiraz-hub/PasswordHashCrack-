import argparse
import hashlib
import itertools
import os
import string
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Generator, Iterable, Optional

SUPPORTED_HASHES = {
    'md5', 'sha1', 'sha224', 'sha256', 'sha384',
    'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512', 'sha512'
}

def check_batch(candidates: list[str], target_hash: str, hash_type: str) -> Optional[str]:
    hash_fn = getattr(hashlib, hash_type)
    for candidate in candidates:
        if hash_fn(candidate.encode('utf-8')).hexdigest() == target_hash:
            return candidate
    return None

def batch_generator(iterable: Iterable[str], batch_size: int = 20000) -> Generator[list[str], None, None]:
    iterator = iter(iterable)
    while True:
        batch = list(itertools.islice(iterator, batch_size))
        if not batch:
            break
        yield batch

def stream_wordlist(file_path: str) -> Generator[str, None, None]:
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            yield line.strip()

def generate_combinations(min_length: int, max_length: int, characters: str) -> Generator[str, None, None]:
    for length in range(min_length, max_length + 1):
        for pwd in itertools.product(characters, repeat=length):
            yield ''.join(pwd)

def crack_hash(
    target_hash: str,
    wordlist: Optional[str] = None,
    hash_type: str = 'md5',
    min_length: int = 1,
    max_length: int = 4,
    characters: str = string.ascii_letters + string.digits,
    max_workers: int = os.cpu_count() or 4,
    batch_size: int = 20000
) -> Optional[str]:
    
    if hash_type not in SUPPORTED_HASHES:
        raise ValueError(f"[!] Unsupported hash type '{hash_type}'. Supported: {sorted(SUPPORTED_HASHES)}")

    target_hash = target_hash.lower().strip()

    if wordlist:
        print(f"[*] Mode: Wordlist attack using file '{wordlist}' ({hash_type.upper()})")
        candidates = stream_wordlist(wordlist)
    elif min_length > 0 and max_length >= min_length:
        total_combos = sum(len(characters) ** l for l in range(min_length, max_length + 1))
        print(f"[*] Mode: Brute-force ({min_length}-{max_length} chars, {total_combos:,} possibilities, {hash_type.upper()})")
        candidates = generate_combinations(min_length, max_length, characters)
    else:
        raise ValueError("[!] You must provide either a valid --wordlist or valid --min_length / --max_length bounds.")

    
    print(f"[*] Utilizing {max_workers} worker processes...")
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = set()
        
        for batch in batch_generator(candidates, batch_size=batch_size):
            
            if len(futures) >= max_workers * 2:
                
                done, futures = wait_for_any(futures)
                for future in done:
                    result = future.result()
                    if result:
                        executor.shutdown(wait=False, cancel_futures=True)
                        return result

            futures.add(executor.submit(check_batch, batch, target_hash, hash_type))

        
        for future in as_completed(futures):
            result = future.result()
            if result:
                return result

    return None

def wait_for_any(futures: set):
    """Utility helper to process tasks without blocking main generation loop."""
    from concurrent.futures import wait, FIRST_COMPLETED
    done, not_done = wait(futures, return_when=FIRST_COMPLETED)
    return done, not_done

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Optimized Multiprocessing Hash Cracker')
    parser.add_argument('hash', help='The target hash to attempt to recover.')
    parser.add_argument('-w', '--wordlist', help='Path to dictionary wordlist file.')
    parser.add_argument('--hash_type', default='md5', choices=sorted(SUPPORTED_HASHES), help='Hashing algorithm used (default: md5).')
    parser.add_argument('--min_length', type=int, default=1, help='Minimum password length for brute-force generation.')
    parser.add_argument('--max_length', type=int, default=4, help='Maximum password length for brute-force generation.')
    parser.add_argument('-c', '--characters', default=string.ascii_letters + string.digits, help='Charset for brute-force generation.')
    parser.add_argument('--max_workers', type=int, default=os.cpu_count() or 4, help='Number of process workers.')
    parser.add_argument('--batch_size', type=int, default=25000, help='Number of passwords per batch submission.')

    args = parser.parse_args()

    found = crack_hash(
        target_hash=args.hash,
        wordlist=args.wordlist,
        hash_type=args.hash_type,
        min_length=args.min_length,
        max_length=args.max_length,
        characters=args.characters,
        max_workers=args.max_workers,
        batch_size=args.batch_size
    )

    if found:
        print(f"\n[+] Match Found: {found}")
    else:
        print("\n[!] Exceeded candidates search space without finding a match.")
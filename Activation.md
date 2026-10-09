---

### Prerequisites
* Python 3.8+ (Uses native standard libraries; **no external pip installations required**).

### Installation
1. Clone or download this project workspace.
2. Save the source code file as `cracker.py`.

---

## Usage Examples

Run the script from your terminal using standard options and flags.

### 1. Dictionary / Wordlist Attack
Target a SHA-256 hash using an explicit password reference list (e.g., `rockyou.txt`):
```bash
python cracker.py 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824 -w rockyou.txt --hash_type sha256
```

### 2. Brute-Force Matrix Attack
Calculate every possible algebraic string permutation up to 5 characters using lowercase letters, uppercase letters, and numerical digits:
```bash
python cracker.py 5d41402abc4b2a76b9719d911017c592 --hash_type md5 --min_length 1 --max_length 5
```

### 3. Customized Character Boundary
Restrict brute-force generation explicitly to numbers (PIN recovery) between 4 and 6 characters long:
```bash
python cracker.py 7c4a8d09ca3762af61e59520943dc26494f8941b --hash_type sha1 --min_length 4 --max_length 6 -c "0123456789"
```

---

## Command Line Options

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `hash` | String | *Required* | The target cryptographic hexadecimal string to recover. |
| `-w`, `--wordlist` | String | `None` | File path to your target dictionary text file. |
| `--hash_type` | String | `md5` | Hashing algorithm matching the target string. |
| `--min_length` | Integer | `1` | Minimum string length for programmatic brute-force generation. |
| `--max_length` | Integer | `4` | Maximum string length for programmatic brute-force generation. |
| `-c`, `--characters`| String | `a-zA-Z0-9` | Custom character set used during brute-force matrix rendering. |
| `--max_workers` | Integer | Max Cores | Total discrete processing threads deployed simultaneously. |
| `--batch_size` | Integer | `25000` | Total string candidates packaged together inside individual worker tasks. |

---

## Ethical Use Policy !!!

This tool is designed purely for **educational research, legitimate penetration testing benchmarks, and administrative credential audits**. 

Do not attempt to audit or recover credentials belonging to environments, applications, or systems for which you do not possess express, written verification of ownership or explicit security assessment authorization. 
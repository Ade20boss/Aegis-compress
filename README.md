# Aegis Huffman Implementation

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Status](https://img.shields.io/badge/Status-Active-green?style=flat-square)

A robust, pure Python implementation of the **Huffman Coding algorithm**. This project provides a set of modular functions to analyze text frequency, construct hierarchical trees, and generate optimized binary codes for lossless data compression.

## ⚡ Features

* **Frequency Analysis:** Efficiently counts unique character occurrences to determine weights.
* **Bottom-Up Tree Construction:** Iteratively combines the two smallest nodes to build a hierarchical structure.
* **Weighted Bit Assignment:** A custom logic that assigns binary bits ('0' or '1') based on branch weight (heavier branches receive '1').
* **Modular Design:** Each step of the algorithm (counting, tree building, sorting, encoding) is separated into distinct, reusable functions.
* **Edge Case Handling:** Includes safeguards for strings with low character variance (e.g., "aaaa").

## 🚀 Getting Started

### Prerequisites
* Python 3.6 or higher.

### Installation
1.  Clone the repository:
    ```bash
    git clone https://github.com/Ade20boss/Aegis-compress.git
    ```
2.  Navigate to the directory:
    ```bash
    cd Aegis-compress
    ```

## 💻 Usage

You can use the `display_code` function to get the final binary string for any input text.

```python
from huffman_encoding import display_code, generate_code

text = "hello world"

# 1. Generate the binary mapping dictionary
mapping = generate_code(text)
print(f"Mapping: {mapping}")
# Output: {'l': '11', 'o': '01', 'e': '000', ...}

# 2. Get the full encoded binary string
binary_string = display_code(text)
print(f"Encoded: {binary_string}")
```

---

⚙️ How It Works
The algorithm proceeds in four distinct stages:

- count_characters: Scans the input string to create a frequency map (e.g., {'a': 5, 'b': 2}).

- huffman_tree: Uses a priority-queue approach to merge the two least frequent nodes into a parent node until a single root remains.

- assign_pos: Traverses the sorted tree. It compares sibling nodes and assigns:

- 1 to the heavier (higher frequency) branch.

- 0 to the lighter (lower frequency) branch.

- generate_code: Walks from the leaf node to the root to compile the final binary sequence for each character.

---

🛡️ Credits
Created: "Forged in aegis"
Author: Adeoluwa Daniel Ademoye



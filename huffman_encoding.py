__created__ = "Forged in aegis"


# Function to assign frequencies to unique letters
def count_characters(text):
    """
    Counts the occurrences of each character in the given string and returns
    a dictionary with characters as keys and their counts as values.
    """
    count_dict = {}
    for i in text:
        # specific optimization: Check if char is already counted to avoid redundant processing
        if i in count_dict:
            continue
        # Count occurrences of the character in the entire string
        count_dict[i] = text.count(i)
    return count_dict


def huffman_tree(p_string):
    """
    Generates a Huffman tree from a given string by calculating character frequencies
    and iteratively combining the two smallest nodes until a single root node remains.
    The resulting structure represents steps used in Huffman coding creation.

    :param p_string: The input string from which the Huffman tree is generated.
    :type p_string: str
    :returns: A list of dictionaries representing the hierarchical structure of the
        Huffman tree, where each dictionary represents a parent node and its
        two child nodes. If the input string contains less than two unique characters,
        their frequency dictionary is directly returned.
    :rtype: list[dict] | dict
    """
    # Step 1: Get initial frequency counts
    binary_dict = count_characters(p_string)
    nodes = []

    # Edge case: If string has less than 2 unique characters, no tree needed
    if len(binary_dict) < 2:
        return binary_dict

    id = 0
    # Step 2: Loop until all nodes are combined into a single root node
    while True:
        values = binary_dict.values()

        # --- Find the 1st smallest node ---
        first_min = min(values)
        # Identify the key for the smallest value
        for k, v in binary_dict.items():
            if v == first_min:
                key_to_remove = k
        # Remove it from the pool so we can find the next smallest
        del binary_dict[key_to_remove]
        first_node = (key_to_remove, first_min)

        # --- Find the 2nd smallest node ---
        second_min = min(values)
        # Generator expression to find key for second smallest value
        key_to_remove1 = next((k for k, v in binary_dict.items() if v == second_min), None)
        del binary_dict[key_to_remove1]
        second_node = (key_to_remove1, second_min)

        # --- Create Parent Node ---
        # Combine the two smallest nodes. Key format: ("parentID", sum_of_weights)
        parent_node = {(f"parent{id}", first_min + second_min): (first_node, second_node)}

        # Add the new parent back into the dictionary for the next iteration
        binary_dict[f"parent{id}"] = first_min + second_min

        # Store the structural step
        nodes.append(parent_node)
        id += 1

        # Break when only one node (the root) remains in the dictionary
        if len(binary_dict) == 1:
            break
    return nodes


def sort_tree(custom_string):
    """
    Sorts the given Huffman tree to ensure nodes are arranged based on frequency.

    The function takes a string input to generate a Huffman Tree and iterates through
    each step of the tree-building process. During traversal, it ensures that the
    child nodes for each parent node are sorted by frequency. This guarantees that
    smaller frequencies are consistently positioned, aiding the proper structure
    of the tree.

    :param custom_string: The input string used for constructing the Huffman tree.
    :type custom_string: str
    :return: A sorted Huffman tree based on node frequencies.
    :rtype: list
    """
    tree = huffman_tree(custom_string)

    # Return immediately if tree is too small to sort
    if len(tree) < 2:
        return tree

    # Iterate through every node/step in the tree construction
    for dictionary in tree:
        key = next(iter(dictionary))  # Get the parent key

        # Sort the children (tuple of nodes) by their frequency (index 1)
        # This ensures smaller frequency is consistently on the left or right
        values_to_sort = sorted(dictionary[key], key=lambda x: x[1])
        dictionary[key] = values_to_sort
    return tree


def assign_pos(user_string):
    """
    Processes a tree structure derived from a string, assigns binary positional
    values to its nodes based on branch weight, and returns the updated tree.
    The function sorts the tree and assigns bits ("0" or "1") to indicate the
    relative weight ('heavier' or 'lighter') of its branches. This operation
    ensures nodes in more significant (heavier) branches are marked appropriately.

    :param user_string: Input string to generate and process a tree structure
    :type user_string: str
    :return: A tree structure with binary positional values assigned to branches
    :rtype: list
    """
    tree = sort_tree(user_string)
    if len(tree) < 2:
        return tree

    # Iterate through sorted nodes to assign binary bits
    for dictionary in tree:
        key = list(dictionary.keys())[0]

        # Determine which child has the larger frequency
        largest = max([dictionary[key][0][1], dictionary[key][1][1]])

        # Convert tuples to lists to make them mutable (so we can append "0" or "1")
        dictionary[key][0] = list(dictionary[key][0])
        dictionary[key][1] = list(dictionary[key][1])

        # Logic: Assign '1' to the heavier (larger) branch, '0' to the lighter branch
        if largest in dictionary[key][0]:
            dictionary[key][0].append("1")
            dictionary[key][1].append("0")
        elif largest in dictionary[key][1]:
            dictionary[key][1].append("1")
            dictionary[key][0].append("0")
    return tree


def find_node_in_tree(node, tree):
    """
    Searches for the given node within a hierarchical tree structure and returns
    the matching dictionary if found.

    This function iterates over a list of dictionary structures, where each
    dictionary contains a single key-value pair. The key is expected to be a
    tuple, with the target node name as its first element. The function stops
    and returns the matching dictionary when the node name matches the target.

    :param node: The target node to search for within the tree.
    :type node: Any
    :param tree: The hierarchical structure containing a list of dictionaries
                 to search in.
    :type tree: list[dict]
    :return: The dictionary containing the target node, or None if not found.
    :rtype: dict | None
    """
    for dictionary in tree:
        key = list(dictionary.keys())[0]
        # Check if the first element of the key tuple (the name) matches the target
        if key[0] == node:
            return dictionary


def generate_code(word):
    """
    Generates a dictionary of binary codes for each unique character in the given
    input string by traversing a pre-constructed tree of binary assignments.
    This function assumes the existence of support functionality like tree construction
    and node traversal methods.

    :param word: A string input for which unique characters' binary codes are to
        be generated
    :type word: str
    :return: A dictionary where keys are unique characters from the input string,
        and values are their corresponding binary codes as strings
    :rtype: dict
    """
    # Get the tree with assigned 0s and 1s
    tree = assign_pos(word)

    codes = {}
    chars = set(word)  # Get unique characters to generate codes for

    for ch in chars:
        code_bits = ""
        # Start traversal from the Root (the last element added to the nodes list)
        current_node = tree[-1]

        while True:
            key = list(current_node.keys())[0]
            left, right = current_node[key]

            # --- Check Left Child ---
            # If left child is the character we are looking for
            if ch == left[0]:
                code_bits += left[2]  # Append the bit (0 or 1)
                break

            # --- Check Right Child ---
            # If right child is the character we are looking for
            if ch == right[0]:
                code_bits += right[2]  # Append the bit (0 or 1)
                break

            # --- Traverse Deeper ---
            # If the left child is a 'parent' node, follow it down
            if left[0].startswith("parent"):
                code_bits += left[2]  # Append path bit
                current_node = find_node_in_tree(left[0], tree)  # Move current context to that node
                continue

            # If the right child is a 'parent' node, follow it down
            if right[0].startswith("parent"):
                code_bits += right[2]  # Append path bit
                current_node = find_node_in_tree(right[0], tree)  # Move current context to that node
                continue

            break  # Safety break if path is lost

        codes[ch] = code_bits

    return codes


def find_indexes(word, letter):
    """
    Find all index positions of a specific letter in a given string.

    This function iterates through each character of the input string and checks
    if it matches the specified letter. If a match is found, the index of the
    character is added to a list, which is then returned.

    :param word: The string in which to search for the letter.
    :type word: str
    :param letter: The character to locate within the string.
    :type letter: str
    :return: A list of indices indicating the positions of the letter in the string.
    :rtype: list[int]
    """
    # Find all index positions of a specific letter in the string
    indexes = []
    for i in range(len(word)):
        if word[i] == letter:
            indexes.append(i)
    return indexes


def find_indexes_of_letters(word):
    """
    Finds the indexes of each letter in the given word.

    This function maps every unique letter in the given word to a list
    of its positions within the word. It leverages helper functions
    like `count_characters` to identify unique letters and
    `find_indexes` to determine their positions.

    :param word: The word for which letter indexes are to be found.
    :type word: str
    :return: A dictionary mapping each unique letter in the word to
             a list of its positions.
    :rtype: dict
    """
    # Map every unique letter to a list of its positions in the original string
    indexes_of_words = {}
    letters = list(count_characters(word).keys())
    for letter in letters:
        pos = find_indexes(word, letter)
        indexes_of_words[letter] = pos
    return indexes_of_words


def display_code(word):
    """
    Generates a binary code representation for a given word by mapping
    each unique character to a binary sequence and constructing the
    final encoded string.

    :param word: The input string to be processed.
    :type word: str
    :return: A binary code string that represents the input word. If the input string
        contains fewer than two unique characters, a dictionary mapping each character
        to their corresponding binary codes is returned instead.
    :rtype: str or dict
    """
    # Step 1: Generate the binary dictionary (e.g., {'a': '01', 'b': '11'})
    code_dict = generate_code(word)

    # Edge case check
    if len(code_dict) < 2:
        return code_dict

    # Step 2: Get positions of all characters
    indices = find_indexes_of_letters(word)

    # Step 3: Construct the final binary string
    code = []
    for letter in code_dict.keys():
        # Insert the binary code into the correct list positions
        for l in indices:
            if letter == l:
                for pos in indices[l]:
                    code.insert(pos, code_dict[letter])

    # Join list into a single string
    return "".join(code)

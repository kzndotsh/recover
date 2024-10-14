from mnemonic import Mnemonic
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

# Initialize the Mnemonic class for using BIP39 methods
mnemo = Mnemonic("english")

# Retrieve the BIP39 word list
bip39_wordlist = mnemo.wordlist

# CHANGE ME:
# Known parts of the seed phrase with placeholders for unknown words
known_phrase = [
    "XXX", "XXX", "XXX", "XXX", "XXX", "XXX", "XXX", "XXX",
    "XXX", "?", "XXX", "XXX", "XXX", "?", "XXX", "XXX",
    "XXX", "XXX", "XXX", "XXX", "?", "XXX", "XXX", "?"
]

# CHANGE ME:
# Indices of the unknown words in the phrase
unknown_indices = [20, 23, ...]

# File to store valid seed phrases
output_file = "valid_seed_phrases.txt"

def check_phrase(possible_word):
    """Check combinations of specific words and return valid seed phrases."""
    valid_phrases = []
    count = 0
    for word2 in bip39_wordlist:
        candidate = known_phrase[:]
        candidate[unknown_indices[0]] = possible_word
        candidate[unknown_indices[1]] = word2
        seed_phrase = " ".join(candidate)
        count += 1
        if mnemo.check(seed_phrase):
            valid_phrases.append(seed_phrase)
    return valid_phrases, count

def find_missing_words(wordlist):
    total_count = 0
    with open(output_file, "w") as f:
        with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            # Run `check_phrase` for each word in the BIP39 list
            results = executor.map(check_phrase, wordlist)
            for valid_phrases, count in results:
                total_count += count
                for phrase in valid_phrases:
                    f.write(f"{phrase}\n")
    print(f"Total number of combinations attempted: {total_count}")

# Execute the function to search for valid seed phrases
find_missing_words(bip39_wordlist)

print(f"Valid seed phrases have been logged to {output_file}")

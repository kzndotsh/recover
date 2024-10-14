from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes

# CHANGE ME:
target_address = "0x0000000000000000000000000000000000000000"

def derive_eth_address_from_seed(seed_phrase, index):
    """ Derive Ethereum address from seed phrase at the specified index. """
    # Generate the seed from the BIP39 mnemonic phrase
    seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()

    # Initialize BIP44 for Ethereum (ETH)
    bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
    
    # Navigate the HD wallet path to derive the desired index address
    # Use Bip44Changes.CHAIN_EXT for "external" or Bip44Changes.CHAIN_INT for "internal" chain
    bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(index)

    # Obtain and return the Ethereum address from the derived public key
    eth_address = bip44_acc.PublicKey().ToAddress()

    return eth_address

def check_wallet(valid_seed_phrases_file):
    with open(valid_seed_phrases_file, "r") as f:
        phrases = f.readlines()

    for phrase in phrases:
        phrase = phrase.strip()
        # Iterate over indices (e.g., first five addresses) to see if any match
        for i in range(5):  # Adjust the range for a thorough search if needed
            derived_address = derive_eth_address_from_seed(phrase, i)
            print(f"Checking: {derived_address}")
            if derived_address.lower() == target_address.lower():
                print(f"Match found! Seed phrase: {phrase}")
                return 

check_wallet("valid_seed_phrases.txt")

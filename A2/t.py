import functools
from hashlib import sha256

print(sha256(f"{'1'}-{'value'}".encode()).hexdigest())
for char in sha256(f"{'1'}-{'value'}".encode()).hexdigest():
    print(char)
print(bin(6).replace('0b','')[::-1].find('1'))
def create_hash_functions(num_hash_functions, size_bit_array):
    """Create a list of runnable hash functions.
    It is important to use lambda functions to create the hash functions.

    Args:
        num_hash_functions (int): The number of hash functions to create.
        size_bit_array (int): The size of the bit array.

    Returns:
        list[function]: A list containing the hash functions.
    """
    # Generate a list of hash functions
    hash_functions = []
    for i in range(num_hash_functions):
        # Create a lambda function that hashes the input
        # using SHA-256 and a unique seed

        # Create the hash function
        hash_function = lambda value, seed=i: (lambda ret: (size_bit_array - 1) & ret)(
            functools.reduce(
                lambda acc, char: seed * acc + ord(char),
                sha256(value.encode()).hexdigest(),  # SHA-256 hash
                0
            )
        )
        
        hash_functions.append(hash_function)
    
    return hash_functions

# Example usage
if __name__ == "__main__":
    num_hashes = 4
    size = 100

    hash_funcs = create_hash_functions(num_hashes, size)

    # Test the hash functions
    sample_string = "test_string"
    for index, func in enumerate(hash_funcs):
        print(f"Hash value for '{sample_string}' using hash function {index}: {func(sample_string)}")

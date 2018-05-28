# take two equal-length buffers and produce their XOR combination


def fixed_xor(string, mask):
	decoded_string = bytes.fromhex(string)
	decoded_mask = bytes.fromhex(mask)
	return bytes([a ^ b for a, b in zip(decoded_string, decoded_mask)]).hex()


example_string = '1c0111001f010100061a024b53535009181c'
example_mask = '686974207468652062756c6c277320657965'
result = fixed_xor(example_string, example_mask)
print(result) # expected: 746865206b696420646f6e277420706c6179
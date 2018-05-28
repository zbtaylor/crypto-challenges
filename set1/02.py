# take two equal-length buffers and produces their XOR combination


def hex_to_bytes(s):
  return bytes.fromhex(s)


def fixed_xor(string, mask):
	decoded_string = hex_to_bytes(string)
	decoded_mask = hex_to_bytes(mask)
	return bytes([a ^ b for a, b in zip(decoded_string, decoded_mask)]).hex()


example_string = '1c0111001f010100061a024b53535009181c'
example_mask = '686974207468652062756c6c277320657965'

result = fixed_xor(example_string, example_mask)
print(result) # expected: 746865206b696420646f6e277420706c6179

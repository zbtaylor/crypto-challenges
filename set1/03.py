# find the single character key this string was XOR'ed against


import string

CHAR_FREQUENCIES_EN = {
	'a': 0.08167,
	'b': 0.01492,
	'c': 0.02782,
	'd': 0.04253,
	'e': 0.12702,
	'f': 0.02228,
	'g': 0.02015,
	'h': 0.06094,
	'i': 0.06966,
	'j': 0.00153,
	'k': 0.00772,
	'l': 0.04025,
	'm': 0.02406,
	'n': 0.06749,
	'o': 0.07507,
	'p': 0.01929,
	'q': 0.00095,
	'r': 0.05987,
	's': 0.06327,
	't': 0.09056,
	'u': 0.02758,
	'v': 0.00978,
	'w': 0.02360,
	'x': 0.00150,
	'y': 0.01974,
	'z': 0.00074
}


def single_byte_xor(string, key):
	return bytes([a ^ ord(key) for a in bytes.fromhex(string)])


def count(result):
	counts = {}

	for c in string.ascii_lowercase:
		counts[c] = 0

	for c in result:
		char = chr(c).lower()
		if char.isalpha():
			counts[char] += 1

	for i in counts:
		counts[i] /= len(result)

	return counts


def compare(count, freq):
	results = []

	for c in string.ascii_lowercase:
		if count[c] != 0:
			remainder = round(count[c] % freq[c], 5)
			results.append(remainder)
		else:
			results.append(0)

	return sum(results) / 26


def decrypt(hex_string):
	options = {}
	results = {}

	for c in string.ascii_letters:
		options[c] = single_byte_xor(hex_string, c)
		char_count = count(options[c])
		score = compare(char_count, CHAR_FREQUENCIES_EN)
		if score > 0.013:
			results[c] = options[c]

	return results


example_hex = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
results = decrypt(example_hex)

print(results)
import base64
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


def hex_to_base64(s):
	return base64.b64encode(bytes.fromhex(s))


def fixed_xor(string, mask):
	b_string = bytes.fromhex(string)
	b_mask = bytes.fromhex(mask)
	return bytes([a ^ b for a, b in zip(b_string, b_mask)]).hex()


def single_xor(string, key):
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
		options[c] = single_xor(hex_string, c)
		char_count = count(options[c])
		score = compare(char_count, CHAR_FREQUENCIES_EN)
		if score > 0.013:
			results[c] = options[c]

	return results

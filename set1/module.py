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


def hex_to_base64(hexstr):
	return base64.b64encode(bytes.fromhex(hexstr))


def fixed_xor(hexstr, hexmask):
	b_string = bytes.fromhex(hexstr)
	b_mask = bytes.fromhex(hexmask)
	return bytes([a ^ b for a, b in zip(b_string, b_mask)])


def single_xor(hexstr, key):
	return bytes([a ^ ord(key) for a in bytes.fromhex(hexstr)])


def score_string(bstring, freqs):
	count = {}
	for c in string.ascii_letters:
		count[c] = 0

	for c in bstring:
		char = chr(c).lower()
		if char in string.ascii_letters:
			count[char] += 1

	return sum([count[a] % freqs[b] for a, b in zip(count, freqs)])

def decrypt(hex_string):
	result = b''
	old_score = 0
	for c in string.ascii_letters:
		out = single_xor(hex_string, c)
		score = score_string(out, CHAR_FREQUENCIES_EN)
		if score > old_score:
			old_score = score
			result = out

	return result

import base64
import string

CHAR_FREQUENCIES_EN = {
	'a': 0.0834,
	'b': 0.0154,
	'c': 0.0273,
	'd': 0.0414,
	'e': 0.1260,
	'f': 0.0203,
	'g': 0.0192,
	'h': 0.0611,
	'i': 0.0671,
	'j': 0.0023,
	'k': 0.0087,
	'l': 0.0424,
	'm': 0.0253,
	'n': 0.0680,
	'o': 0.0770,
	'p': 0.0166,
	'q': 0.0009,
	'r': 0.0568,
	's': 0.0611,
	't': 0.0937,
	'u': 0.0285,
	'v': 0.0106,
	'w': 0.0234,
	'x': 0.0020,
	'y': 0.0204,
	'z': 0.0006
}

def hex_to_base64(hexstr):
	return base64.b64encode(bytes.fromhex(hexstr))


def fixed_xor(hexstr, hexmask):
	b_string = bytes.fromhex(hexstr)
	b_mask = bytes.fromhex(hexmask)
	return bytes([a ^ b for a, b in zip(b_string, b_mask)])


def single_char_xor(hexstr, key):
	return bytes([a ^ ord(key) for a in bytes.fromhex(hexstr)])


def score_string(bstring, freqs):
	score = 0
	count = 0
	for c in bstring:
			char = chr(c).lower()
			if char in freqs:
					score += freqs[char]
					count += 1
			else:
				count += 1
	return score


def find_single_key(hex_string):
	result = b''
	old_score = 0
	for c in string.ascii_letters:
		out = single_char_xor(hex_string, c)
		score = score_string(out, CHAR_FREQUENCIES_EN)
		if score > old_score:
			old_score = score
			result = out
	return result

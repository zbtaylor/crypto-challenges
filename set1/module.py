import base64
import string

CHAR_FREQUENCIES_EN = {
	'e': 0.1249,
	't': 0.0928,
	'a': 0.0804,
	'o': 0.0764,
	'i': 0.0757,
	'n': 0.0723,
	's': 0.0651,
	'r': 0.0628,
	'h': 0.0505,
	'l': 0.0407,
	'd': 0.0382,
	'c': 0.0334,
	'u': 0.0273,
	'm': 0.0251,
	'f': 0.0240,
	'p': 0.0214,
	'g': 0.0187,
	'w': 0.0168,
	'y': 0.0166,
	'b': 0.0148,
	'v': 0.0105,
	'k': 0.0054,
	'x': 0.0023,
	'j': 0.0016,
	'q': 0.0012,
	'z': 0.0009
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
	for c in bstring:
		char = chr(c).lower()
		if char in freqs:
			score += freqs[char]
	# checking for spaces seems to work for now
	if not b' ' in bstring:
		score = 0
	return score


def find_single_key(hex_string):
	result = b''
	old_score = 0
	for c in string.printable:
		out = single_char_xor(hex_string, c)
		score = score_string(out, CHAR_FREQUENCIES_EN)
		if score > old_score:
			old_score = score
			result = out
	return (score, result)


def find_in_list(hexlist):
	result = b''
	old_score = 0
	for l in hexlist:
		if hex_to_base64(l):
			out = find_single_key(l)
			if out[0] > old_score:
				old_score = out[0]
				result = out[1]
	return result


def build_corpus_from_file(file):
	file = open(file)
	result = [line.rstrip('\n') for line in file]
	file.close()
	return result
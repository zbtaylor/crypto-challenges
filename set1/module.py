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

BIGRAM_FREQUENCIES_EN = {
	'th': 0.0356,
	'he': 0.0307,
	'in': 0.0243,
	'er': 0.0205,
	'an': 0.0199,
	're': 0.0185,
	'on': 0.0176,
	'at': 0.0149,
	'en': 0.0145,
	'nd': 0.0135,
	'ti': 0.0134,
	'es': 0.0134,
	'or': 0.0128,
	'te': 0.0120,
	'of': 0.0117,
	'ed': 0.0117,
	'is': 0.0113,
	'it': 0.0112,
	'al': 0.0109,
	'ar': 0.0107,
	'st': 0.0105,
	'to': 0.0104,
	'nt': 0.0104,
	'ng': 0.0095,
	'se': 0.0093,
	'ha': 0.0093,
	'as': 0.0087,
	'ou': 0.0087,
	'io': 0.0083,
	'le': 0.0083,
	've': 0.0083,
	'co': 0.0079,
	'me': 0.0079,
	'de': 0.0076,
	'hi': 0.0076,
	'ri': 0.0073,
	'ro': 0.0073,
	'ic': 0.0070,
	'ne': 0.0069,
	'ea': 0.0069,
	'ra': 0.0069,
	'ce': 0.0065,
	'li': 0.0062,
	'ch': 0.0060,
	'll': 0.0058,
	'be': 0.0058,
	'ma': 0.0057,
	'si': 0.0055,
	'om': 0.0055,
	'ur': 0.0054
}


def hex_to_base64(hexstr):
	return base64.b64encode(bytes.fromhex(hexstr))


def fixed_xor(hexstr, hexmask):
	b_string = bytes.fromhex(hexstr)
	b_mask = bytes.fromhex(hexmask)
	return bytes([a ^ b for a, b in zip(b_string, b_mask)])


def single_char_xor(hexstr, key):
	return bytes([a ^ ord(key) for a in bytes.fromhex(hexstr)])


def score_string_char(bstring, freqs):
	score = 0
	count = 0
	for c in bstring:
		char = chr(c).lower()
		if char in freqs:
			score += freqs[char]
			count += 1
	# weed out some obvious nonsense
	if not b' ' in bstring:
		return 0
	return score * (count / len(bstring))


def score_string_bigram(bstring, freqs):
	score = 0
	bigrams = []
	string = ''
	# decode for easy comparison with frequency chart
	try:
		string = bstring.decode().replace(' ', '')
	except:
		return 0
	for i in range(0, len(string)):
		bigrams.append(string[i:i+2])
	for b in bigrams:
		if b in freqs:
			score += freqs[b]
	return score


def find_single_key(hex_string):
	result = b''
	best_score = 0
	for c in string.printable:
		out = single_char_xor(hex_string, c)
		score = score_string_bigram(out, BIGRAM_FREQUENCIES_EN)
		if score > best_score:
			best_score = score
			result = out
	return (best_score, result)


def find_in_list(hexlist):
	result = b''
	best_score = 0
	for l in hexlist:
		if hex_to_base64(l):
			out = find_single_key(l)
			if out[0] > best_score:
				best_score = out[0]
				result = out[1]
	return result


def build_corpus_from_file(file):
	file = open(file)
	result = [line.rstrip('\n') for line in file]
	file.close()
	return result

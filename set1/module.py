import base64, string

BIGRAM_FREQS = {
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


###############################
# ALWAYS OPERATE ON RAW BYTES #
###############################


def hex_to_base64(hexstr):
	'''Converts hexadecimal to base64.
	
	Args:
	hexstr (str): String of hex digits to be converted.

	Returns:
	bytes: Base64 encoded bytes literal.
	'''
	raw_bytes = bytes.fromhex(hexstr)
	return base64.b64encode(raw_bytes)


def fixed_length_xor(hexstr, hexmask):
	'''XOR two hexadecimal strings of matching length.

	Args:
	hexstr (str): String of hex digits to be encrypted.
	hexmask (str): String of hex digits to XOR against.

	Returns:
	bytes: Hexadecimal encoded bytes literal.
	'''
	bytes1, bytes2 = bytes.fromhex(hexstr), bytes.fromhex(hexmask)
	return bytes([a ^ b for a, b in zip(bytes1, bytes2)])


def single_char_xor(hexstr, key):
	'''XOR a hexadecimal string against a single key.

	Args:
	hexstr (str): String of hex digits to be encrypted.
	key (str): The single character to XOR against.

	Returns:
	bytes: Hexadecimal encoded bytes literal.
	'''
	return bytes([a ^ ord(key) for a in bytes.fromhex(hexstr)])


def repeating_key_xor(string, key):
	'''XOR a string against a repeating key.

	Args:
	string (str): The string to be encrypted.
	key (str): The key to be repeated and XOR'ed against.

	Returns:
	bytearray: A bytearray containing the encrypted bytes.
	'''
	result = bytearray(b'')
	i = 0
	for c in string:
		result.append(ord(c) ^ ord(key[i]))
		if i < len(key) - 1:
			i += 1
		else:
			i = 0
	return result


def score_string(bstring):
	'''Score the likelihood that a string contains English text.
	
	Decodes the bytes literal and then runs through it looking for common English
	bigrams (sequence of two adjacent letters). Add the frequency of a bigram to
	the score every time one is found. Strings with higher scores are more likely
	to be English.

	Args:
	bstring (bytes): Bytes literal to be decoded and scored.

	Returns:
	int: The sum of frequency values for all bigrams found.
	'''
	score = 0
	bigrams = []
	string = ''
	try:
		string = bstring.decode().replace(' ', '')
	except:
		return 0
	for i in range(0, len(string)):
		bigrams.append(string[i:i+2])
	for b in bigrams:
		if b in BIGRAM_FREQS:
			score += BIGRAM_FREQS[b]
	return score


def find_single_key(hexstr):
	'''Finds the best single character XOR key to decrypt a string.

	XORs the given string against every printable character, scores each result,
	and keeps track of the best score. Returns the best result based on simple
	bigram frequency analysis.

	Args:
	hexstr (str): The hex string to XOR.

	Returns:
	(int, bytes): Returns the best score and accompanying result as a tuple.
	'''
	result = b''
	best_score = 0
	for c in string.printable:
		out = single_char_xor(hexstr, c)
		score = score_string(out)
		if score > best_score:
			best_score = score
			result = out
	return (best_score, result)


def find_in_list(hexlist):
	'''Finds the line in a list that has been single character XOR'ed.

	Args:
	hexlist (list): List of hex strings to sift through.

	Return:
	bytes: Bytes literal of the decrypted hex with the highest score.
	'''
	result = b''
	best_score = 0
	for l in hexlist:
		out = find_single_key(l)
		if out[0] > best_score:
			best_score = out[0]
			result = out[1]
	return result


def build_corpus_from_file(filepath):
	'''Takes a text file and appends each line to a list

	Args:
	file (str): Path to text file.

	Returns:
	list: A list containing each line of text as a string.
	'''
	file = open(filepath)
	result = [line.rstrip('\n') for line in file]
	file.close()
	return result


def string_to_bits(string):
	'''Converts a string to it's binary representation.

	Args:
	string (str): The string to convert.

	Returns:
	string: A string containing only ones and zeroes.
	'''
	result = ''
	for c in string:
		bits = bin(ord(c))[2:]
		bits = '00000000'[len(bits):] + bits # makes sure each is a 8 full bits
		result += bits
	return result


def hamming_distance(str1, str2):
	'''Computes the hamming distance between two same-length strings.

	Args:
	str1 (str): First string to compare.
	str2 (str): Second string to compare.

	Returns:
	int: Sum of bits that differ between the two strings.
	'''
	bits1 = string_to_bits(str1)
	bits2 = string_to_bits(str2)
	return sum([ord(a) ^ ord(b) for a, b in zip(bits1, bits2)])

	

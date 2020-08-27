import base64
import string
import binascii


BIGRAM_FREQS = {
    'th': 0.0356, 'he': 0.0307, 'in': 0.0243, 'er': 0.0205, 'an': 0.0199,
    're': 0.0185, 'on': 0.0176, 'at': 0.0149, 'en': 0.0145, 'nd': 0.0135,
    'ti': 0.0134, 'es': 0.0134, 'or': 0.0128, 'te': 0.0120, 'of': 0.0117,
    'ed': 0.0117, 'is': 0.0113, 'it': 0.0112, 'al': 0.0109, 'ar': 0.0107,
    'st': 0.0105, 'to': 0.0104, 'nt': 0.0104, 'ng': 0.0095, 'se': 0.0093,
    'ha': 0.0093, 'as': 0.0087, 'ou': 0.0087, 'io': 0.0083, 'le': 0.0083,
    've': 0.0083, 'co': 0.0079, 'me': 0.0079, 'de': 0.0076, 'hi': 0.0076,
    'ri': 0.0073, 'ro': 0.0073, 'ic': 0.0070, 'ne': 0.0069, 'ea': 0.0069,
    'ra': 0.0069, 'ce': 0.0065, 'li': 0.0062, 'ch': 0.0060, 'll': 0.0058,
    'be': 0.0058, 'ma': 0.0057, 'si': 0.0055, 'om': 0.0055, 'ur': 0.0054
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


def score_string_bigram(bstring):
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
        bigrams.append(string[i:i+2].lower())
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
    (int, bytes, char): Best score, result, and key as a tuple.
    '''
    result = b''
    best_score = 0
    key = ''
    for c in string.printable:
        out = single_char_xor(hexstr, c)
        score = score_string_bigram(out)
        if score > best_score:
            best_score = score
            result = out
            key = c
    return (best_score, result, key)


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


def build_list_from_file(filepath):
    '''Puts each line of a text file in a list, regardless of encoding.

    Args:
    filepath (str): Path to text file.

    Returns:
    list: A list containing each line of text as a string.
    '''
    file = open(filepath)
    result = [line.rstrip('\n') for line in file]
    file.close()
    return result


def build_corpus_from_file_b64(filepath):
    '''Takes a text file containing base64 and creates a corpus of bytes.

    Args: 
    filepath (str): Path to text file.

    Returns:
    bytes: A bytes object containing the contents of the file.
    '''
    file = open(filepath)
    result = b''.join([base64.b64decode(line.rstrip('\n')) for line in file])
    file.close()
    return result


def string_to_bits(string):
    '''Converts a string of text to it's binary representation.

    Args:
    string (str): The string to convert.

    Returns:
    string: A string of binary without the '0b' prefix. E.g. '000101011101001100'
    '''
    binary = ''
    for c in string:
        bits = bin(ord(c))[2:]
        # makes sure each is a 8 full bits
        bits = '00000000'[len(bits):] + bits
        binary += bits
    return binary


def bytes_to_bits(bytestring):
    '''Converts a bytes literal to it's binary representation.

    Args:
    bytestring (bytes): A bytes literal.

    Returns:
    string: A string of binary without the '0b' prefix.
    '''
    binary = ''
    for b in bytestring:
        bits = bin(b)[2:]
        bits = '00000000'[len(bits):] + bits
        binary += bits
    return binary


def hamming_distance_str(string1, string2):
    '''Computes the hamming distance between two same-length binary strings.

    Args:
    string1 (str): String of binary data. E.g. '000101011101001100'
    string2 (str): String of binary data. E.g. '001110101110000101'

    Returns:
    int: Sum of bits that differ between the two strings.
    '''
    bstring1 = binascii.a2b_qp(string1)
    bstring2 = binascii.a2b_qp(string2)
    if len(bstring1) != len(bstring2):
        print('Strings must be the same length.')
        return False
    return sum([a ^ b for a, b in zip(bstring1, bstring2)])


def hamming_distance(bstring1, bstring2):
    '''Computes the hamming distance between two same-length binary strings.

    Args:
    bstring1 (str): Byte literal
    bstring2 (str): Byte literal

    Returns:
    int: Sum of bits that differ between the two strings.
    '''
    if len(bstring1) != len(bstring2):
        print('Strings must be the same length.')
        return False
    return sum([a ^ b for a, b in zip(bstring1, bstring2)])


def guess_repeating_key_size(corpus, low, high):
    '''Finds the most likely repeating key size (in bytes) from a range of sizes.

    For each keysize in range(low, high), breaks the corpus in to two consecutive
    chunks of keysize number of bytes and computes the hamming distance between
    each chunk. The keysize with the lowest normalized hamming distance is
    returned.

    Args:
    corpus (bytes): Body of text to eventually be decrypted.
    low (int): Smallest keysize to start guessing with.
    high (int): Largest keysize to end guessing with.

    Returns:
    int: Keysize found to have the lowest normalized hamming distance.
    '''
    best_distance = 9999
    keysize = 0
    for num_bytes in range(low, high):
        bin1 = corpus[:num_bytes]
        bin2 = corpus[num_bytes:num_bytes * 2]
        new_distance = hamming_distance(bin1, bin2) / num_bytes
        if new_distance < best_distance:
            best_distance = new_distance
            keysize = num_bytes
    return keysize


def block_ciphertext(corpus, num_bytes):
    '''Creates a list of byte literals of a given size.

    Args:
    corpus (bytes): Body of text to be blocked.
    num_bytes (int): The size, in bytes, of the blocks to be made.

    Returns:
    list: Contains num_bytes sized blocks of the corpus.
    '''
    blocks = []
    for i in range(0, len(corpus), num_bytes):
        blocks.append(corpus[i:i + num_bytes])
    return blocks


def transpose_blocks(blocks, keysize):
    '''Transpose each byte of each block to a new list of byte literals.

    Args:
    blocks (list): List of byte literals to be transposed.
    keysize (int): Number of bytes expected to be in each block.

    Returns:
    list: A list of length keysize containing byte literals.
    '''
    if len(blocks[0]) != keysize:
        print("Block size does not match key size.")
        return False
    transposed = []
    for i in range(0, keysize):
        transposed.append([])
    for block in blocks:
        for i in range(0, keysize):
            transposed[i].append(block[i:i + 1])
    for i in range(0, len(transposed)):
        transposed[i] = b''.join(transposed[i])
    return transposed

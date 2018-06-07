import unittest
import set1.module as s1

class TestSet1(unittest.TestCase):

	def test_challenge_one(self):
		hexstr = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
		guess = s1.hex_to_base64(hexstr).decode('ascii')
		answer = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
		self.assertEqual(guess, answer)


	def test_challenge_two(self):
		hexstr = '1c0111001f010100061a024b53535009181c'
		hexmask = '686974207468652062756c6c277320657965'
		guess = s1.fixed_length_xor(hexstr, hexmask).hex()
		answer = '746865206b696420646f6e277420706c6179'
		self.assertEqual(guess, answer)


	def test_challenge_three(self):
		hexstr = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736' 
		guess = s1.find_single_key(hexstr)[1].decode('ascii')
		answer = "Cooking MC's like a pound of bacon"
		self.assertEqual(guess, answer)


	def test_challenge_four(self):
		hex_lines = s1.build_list_from_file('./data/set1challenge4.txt')
		guess = s1.find_in_list(hex_lines).decode('ascii')
		answer = 'Now that the party is jumping\n'
		self.assertEqual(guess, answer)


	def test_challenge_five(self):
		to_encode = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
		key = 'ICE'
		guess = s1.repeating_key_xor(to_encode, key).hex()
		answer = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'
		self.assertEqual(guess, answer)


	def test_hamming_distance(self):
		str1 = s1.string_to_bits('this is a test')
		str2 = s1.string_to_bits('wokka wokka!!!')
		guess = s1.hamming_distance(str1, str2)
		answer = 37
		self.assertEqual(guess, answer)

	def test_challenge_six(self):
		corpus = s1.build_corpus_from_file_b64('./data/set1challenge6.txt')
		keysize = s1.guess_repeating_key_size(corpus, 2, 40)
		


if __name__ == '__main__':
    unittest.main()
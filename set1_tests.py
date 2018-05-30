import unittest
import set1.module as s1

class TestSet1(unittest.TestCase):

	def test_one(self):
		hex_s = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
		guess = s1.hex_to_base64(hex_s)
		answer = b'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
		self.assertEqual(guess, answer)


	def test_two(self):
		hex_s = '1c0111001f010100061a024b53535009181c'
		mask = '686974207468652062756c6c277320657965'
		guess = s1.fixed_xor(hex_s, mask)
		answer = bytes.fromhex('746865206b696420646f6e277420706c6179')
		self.assertEqual(guess, answer)


	def test_three(self):
		hex_s = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736' 
		guess = s1.decrypt(hex_s)
		answer = b'Cooking MC\'s like a pound of bacon'
		self.assertEqual(guess, answer)


if __name__ == '__main__':
    unittest.main()
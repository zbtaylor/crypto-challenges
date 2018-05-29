import set1.module as s1

# challenge 1
c1_hex = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
c1_result = s1.hex_to_base64(c1_hex)
print('Challenge 1:')
print(c1_result) # expected: SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t

# challenge 2
c2_hex = '1c0111001f010100061a024b53535009181c'
c2_mask = '686974207468652062756c6c277320657965'
c2_result = s1.fixed_xor(c2_hex, c2_mask)
print('Challenge 2:')
print(c2_result) # expected: 746865206b696420646f6e277420706c6179

# challenge 3
c3_hex = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
c3_result = s1.decrypt(c3_hex)
print('Challenge 3:')
print(c3_result)
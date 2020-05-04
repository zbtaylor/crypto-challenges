# Python3 Encoding

## Fundamentals

The only thing that a computer can store is bytes.

To store something in a computer, you must first encode it.

A byte string is a sequence of bytes. It isn't human readable.

A character string, on the other hand, is a sequence of characters. It is human readable.

A character string can't be directly stored on a computer. It must be encoded first.

Encoding a character string converts it to a byte string.

There are multiple encodings through which a character string can be converted to a byte string; like ASCII or UTF-8.

## Example

    'I am a string'.encode('ASCII')

The line above will encode the character string `'I am a string'` using the ASCII encoding. This will result in the byte string `b'I am a string'`.

If byte strings aren't human readable, how does Python display it in the terminal in a way we can read?

When Python is printing a byte string to the terminal it automatically decodes it from ASCII (and I assume adds the 'b' to indicate that what you are seeing is the ASCII representation of a byte string instead of a character string).

    b'I am a string'.decode('ASCII')

This line will decode the byte string `b'I am a string'` using the provided ASCII encoding and return the character string `'I am a string'`.

How does Python know that the passed byte string was encoded with ASCII?

The answer is that it doesn't - sort of. In Python 2, strings are encoded with ASCII by default. In Python 3, the default string encoding is Unicode. So why can we decode the byte string `b'I am a string'` to ASCII, in Python 3, and still get the correct result?

That's because the first 128 characters in the ASCII encoding are the same as those in Unicode, which are both comprised of the basic English alphabet characters.

For example, 'A' in ASCII is represented by the hexadecimal value `0041`.

In UTF-8 Unicode, 'A' is represented as `U+0041` which is the save hex value.

Many encodings will match for the first 128 characters, so it's not always obvious which is being used.

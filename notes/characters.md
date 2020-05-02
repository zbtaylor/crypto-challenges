# Characters

## Origins

Character sets hold values for the 256 unsigned integers available in the range of one byte (0-255).

In the beginning there were OEM character sets where the first 128 characters (0-127) were the same standard english characters without accents and the upper 128 (128-255) were whatever the manufacturer chose to make them.

This OEM free-for-all made exchanging documents difficult because the upper byte characters would always display differently on different computers.

## ANSI

The ANSI standard codified the first 128 characters, and the upper 128 depended on where you lived. These different systems for the upper 128 were called 'code pages.'

This made users in the same language more standardized but using multiple languages on a computer didn't work unless you wrote your own custom programs.

## Asia

Asian country were doing even crazier things because they have so many characters in their alphabets. Some solutions called 'double byte character sets' used two bytes for some characters and only one for others.

This made moving backwards and forwards in strings difficult.

At the time this was all fine-ish because the internet didn't exist yet and moving strings across regions or languages was rare.

## Unicode

Unicode attempted to create a single character set encompassing all reasonable writing system.

Myth: Unicode characters are all 16 bit codes where each character takes 16 bits and therefore there are 65,536 possible chatacters.

This is not true. Unicode thinks of characters differently. In Unicode, a letter maps to a code point, which is really just a theoretical concept.

For example, 'A' is the same character across fonts, but 'A' is not considered the same as 'a' in Unicode.

Each letter in every alphabet is assigned a number like 'U+0041', which is the Unicode code point for the letter A. The 'U+' means unicode and the '0041' is hexadecimal.

## Early Unicode Encoding

The string

    Hello

Is represented as

    U+0048 U+0065 U+006C U+006C U+006F

in Unicde code points.

But that's still not something the computer can store.

Early efforts in encoding Unicode suggested storing each character as two bytes. But that left the door open for the reversing of the order of bytes to account for endianness.

Thus the convention of storing 'FE FF' or 'FF FE' at the beginning of every Unicode string to incidate which order was being used. This is called the 'Unicode byte order mark.'

Unicode was ignored for awhile because of it's complicatedness and American programmers sneering at the idea of doubling storage space required for strings now that characters would require two bytes.

## UTF-8

In UTF-8 the first 128 characters (0-127) are stored with a single 8-bit byte. Only code points 128 and above are stored in 2 bytes or more. In fact some go up to 6 bytes.

This means English text looks the same in UTF-8 as it did in ASCII, ANSI, and most typical OEM character sets that existed at the time. Only the rest of the world has to jump through hoops!

## Unicode Encoding

UTF-16: 16 bits per character.
UCS-2: 2 bytes per character.
UTF-8: first 128 are one byte, last 128 are 2-6 bytes.

Quite a few others, like UTF-7 or UCS-4.

Each Unicode code point can be encoded in any old-school encoding scheme too, but with one major catch: some of the letters might not show up. If there's no equivalent to the Unicode character you're encoding in an old scheme, you'll see a question mark or a box.

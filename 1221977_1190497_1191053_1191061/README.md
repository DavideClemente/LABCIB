steps to get c&c password

`openssl base64 -d -in encrypted.txt -out encrypted.bin`

`openssl rsautl -decrypt -inkey private_key.pem -in encrypted.bin -out decrypted.txt`

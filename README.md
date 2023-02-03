# Streech

This repo or atleast streech.py file encrypts a text in a unsafe way. This repo is made for fun and is firstly developed from phone.

## Usage

**Command Line**

```sh
python3 streech.py <text> [char]=[int] -e/-d
```

**Import Usage** (**Example**)
```python
from streech import encryptf, decryptf

text = "Hello, World!"
char = "k"
num = 5

encrypted = encryptf(text, (char, num))
decrypted = decryptf(encrypted, (char, num))
print(decrypted == text)
```

## Install

```sh
git clone https://github.com/RimuEirnarn/streech
```

## License

Licensed in MIT

# Simple RSA

> A straightforward API to perform basic RSA-based operations.

[![Latest Version on PyPI](https://img.shields.io/pypi/v/simple-rsa.svg)](https://pypi.python.org/pypi/simple-rsa/)
[![Supported Implementations](https://img.shields.io/pypi/pyversions/simple-rsa.svg)](https://pypi.python.org/pypi/simple-rsa/)
[![Build Status](https://secure.travis-ci.org/christophevg/py-simple-rsa.svg?branch=master)](http://travis-ci.org/christophevg/py-simple-rsa)
[![Coverage Status](https://coveralls.io/repos/github/christophevg/py-simple-rsa/badge.svg?branch=master)](https://coveralls.io/github/christophevg/py-simple-rsa?branch=master)
[![Built with PyPi Template](https://img.shields.io/badge/PyPi_Template-v0.0.6-blue.svg)](https://github.com/christophevg/pypi-template)

## Rationale

Any cryptographic library exposes all possibilities, and it should. But sometimes you just want a simple `sign` and `validate` API. That is what this wrapper module around the Cryptography module is. Nothing more, nothing less.

## Getting Started

The module basically exposes the following functions:

- `generate_key_pair()` returning a tuple of private and public keys
- `encode(key)` returning an encoded key
- `decode(pem)` returning a key
- `sign(payload, key)` returning a signature
- `validate(payload, signature, key)` returning True or an Exception

```bash
$ python
Python 2.7.15 (default, Dec 27 2018, 11:55:59) 
[GCC 4.2.1 Compatible Apple LLVM 10.0.0 (clang-1000.11.45.5)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import simple_rsa as rsa
>>> private, public = rsa.generate_key_pair()
>>> rsa.encode(public)
'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5C15SFjpTCrdqB+0zFyu\nC9KJkNT1byzQPyATtLze/PNWjfqYL0RjvL4cmvmBWLeTQvnDx9SQfnQT02+4Q8Ov\nOaRTPqghEJctAh7KHwZfQzH29miC1WxXtGFcMFoAj17WPyMaOO3EcHqb4ttnAAPD\nt6B415HtGZo4oH6xY7QMj4eRceTv4++zACNHvqArO3bFFiNTBC8vCOpIg3xsYV4w\n7lQZs2lwGlzXPFJUeZglvsWTPJ54E1KabtkC/wSRFZBYtml8ZvzFfNDTOhcDyBR9\nVTV4K7iIGXG0A9C7mmj3hgALS3qSP5EK6fi51ufg98WokCLFcTSD/EphUlixazPo\nOQIDAQAB\n-----END PUBLIC KEY-----\n'
>>> payload = b"something important"
>>> signature = rsa.sign(payload, private)
>>> assert rsa.validate(payload, signature, public)
>>> another_payload = b"something else"
>>> another_signature = rsa.sign(another_payload, private)
>>> assert rsa.validate(payload, another_signature, public)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "simple_rsa/__init__.py", line 74, in validate
    hashes.SHA256()
  File "/usr/local/lib/python2.7/site-packages/cryptography/hazmat/backends/openssl/rsa.py", line 477, in verify
    self._backend, padding, algorithm, self, signature, data
  File "/usr/local/lib/python2.7/site-packages/cryptography/hazmat/backends/openssl/rsa.py", line 272, in _rsa_sig_verify
    raise InvalidSignature
cryptography.exceptions.InvalidSignature
```

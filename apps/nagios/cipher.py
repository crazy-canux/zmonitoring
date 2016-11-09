# -*- coding: utf-8 -*-
# Copyright (C) Faurecia <http://www.faurecia.com/>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""This module provides the class :class:`AESCipher` to easily encrypt /
decrypt strings using an AES cipher."""

from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):
    def __init__(self, private_key, iv=None):
        """Initialize a new AES cipher instance.

        Encrypt / Decrypt a string with provided ``private_key``, a string that
        should be a multiple of 16 for its length. The optional ``iv`` argument
        is the Initialization Vector (IV) that should be randomly set to
        enforce the cipher (this is the default behavior if None).

        :param private_key: the private key used for this cipher as a string of
        lenght multiple of 16.
        :param iv: the initialization vector string (see above).
        """
        self.private_key = private_key
        self.iv = Random.new().read(AES.block_size) if not iv else iv

    def encrypt(self, string):
        """Encrypt the ``string`` using AES cipher."""
        cipher = AES.new(self.private_key, AES.MODE_CBC, self.iv)
        return cipher.encrypt(_pad(string))

    def decrypt(self, data):
        """Decrypt the ``data`` using AES cipher."""
        cipher = AES.new(self.private_key, AES.MODE_CBC, self.iv)
        return _unpad(cipher.decrypt(data))


def _pad(data):
    """Pad the data to encrypt to be a multiple of 16."""
    # return data if no padding is required
    if len(data) % 16 == 0:
        return data

    # subtract one byte that should be the 0x80
    # if 0 bytes of padding are required, it means only
    # a single \x80 is required.
    padding_required = 15 - (len(data) % 16)
    data = "%s\x80" % data
    data = "%s%s" % (data, "\x00" * padding_required)
    return data


def _unpad(data):
    """Remove padding from the decrypted data."""
    if not data:
        return data
    data = data.rstrip("\x00")
    if data[-1] == "\x80":
        return data[:-1]
    else:
        return data

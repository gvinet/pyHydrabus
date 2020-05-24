# Copyright 2020 Guillaume VINET
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from .protocol import Protocol


class NFC1Reader(Protocol):
    """
    Smartcard protocol handler

    :example:

    >>> #Read ATR from a smartcard
    >>> import pyHydrabus
    >>> sm=pyHydrabus.Smartcard('/dev/hydrabus')
    >>> sm.prescaler=12
    >>> sm.baud=9600
    >>> sm.rst=1;sm.rst=0;sm.read(1)

    """

    def __init__(self, port=""):
        # self._config = 0b0000
        # self._rst = 1
        # self._baud = 9600
        # self._prescaler = 12
        # self._guardtime = 16
        super().__init__(name=b"NFC1", fname="NFC1Reader", mode_byte=b"\x0C", port=port)

    def set_mode_iso14443_A(self):
        """Configure HydraNFC1 to communicate with ISO 14443 Type A cards.

        :return: None
        """
        self._hydrabus.write(b"\x05")

    def rf_off(self):
        """Set RF Field off.

        :return: None
        """
        self._hydrabus.write(b"\x01")

    def rf_on(self):
        """Set RF Field on.

        :return: None
        """
        self._hydrabus.write(b"\x02")

    def send_bits(self, data, nb_bits):
        """

        :param data: integer equal or lower than 128 (0x80)
        :param nb_bits: integer indicating the number of bits to send, between
        1 and 7.
        :return: the card answer (bytes)
        """

        if data not in range(128):
            ValueError(f"Incorrect data value: {data}. It must be an integer equal or lower than 128 (0x80).")

        if nb_bits not in range(1, 8):
            ValueError(f"Incorrect nb_bits value: {nb_bits}. It must be an integer between 1 and 7.")

        self._hydrabus.write(b"\x03")
        self._hydrabus.write(bytes([data, nb_bits]))

        length = self._hydrabus.read(1)[0]

        return self._hydrabus.read(length)

    def send_bytes(self, data):
        """

        :param data: hexadecimal string
        :return: the card answer (bytes)
        """
        try:
            data_b = bytes.fromhex(data)
        except:
            raise ValueError("Incorrect data value. It must be an hexadecimal string")

        self._hydrabus.write(b"\x04")
        self._hydrabus.write(bytes([len(data_b)]))
        self._hydrabus.write(data_b)

        length = self._hydrabus.read(1)[0]
        return self._hydrabus.read(length)

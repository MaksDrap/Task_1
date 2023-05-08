class UnsignedInt:
    def __init__(self, num=0):
        self.num = num
        self.uint_array = []

    def set_from_hex_string(self, hex_string):
        self.uint_array = []
        for i in range(len(hex_string) // 8 + 1):
            uint_str = hex_string[max(len(hex_string) - 8 * (i + 1), 0):len(hex_string) - 8 * i]
            if uint_str:
                uint = int(uint_str, 16)
                self.uint_array.insert(0, uint)
        self.num = self.uint_array[0] if self.uint_array else 0

    def set_from_decimal_string(self, decimal_string):
        self.uint_array = []
        while decimal_string > 0:
            uint = decimal_string & 0xFFFFFFFF
            self.uint_array.insert(0, uint)
            decimal_string >>= 32
        self.num = self.uint_array[0]

    def get_hex_string(self):
        hex_string = ''
        for uint in self.uint_array:
            hex_string = '{:08x}'.format(uint) + hex_string
        return hex_string.lstrip('0') if hex_string else '0'


    def get_decimal_string(self):
        decimal_string = 0
        for uint in self.uint_array:
            decimal_string <<= 32
            decimal_string += uint
        return str(decimal_string)


    def test_unsigned_int(self):
        # Тест set_from_hex_string і get_hex_string
        unsigned_int = UnsignedInt()
        unsigned_int.set_from_hex_string('3211')
        assert unsigned_int.get_hex_string() == '3211'
        unsigned_int.set_from_hex_string('ffffffff')
        assert unsigned_int.get_hex_string() == 'ffffffff'
        unsigned_int.set_from_hex_string('100000000')
        assert unsigned_int.get_hex_string() == '100000000'

        # Тест set_from_decimal_string і get_decimal_string
        unsigned_int = UnsignedInt()
        unsigned_int.set_from_decimal_string(12345)
        assert unsigned_int.get_decimal_string() == '12345'
        unsigned_int.set_from_decimal_string(4294967296)
        assert unsigned_int.get_decimal_string() == '4294967296'
        unsigned_int.set_from_decimal_string(18446744073709551615)
        assert unsigned_int.get_decimal_string() == '18446744073709551615'

        # Тест крайніх випадків
        unsigned_int = UnsignedInt()
        unsigned_int.set_from_hex_string('0')
        assert unsigned_int.get_hex_string() == '0'
        unsigned_int.set_from_decimal_string

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

    def get_hex_string2(self):
        hex_string = ''
        for uint in self.uint_array:
            hex_string += '{:08x}'.format(uint)
        return hex_string.lstrip('0') if hex_string else '0'


    def get_decimal_string(self):
        decimal_string = 0
        for uint in self.uint_array:
            decimal_string <<= 32
            decimal_string += uint
        return str(decimal_string)

    def karatsuba(self, other):
        if self.num == 0 or other.num == 0:
            return UnsignedInt()

        if self.num < 0 or other.num < 0:
            raise ValueError("Karatsuba algorithm only supports unsigned integers.")

        if len(self.uint_array) == 0 or len(other.uint_array) == 0:
            return UnsignedInt()

        if len(self.uint_array) == 1 or len(other.uint_array) == 1:
            return self * other

        max_len = max(len(self.uint_array), len(other.uint_array))
        m = (max_len + 1) // 2

        high1, low1 = self.split_at(m)
        high2, low2 = other.split_at(m)

        z0 = low1.karatsuba(low2)
        z2 = high1.karatsuba(high2)

        sum_high_low1 = high1 + low1
        sum_high_low2 = high2 + low2

        z1 = sum_high_low1.karatsuba(sum_high_low2)
        z1 -= z0
        z1 -= z2

        result = z2.shiftL(2 * m) + z1.shiftL(m) + z0
        return result

    def __mul__(self, other):
        if isinstance(other, int):
            other = UnsignedInt(other)

        result = UnsignedInt()
        # Perform multiplication logic here
        return result

    def __add__(self, other):
        if isinstance(other, int):
            other = UnsignedInt(other)

        result = UnsignedInt()
        carry = 0
        min_len = min(len(self.uint_array), len(other.uint_array))
        for i in range(min_len):
            uint = self.uint_array[i] + other.uint_array[i] + carry
            carry = uint >> 32
            result.uint_array.append(uint & 0xFFFFFFFF)
        for i in range(min_len, len(self.uint_array)):
            uint = self.uint_array[i] + carry
            carry = uint >> 32
            result.uint_array.append(uint & 0xFFFFFFFF)
        for i in range(min_len, len(other.uint_array)):
            uint = other.uint_array[i] + carry
            carry = uint >> 32
            result.uint_array.append(uint & 0xFFFFFFFF)
        if carry:
            result.uint_array.append(carry)
        result.num = result.uint_array[0] if result.uint_array else 0
        return result


    def split_at(self, index):
            high = UnsignedInt()
            low = UnsignedInt()

            if index >= len(self.uint_array):
                high.uint_array = self.uint_array[:]
            else:
                high.uint_array = self.uint_array[:index]
                low.uint_array = self.uint_array[index:]

            return high, low

# Example usage of the Karatsuba algorithm for multiplication
a = UnsignedInt()
a.set_from_hex_string("7d7deab2affa38154326e96d350deee1")
b = UnsignedInt()
b.set_from_hex_string("97f92a75b3faf8939e8e98b96476fd22")
c = a.karatsuba(b)

print(c.get_hex_string())

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


    def INV(self):
        for i in range(len(self.uint_array)):
            self.uint_array[i] = ~self.uint_array[i]

    def XOR(self, other):
        result = UnsignedInt()
        for i in range(max(len(self.uint_array), len(other.uint_array))):
            uint1 = self.uint_array[i] if i < len(self.uint_array) else 0
            uint2 = other.uint_array[i] if i < len(other.uint_array) else 0
            result.uint_array.insert(0, uint1 ^ uint2)
        result.num = result.uint_array[0] if result.uint_array else 0
        return result

    def OR(self, other):
        result = UnsignedInt()
        for i in range(max(len(self.uint_array), len(other.uint_array))):
            uint1 = self.uint_array[i] if i < len(self.uint_array) else 0
            uint2 = other.uint_array[i] if i < len(other.uint_array) else 0
            result.uint_array.insert(0, uint1 | uint2)
        result.num = result.uint_array[0] if result.uint_array else 0

    def AND(self, other):
        result = UnsignedInt()
        min_len = min(len(self.uint_array), len(other.uint_array))
        for i in range(min_len):
            uint = self.uint_array[i] & other.uint_array[i]
            result.uint_array.append(uint)
        return result

    def shiftR(self, n):
        result = UnsignedInt()
        q = n // 32
        r = n % 32
        for i in range(q, len(self.uint_array)):
            uint = self.uint_array[i] >> r
            if i < len(self.uint_array) - 1 and r > 0:
                uint |= self.uint_array[i + 1] << (32 - r)
            result.uint_array.append(uint)
        return result

    def shiftL(self, n):
        result = UnsignedInt()
        q = n // 32
        r = n % 32
        for i in range(len(self.uint_array) - 1, q - 1, -1):
            uint = self.uint_array[i] << r
            if i > 0 and r > 0:
                uint |= self.uint_array[i - 1] >> (32 - r)
            result.uint_array.insert(0, uint)
        return result
    def ADD(self, other):
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

    def SUB(self, other):
        result = UnsignedInt()
        borrow = 0
        min_len = min(len(self.uint_array), len(other.uint_array))
        for i in range(min_len):
            uint = self.uint_array[i] - other.uint_array[i] - borrow
            borrow = 0 if uint >= 0 else 1
            result.uint_array.append(uint & 0xFFFFFFFF)
        for i in range(min_len, len(self.uint_array)):
            uint = self.uint_array[i] - borrow
            borrow = 0 if uint >= 0 else 1
            result.uint_array.append(uint & 0xFFFFFFFF)
        if borrow:
            raise ValueError("Subtraction resulted in a negative value.")
        result.num = result.uint_array[0] if result.uint_array else 0
        return result

    def MOD(self, other):
        result = UnsignedInt()
        dividend = self
        divisor = other
        if divisor.num == 0:
            raise ZeroDivisionError('division by zero')
        if dividend.num == 0:
            return result
        if divisor.num == 1:
            return result
        if divisor.num > dividend.num:
            return dividend
        q = dividend.num // divisor.num
        result.uint_array.append(dividend.num - q * divisor.num)
        while len(dividend.uint_array) > 0:
            dividend.uint_array.pop()
        while len(divisor.uint_array) > 0 and divisor.uint_array[-1] == 0:
            divisor.uint_array.pop()
        while len(dividend.uint_array) > 0:
            dividend.uint_array.insert(0, 0)
            dividend = dividend.ADD(divisor)
            if divisor.num > dividend.num:
                break
            q = dividend.num // divisor.num
            result.uint_array.insert(0, dividend.num - q * divisor.num)
            while len(divisor.uint_array) > 0 and divisor.uint_array[-1] == 0:
                divisor.uint_array.pop()
        return result

    def MUL(self, other):
        result = UnsignedInt()
        carry = 0
        for i in range(len(self.uint_array)):
            for j in range(len(other.uint_array)):
                uint_product = self.uint_array[i] * other.uint_array[j]
                position = i + j
                while len(result.uint_array) <= position:
                    result.uint_array.append(0)
                uint_sum = result.uint_array[position] + uint_product + carry
                result.uint_array[position] = uint_sum & 0xFFFFFFFF
                carry = uint_sum >> 32

        if carry > 0:
            result.uint_array.append(carry)

        return result


numberA = UnsignedInt()
numberB = UnsignedInt()
numberC = UnsignedInt()
numberD = UnsignedInt()
numberF = UnsignedInt()
numberG = UnsignedInt()

numberA.set_from_hex_string('51bf608414ad5726a3c1bec098f77b1b54ffb2787f8d528a74c1d7fde6470ea4')
numberB.set_from_hex_string('403db8ad88a3932a0b7e8189aed9eeffb8121dfac05c3512fdb396dd73f6331c')
numberC = numberA.XOR(numberB)

print(numberC.get_hex_string())

numberD.set_from_hex_string('36f028580bb02cc8272a9a020f4200e346e276ae664e45ee80745574e2f5ab80')
numberF.set_from_hex_string('70983d692f648185febe6d6fa607630ae68649f7e6fc45b94680096c06e4fadb')
numberG = numberD.ADD(numberF)

print(numberG.get_hex_string2())

a = UnsignedInt()
a.set_from_hex_string("33ced2c76b26cae94e162c4c0d2c0ff7c13094b0185a3c122e732d5ba77efebc")
b = UnsignedInt()
b.set_from_hex_string("22e962951cb6cd2ce279ab0e2095825c141d48ef3ca9dabf253e38760b57fe03")
c = UnsignedInt()
c = a.SUB(b)

print(c.get_hex_string2())

a1 = UnsignedInt()
a1.set_from_hex_string("7d7deab2affa38154326e96d350deee1")
b1 = UnsignedInt()
b1.set_from_hex_string("97f92a75b3faf8939e8e98b96476fd22")
c1 = a1.MUL(b1)

print(c1.get_hex_string())






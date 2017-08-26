def cast(var):
    if isinstance(var, list):
        var = ''.join(map(cast, var))
    elif isinstance(var, int):
        var = str(int(var))
    else:
        var = str(var)
    return var

def bitflip(value):
    value = list(map(int, bin(value)[2:]))
    for i in range(len(value)):
        value[i] ^= 1
    value = ''.join(map(str, value))
    return int(value, 2)

class Comparison:
    def __ge__(self, y):
        return cast(self) >= cast(y)
    def __le__(self, y):
        return cast(self) <= cast(y)
    def __gt__(self, y):
        return cast(self) > cast(y)
    def __lt__(self, y):
        return cast(self) < cast(y)

class Int(Comparison, int):
    pass

class Str(Comparison, str):
    @staticmethod
    def __count_lens(length, y):
        lens = [0]*y
        i = 0
        l = length
        while l:
            lens[i] += 1
            i += 1
            i %= len(lens)
            l -= 1
        return lens

    def __add__(self, y):
        return self + str(y)

    def __sub__(self, y):
        if not isinstance(y, int):
            return self
        return self[:-y]
    
    def __floordiv__(self, y):
        if not isinstance(y, int) or y > len(self):
            return self
        chunks = []
        i = 0
        for i in range(y, len(self), y):
            chunks.append(self[[i-y,0][i-y<0]:i])
        chunks.append(self[i:])
        return chunks

    def __truediv__(self, y):
        if not isinstance(y, int):
            return self
        lens = Str.__count_lens(len(self), y)
        chunks = []
        s = self
        for index in lens:
            chunks.append(s[:index])
            s = s[index:]
        return chunks

    def __mod__(self, y):
        if y == len(self):
            return ''
        return (self // y)[-1]

    def __pow__(self, y):
        if not isinstance(y, int):
            return self
        return ''.join(map(lambda c: c*y, self))

    def __invert__(self):
        s = list(map(lambda c: bitflip(ord(c)), self))
        return ''.join(map(chr, s))

    def __xor__(self, y):
        if isinstance(y, int):
            s = list(map(lambda c: ord(c) ^ y, self))
            return ''.join(map(chr, s))
        elif isinstance(y, str):
            s = list(map(lambda a: ord(a[0]) ^ ord(a[1]), zip(self, y)))
        else:
            s = list(map(ord, self))
        return ''.join(map(chr, s))

    def __and__(self, y):
        if isinstance(y, int):
            b = bin(y)[2:]
            x = ''.join(map(lambda c: bin(ord(c))[2:], self))
            while len(x)%8 != 0:
                x = '0'+x
            while len(x) > len(b):
                b += b
            x, b = list(map(eval, x)), list(map(eval, b))
            for i in range(len(x)):
                x[i] = str(int(x[i] == 1 == b[i]))
            x = ''.join(map(lambda x: chr(int(x, 2)), Str(''.join(x))//8))
            return x
        return ''.join(map(lambda a: ord(a[0])&ord(a[1]), zip(self, y)))

    def __or__(self, y):
        if isinstance(y, int):
            b = bin(y)[2:]
            x = ''.join(map(lambda c: bin(ord(c))[2:], self))
            while len(x)%8 != 0:
                x = '0'+x
            while len(x) > len(b):
                b += b
            x, b = list(map(eval, x)), list(map(eval, b))
            for i in range(len(x)):
                x[i] = str(int(x[i] == 1 or b[i] == 1))
            x = ''.join(map(lambda x: chr(int(x, 2)), Str(''.join(x))//8))
            return x
        return ''.join(map(lambda a: ord(a[0])|ord(a[1]), zip(self, y)))

    def __radd__(self, y):
        return str(y) + self
    
    __rsub__ = __sub__
    __rtruediv__ = __truediv__
    __rfloordiv__ = __floordiv__
    __ror__ = __or__
    __rand__ = __and__
    __rmod__ = __mod__
    __rpow__ = __pow__
    __rxor__ = __xor__

class List(Comparison, list):
    def __add__(self, y):
        return list(map(lambda a: a+y, self))
    def __sub__(self, y):
        return list(map(lambda a: a-y, self))
    def __mul__(self, y):
        return list(map(lambda a: a*y, self))
    def __mod__(self, y):
        return list(map(lambda a: a%y, self))
    def __or__(self, y):
        return list(map(lambda a: a|y, self))
    def __and__(self, y):
        return list(map(lambda a: a&y, self))
    def __xor__(self, y):
        return list(map(lambda a: a^y, self))
    def __pow__(self, y):
        return list(map(lambda a: a**y, self))
    def __truediv__(self, y):
        return list(map(lambda a: a/y, self))
    def __floordiv__(self, y):
        return list(map(lambda a: a//y, self))
    def __radd__(self, y):
        return list(map(lambda a: y+a, self))
    def __rsub__(self, y):
        return list(map(lambda a: y-a, self))
    def __rmul__(self, y):
        return list(map(lambda a: y*a, self))
    def __rmod__(self, y):
        return list(map(lambda a: y%a, self))
    def __ror__(self, y):
        return list(map(lambda a: y|a, self))
    def __rand__(self, y):
        return list(map(lambda a: y&a, self))
    def __rxor__(self, y):
        return list(map(lambda a: y^a, self))
    def __rpow__(self, y):
        return list(map(lambda a: y**a, self))
    def __rtruediv__(self, y):
        return list(map(lambda a: y/a, self))
    def __rfloordiv__(self, y):
        return list(map(lambda a: y//a, self))
    
class Bool(Comparison, int):
    pass

class Float(Comparison, float):
    pass

print(Str('Hello') // 3)

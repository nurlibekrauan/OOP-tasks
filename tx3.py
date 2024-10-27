class Operation:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def calculate(self):
        raise NotImplementedError("Метод calculate() должен быть реализован в подклассе")

    def __add__(self, other):
        if isinstance(other, Operation):
            return Addition(self.a + other.a, self.b + other.b)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Operation):
            return Subtraction(self.a - other.a, self.b - other.b)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Operation):
            return Multiplication(self.a * other.a, self.b * other.b)
        return NotImplemented

    def __repr__(self):
        return f"Operation(a={self.a}, b={self.b})"


class Addition(Operation):
    def calculate(self):
        return self.a + self.b

    def __add__(self, other):
        # Делегирование через super()
        result = super().__add__(other)
        return result


class Subtraction(Operation):
    def calculate(self):
        return self.a - self.b

    def __sub__(self, other):
        # Делегирование через super()
        result = super().__sub__(other)
        return result


class Multiplication(Operation):
    def calculate(self):
        return self.a * self.b

    def __mul__(self, other):
        # Делегирование через super()
        result = super().__mul__(other)
        return result


# Пример использования
op1 = Addition(5, 10)
op2 = Subtraction(20, 5)
op3 = Multiplication(4, 6)

# Умножение op2 * op3, затем сложение с op1
result = op1 + op2 * op3

print(result)  # Operation(a=5, b=10)

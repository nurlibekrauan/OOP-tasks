class Geom:
    name = "Geom"

    def __init__(self, x1, y1, x2, y2):
        print(f"инициализатор Geom для класса {self.__class__}")
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self):
        print("Рисование линии")


class Line(Geom):

    def draw(self):
        print("Рисование линии")


class React(Geom):
    def __init__(self, x1, y1, x2, y2, fill=None):
        # инициализатор базового класса нужно вызывать первее всех!!!
        super().__init__(x1, y1, x2, y2) # делегирование
        print("инициализатор Rect")
        self.fill = fill

    def draw(self):
        print("Рисование ")


l = Line(0, 0, 10, 10)
r = React(1, 2, 3, 4)
print(l.__dict__)
print(r.__dict__)

class EmployeeManager:
    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def validate_name(self, value, **kwargs):
        min_len = self.kwargs.get("min_len")
        max_len = self.kwargs.get("max_len")
        if not isinstance(value, str):
            raise ValueError("Имя должно быть строкой")
        if self.kwargs:
            if not min_len < len(value) < max_len:
                raise ValueError(f"имя должно быть в диапазоне ({min_len})-({max_len})")

    def validate_age(self, value, **kwargs):
        max_age = self.kwargs.get("max_age")
        min_age = self.kwargs.get("min_age")
        if not isinstance(value, int):
            raise ValueError("Возраст должен быть числом")
        if kwargs:
            if not min_age <= value <= max_age:
                raise ValueError(
                    f"возраст должен быть в диапазоне ({min_age}-{max_age})"
                )

    def validate_salary(self, value, **kwargs):
        min_salary = self.kwargs.get("min_salary")
        max_salary = self.kwargs.get("max_salary")
        if not isinstance(value, (int, float)):
            raise ValueError("Зарплата должна быть числом")
        if kwargs:
            if not min_salary <= value <= max_salary:
                raise ValueError(
                    f"зарплата должна быть в диапазоне ({min_salary}-{max_salary})"
                )

    def __set__(self, instance, value):
        if self.name == "_employee_name":
            self.validate_name(value, **self.kwargs)
        elif self.name == "_age":
            self.validate_age(value, **self.kwargs)
        elif self.name == "_salary":
            self.validate_salary(value, **self.kwargs)
        else:
            raise AttributeError(f"Нет атрибута '{self.name}'")
        setattr(instance, self.name, value)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)


class Employee:
    employee_name = EmployeeManager(min_len=0, max_len=100)
    age = EmployeeManager(min_age=18, max_age=100)
    salary = EmployeeManager(min_salary=1000, max_salary=99999)

    def __init__(self, employee_name, age, salary):
        self.employee_name = employee_name
        self.age = age
        self.salary = salary


class Manager(Employee):
    def __init__(self, employee_name, age, salary):
        super().__init__(employee_name, age, salary)


employee = Employee(employee_name="John Doe", age=25, salary=3000)
manager = Manager(employee_name="Alice", age=30, salary=5000)

print(employee.employee_name, employee.age, employee.salary)
print(manager.employee_name, manager.age, manager.salary)

import os
import functools
from pathlib import Path
import logging
from datetime import datetime

# Определяем рабочую директорию относительно домашнего каталога пользователя
base_dir = Path.home() / "stepik_application"  # Директория для приложения
log_dir = base_dir / "logs"  # Директория для логов
log_dir.mkdir(parents=True, exist_ok=True)  # Создаем папку для логов, если она не существует

# Переключаемся в рабочую директорию приложения
os.chdir(base_dir)
print("Рабочая директория:", os.getcwd())

# Создаем папку "application" при необходимости
app_dir = base_dir / "application"
app_dir.mkdir(parents=True, exist_ok=True)
os.chdir(app_dir)
print("Директория приложения:", os.getcwd())


class Logger:
    def __init__(self):
        self.loggers = {}

    def __call__(self, cls):
        """Декоратор для логирования методов класса."""
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                setattr(cls, attr_name, self.log_method(attr_value))
        return cls

    def get_logger(self, instance):
        if instance.name not in self.loggers:
            log_file_path = log_dir / f"{instance.name}_log.log"
            user_logger = logging.getLogger(instance.name)
            user_logger.setLevel(logging.INFO)
            if not user_logger.handlers:
                file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
                formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",
                                              datefmt="%Y-%m-%d %H:%M:%S")
                file_handler.setFormatter(formatter)
                user_logger.addHandler(file_handler)
            self.loggers[instance.name] = user_logger
        return self.loggers[instance.name]

    def log_method(self, method):
        """Декоратор для логирования вызовов метода"""
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            instance = args[0]
            logger = self.get_logger(instance)
            log_message = (f"Метод: {method.__name__}\nАргументы: {args[1:]}\nКлючевые аргументы: {kwargs}\n")
            logger.info(log_message)
            return method(*args, **kwargs)
        return wrapper


@Logger()
class User:
    def __init__(self, name: str, **kwargs) -> None:
        self.name = name
        self.user_dir = base_dir / "Users"  # Каталог для данных пользователей
        self.save_user_info(**kwargs)
        self.load()

    def _get_user_file_path(self) -> Path:
        return self.user_dir / f"{self.name}.txt"

    def load(self) -> None:
        user_file_path = self._get_user_file_path()
        if user_file_path.exists():
            with user_file_path.open("r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            key, value = line.strip().split("=", 1)
                            setattr(self, key.strip(), value.strip())
                        except ValueError:
                            logging.error(f"Ошибка при чтении строки: {line.strip()}. Пропуск.")
            logging.info(f"Данные для пользователя {self.name} загружены.")
        else:
            logging.warning(f"Файл для пользователя {self.name} не найден. Создается новый.")

    def save_user_info(self, **kwargs) -> None:
        self.user_dir.mkdir(exist_ok=True)
        user_file_path = self._get_user_file_path()
        current_data = {}
        if user_file_path.exists():
            with user_file_path.open("r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            key, value = line.strip().split("=", 1)
                            current_data[key.strip()] = value.strip()
                        except ValueError:
                            logging.error(f"Ошибка при чтении строки: {line.strip()}. Пропуск.")
        current_data["name"] = self.name
        for key, value in kwargs.items():
            current_data[key] = value
        with user_file_path.open("w", encoding="utf-8") as f:
            for key, value in current_data.items():
                f.write(f"{key}={value}\n")
        logging.info(f"Информация о пользователе {self.name} сохранена в файл.")

    def read_user_info(self) -> None:
        """Читает и выводит информацию о пользователе."""
        user_file_path = self._get_user_file_path()
        if user_file_path.exists():
            with user_file_path.open("r", encoding="utf-8") as f:
                print(f"Данные для пользователя {self.name}:")
                for line in f:
                    print(line.strip())
            logging.info(f"Данные для пользователя {self.name} выведены.")
        else:
            print(f"Файл пользователя {self.name} не найден.")
            logging.error(f"Файл пользователя {self.name} не найден.")

    def del_user_info(self, key: str) -> None:
        """
        Очищает значение по указанному ключу в файле пользователя, записывая пустую строку.
        """
        user_file_path = self._get_user_file_path()

        if key in vars(self):
            setattr(self, key, "")  # Обновляем значение на пустую строку

            # Чтение и перезапись файла
            if user_file_path.exists():
                with user_file_path.open("r", encoding="utf-8") as f:
                    lines = f.readlines()

                with user_file_path.open("w", encoding="utf-8") as f:
                    for line in lines:
                        if line.startswith(f"{key}="):
                            f.write(f"{key}=\n")  # Очищаем значение
                        else:
                            f.write(line)

                logging.info(
                    f"Значение для ключа {key} пользователя {self.name} очищено."
                )
            else:
                print(f"Файл пользователя {self.name} не найден.")
                logging.error(f"Файл пользователя {self.name} не найден.")
        else:
            print(f"Ключ {key} не найден у пользователя {self.name}.")
            logging.warning(f"Ключ {key} не найден у пользователя {self.name}.")

    def write_data(self, file_name: str, data: str) -> None:
        """Записывает данные в файл пользователя."""
        files_dir = Path("files") / "Users" / self.name
        files_dir.mkdir(
            parents=True, exist_ok=True
        )  # Создаем директорию, если не существует
        file_path = files_dir / file_name

        with file_path.open("a+", encoding="utf-8") as f:
            f.write(data + "\n")
            logging.info(f"Данные успешно записаны в {file_name}.")

    def read_data(self, file_name: str) -> str:
        """Читает данные из файла пользователя."""
        file_path = Path("files") / "Users" / self.name / file_name

        if file_path.exists():
            with file_path.open("r", encoding="utf-8") as f:
                data = f.read()
                print(f"Данные из файла {file_name}:\n{data}")
                logging.info(f"Данные из файла {file_name} успешно прочитаны.")
                return data
        else:
            print(f"Файл {file_name} не найден.")
            logging.error(f"Файл {file_name} не найден.")
            return ""


@Logger()
class Admin(User):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def read_data(self, file_name: str, user: str = None) -> str:
        """
        Читает данные из файла указанного пользователя. Если user не указан, используется текущий пользователь.
        """
        user = (
            user or self.name
        )  # Если user не передан, используется текущий пользователь
        files_dir = Path("files") / "Users" / user
        file_path = files_dir / file_name

        if file_path.exists() and file_path.is_file():
            with file_path.open("r", encoding="utf-8") as f:
                data = f.read()
                print(f"Данные из файла {file_name} пользователя {user}:\n{data}")
                return data
        else:
            print(f"Файл {file_name} не найден для пользователя {user}.")
            return ""

    def write_data(self, file_name: str, data: str, user: str = None) -> None:
        """
        Записывает данные в файл указанного пользователя. Если user не указан, используется текущий пользователь.
        """
        user = user or self.name
        files_dir = Path("files") / "Users" / user
        files_dir.mkdir(parents=True, exist_ok=True)
        file_path = files_dir / file_name

        with file_path.open("a+", encoding="utf-8") as f:
            f.write(data + "\n")
            print(f"Данные успешно записаны в файл {file_name} пользователя {user}")

    def read_logs(self, log_file_name="log.txt", user=None) -> str:
        """
        Читает логи указанного пользователя. Если user не указан, читается лог текущего пользователя.
        """
        user = user or self.name
        logs_dir = Path("logs")
        log_file_path = logs_dir / f"{user}_{log_file_name}"

        if log_file_path.exists() and log_file_path.is_file():
            with log_file_path.open("r", encoding="utf-8") as f:
                data = f.read()
                print(f"Лог-файл {log_file_name} пользователя {user}:\n{data}")
                return data
        else:
            print(f"Лог-файл {log_file_name} не найден для пользователя {user}.")
            return ""


class SuperAdmin(Admin):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def create_user(self, username, role=User, **kwargs):
        if issubclass(role, User) and not issubclass(role, Admin):
            return User(username, **kwargs)
        elif issubclass(role, Admin):
            return Admin(username, **kwargs)
        else:
            raise ValueError("Invalid role specified.")

    def del_user(self, username):
        user_file_path = Path("files") / "Users" / f"{username}.txt"
        if user_file_path.exists():
            os.remove(user_file_path)
            print(f"Пользователь {username} удален.")
            logging.info(f"Пользователь {username} удален.")
        else:
            print(f"Пользователь {username} не найден.")
            logging.error(f"Пользователь {username} не найден.")

    def change_user_info(self, username, **kwargs):
        user_file_path = Path("Users") / f"{username}.txt"
        if user_file_path.exists():
            try:
                with user_file_path.open("w", encoding="utf-8") as f:
                    f.write(f"name={username}\n")
                    for k, v in kwargs.items():
                        f.write(f"{k}={v}\n")
                print(f"Информация пользователя {username} успешно изменена.")
                logging.info(f"Информация пользователя {username} успешно изменена.")
            except Exception as e:
                print("Ошибка при изменении данных:", e)
                logging.error(
                    f"Ошибка при изменении данных пользователя {username}: {e}"
                )
        else:
            print(f"Пользователь {username} не найден.")
            logging.error(f"Пользователь {username} не найден.")

    def rename_file(self, file_path, new_name):
        try:
            new_file_path = Path(file_path).with_name(new_name)
            os.rename(file_path, new_file_path)
            print(f"Файл {file_path} переименован в {new_name}.")
            logging.info(f"Файл {file_path} переименован в {new_name}.")
        except Exception as e:
            print("Ошибка при переименовании файла:", e)
            logging.error(f"Ошибка при переименовании файла {file_path}: {e}")

    def rename_dir(self, dir_path, new_name):
        try:
            new_dir_path = Path(dir_path).parent / new_name
            os.rename(dir_path, new_dir_path)
            print(f"Директория {dir_path} переименована в {new_name}.")
            logging.info(f"Директория {dir_path} переименована в {new_name}.")
        except Exception as e:
            print("Ошибка при переименовании директории:", e)
            logging.error(f"Ошибка при переименовании директории {dir_path}: {e}")

    def create_log(self, data, user=None, log_file_name="log.txt"):
        if user is None:
            user = self.name
        logs_dir = Path("logs")
        log_file_path = logs_dir / f"{user}_{log_file_name}"
        logs_dir.mkdir(parents=True, exist_ok=True)
        try:
            with log_file_path.open("a", encoding="utf-8") as f:
                f.write(f"{data}\n")
            print(f"Лог записан в {log_file_path}.")
            logging.info(f"Лог записан в {log_file_path}.")
        except Exception as e:
            print("Ошибка при записи в лог-файл:", e)
            logging.error(f"Ошибка при записи в лог-файл {log_file_path}: {e}")

    def read_all_logs(self, log_file_name="log.txt"):
        logs_dir = Path("logs")
        log_file_path = logs_dir / log_file_name
        if log_file_path.exists() and log_file_path.is_file():
            try:
                with log_file_path.open("r", encoding="utf-8") as f:
                    data = f.read()
                    print(f"Лог-файл {log_file_name}:\n{data}")
                    return data
            except Exception as e:
                print("Ошибка при чтении данных:", e)
                logging.error(f"Ошибка при чтении данных из {log_file_path}: {e}")
                return ""
        else:
            print(f"Лог-файл {log_file_name} не найден.")
            logging.error(f"Лог-файл {log_file_name} не найден.")
            return ""


def main():
    while True:
        try:
            print("Добро пожаловать! Выберите права доступа:")
            print("1. Пользователь")
            print("2. Админ")
            print("3. Супер Админ")

            access_level = input("Введите номер вашего уровня доступа: ")
            name = input("введите имя пользователя: ")
            ui = input(
                "Введите дополнительные параметры, если хотите, иначе пропустите: "
            ).strip()

            skwargs = {}
            if ui:
                try:
                    skwargs = {k: v for s in ui.split() for k, v in [s.split('=', 1)]}
                except ValueError:
                    print("Ошибка: Параметры должны быть в формате ключ=значение.")
                    continue
            
            print(name, skwargs)
            if access_level == "1":
                user = User(name, **skwargs) if skwargs is not None else User(name)
                user_menu(user)
            elif access_level == "2":
                user = Admin(name, **skwargs)
                admin_menu(user)

            elif access_level == "3":
                user = SuperAdmin(name,**skwargs)
                superadmin_menu(user)
            else:
                print("Неверный выбор. Попробуйте снова.")
        except Exception as e:
            print(e)


def user_menu(user):
    while True:
        print("\nМеню пользователя:")
        print("1. Прочитать информацию о себе")
        print("2. Обновить информацию")
        print("3. Удалить информацию по ключу")
        print("4. Записать данные в файл")
        print("5. Прочитать данные из файла")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            user.read_user_info()
        elif choice == "2":
            key = input("Введите ключ для обновления: ")
            value = input("Введите новое значение: ")
            user.save_user_info(**{key: value})
        elif choice == "3":
            key = input("Введите ключ для удаления: ")
            user.del_user_info(key)
        elif choice == "4":
            file_name = input("Введите имя файла: ")
            data = input("Введите данные для записи: ")
            user.write_data(file_name, data)
        elif choice == "5":
            file_name = input("Введите имя файла: ")
            user.read_data(file_name)
        elif choice == "6":
            print("Выход из меню пользователя.")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


def admin_menu(user):
    while True:
        print("\nМеню админа:")
        print("1. Прочитать информацию о себе")
        print("2. Прочитать данные пользователя")
        print("3. Записать данные пользователя")
        print("4. Прочитать логи")
        print("5. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            user.read_user_info()
        elif choice == "2":
            username = input("Введите имя пользователя: ")
            file_name = input("Введите имя файла: ")
            user.read_data(file_name, username)
        elif choice == "3":
            username = input("Введите имя пользователя: ")
            file_name = input("Введите имя файла: ")
            data = input("Введите данные для записи: ")
            user.write_data(file_name, data, username)
        elif choice == "4":
            user.read_logs()
        elif choice == "5":
            print("Выход из меню админа.")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


def superadmin_menu(user):
    while True:
        print("\nМеню супер админа:")
        print("1. Создать нового пользователя")
        print("2. Удалить пользователя")
        print("3. Изменить информацию пользователя")
        print("4. Переименовать файл")
        print("5. Переименовать директорию")
        print("6. Создать лог")
        print("7. Прочитать все логи")
        print("8. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            username = input("Введите имя нового пользователя: ")
            role = input("Введите роль (User/Admin): ")
            if role.lower() == "admin":
                user.create_user(username, role=Admin)
            else:
                user.create_user(username, role=User)
        elif choice == "2":
            username = input("Введите имя пользователя для удаления: ")
            user.del_user(username)
        elif choice == "3":
            username = input("Введите имя пользователя для изменения информации: ")
            key = input("Введите ключ для изменения: ")
            value = input("Введите новое значение: ")
            user.change_user_info(username, **{key: value})
        elif choice == "4":
            file_path = input("Введите путь к файлу: ")
            new_name = input("Введите новое имя файла: ")
            user.rename_file(file_path, new_name)
        elif choice == "5":
            dir_path = input("Введите путь к директории: ")
            new_name = input("Введите новое имя директории: ")
            user.rename_dir(dir_path, new_name)
        elif choice == "6":
            data = input("Введите данные для лога: ")
            user.create_log(data)
        elif choice == "7":
            user.read_all_logs()
        elif choice == "8":
            print("Выход из меню супер админа.")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()

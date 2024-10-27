
# User Management System

Эта программа предоставляет систему управления пользователями с уровнями доступа, логированием и функционалом для сохранения и обновления информации о пользователях. Программа поддерживает различные уровни доступа: Пользователь, Админ и Супер Админ, каждый из которых имеет свои права и возможности.

## Установка

### Требования
- Python 3.6 или выше
- Модули, используемые в программе:
  - `os`
  - `functools`
  - `pathlib`
  - `logging`
  - `datetime`

### Запуск программы
1. Скачайте репозиторий с программой.
2. Откройте командную строку и перейдите в папку с программой.
3. Запустите программу с помощью команды:
   ```bash
   python <имя_файла>.py
   ```

## Использование

### Права доступа

Программа поддерживает три уровня доступа:

1. **Пользователь** – может читать, обновлять и удалять информацию о себе.
2. **Админ** – имеет доступ к чтению и записи данных пользователей, а также к логам.
3. **Супер Админ** – имеет полный доступ к данным пользователей и логам, может управлять пользователями (создавать и удалять их).

### Функциональные возможности

#### Доступно для всех пользователей:
- **Чтение информации** – Пользователь может просмотреть свои данные.
- **Обновление информации** – Пользователь может добавить или обновить свои данные.
- **Удаление данных** – Пользователь может удалить определенные данные по ключу.
- **Запись данных в файл** – Пользователь может записывать данные в отдельный файл.

#### Доступно для администраторов:
- **Чтение данных пользователя** – Администратор может просматривать данные о любом пользователе.
- **Запись данных пользователя** – Администратор может записывать данные для пользователя.
- **Чтение логов** – Администратор может просматривать лог-файлы определенных пользователей.

#### Доступно для супер администраторов:
- **Создание пользователя** – Создание нового пользователя с определенными данными.
- **Удаление пользователя** – Удаление данных пользователя.
- **Изменение информации пользователя** – Изменение информации о пользователе.
- **Переименование файлов и директорий** – Возможность переименовывать файлы и папки.
- **Создание и чтение всех логов** – Возможность создавать лог-файлы и читать их для любых пользователей.

## Структура проекта

- **User** – Класс, реализующий базовые функции пользователя.
- **Admin** – Класс, наследуемый от `User`, расширяющий его возможностями администратора.
- **SuperAdmin** – Класс, наследуемый от `Admin`, предоставляющий полный доступ и возможности по управлению пользователями.
- **Logger** – Декоратор для логирования вызовов методов, который записывает действия и аргументы функций в лог-файлы.

## Примеры

### Пример запуска

1. Запустите программу и выберите уровень доступа (например, «1» для пользователя).
2. Введите имя пользователя и дополнительные параметры, если это необходимо.
3. Введите номер нужного действия в меню.

```plaintext
Добро пожаловать! Выберите права доступа:
1. Пользователь
2. Админ
3. Супер Админ
Введите номер вашего уровня доступа: 1
Введите имя пользователя: Alex
Введите дополнительные параметры, если хотите, иначе пропустите: возраст=25 город=Москва
```

### Пример использования функций

#### Запись данных
Пользователь может записать данные в файл с помощью команды в меню:

```plaintext
Выберите действие: 4
Введите имя файла: data.txt
Введите данные для записи: Добро пожаловать в систему!
```

#### Чтение логов (для Админа)
Администратор может просматривать логи пользователей:

```plaintext
Выберите действие: 4
Введите имя файла логов: user_log.txt
```

## Логирование

Каждое действие пользователя логируется и сохраняется в файле `logs` в формате:
```plaintext
YYYY-MM-DD HH:MM:SS - Уровень - Сообщение
```
Пример:
```plaintext
2024-10-27 15:35:00 - INFO - Пользователь Alex записал данные в файл data.txt.
```

## Поддержка

Если у вас возникли вопросы или предложения по улучшению, пожалуйста, свяжитесь с разработчиком.

## Лицензия

Этот проект выпущен под MIT лицензией.

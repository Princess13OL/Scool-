-- Таблица Классы
CREATE TABLE Классы (
    ID_класса INTEGER PRIMARY KEY AUTOINCREMENT,
    Название_класса TEXT,
    Год_обучения INTEGER
);

-- Таблица Студенты
CREATE TABLE Студенты (
    ID_студента INTEGER PRIMARY KEY AUTOINCREMENT,
    ФИО TEXT,
    Дата_рождения DATE,
    Контактный_номер TEXT,
    Email TEXT,
    Класс_ID INTEGER,
    FOREIGN KEY (Класс_ID) REFERENCES Классы(ID_класса)
);

-- Таблица Учителя
CREATE TABLE Учителя (
    ID_учителя INTEGER PRIMARY KEY AUTOINCREMENT,
    ФИО TEXT,
    Предмет TEXT,
    Контактный_номер TEXT,
    Email TEXT
);

-- Таблица Родители
CREATE TABLE Родители (
    ID_родителя INTEGER PRIMARY KEY AUTOINCREMENT,
    ФИО TEXT,
    Контактный_номер TEXT,
    Email TEXT
);

-- Промежуточная таблица для связи Студенты и Родители (M:N)
CREATE TABLE Студенты_Родители (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Студент_ID INTEGER,
    Родитель_ID INTEGER,
    FOREIGN KEY (Студент_ID) REFERENCES Студенты(ID_студента),
    FOREIGN KEY (Родитель_ID) REFERENCES Родители(ID_родителя)
);

-- Таблица Расписание
CREATE TABLE Расписание (
    ID_расписания INTEGER PRIMARY KEY AUTOINCREMENT,
    Класс_ID INTEGER,
    Учитель_ID INTEGER,
    Предмет TEXT,
    Дата DATE,
    FOREIGN KEY (Класс_ID) REFERENCES Классы(ID_класса),
    FOREIGN KEY (Учитель_ID) REFERENCES Учителя(ID_учителя)
);

-- Таблица Оценки
CREATE TABLE Оценки (
    ID_оценки INTEGER PRIMARY KEY AUTOINCREMENT,
    Студент_ID INTEGER,
    Учитель_ID INTEGER,
    Предмет TEXT,
    Оценка INTEGER,
    Дата_выставления DATE,
    FOREIGN KEY (Студент_ID) REFERENCES Студенты(ID_студента),
    FOREIGN KEY (Учитель_ID) REFERENCES Учителя(ID_учителя)
);

-- Таблица Домашние задания
CREATE TABLE Домашние_задания (
    ID_задания INTEGER PRIMARY KEY AUTOINCREMENT,
    Студент_ID INTEGER,
    Учитель_ID INTEGER,
    Предмет TEXT,
    Описание TEXT,
    Дата_сдачи DATE,
    Статус TEXT CHECK(Статус IN ('выполнено', 'не выполнено')),
    FOREIGN KEY (Студент_ID) REFERENCES Студенты(ID_студента),
    FOREIGN KEY (Учитель_ID) REFERENCES Учителя(ID_учителя)
);

-- Таблица Уведомления
CREATE TABLE Уведомления (
    ID_уведомления INTEGER PRIMARY KEY AUTOINCREMENT,
    Родитель_ID INTEGER,
    Учитель_ID INTEGER,
    Сообщение TEXT,
    Дата_уведомления DATE,
    FOREIGN KEY (Родитель_ID) REFERENCES Родители(ID_родителя),
    FOREIGN KEY (Учитель_ID) REFERENCES Учителя(ID_учителя)
);
-- Добавление классов
INSERT INTO Классы (Название_класса, Год_обучения) VALUES ('10-A', 2023);
INSERT INTO Классы (Название_класса, Год_обучения) VALUES ('11-B', 2023);

-- Добавление студентов
INSERT INTO Студенты (ФИО, Дата_рождения, Контактный_номер, Email, Класс_ID) VALUES ('Иванов Иван Иванович', '2005-05-15', '+79991234567', 'ivanov@example.com', 1);
INSERT INTO Студенты (ФИО, Дата_рождения, Контактный_номер, Email, Класс_ID) VALUES ('Петров Петр Петрович', '2006-07-20', '+79992345678', 'petrov@example.com', 1);

-- Добавление учителей
INSERT INTO Учителя (ФИО, Предмет, Контактный_номер, Email) VALUES ('Сидорова Анна Владимировна', 'Математика', '+79993456789', 'sidorova@example.com');
INSERT INTO Учителя (ФИО, Предмет, Контактный_номер, Email) VALUES ('Козлов Дмитрий Сергеевич', 'Физика', '+79994567890', 'kozlov@example.com');

-- Добавление родителей
INSERT INTO Родители (ФИО, Контактный_номер, Email) VALUES ('Иванова Мария Петровна', '+79995678901', 'ivanova@example.com');
INSERT INTO Родители (ФИО, Контактный_номер, Email) VALUES ('Петрова Ольга Ивановна', '+79996789012', 'petrova@example.com');

-- Добавление связей Студенты-Родители
INSERT INTO Студенты_Родители (Студент_ID, Родитель_ID) VALUES (1, 1);
INSERT INTO Студенты_Родители (Студент_ID, Родитель_ID) VALUES (2, 2);

-- Добавление расписания
INSERT INTO Расписание (Класс_ID, Учитель_ID, Предмет, Дата) VALUES (1, 1, 'Математика', '2023-10-01');
INSERT INTO Расписание (Класс_ID, Учитель_ID, Предмет, Дата) VALUES (1, 2, 'Физика', '2023-10-02');

-- Добавление оценок
INSERT INTO Оценки (Студент_ID, Учитель_ID, Предмет, Оценка, Дата_выставления) VALUES (1, 1, 'Математика', 5, '2023-10-01');
INSERT INTO Оценки (Студент_ID, Учитель_ID, Предмет, Оценка, Дата_выставления) VALUES (2, 2, 'Физика', 4, '2023-10-02');

-- Добавление домашних заданий
INSERT INTO Домашние_задания (Студент_ID, Учитель_ID, Предмет, Описание, Дата_сдачи, Статус) VALUES (1, 1, 'Математика', 'Решить задачи на странице 45', '2023-10-05', 'не выполнено');
INSERT INTO Домашние_задания (Студент_ID, Учитель_ID, Предмет, Описание, Дата_сдачи, Статус) VALUES (2, 2, 'Физика', 'Подготовить доклад по теме "Электричество"', '2023-10-06', 'выполнено');

-- Добавление уведомлений
INSERT INTO Уведомления (Родитель_ID, Учитель_ID, Сообщение, Дата_уведомления) VALUES (1, 1, 'Ваш ребенок не сдал домашнее задание по математике.', '2023-10-03');
INSERT INTO Уведомления (Родитель_ID, Учитель_ID, Сообщение, Дата_уведомления) VALUES (2, 2, 'Ваш ребенок получил оценку 4 по физике.', '2023-10-04');
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Студент(db.Model):
    __tablename__ = 'Студенты'
    ID_студента = db.Column(db.Integer, primary_key=True)
    ФИО = db.Column(db.String, nullable=False)
    Дата_рождения = db.Column(db.Date, nullable=False)
    Контактный_номер = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False)
    Класс_ID = db.Column(db.Integer, db.ForeignKey('Классы.ID_класса'))

class Учитель(db.Model):
    __tablename__ = 'Учителя'
    ID_учителя = db.Column(db.Integer, primary_key=True)
    ФИО = db.Column(db.String, nullable=False)
    Предмет = db.Column(db.String, nullable=False)
    Контактный_номер = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False)

class Родитель(db.Model):
    __tablename__ = 'Родители'
    ID_родителя = db.Column(db.Integer, primary_key=True)
    ФИО = db.Column(db.String, nullable=False)
    Контактный_номер = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False)

class СтудентыРодители(db.Model):
    __tablename__ = 'Студенты_Родители'
    ID = db.Column(db.Integer, primary_key=True)
    Студент_ID = db.Column(db.Integer, db.ForeignKey('Студенты.ID_студента'))
    Родитель_ID = db.Column(db.Integer, db.ForeignKey('Родители.ID_родителя'))

class Расписание(db.Model):
    __tablename__ = 'Расписание'
    ID_расписания = db.Column(db.Integer, primary_key=True)
    Класс_ID = db.Column(db.Integer, db.ForeignKey('Классы.ID_класса'))
    Учитель_ID = db.Column(db.Integer, db.ForeignKey('Учителя.ID_учителя'))
    Предмет = db.Column(db.String, nullable=False)
    Дата = db.Column(db.Date, nullable=False)

class Оценка(db.Model):
    __tablename__ = 'Оценки'
    ID_оценки = db.Column(db.Integer, primary_key=True)
    Студент_ID = db.Column(db.Integer, db.ForeignKey('Студенты.ID_студента'))
    Учитель_ID = db.Column(db.Integer, db.ForeignKey('Учителя.ID_учителя'))
    Предмет = db.Column(db.String, nullable=False)
    Оценка = db.Column(db.Integer, nullable=False)
    Дата_выставления = db.Column(db.Date, nullable=False)

class ДомашнееЗадание(db.Model):
    __tablename__ = 'Домашние_задания'
    ID_задания = db.Column(db.Integer, primary_key=True)
    Студент_ID = db.Column(db.Integer, db.ForeignKey('Студенты.ID_студента'))
    Учитель_ID = db.Column(db.Integer, db.ForeignKey('Учителя.ID_учителя'))
    Предмет = db.Column(db.String, nullable=False)
    Описание = db.Column(db.String, nullable=False)
    Дата_сдачи = db.Column(db.Date, nullable=False)
    Статус = db.Column(db.String, nullable=False)

class Уведомление(db.Model):
    __tablename__ = 'Уведомления'
    ID_уведомления = db.Column(db.Integer, primary_key=True)
    Родитель_ID = db.Column(db.Integer, db.ForeignKey('Родители.ID_родителя'))
    Учитель_ID = db.Column(db.Integer, db.ForeignKey('Учителя.ID_учителя'))
    Сообщение = db.Column(db.String, nullable=False)
    Дата_уведомления = db.Column(db.Date, nullable=False)


class Класс(db.Model):
    __tablename__ = 'Классы'
    ID_класса = db.Column(db.Integer, primary_key=True)
    Название_класса = db.Column(db.String, unique=True, nullable=False)
    Год_обучения = db.Column(db.Integer, nullable=False)
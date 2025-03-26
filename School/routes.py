from flask import request, jsonify, render_template
from models import Класс, Студент, Учитель, Родитель, Расписание, Оценка, ДомашнееЗадание, Уведомление
from app import db

def init_routes(app, db):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/main')
    def main():
        return render_template('main.html')

    @app.route('/api/classes', methods=['GET'])
    def get_classes():
        classes = Класс.query.all()
        return jsonify([{'ID_класса': cls.ID_класса, 'Название_класса': cls.Название_класса, 'Год_обучения': cls.Год_обучения} for cls in classes])

    @app.route('/api/students', methods=['GET'])
    def get_students():
        students = Студент.query.all()
        return jsonify([{'ID_студента': student.ID_студента, 'ФИО': student.ФИО, 'Дата_рождения': student.Дата_рождения.isoformat(), 'Контактный_номер': student.Контактный_номер, 'Email': student.Email} for student in students])

    @app.route('/api/teachers', methods=['GET'])
    def get_teachers():
        teachers = Учитель.query.all()
        return jsonify([{'ID_учителя': teacher.ID_учителя, 'ФИО': teacher.ФИО, 'Предмет': teacher.Предмет, 'Контактный_номер': teacher.Контактный_номер, 'Email': teacher.Email} for teacher in teachers])

    @app.route('/api/schedule', methods=['GET'])
    def get_schedule():
        user_class = request.args.get('class')
        schedule = Расписание.query.filter_by(Класс_ID=user_class).all()
        return jsonify([{'ID_расписания': item.ID_расписания, 'Класс_ID': item.Класс_ID, 'Учитель_ID': item.Учитель_ID, 'Предмет': item.Предмет, 'Дата': item.Дата.isoformat()} for item in schedule])

    @app.route('/api/grades', methods=['GET'])
    def get_grades():
        user_class = request.args.get('class')
        grades = Оценка.query.filter_by(Класс_ID=user_class).all()
        return jsonify([{'ID_оценки': grade.ID_оценки, 'Студент_ID': grade.Студент_ID, 'Учитель_ID': grade.Учитель_ID, 'Предмет': grade.Предмет, 'Оценка': grade.Оценка, 'Дата_выставления': grade.Дата_выставления.isoformat()} for grade in grades])

    @app.route('/api/homework', methods=['GET'])
    def get_homework():
        user_class = request.args.get('class')
        homework = ДомашнееЗадание.query.filter_by(Класс_ID=user_class).all()
        return jsonify([{'ID_задания': hw.ID_задания, 'Студент_ID': hw.Студент_ID, 'Учитель_ID': hw.Учитель_ID, 'Предмет': hw.Предмет, 'Описание': hw.Описание, 'Дата_сдачи': hw.Дата_сдачи.isoformat(), 'Статус': hw.Статус} for hw in homework])

    @app.route('/api/notifications', methods=['GET'])
    def get_notifications():
        user_class = request.args.get('class')
        notifications = Уведомление.query.filter_by(Класс_ID=user_class).all()
        return jsonify([{'ID_уведомления': notification.ID_уведомления, 'Родитель_ID': notification.Родитель_ID, 'Учитель_ID': notification.Учитель_ID, 'Сообщение': notification.Сообщение, 'Дата_уведомления': notification.Дата_уведомления.isoformat()} for notification in notifications])

    @app.route('/api/grades', methods=['POST'])
    def add_grade():
            data = request.get_json()
            new_grade = Оценка(     
            Студент_ID=data['Студент_ID'],
             Учитель_ID=data['Учитель_ID'],
             Предмет=data['Предмет'],
            Оценка=data['Оценка'],
            Дата_выставления=data['Дата_выставления']
            )
            db.session.add(new_grade)
            db.session.commit()

            # Отправка уведомления родителю
            student = Студент.query.get(data['Студент_ID'])
            parent = Родитель.query.filter_by(ID_родителя=student.Родитель_ID).first()
            if parent:
                new_notification = Уведомление(
                    Родитель_ID=parent.ID_родителя,
                    Учитель_ID=data['Учитель_ID'],
                    Сообщение=f'Ваш ребенок получил оценку {data["Оценка"]} по предмету {data["Предмет"]}.',
                    Дата_уведомления=data['Дата_выставления']
                )
                db.session.add(new_notification)
                db.session.commit()

            return jsonify({'message': 'Оценка добавлена'}), 201

    @app.route('/api/homework', methods=['POST'])
    def add_homework():
            data = request.get_json()
            new_homework = ДомашнееЗадание(
                Студент_ID=data['Студент_ID'],
                Учитель_ID=data['Учитель_ID'],
                Предмет=data['Предмет'],
                Описание=data['Описание'],
                Дата_сдачи=data['Дата_сдачи'],
                Статус='не выполнено'
            )
            db.session.add(new_homework)
            db.session.commit()

            # Отправка уведомления родителю
            student = Студент.query.get(data['Студент_ID'])
            parent = Родитель.query.filter_by(ID_родителя=student.Родитель_ID).first()
            if parent:
                new_notification = Уведомление(
                    Родитель_ID=parent.ID_родителя,
                    Учитель_ID=data['Учитель_ID'],
                    Сообщение=f'Вашему ребенку задано домашнее задание по предмету {data["Предмет"]}.',
                    Дата_уведомления=data['Дата_сдачи']
                )
                db.session.add(new_notification)
                db.session.commit()

            return jsonify({'message': 'Домашнее задание добавлено'}), 201
        
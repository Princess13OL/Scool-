from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модели

class Уведомление(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ученик_id = db.Column(db.Integer, db.ForeignKey('ученик.id'))
    сообщение = db.Column(db.String, nullable=False)
    дата = db.Column(db.DateTime, default=datetime.utcnow)
class Ученик(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    имя = db.Column(db.String, nullable=False)
    класс = db.Column(db.Integer, nullable=False)

class Оценка(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ученик_id = db.Column(db.Integer, db.ForeignKey('ученик.id'))
    предмет = db.Column(db.String, nullable=False)
    оценка = db.Column(db.Integer, nullable=False)
class Учитель(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    имя = db.Column(db.String, nullable=False)
    пароль = db.Column(db.String, nullable=False)  # Пароль для входа
    предметы = db.Column(db.String, nullable=False)  # Список предметов через запятую
    классы = db.Column(db.String, nullable=False)  # Список классов через запятую

class Предмет(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    название = db.Column(db.String, nullable=False)

class Класс(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    номер = db.Column(db.Integer, nullable=False)
class Задание(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ученик_id = db.Column(db.Integer, db.ForeignKey('ученик.id'))
    предмет = db.Column(db.String, nullable=False)
    описание = db.Column(db.String, nullable=False)
class Расписание(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        класс = db.Column(db.Integer, nullable=False)  # Класс, для которого составлено расписание
        день_недели = db.Column(db.String, nullable=False)  # День недели (например, "Понедельник")
        предмет = db.Column(db.String, nullable=False)  # Название предмета
        время_начала = db.Column(db.String, nullable=False)  # Время начала урока (например, "09:00")
        время_окончания = db.Column(db.String, nullable=False)  # Время окончания урока (например, "09:45")


# Создание базы данных и тестовых данных


# Создание базы данных и тестовых данных
with app.app_context():
    try:
        db.create_all()
        print("База данных создана или уже существует")

        # Добавляем тестовых учеников
        if not Ученик.query.first():
            ученики = [
                Ученик(имя="Иван Иванов", класс=1),
                Ученик(имя="Петр Петров", класс=1),
                Ученик(имя="Сидор Сидоров", класс=1),
                Ученик(имя="Анна Аннова", класс=2),
                Ученик(имя="Мария Маринова", класс=2),
                Ученик(имя="Ольга Ольгова", класс=2),
            ]
            db.session.add_all(ученики)
            db.session.commit()
            print("Тестовые данные добавлены")

    except Exception as e:
        print(f"Ошибка: {e}")

   
# Маршрут для страницы директора
@app.route('/director')
def director():
    return render_template('director.html')




@app.route('/director/teachers')
def manage_teachers_page():
    return render_template('manage_teachers.html')
# Маршрут для отправки уведомления учителям
@app.route('/director/notify-teachers', methods=['GET', 'POST'])
def notify_teachers():
    if request.method == 'POST':
        сообщение = request.form.get('сообщение')
        # Логика отправки уведомления учителям
        return jsonify({'сообщение': 'Уведомление отправлено учителям'}), 200
    return render_template('notify_teachers.html')
@app.route('/director/teachers', methods=['GET', 'POST'])
def manage_teachers():
        if request.method == 'POST':
            данные = request.get_json()
            print("Полученные данные:", данные)  # Логируем данные
            новый_учитель = Учитель(
                имя=данные['имя'],
                пароль=данные['пароль'],
                предметы=','.join(данные['предметы']),
                классы=','.join(данные['классы'])
            )
            db.session.add(новый_учитель)
            db.session.commit()
            return jsonify({'сообщение': 'Учитель добавлен'}), 201
        учителя = Учитель.query.all()
        return jsonify([{
            'id': у.id,
            'имя': у.имя,
            'предметы': у.предметы.split(','),
            'классы': у.классы.split(',')
        } for у in учителя]), 200

# Маршрут для отправки уведомления родителям
@app.route('/director/notify-parents', methods=['GET', 'POST'])
def notify_parents():
    if request.method == 'POST':
        сообщение = request.form.get('сообщение')
        # Логика отправки уведомления родителям
        return jsonify({'сообщение': 'Уведомление отправлено родителям'}), 200
    return render_template('notify_parents.html')

# Маршрут для редактирования расписания
@app.route('/director/edit-schedule', methods=['GET', 'POST'])
def edit_schedule():
    if request.method == 'POST':
        данные = request.get_json()
        # Логика редактирования расписания
        return jsonify({'сообщение': 'Расписание обновлено'}), 200
    return render_template('edit_schedule.html')
    # Маршрут для удаления урока
@app.route('/api/schedule/<int:lesson_id>', methods=['DELETE'])
def delete_lesson(lesson_id):
        try:
            урок = Расписание.query.get_or_404(lesson_id)
            db.session.delete(урок)
            db.session.commit()
            return jsonify({'сообщение': 'Урок удален'}), 200
        except Exception as e:
            print(f"Ошибка при удалении урока: {e}")
            return jsonify({'ошибка': 'Произошла ошибка при удалении урока'}), 500

    # Маршрут для редактирования урока
@app.route('/api/schedule/<int:lesson_id>', methods=['PUT'])
def edit_lesson(lesson_id):
                try:
                    данные = request.get_json()
                    урок = Расписание.query.get_or_404(lesson_id)

                    # Проверка на конфликт времени
                    conflicting_lesson = Расписание.query.filter(
                        Расписание.id != lesson_id,  # Исключаем текущий урок из проверки
                        Расписание.класс == данные['класс'],
                        Расписание.день_недели == данные['день_недели']
                    ).filter(
                        (Расписание.время_начала <= данные['время_начала']) & (Расписание.время_окончания > данные['время_начала']) |
                        (Расписание.время_начала < данные['время_окончания']) & (Расписание.время_окончания >= данные['время_окончания']) |
                        (Расписание.время_начала >= данные['время_начала']) & (Расписание.время_окончания <= данные['время_окончания'])
                    ).first()

                    if conflicting_lesson:
                        return jsonify({'ошибка': 'В это время уже стоит урок'}), 400

                    # Обновляем данные урока
                    урок.класс = данные['класс']
                    урок.день_недели = данные['день_недели']
                    урок.предмет = данные['предмет']
                    урок.время_начала = данные['время_начала']
                    урок.время_окончания = данные['время_окончания']

                    db.session.commit()
                    return jsonify({'сообщение': 'Урок обновлен'}), 200
                except Exception as e:
                    print(f"Ошибка при редактировании урока: {e}")
                    return jsonify({'ошибка': 'Произошла ошибка при редактировании урока'}), 500
# Маршруты
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/student')
def student():
    return render_template('student.html')
@app.route('/schedule')
def schedule():
    return render_template('schedule.html')
@app.route('/parent')
def parent():
    return render_template('parent.html')
@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

# Получить оценки ученика

@app.route('/api/students', methods=['GET'])
def get_students():
    ученики = Ученик.query.all()
    return jsonify([{'id': у.id, 'имя': у.имя} for у in ученики])

@app.route('/api/grades/<int:student_id>', methods=['GET'])
def get_grades(student_id):
    оценки = Оценка.query.filter_by(ученик_id=student_id).all()
    return jsonify([{'предмет': о.предмет, 'оценка': о.оценка} for о in оценки])

@app.route('/api/tasks/<int:student_id>', methods=['GET'])
def get_tasks(student_id):
    задания = Задание.query.filter_by(ученик_id=student_id).all()
    return jsonify([{'предмет': з.предмет, 'описание': з.описание} for з in задания])
# Получить задания ученика

# Получить учеников по классу
@app.route('/api/students/<int:class_id>', methods=['GET'])
def get_students_by_class(class_id):
    ученики = Ученик.query.filter_by(класс=class_id).all()
    return jsonify([{'id': у.id, 'имя': у.имя} for у in ученики])
# Добавить оценку (для учителя)
@app.route('/api/grades', methods=['POST'])
def add_grade():
    данные = request.get_json()
    новая_оценка = Оценка(
        ученик_id=данные['ученик_id'],
        предмет=данные['предмет'],
        оценка=данные['оценка']
    )
    db.session.add(новая_оценка)
    db.session.commit()
    return jsonify({'сообщение': 'Оценка добавлена'}), 201

# Добавить задание (для учителя)
# Добавить задание для всего класса
@app.route('/api/class-tasks', methods=['POST'])
def add_class_task():
    данные = request.get_json()
    ученики = Ученик.query.filter_by(класс=данные['класс']).all()
    for ученик in ученики:
        новое_задание = Задание(
            ученик_id=ученик.id,
            предмет=данные['предмет'],
            описание=данные['описание']
        )
        db.session.add(новое_задание)
    db.session.commit()
    return jsonify({'сообщение': 'Задание добавлено для всего класса'}), 201
@app.route('/api/schedule', methods=['GET'])
def get_all_schedule():
        try:
            расписание = Расписание.query.all()
            return jsonify([{
                'id': р.id,
                'класс': р.класс,
                'день_недели': р.день_недели,
                'предмет': р.предмет,
                'время_начала': р.время_начала,
                'время_окончания': р.время_окончания
            } for р in расписание])
        except Exception as e:
            print(f"Ошибка при получении расписания: {e}")
            return jsonify({'ошибка': 'Произошла ошибка при загрузке расписания'}), 500
@app.route('/api/schedule/<int:class_id>', methods=['GET'])
def get_schedule(class_id):
    try:
        if not class_id:
            return jsonify({'ошибка': 'Не указан class_id'}), 400

        расписание = Расписание.query.filter_by(класс=class_id).all()
        if not расписание:
            return jsonify({'ошибка': 'Расписание для указанного класса не найдено'}), 404

        return jsonify([{
            'день_недели': р.день_недели,
            'предмет': р.предмет,
            'время_начала': р.время_начала,
            'время_окончания': р.время_окончания
        } for р in расписание])
    except Exception as e:
        print(f"Ошибка при получении расписания для класса {class_id}: {e}")
        return jsonify({'ошибка': 'Произошла ошибка при получении расписания'}), 500

@app.route('/api/schedule', methods=['POST'])
def add_schedule():
    try:
        данные = request.get_json()
        класс = данные['класс']
        день_недели = данные['день_недели']
        время_начала = данные['время_начала']
        время_окончания = данные['время_окончания']

        # Проверка на конфликт времени
        conflicting_lesson = Расписание.query.filter_by(
            класс=класс,
            день_недели=день_недели
        ).filter(
            (Расписание.время_начала <= время_начала) & (Расписание.время_окончания > время_начала) |
            (Расписание.время_начала < время_окончания) & (Расписание.время_окончания >= время_окончания) |
            (Расписание.время_начала >= время_начала) & (Расписание.время_окончания <= время_окончания)
        ).first()

        if conflicting_lesson:
            return jsonify({'ошибка': 'В это время уже стоит урок'}), 400

        новое_расписание = Расписание(
            класс=класс,
            день_недели=день_недели,
            предмет=данные['предмет'],
            время_начала=время_начала,
            время_окончания=время_окончания
        )
        db.session.add(новое_расписание)
        db.session.commit()
        return jsonify({'сообщение': 'Урок добавлен'}), 201
    except Exception as e:
        print(f"Ошибка при добавлении урока: {e}")
        return jsonify({'ошибка': 'Произошла ошибка при добавлении урока'}), 500
# Отправить сообщение родителю
@app.route('/api/notifications', methods=['POST'])
def send_notification():
        данные = request.get_json()
        новое_сообщение = Уведомление(
            ученик_id=данные['ученик_id'],
            сообщение=данные['сообщение']
        )
        db.session.add(новое_сообщение)
        db.session.commit()
        return jsonify({'сообщение': 'Уведомление отправлено'}), 201

@app.route('/api/notifications/<int:student_id>', methods=['GET'])
def get_notifications(student_id):
        уведомления = Уведомление.query.filter_by(ученик_id=student_id).all()
        return jsonify([{'сообщение': у.сообщение, 'дата': у.дата} for у in уведомления])


with app.app_context():
    # Добавляем тестовые оценки
  if not Оценка.query.first():
    оценки = [
        Оценка(ученик_id=1, предмет="Математика", оценка=5),
        Оценка(ученик_id=1, предмет="Русский", оценка=4),
        ]
    db.session.add_all(оценки)
    db.session.commit()
      


    # Добавляем тестовое расписание
    if not Расписание.query.first():
        расписание = [
            Расписание(класс=1, день_недели="Понедельник", предмет="Математика", время_начала="09:00", время_окончания="09:45"),
            Расписание(класс=1, день_недели="Понедельник", предмет="Русский", время_начала="10:00", время_окончания="10:45"),
            Расписание(класс=2, день_недели="Понедельник", предмет="Литература", время_начала="09:00", время_окончания="09:45"),
        ]
        db.session.add_all(расписание)
        db.session.commit()
        print("Тестовое расписание добавлено")
    # Добавляем тестовые задания
  if not Задание.query.first():
        задания = [ Задание(ученик_id=1, предмет="Математика", описание="Решить задачи на стр. 10"),
            Задание(ученик_id=1, предмет="Русский", описание="Написать сочинение"),
        ]
        db.session.add_all(задания)
        db.session.commit()
      
  if not Уведомление.query.first():
                уведомления = [
                    Уведомление(ученик_id=1, сообщение="Пожалуйста, проверьте домашнее задание."),
                    Уведомление(ученик_id=1, сообщение="Родительское собрание в пятницу."),
                ]
                db.session.add_all(уведомления)
                db.session.commit()
if __name__ == '__main__':
        app.run(debug=True)

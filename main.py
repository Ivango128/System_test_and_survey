from flask import Flask, render_template, url_for, request, redirect, session, send_from_directory
from first_power import laad_dotenv_first_power, load_dotenv_SK
from control_BD import MyBD
from hesh import get_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = load_dotenv_SK()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        password_bd = my_bd.get_password_for_login(login)
        if login == 'admin' and get_hash(password) == password_admin:
            session['admin'] = True
            return redirect(url_for('admin'))
        try:
            if password_bd == password:
                session['isAuthorized'] = True
                return redirect(url_for('index'))
            else:
                return render_template('uthorized_error.html')
        except:
            return render_template('uthorized_error.html')
    else:
        if 'isAuthorized' in session and session['isAuthorized']:
            return render_template('index.html')
        else:
            session['isAuthorized'] = False
            return render_template('uthorized.html')

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if 'admin' in session and session['admin']:
        table_interviewer_all = my_bd.get_interviewer_all()
        print(table_interviewer_all)
        return render_template('admin.html', interviewers=table_interviewer_all)
    else:
        return redirect(url_for('index'))

@app.route('/create-report')
def create_report():
    return render_template('create-report.html')

@app.route('/quit')
def quit():
    session.clear()
    return redirect(url_for('index'))

@app.route('/create-report/<report>')
def get_report(report):
    return send_from_directory(directory='reports', path=report)

@app.route('/create-test', methods=['POST', 'GET'])
def create_test():
    if request.method == "POST":
        title_test = request.form['input__title__create__quiz']
        description_test = request.form['input__description__create__quiz']
        # session["curent_test"] = 1
        isTitleInBD = my_bd.save_title_quiz(title_test, description_test, 'test')
        if isTitleInBD:
            # делаем запрос на ид викторины, потом в сесию присваиваем значение текущей викторины
            return redirect(url_for('questions_test_create', title_test=title_test, id=1))
        else:
            return render_template('create-quiz-error.html')

    else:
        return render_template('create-quiz.html', type='теста')

@app.route('/create-test/questions<title_test>/<int:id>', methods=['POST', 'GET'])
def questions_test_create(title_test, id):
    if request.method == "POST":
        id_question = session['id_questions']
        question_data = request.form.to_dict()
        print(question_data)
        question_from_data = question_data['question']
        id_question_from_data = -1
        is_one_list_from_data = False
        is_closed_question_from_data = False
        right_answer_from_data = 'NoN'
        numbers_right_answer_from_data = [-1]
        answer_options_from_data = ['NoN']

        if question_data['is_closed_question'] == 'True':
            is_closed_question_from_data = True
            numbers_right_answer_from_data.clear()
            answer_options_from_data.clear()
        else:
            is_closed_question_from_data = False
            right_answer_from_data = question_data['right_answer']

        for key in question_data:

            if is_closed_question_from_data:

                if question_data['is_one_list'] == 'True':
                    is_one_list_from_data = True
                else:
                    is_one_list_from_data = False

                if 'right_answer' in key and is_one_list_from_data:
                    print('work!')
                    numbers_right_answer_from_data.append(int(question_data['right_answer']))
                if 'right_answer' in key and not is_one_list_from_data:
                    numbers_right_answer_from_data.append(int(key.split('/')[1]))

                if 'answer' in key and not ('right_answer' in key):
                    answer_options_from_data.append(question_data[key])

            if 'id_question' in key:
                id_question_from_data = int(key.split('/')[1])


        print(id_question_from_data, id_question)
        if id_question_from_data == id_question:
            session['id_questions'] += 1
            print('Вопрос:', question_from_data)
            print('Закрытый:', is_closed_question_from_data)
            print('Один верный:', is_one_list_from_data)
            print('Номера верных:', numbers_right_answer_from_data)
            print('Варианты ответов', answer_options_from_data)
            print('Один правельный:', right_answer_from_data)

            id_answers_from_bd = my_bd.save_answers_options(answer_options_from_data, numbers_right_answer_from_data, right_answer_from_data)
            print(id_answers_from_bd)

            return redirect(url_for('questions_test_create', title_test=title_test, id=session['id_questions']))
        else:
            print('Error ...')
            return redirect(url_for('questions_test_create', title_test=title_test, id=session['id_questions']))
    else:
        session['id_questions'] = id
        return render_template('questions-test.html', title_test=title_test, id=session['id_questions'])

if __name__ == '__main__':
    host_bd, port_bd, user_bd, password_bd, dbname_bd, password_admin = laad_dotenv_first_power()
    my_bd = MyBD(host=host_bd, port=port_bd, user=user_bd, password=password_bd, dbname=dbname_bd)
    app.run(debug=True)

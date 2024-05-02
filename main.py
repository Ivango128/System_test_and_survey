from flask import Flask, render_template, url_for, request, redirect, session, send_file, send_from_directory
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
    #report_file_pdf = 'reports/'+report
    print(report)
    return send_from_directory(directory='reports', path=report)

@app.route('/create-test', methods=['POST', 'GET'])
def create_test():
    if request.method == "POST":
        title_test = request.form['input__title__create__quiz']
        description_test = request.form['input__description__create__quiz']
        #session["curent_test"] = 1
        isTitleInBD = my_bd.save_title_quiz(title_test, description_test, 'test')
        print(request.form.to_dict())
        if isTitleInBD:
            return redirect(url_for('questions_test_create', title_test=title_test, id=1))
        else:
            return render_template('create-quiz-error.html')

    else:
        return render_template('create-quiz.html', type='теста')

@app.route('/create-test/questions<title_test>/<int:id>', methods=['POST', 'GET'])
def questions_test_create(title_test, id):
    if request.method == "POST":
        session['id_questions'] +=1
        return render_template('questions-test.html', title_test=title_test, id=session['id_questions'])
    else:
        session['id_questions'] = 1
        return render_template('questions-test.html', title_test=title_test, id=session['id_questions'])

if __name__ == '__main__':
    host_bd, port_bd, user_bd, password_bd, dbname_bd, password_admin = laad_dotenv_first_power()
    my_bd = MyBD(host=host_bd, port=port_bd, user=user_bd, password=password_bd, dbname=dbname_bd)
    app.run(debug=True)
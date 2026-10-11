from flask import Flask, render_template, request
import mysql.connector as ms

app = Flask(__name__)

def get_db():
    return ms.connect(host="localhost", user="root", password='bhumi123', database='delightsun')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/add_patient', methods=['GET','POST'])
def add_patient():
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        mobile = request.form['mobile']
        cn = get_db()
        cur = cn.cursor()
        cur.execute("insert into patients(name,age,city,mobile) values(%s,%s,%s,%s)",(name,age,city,mobile))
        cn.commit()
        msg = '✅ Patient Added Successfully!'
    return render_template('add_patient.html', msg=msg)

@app.route('/patients')
def patients():
    cn = get_db()
    cur = cn.cursor()
    cur.execute("select * from patients")
    rec = cur.fetchall()
    return render_template('patients.html', patients=rec)

@app.route('/add_doctor', methods=['GET','POST'])
def add_doctor():
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        dep = request.form['department']
        age = request.form['age']
        city = request.form['city']
        mobile = request.form['mobile']
        fees = request.form['fees']
        salary = request.form['salary']
        cn = get_db()
        cur = cn.cursor()
        cur.execute("insert into doctors(name,department,age,city,mobile,fees,salary) values(%s,%s,%s,%s,%s,%s,%s)",
                    (name,dep,age,city,mobile,fees,salary))
        cn.commit()
        msg = '✅ Doctor Added Successfully!'
    return render_template('add_doctor.html', msg=msg)

@app.route('/doctors')
def doctors():
    cn = get_db()
    cur = cn.cursor()
    cur.execute("select * from doctors")
    rec = cur.fetchall()
    return render_template('doctors.html', doctors=rec)


@app.route('/hospital_info')
def hospital_info():
    return render_template('hospital_info.html')

@app.route('/appointment', methods=['GET','POST'])
def appointment():
    msg = ''
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        department = request.form['department']
        date = request.form['date']
        cn = get_db()
        cur = cn.cursor()
        cur.execute("create table if not exists appointments(aid int primary key AUTO_INCREMENT, patient_name varchar(65), doctor_name varchar(56), department varchar(45), date varchar(20), status varchar(20) default 'Pending')")
        cur.execute("insert into appointments(patient_name,doctor_name,department,date) values(%s,%s,%s,%s)",
                    (patient_name,doctor_name,department,date))
        cn.commit()
        msg = '✅ Appointment Booked Successfully!'
    cn = get_db()
    cur = cn.cursor()
    try:
        cur.execute("select * from appointments")
        appointments = cur.fetchall()
    except:
        appointments = []
    return render_template('appointment.html', msg=msg, appointments=appointments)

@app.route('/view_appointments')
def view_appointments():
    cn = get_db()
    cur = cn.cursor()
    try:
        cur.execute("select * from appointments")
        appts = cur.fetchall()
    except:
        appts = []
    return render_template('view_appointments.html', appointments=appts)

if __name__ == '__main__':
    app.run(debug=True)
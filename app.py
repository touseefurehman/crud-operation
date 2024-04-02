from flask import Flask, render_template, request, flash, url_for, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)
app.secret_key = '1231243cssfsdgdszewdf$#%$#543'
app.config['UPLOAD_FOLDER'] = 'media/'
app.config['MEDIA_FOLDER'] = 'media/'

# migrate = Migrate(app, db)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True) #primary key is trure because its not nullable
    first_name = db.Column(db.String(100), nullable=False)   #primary key is flase because its nullable
    last_name = db.Column(db.String(100), nullable=False)   #primary key is flase because its nullable
    photo_filename = db.Column(db.String(255))    
    file_path = db.Column(db.String(255), nullable=True)    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

def create_tables():
    with app.app_context():
        db.create_all()

create_tables()


@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(app.config['MEDIA_FOLDER'], filename)


@app.route('/')
def index():
    student = Student.query.all()
    
    context = {
        "student":student
    }
    return render_template("index.html", context=context)

@app.route('/add-student/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        photo = request.files['photo']  # Get the uploaded photo
        print("fsdfsdf", photo)
        # Save the photo to a secure filename
        if photo:
            filename = secure_filename(photo.filename)
            path =  os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(path)
        new_student = Student(first_name=first_name, last_name=last_name, photo_filename=filename, file_path=path)
        

        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully')
        return render_template("add.html")
    return render_template("add.html")



@app.route('/delete/<int:id>', methods=['GET'])
def delete_record(id):
    record = Student.query.get_or_404(id)
    print(record)
    record.delete()
    flash("Student Delted Successfully!")
    return redirect(url_for('index'))

@app.route('/edit-student/<int:id>', methods=['GET', 'POST'])
def edit_record(id):
    record = Student.query.get_or_404(id)
    print(record)
    if request.method == 'POST':
        record.first_name = request.form['first_name']
        record.last_name = request.form['last_name']
        
        if 'photo' in request.files:
            photo = request.files['photo']
            # Check if a file was selected
            if photo.filename != '':
                # Save the photo to a secure filename
                filename = secure_filename(photo.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                photo.save(path)
                # Update the student's photo information
                record.photo_filename = filename
                record.file_path = path
        db.session.commit()
        flash('Student Updated successfully')
        return redirect(url_for('index'))

    return render_template("edit.html", student=record)

if __name__ == '__main__':
    app.run(debug=True)

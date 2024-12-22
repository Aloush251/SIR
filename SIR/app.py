from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# إنشاء اتصال بقاعدة البيانات
def get_db_connection():
    conn = sqlite3.connect('questions.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    query = ''
    if request.method == 'POST':
        query = request.form['query']
        algorithm = request.form['algorithm']
        
        conn = get_db_connection()
        if algorithm == "Boolean":
            results = conn.execute('SELECT id, question, answer FROM questions WHERE question LIKE ?', ('%' + query + '%',)).fetchall()
        elif algorithm == "Extended Boolean":
            results = conn.execute('SELECT id, question, answer FROM questions WHERE question LIKE ?', ('%' + query + '%',)).fetchall()
        elif algorithm == "Vector Space":
            results = conn.execute('SELECT id, question, answer FROM questions WHERE question LIKE ?', ('%' + query + '%',)).fetchall()
        conn.close()

    return render_template('index.html', results=results, query=query)

if __name__ == '__main__':
    app.run(debug=True)
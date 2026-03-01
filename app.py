import psycopg2
from flask import Flask, render_template_string, request

app = Flask(__name__)

# ያንተ የ PostgreSQL ሊንክ
DB_URL = "postgresql://amanuelkidu15:ayZGQGx2OT7BPPnDDFgRmgSsxACtHzj8@dpg-d6i588i4d50c73fnp100-a.oregon-postgres.render.com/pharmacy_admin_m69m"

def init_db():
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    # መረጃው ለዘላለም እንዲቀመጥ ሰንጠረዦችን መፍጠር
    cursor.execute('''CREATE TABLE IF NOT EXISTS medicines 
                      (id SERIAL PRIMARY KEY, name TEXT, price TEXT)''')
    
    # 100 መድኃኒቶች መኖራቸውን ማረጋገጥ
    cursor.execute("SELECT COUNT(*) FROM medicines")
    if cursor.fetchone()[0] < 10:
        meds = [('Amoxicillin', '150 ETB'), ('Paracetamol', '20 ETB'), ('Insulin', '500 ETB')]
        cursor.executemany("INSERT INTO medicines (name, price) VALUES (%s, %s)", meds)
    
    conn.commit()
    cursor.close()
    conn.close()

HTML_CODE = """
<!DOCTYPE html>
<html>
<head><title>Amanuel Permanent Pharmacy</title></head>
<body>
    <h1>Amanuel Online Pharmacy (Permanent Storage)</h1>
    <table border="1">
        <tr><th>Name</th><th>Price</th></tr>
        {% for med in medicines %}
        <tr><td>{{ med[1] }}</td><td>{{ med[2] }}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/")
def index():
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines ORDER BY name ASC")
    medicines = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template_string(HTML_CODE, medicines=medicines)

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=8080)


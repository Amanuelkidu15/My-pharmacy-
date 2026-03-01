import sqlite3
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# ዳታቤዝ መፍጠር እና ዋና ዋና መድኃኒቶችን መመዝገብ
def init_db():
    conn = sqlite3.connect('pharmacy.db')
    cursor = conn.cursor()
    # የመድኃኒት ሰንጠረዥ
    cursor.execute('''CREATE TABLE IF NOT EXISTS medicines 
                      (id INTEGER PRIMARY KEY, name TEXT, price TEXT)''')
    
    # የትዕዛዝ ሰንጠረዥ
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                      (id INTEGER PRIMARY KEY, customer_name TEXT, med_name TEXT, phone TEXT)''')
    
    # በብዛት የሚፈለጉ መድኃኒቶች ዝርዝር
    essential_meds = [
        ('Amoxicillin 500mg', '150 ETB'),
        ('Paracetamol 500mg', '20 ETB'),
        ('Azithromycin 500mg', '300 ETB'),
        ('Ciprofloxacin 500mg', '250 ETB'),
        ('Diclofenac 50mg', '80 ETB'),
        ('Omeprazole 20mg', '120 ETB'),
        ('Metformin 500mg', '110 ETB'),
        ('Amlodipine 5mg', '140 ETB'),
        ('Albendazole 400mg', '50 ETB'),
        ('ORS (Oral Rehydration)', '15 ETB')
    ]
    
    # ዝርዝሩ በዳታቤዙ ውስጥ መኖሩን ማረጋገጥ
    cursor.execute("SELECT COUNT(*) FROM medicines")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO medicines (name, price) VALUES (?, ?)", essential_meds)
    
    conn.commit()
    conn.close()

HTML_CODE = """
<!DOCTYPE html>
<html>
<head><title>Amanuel Pharmacy</title></head>
<body>
    <h1>Amanuel Online Pharmacy</h1>
    <h3>Available Medicines (Alphabetical)</h3>
    <table border="1">
        <tr><th>Name</th><th>Price</th></tr>
        {% for med in medicines %}
        <tr><td>{{ med[1] }}</td><td>{{ med[2] }}</td></tr>
        {% endfor %}
    </table>
    <hr>
    <h3>Order Now</h3>
    <form method="POST">
        Name: <input type="text" name="customer_name" required><br>
        Medicine: <input type="text" name="med_name" required><br>
        Phone: <input type="text" name="phone" required><br>
        <button type="submit">Place Order</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect('pharmacy.db')
    cursor = conn.cursor()
    
    if request.method == "POST":
        c_name = request.form.get("customer_name")
        m_name = request.form.get("med_name")
        phone = request.form.get("phone")
        cursor.execute("INSERT INTO orders (customer_name, med_name, phone) VALUES (?, ?, ?)", 
                       (c_name, m_name, phone))
        conn.commit()
    
    # መድኃኒቶችን በፊደል ቅደም ተከተል ማውጣት
    cursor.execute("SELECT * FROM medicines ORDER BY name ASC")
    medicines = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_CODE, medicines=medicines)

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=8080)


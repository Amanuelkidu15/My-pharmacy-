import sqlite3
from flask import Flask, render_template_string, request

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('pharmacy.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS medicines (id INTEGER PRIMARY KEY, name TEXT, price TEXT)''')
    
    # 100 ዋና ዋና መድኃኒቶች ዝርዝር (ምሳሌ)
    meds_100 = [
        ('Abacavir', '450 ETB'), ('Acetazolamide', '120 ETB'), ('Acyclovir', '200 ETB'),
        ('Albendazole', '45 ETB'), ('Albuterol', '320 ETB'), ('Allopurinol', '150 ETB'),
        ('Alprazolam', '180 ETB'), ('Amiodarone', '400 ETB'), ('Amitriptyline', '90 ETB'),
        ('Amlodipine', '130 ETB'), ('Amoxicillin', '140 ETB'), ('Ampicillin', '125 ETB'),
        ('Artesunate', '250 ETB'), ('Aspirin', '15 ETB'), ('Atropine', '85 ETB'),
        ('Azithromycin', '280 ETB'), ('Bacitracin', '110 ETB'), ('Beclomethasone', '350 ETB'),
        ('Benzathine Penicillin', '100 ETB'), ('Bisoprolol', '160 ETB'), ('Calamine', '70 ETB'),
        ('Calcium Gluconate', '210 ETB'), ('Captopril', '115 ETB'), ('Carbamazepine', '190 ETB'),
        ('Ceftriaxone', '240 ETB'), ('Cephalexin', '175 ETB'), ('Chloramphenicol', '130 ETB'),
        ('Chloroquine', '60 ETB'), ('Chlorpromazine', '145 ETB'), ('Cimetidine', '95 ETB'),
        ('Ciprofloxacin', '220 ETB'), ('Clindamycin', '310 ETB'), ('Clotrimazole', '80 ETB'),
        ('Cloxacillin', '140 ETB'), ('Codeine', '200 ETB'), ('Colchicine', '260 ETB'),
        ('Dapsone', '120 ETB'), ('Dexamethasone', '55 ETB'), ('Diazepam', '90 ETB'),
        ('Diclofenac', '75 ETB'), ('Digoxin', '180 ETB'), ('Doxycycline', '135 ETB'),
        ('Enalapril', '110 ETB'), ('Epinephrine', '400 ETB'), ('Ergotamine', '215 ETB'),
        ('Erythromycin', '165 ETB'), ('Ethambutol', '190 ETB'), ('Ferrous Sulfate', '40 ETB'),
        ('Fluconazole', '230 ETB'), ('Fluoxetine', '270 ETB'), ('Furosemide', '85 ETB'),
        ('Gentamicin', '120 ETB'), ('Glibenclamide', '105 ETB'), ('Griseofulvin', '155 ETB'),
        ('Haloperidol', '140 ETB'), ('Heparin', '500 ETB'), ('Hydralazine', '195 ETB'),
        ('Hydrochlorothiazide', '95 ETB'), ('Hydrocortisone', '130 ETB'), ('Ibuprofen', '65 ETB'),
        ('Insulin (Regular)', '450 ETB'), ('Iodine', '40 ETB'), ('Ipratropium', '380 ETB'),
        ('Isoniazid', '115 ETB'), ('Isosorbide', '225 ETB'), ('Ketoconazole', '185 ETB'),
        ('Lidocaine', '140 ETB'), ('Loperamide', '50 ETB'), ('Loratadine', '90 ETB'),
        ('Magnesium Sulfate', '160 ETB'), ('Mebendazole', '45 ETB'), ('Metformin', '110 ETB'),
        ('Methyldopa', '200 ETB'), ('Metoclopramide', '75 ETB'), ('Metronidazole', '85 ETB'),
        ('Morphine', '350 ETB'), ('Multivitamin', '120 ETB'), ('Naloxone', '450 ETB'),
        ('Neomycin', '130 ETB'), ('Nifedipine', '145 ETB'), ('Nitrofurantoin', '210 ETB'),
        ('Nystatin', '105 ETB'), ('Omeprazole', '115 ETB'), ('ORS', '15 ETB'),
        ('Oxytocin', '280 ETB'), ('Paracetamol', '20 ETB'), ('Penicillin V', '100 ETB'),
        ('Phenobarbital', '135 ETB'), ('Phenytoin', '160 ETB'), ('Prednisolone', '70 ETB'),
        ('Promethazine', '85 ETB'), ('Propranolol', '125 ETB'), ('Pyrazinamide', '150 ETB'),
        ('Quinine', '240 ETB'), ('Ranitidine', '110 ETB'), ('Rifampicin', '200 ETB'),
        ('Salbutamol Inhaler', '350 ETB'), ('Silver Sulfadiazine', '180 ETB'), ('Spironolactone', '210 ETB'),
        ('Tetracycline', '95 ETB'), ('Tramadol', '150 ETB'), ('Vitamin K', '130 ETB'), ('Warfarin', '190 ETB')
    ]
    
    cursor.execute("SELECT COUNT(*) FROM medicines")
    if cursor.fetchone()[0] < 50: # ዝርዝሩ ካልሞላ እንዲሞላ
        cursor.executemany("INSERT INTO medicines (name, price) VALUES (?, ?)", meds_100)
    
    conn.commit()
    conn.close()

init_db()

HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
    <title>Amanuel 100+ Pharmacy</title>
    <style>
        body { font-family: Arial; margin: 20px; background-color: #f4f4f4; }
        table { width: 100%; border-collapse: collapse; background: white; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
        th { background-color: #007bff; color: white; }
    </style>
</head>
<body>
    <h1>Amanuel Pharmacy Inventory (100+ Meds)</h1>
    <table>
        <tr><th>ID</th><th>Medicine Name</th><th>Price</th></tr>
        {% for med in medicines %}
        <tr><td>{{ med[0] }}</td><td>{{ med[1] }}</td><td>{{ med[2] }}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/")
def index():
    conn = sqlite3.connect('pharmacy.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medicines ORDER BY name ASC")
    medicines = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_CODE, medicines=medicines)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)



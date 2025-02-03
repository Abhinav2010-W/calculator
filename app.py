from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_income_tax(age, total_income, regime, salaried, deductions=0):
    tax = 0
    taxable_income = total_income - (50000 if salaried else 0) - deductions
    taxable_income = max(taxable_income, 0)
    
    if regime == 'old':
        if age < 60:
            exemption_limit = 250000
        elif 60 <= age < 80:
            exemption_limit = 300000
        else:
            exemption_limit = 500000
        
        taxable_amount = max(taxable_income - exemption_limit, 0)
        if taxable_amount > 500000:
            tax += (taxable_amount - 500000) * 0.30
            taxable_amount = 500000
        if taxable_amount > 250000:
            tax += (taxable_amount - 250000) * 0.20
            taxable_amount = 250000
        tax += taxable_amount * 0.05
        
        if taxable_income <= 500000:
            tax -= min(tax, 12500)
    
    elif regime == 'new':
        taxable_income = total_income - (50000 if salaried else 0)
        taxable_income = max(taxable_income, 0)
        remaining = taxable_income
        
        if remaining > 1500000:
            tax += (remaining - 1500000) * 0.30
            remaining = 1500000
        if remaining > 1200000:
            tax += (remaining - 1200000) * 0.20
            remaining = 1200000
        if remaining > 900000:
            tax += (remaining - 900000) * 0.15
            remaining = 900000
        if remaining > 600000:
            tax += (remaining - 600000) * 0.10
            remaining = 600000
        if remaining > 300000:
            tax += (remaining - 300000) * 0.05
        
        if taxable_income <= 700000:
            tax -= min(tax, 25000)
    
    cess = tax * 0.04
    total_tax = tax + cess
    return round(total_tax, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    tax = None
    if request.method == 'POST':
        age = int(request.form['age'])
        total_income = float(request.form['income'])
        regime = request.form['regime']
        salaried = request.form['salaried'] == 'yes'
        deductions = float(request.form['deductions']) if 'deductions' in request.form else 0
        
        tax = calculate_income_tax(age, total_income, regime, salaried, deductions)
    
    return render_template('index.html', tax=tax)

if __name__ == '__main__':
    app.run(debug=True)

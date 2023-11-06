from flask import Flask, render_template, request, redirect, url_for

class RoomiesFinance:
    debt_settled = ''
    def __init__(self):
        self.debt_list = []
        self.josue_debt = 0
        self.daniela_debt = 0
        self.daniela_description = self.debt_settled
        self.josue_description = self.debt_settled
    
    def sum_amount(self, person):
        sum_josue = 0
        sum_daniela = 0
        
        for obj in self.debt_list:
            if obj["person"] == "Josue":
                sum_josue += obj["amount"]
                self.josue_description = obj["description"]
            if obj["person"] == "josue_debts_settled":
                sum_josue -= obj["amount"]
                
            if obj["person"] == "Daniela":
                sum_daniela += obj["amount"]
                self.daniela_description = obj["description"]
            if obj["person"] == "daniela_debts_settled":
                sum_daniela -= obj["amount"]
                
        if person == "Josue":
            return sum_josue
        else:
            return sum_daniela
                
                
    def edit_debt_amount(self):
        sum_josue = 0
        sum_daniela = 0
        
        for obj in self.debt_list:
            if obj["person"] == "Josue":
                sum_josue += obj["amount"]
                self.josue_description = obj["description"]
            if obj["person"] == "josue_debts_settled":
                sum_josue -= obj["amount"]
                
            if obj["person"] == "Daniela":
                sum_daniela += obj["amount"]
                self.daniela_description = obj["description"]
            if obj["person"] == "daniela_debts_settled":
                sum_daniela -= obj["amount"]
        
        if sum_daniela > sum_josue:
            self.daniela_debt = sum_daniela - sum_josue 
            self.josue_debt = 0
            self.josue_description = self.debt_settled
            return
        if sum_daniela == sum_josue:
            self.daniela_description= self.debt_settled
            self.josue_description = self.debt_settled
        
        self.daniela_debt=0
        self.daniela_description = self.debt_settled
        self.josue_debt = sum_josue - sum_daniela	

    
    def add_debt(self, person, amount, description):
        self.debt_list.append({
            "person": person,
            "amount": amount,
            "description":description
        })
        
        print("Lista de deudas", self.debt_list)
        self.edit_debt_amount()
        

    def list_debts(self):
        return (self.josue_debt, self.daniela_debt)

    def get_debt_status(self):
        if self.josue_debt > self.daniela_debt:
            return "Josue is $ {} in debt with Daniela.".format(self.josue_debt - self.daniela_debt)
        elif self.daniela_debt > self.josue_debt:
            return "Daniela is $ {} in debt with Josue.".format(self.daniela_debt - self.josue_debt)
        else:
            return "No one is in debt."

    def pay_all_debts(self):
        sum_total_daniela = self.sum_amount("Daniela")
        sum_total_josue = self.sum_amount("Josue")
        
        if sum_total_daniela > sum_total_josue:
            self.debt_list.append({
                "person":"daniela_debts_settled",
                "amount":sum_total_daniela,
                "description":"All debts settled"
            })
        if sum_total_josue > sum_total_daniela:
            self.debt_list.append({
                "person":"josue_debts_settled",
                "amount":sum_total_josue,
                "description":"All debts settled"
            })
        
        self.edit_debt_amount()


app = Flask(__name__)
finance_manager = RoomiesFinance()

@app.route('/')
def index():
    josue_debt, daniela_debt = finance_manager.list_debts()
    daniela_description = finance_manager.daniela_description
    josue_description = finance_manager.josue_description
    debt_status = finance_manager.get_debt_status()
    return render_template('index.html', josue_debt=josue_debt, daniela_debt=daniela_debt, debt_status=debt_status, debt_list=finance_manager.debt_list, josue_description = josue_description, daniela_description = daniela_description)


@app.route('/add_debt', methods=['POST'])
def add_debt():
    person = request.form['person']
    amount = float(request.form['amount'])
    description = request.form['description']
    finance_manager.add_debt(person, amount,description)
    return redirect(url_for('index'))

@app.route('/edit_debt', methods=['POST'])
def edit_debt():
    debt_id = int(request.form['debt_id'])
    new_amount = float(request.form['new_amount'])
    new_description = request.form['new_description']
    
    # Actualiza la deuda en la lista de deudas
    debt = finance_manager.debt_list[debt_id - 1]  # Resta 1 para obtener el índice correcto
    debt['amount'] = new_amount
    debt['description'] = new_description
    
    print("debt",debt)
    
    finance_manager.edit_debt_amount()
    
    return redirect(url_for('index'))


@app.route('/search_debt', methods=['GET'])
def search_debt():
    query = request.args.get('query')  # Obtiene el término de búsqueda de la URL
    results = []

    for debt in finance_manager.debt_list:
        if query.lower() in debt['description'].lower():  # Realiza una búsqueda sin distinción entre mayúsculas y minúsculas
            results.append(debt)

    return render_template('search_results.html', query=query, results=results)

@app.route('/pay_all_debts', methods=['POST'])
def pay_all_debts():
    finance_manager.pay_all_debts()
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)

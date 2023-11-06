class RoomiesFinance:
    def __init__(self):
        self.josue_debt = 0
        self.daniela_debt = 0

    def add_debt(self, person, amount):
        if person == "Josue":
            self.josue_debt += amount 
            if self.daniela_debt > 0:
                self.daniela_debt -= amount
                self.josue_debt -= amount
                if self.daniela_debt < 0:
                    self.josue_debt += -self.daniela_debt
                    self.daniela_debt = 0
        elif person == "Daniela":
            self.daniela_debt += amount 
            if self.josue_debt > 0:
                self.josue_debt -= amount
                self.daniela_debt -= amount
                if self.josue_debt < 0:
                    self.daniela_debt += -self.josue_debt
                    self.josue_debt = 0



        else:
            print("Person not found!")

    def list_debts(self):
        return f"Josue's debt: {self.josue_debt}, Daniela's debt: {self.daniela_debt}"

    def get_debt_status(self):
        if self.josue_debt > self.daniela_debt:
            return "Josue is in debt with Daniela."
        elif self.daniela_debt > self.josue_debt:
            return "Daniela is in debt with Josue."
        else:
            return "No one is in debt."

    def pay_all_debts(self):
        self.josue_debt = 0
        self.daniela_debt = 0

def main():
    finance_manager = RoomiesFinance()

    while True:
        print("\nRoomies Finance")
        print("1. Add Debt")
        print("2. List Debts")
        print("3. Debt Status")
        print("4. Pay All Debts")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            person = input("Enter the person (Josue or Daniela): ")
            amount = float(input("Enter the amount: "))
            finance_manager.add_debt(person, amount)
        elif choice == "2":
            print(finance_manager.list_debts())
        elif choice == "3":
            print(finance_manager.get_debt_status())
        elif choice == "4":
            finance_manager.pay_all_debts()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

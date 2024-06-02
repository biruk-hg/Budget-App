class Category():
    def __init__(self, name):
        self.name = name
        self.ledger = []

    #Method to deposit money
    def deposit(self, amount, description=''):
        if amount <= 0:
            return f'Invalid deposit of {amount}.'
        if description is None:
            descripton = ''
        depo = {"amount": amount, "description": description}
        return self.ledger.append(depo)
    
    #Method to withdraw money
    def withdraw(self, amount, description=''):
        if amount < 0 or not self.check_funds(amount):
            return False
        wdraw = {"amount": -amount, "description": description}
        self.ledger.append(wdraw)
        return True
    
    #Method to find total
    def get_balance(self):
        balance = sum(item['amount'] for item in self.ledger)
        return balance

    #Method to transfer money 
    def transfer(self, amount, category):
        if amount < 0 or not self.check_funds(amount):
            return False
        self.withdraw(amount, f'Transfer to {category.name}')
        category.deposit(amount, f'Transfer from {self.name}')
        return True

    #Method to check amount of money
    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        return True
    
    def __str__(self):
        output = f"{self.name:*^30}\n"
        for entry in self.ledger:
            description = entry['description'][:23]
            amount = f"{entry['amount']:>7.2f}\n"
            output += f"{description:<23}{amount}"
        output += f"Total: {self.get_balance():.2f}"
        return output

def create_spend_chart(categories):
    chart = "Percentage spent by category\n"

    #Calculate total withdrawals for each category
    total_withdrawals = []
    category_names = []
    for category in categories:
        total = sum(-item['amount'] for item in category.ledger if item['amount'] < 0)
        total_withdrawals.append(total)
        category_names.append(category.name)

    total_spent = sum(total_withdrawals)
    percentages = [(withdrawal / total_spent) * 100 for withdrawal in total_withdrawals]

    #Build the percentage bars
    for i in range(100, -1, -10):
        chart += f"{i:>3}|"
        for percent in percentages:
            if percent >= i:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    #Add the horizontal line
    chart += "    " + "-" * (3 * len(categories) + 1) + "\n"

    #Add category names vertically
    max_len = max(len(name) for name in category_names)
    for i in range(max_len):
        chart += "     "
        for name in category_names:
            if i < len(name):
                chart += f"{name[i]}  "
            else:
                chart += "   "
        chart += "\n"

    return chart.rstrip("\n")

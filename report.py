import csv
from collections import defaultdict
from datetime import datetime


def read_csv(file_path):
    expenses = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                expense_id = row['expense_id']
                expense_type = row['expense_type'] or 'Unknown'
                amount = float(row['amount']) if row['amount'] else 0.0
                expense_date = row['expense_date']
                payment_method = row['payment_method'] or 'Unknown'

                expenses.append({
                    'expense_id': expense_id,
                    'expense_type': expense_type,
                    'amount': amount,
                    'expense_date': expense_date,
                    'payment_method': payment_method
                })
            except ValueError:
                continue
    return expenses


def calculate_expenses(expenses):
    total_expense = 0.0
    total_by_type = defaultdict(float)
    total_by_payment = defaultdict(float)
    daily_expenses = defaultdict(float)
    monthly_expenses = defaultdict(float)
    breakdown_by_type_and_payment = defaultdict(lambda: defaultdict(float))

    for expense in expenses:
        amount = expense['amount']
        total_expense += amount
        total_by_type[expense['expense_type']] += amount
        total_by_payment[expense['payment_method']] += amount

        date = expense['expense_date']
        if date:
            try:
                day = datetime.strptime(date, '%Y-%m-%d').date()
                daily_expenses[day] += amount

                month = day.month
                monthly_expenses[month] += amount
            except ValueError:
                print(f"Skipping invalid date format: {date}")
                continue  # Skip invalid dates

        breakdown_by_type_and_payment[expense['expense_type']][expense['payment_method']] += amount

    return total_expense, total_by_type, total_by_payment, daily_expenses, monthly_expenses, breakdown_by_type_and_payment


def print_report(total_expense, total_by_type, total_by_payment, daily_expenses, monthly_expenses,
                 breakdown_by_type_and_payment):
    # Total Expense
    print(f"Total Expense: ${total_expense:.2f}\n")

    # Total by Expense Type
    print("Total by Expense Type:")
    for expense_type, total in total_by_type.items():
        print(f"{expense_type}: ${total:.2f}")
    print()

    # Total by Payment Method
    print("Total by Payment Method:")
    for payment_method, total in total_by_payment.items():
        print(f"{payment_method}: ${total:.2f}")
    print()

    # Top 3 Expense Types
    print("Top 3 Expense Types:")
    top_3_expense_types = sorted(total_by_type.items(), key=lambda x: x[1], reverse=True)[:3]
    for expense_type, total in top_3_expense_types:
        print(f"{expense_type}: ${total:.2f}")
    print()

    # Day with Highest Expenses
    if daily_expenses:
        highest_expense_day = max(daily_expenses, key=daily_expenses.get)
        print(f"Day with Highest Expenses: {highest_expense_day} with ${daily_expenses[highest_expense_day]:.2f}\n")

    # Month-wise Total Expenses
    print("Month-wise Total Expenses:")
    for month in sorted(monthly_expenses):
        print(f"{month:02}: ${monthly_expenses[month]:.2f}")
    print()

    # Expense Type Breakdown by Payment Method
    print("Expense Type Breakdown by Payment Method:")
    print(f"{'Expense Type':<20} {'Credit Card':<15} {'Cash':<15} {'Total':<15}")
    print('-' * 65)

    for expense_type, payments in breakdown_by_type_and_payment.items():
        credit_card_total = payments.get('Credit Card', 0.0)
        cash_total = payments.get('Cash', 0.0)
        total = credit_card_total + cash_total
        print(f"{expense_type:<20} ${credit_card_total:<14.2f} ${cash_total:<14.2f} ${total:<14.2f}")

    print('-' * 65)
    print(f"{'Total':<20} ${total_by_payment.get('Credit Card', 0.0):<14.2f} ${total_by_payment.get('Cash', 0.0):<14.2f} ${total_expense:<14.2f}")


if __name__ == '__main__':
    file_path = 'expenses.csv'
    expenses = read_csv(file_path)

    total_expense, total_by_type, total_by_payment, daily_expenses, monthly_expenses, breakdown_by_type_and_payment = calculate_expenses(
        expenses)

    print_report(total_expense, total_by_type, total_by_payment, daily_expenses, monthly_expenses,
                 breakdown_by_type_and_payment)

def calculate_total_interest_paid(loan_amount, annual_interest_rate, loan_term_years):
    monthly_interest_rate = annual_interest_rate / 12 / 100
    total_number_of_payments = loan_term_years * 12

    numerator = monthly_interest_rate * loan_amount
    denominator = 1 - (1 + monthly_interest_rate) ** (-total_number_of_payments)

    monthly_payment = int(numerator / denominator)

    total_paid = monthly_payment * total_number_of_payments
    total_interest_paid = int(total_paid - loan_amount)  # Total amount of interest paid

    return total_interest_paid


def calculate_amortization_table(loan_amount, annual_interest_rate, loan_term_years):
    # Convert annual interest rate to monthly and make it a proportion
    monthly_interest_rate = (annual_interest_rate / 100) / 12

    # Number of monthly payments
    number_of_payments = loan_term_years * 12

    # Calculate the monthly payment using the formula for an amortizing loan
    monthly_payment = loan_amount * (monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -number_of_payments))

    # Create the amortization table
    amortization_table = []

    for payment_number in range(1, number_of_payments + 1):
        interest_payment = loan_amount * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        loan_amount -= principal_payment

        amortization_table.append(
            {
                "Payment Number": payment_number,
                "Principal Payment": principal_payment,
                "Interest Payment": interest_payment,
                "Remaining Loan Balance": loan_amount,
            }
        )

    return amortization_table


calculate_amortization_table(1_000_000, 5, 10)
t1 = calculate_amortization_table(1_000_000, 5, 30)

# Print the amortization table
for payment in t1:
    print(payment)

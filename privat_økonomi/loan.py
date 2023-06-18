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
                "payment_number": payment_number,
                "afdrag": -principal_payment,
                "rente": -interest_payment,
                "resterende_lån": loan_amount,
            }
        )

    if len(amortization_table) % 12 != 0:
        raise Exception(f"Amortization table includes non-full years with len {len(amortization_table)}")

    total_rente = sum([e["rente"] for e in amortization_table])
    total_afdrag = sum([e["afdrag"] for e in amortization_table])
    return amortization_table, total_rente, total_afdrag

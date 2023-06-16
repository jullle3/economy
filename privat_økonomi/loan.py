def calculate_total_interest_paid(loan_amount, annual_interest_rate, loan_term_years):
    monthly_interest_rate = annual_interest_rate / 12 / 100
    total_number_of_payments = loan_term_years * 12

    numerator = monthly_interest_rate * loan_amount
    denominator = 1 - (1 + monthly_interest_rate)**(-total_number_of_payments)

    monthly_payment = int(numerator / denominator)

    total_paid = monthly_payment * total_number_of_payments
    total_interest_paid = int(total_paid - loan_amount)  # Total amount of interest paid

    return total_interest_paid


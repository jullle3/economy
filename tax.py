TAX_PERCENT = 42
INCOME = 500_000

low_interest = 30_000
high_interest = 48_000

tax_cheap_year = (INCOME - low_interest * 0.336) * 0.42
tax_expensive_year = (INCOME - high_interest * 0.336) * 0.42

print(tax_cheap_year)
print(tax_expensive_year)

extra_interest = high_interest - low_interest
saving_on_tax = tax_cheap_year - tax_expensive_year
print(f'Saved {saving_on_tax} on taxes, but paid {extra_interest} more in interest. Total extra paid = {extra_interest - saving_on_tax}')

skat_uden_kørsels_fradrag = INCOME * 0.42
skat_med_kørsels_fradrag = (INCOME - 10000) * 0.42

print(f'{skat_uden_kørsels_fradrag=}')
print(f'{skat_med_kørsels_fradrag=}')
print(f'saved {skat_uden_kørsels_fradrag - skat_med_kørsels_fradrag}')

from privat_økonomi.income import Income
from privat_økonomi.loan import calculate_total_interest_paid
from privat_økonomi.utils import pexit

EXPECTED_YEARLY_INCREASE_PERCENT = 0.05


class SimpleProperty:
    """
     Samling af betydelige udgifter for enten Leje, Andel eller Ejer bolig

     TODO: Beregn
        Skat
        Renter
     """

    def __init__(self, pris, månedlig_bolig_udgift, years, income: int, _type: str):
        """Alle beregninger er i år, med mandre andet er angivet"""
        self.years = years
        self.type = _type
        self.bolig_pris = pris
        self.forventet_fremtidig_pris = self.calc_expected_property_value()
        self.forventet_pristtigning = self.forventet_fremtidig_pris - self.bolig_pris
        # Antager man ligger minimums udbetaling på 5%
        self.udbetaling = pris * 0.05
        self.lån = pris * 0.95
        self.renter_total = calculate_total_interest_paid(self.lån, 6, 10)
        self.renter = self.renter_total // years
        self.stiftelsesomkostninger = 10000

        # Omkostninger til staten
        # https://domstol.dk/tinglysningsretten/tingboegerne/tinglysningsafgifter/
        # 1.45% af det pantsikrede beløb
        self.tinglysningsafgift = self.lån * 0.0145 + 1660
        self.engangs_omkostninger = self.stiftelsesomkostninger + self.tinglysningsafgift

        self.income = Income(income, self.renter)
        self.prisstigninger = 0
        self.gevinst_efter_skat = self.income.gevinst + self.prisstigninger

    def calc_expected_property_value(self):
        return int(self.bolig_pris * (1 + EXPECTED_YEARLY_INCREASE_PERCENT) ** self.years)


    def __str__(self):
        return f'Pris {self.bolig_pris:<20} \n' \
               f'Forventet årlig prisstigning {EXPECTED_YEARLY_INCREASE_PERCENT}% = \n' \
               f'Indkomst over 10 år {self.gevinst_efter_skat}'


YEARS = 10
print(SimpleProperty(1_150_000, 3000, YEARS, 500_000, 'andel'))
exit()
andels_bolig = SimpleProperty(1_150_000, 3000, YEARS, 500_000)
ny_andels_bolig = SimpleProperty(3_000_000, 3000, YEARS)
ejer_bolig = SimpleProperty(3_000_000, 3000, YEARS)

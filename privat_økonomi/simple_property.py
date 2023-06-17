from privat_økonomi.loan import calculate_total_interest_paid, calculate_amortization_table
from privat_økonomi.utils import out, pexit
from privat_økonomi.income import Income

EXPECTED_YEARLY_INCREASE_PERCENT = 0.05
LOAN_INTEREST_RATE = 6


def _format(num):
    return '{:,}'.format(num).replace(",", ".")


class SimpleProperty:
    """
    Samling af betydelige udgifter for enten Leje, Andel eller Ejer bolig

    TODO: Beregn
       Skat
       Renter
    """

    def __init__(self, pris, bolig_udgift, years, income: int, _type: str):
        self.bolig_udgift_årlig = -bolig_udgift * 12
        self.years = years
        self.type = _type
        self.pris = pris
        self.forventet_fremtidig_pris = self.calc_expected_property_value()
        self.forventet_pristtigning_årlig = (self.forventet_fremtidig_pris - self.pris) // years

        # Lån
        # Antager man ligger minimums udbetaling på 5%
        self.udbetaling = pris * 0.05
        self.lån = pris * 0.95
        self.renter_total = -calculate_total_interest_paid(self.lån, LOAN_INTEREST_RATE, years)
        tmp = calculate_amortization_table(self.lån, LOAN_INTEREST_RATE, years)
        self.renter_årlige = self.renter_total // years
        self.stiftelsesomkostninger = -10000
        # Omkostninger til staten
        # https://domstol.dk/tinglysningsretten/tingboegerne/tinglysningsafgifter/
        # 1.45% af det pantsikrede beløb
        self.tinglysningsafgift = -(self.lån * 0.0145 + 1660)
        self.engangs_omkostninger = self.stiftelsesomkostninger + self.tinglysningsafgift

        # Beregn resultat
        self.total_indtægter = self.forventet_pristtigning_årlig * years
        self.indkomst_årlig = Income(income, self.renter_årlige)
        self.total_udgifter = (
            self.indkomst_årlig.indkomst_ændring * years + self.bolig_udgift_årlig * years + self.engangs_omkostninger
        )

        # Forvent 50_000 kr til ejendomsmægler da de ikke kan sælges gennem dba
        if self.type.lower() == "ejer":
            self.total_udgifter += 50_000

        self.gevinst_efter_skat = self.total_indtægter + self.total_udgifter

        # TODO: verificer om det virker
        self.år_før_profit = self.calculate_profitable_years()
        self._out()

    def calc_expected_property_value(self):
        return int(self.pris * (1 + EXPECTED_YEARLY_INCREASE_PERCENT) ** self.years)

    def _out(self):
        out(
            self.type,
            self.years,
            int(EXPECTED_YEARLY_INCREASE_PERCENT * 100),
            LOAN_INTEREST_RATE,
            self.pris,
            self.forventet_fremtidig_pris,
            int(self.engangs_omkostninger),
            self.renter_total,
            _format(int(self.gevinst_efter_skat)),
            self.bolig_udgift_årlig * self.years,
            int(self.total_udgifter),
            self.total_indtægter,
        )

    def calculate_profitable_years(self):
        years = 0
        while self.gevinst_efter_skat < 0:
            years += 1
            self.years = years
            self.forventet_fremtidig_pris = self.calc_expected_property_value()
            self.forventet_pristtigning_årlig = (self.forventet_fremtidig_pris - self.pris) // years
            self.total_indtægter = self.forventet_pristtigning_årlig * years
            self.total_udgifter = (
                    self.indkomst_årlig.indkomst_ændring * years + self.bolig_udgift_årlig * years + self.engangs_omkostninger
            )
            if self.type.lower() == "ejer":
                self.total_udgifter += 50_000
            self.gevinst_efter_skat = self.total_indtægter + self.total_udgifter
        return years


# TODO: Beregn præcis hvor mange år der går før en bolig har tjent sig hjem. Dette vil nok kræve en armotiseringstabel
YEARS = 10
SimpleProperty(1_150_000, 3000, YEARS, 500_000, "Andel")
SimpleProperty(2_790_000, 6000, YEARS, 500_000, "Andel")
SimpleProperty(4_000_000, 3500, YEARS, 500_000, "Andel")
exit()
ny_andels_bolig = SimpleProperty(3_000_000, 3000, YEARS)
ejer_bolig = SimpleProperty(3_000_000, 3000, YEARS)

from privat_økonomi.loan import calculate_total_interest_paid, calculate_amortization_table
from privat_økonomi.utils import out, pexit
from privat_økonomi.income import Income

EXPECTED_YEARLY_INCREASE_PERCENT = 0.05
LOAN_INTEREST_RATE = 6
EJENDOMSMÆGLER_PRIS = -80_000

def _format(num):
    return '{:,}'.format(num).replace(",", ".")


class SimpleProperty:
    """
    Samling af betydelige udgifter for enten Leje, Andel eller Ejer bolig

    TODO: Beregn
       Skat
       Renter
    """

    def __init__(self, pris, bolig_udgift, år, income: int, _type: str, udbetaling: int, validate=False):
        self.bolig_udgift_årlig = -bolig_udgift * 12
        self.years = år
        self.type = _type
        self.pris = pris
        self.forventet_fremtidig_pris = self.calc_expected_property_value()
        self.forventet_pristtigning_årlig = (self.forventet_fremtidig_pris - self.pris) // år

        # Lån
        self.udbetaling = udbetaling
        self.lån = pris - udbetaling

        if validate:
            # Lovpligtig minimums udbetaling på 5%
            if udbetaling / self.lån < 0.05:
                raise Exception(f"Minimums betaling skal være højere end {udbetaling / self.lån}")

        self.renter_total = -calculate_total_interest_paid(self.lån, LOAN_INTEREST_RATE, år)

        self.renter_årlige = self.renter_total // år
        self.ekspeditionsgebyrer = -9000
        self.etablering_af_boliglån = -7600
        # Omkostninger til staten
        # https://www.bolius.dk/omkostninger-ved-at-koebe-bolig-18145
        # 0.6% af boligens værdi + lidt
        self.tinglysning_skøde = -(self.pris * 0.006 + 1850)
        # 1.45% af det lånte beløb + lidt
        # Dog påstår bolius at man reelt sparrer en del ved at overtage sælgers pant
        self.tinglysning_realkredit = -((self.lån * 0.0145 + 1660) * 0.25)
        self.advokat_bistand = -5000
        self.engangs_omkostninger = self.ekspeditionsgebyrer + self.tinglysning_realkredit + self.tinglysning_skøde + self.advokat_bistand + self.etablering_af_boliglån

        # Beregn resultat
        self.total_indtægter = self.forventet_pristtigning_årlig * år
        self.indkomst_årlig = Income(income, self.renter_årlige)
        self.total_udgifter = (
                self.indkomst_årlig.indkomst_ændring * år + self.bolig_udgift_årlig * år + self.engangs_omkostninger
        )

        # Forvent 50_000 kr til ejendomsmægler da de ikke kan sælges gennem dba
        if self.type.lower() == "ejer":
            self.total_udgifter += EJENDOMSMÆGLER_PRIS

        self.gevinst_efter_skat = self.total_indtægter + self.total_udgifter

        # TODO: Beregn udgifter pr år
        self.udgifter_pr_år = self.calc_udgifter_pr_år()
        # TODO: verificer om det virker
        # self.år_før_profit = self.calculate_profitable_years()
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
            int(self.total_udgifter // self.years),
            int(self.udgifter_pr_år[1]['udgifter']),
            int(self.udgifter_pr_år[2]['udgifter']),
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

    def calc_udgifter_pr_år(self) -> dict:
        years = {}

        armotiserings_tabel, _, _ = calculate_amortization_table(self.lån, LOAN_INTEREST_RATE, self.years)

        num_years = len(armotiserings_tabel) // 12
        for year in range(1, num_years+1):
            start = (year - 1) * 12
            end = year * 12
            årlig_afdrag = sum(payment['afdrag'] for payment in armotiserings_tabel[start:end])
            årlig_rente = sum(payment['rente'] for payment in armotiserings_tabel[start:end])
            resterende_lån = armotiserings_tabel[start:end][-1]['resterende_lån']

            years[year] = {
                'afdrag': int(årlig_afdrag),
                'rente': int(årlig_rente),
                'udgifter': int(årlig_rente) + self.bolig_udgift_årlig,
                "resterende_lån": int(resterende_lån)
            }

        # Første år har udgifter til tinglysning + låneomkostninger
        years[1]["udgifter"] += self.engangs_omkostninger

        # Sidste år har udgifter til Ejendomsmægler, hvis det er en ejer bolig
        if self.type.lower() == "ejer":
            years[self.years]["udgifter"] += EJENDOMSMÆGLER_PRIS

        return years


YEARS = 10
UDBETALING = 100_000
INDKOMST = 500_000

SimpleProperty(1_150_000, 3000, YEARS, INDKOMST, "Andel", UDBETALING)
# SimpleProperty(2_790_000, 6000, YEARS, INDKOMST, "Andel", UDBETALING)
SimpleProperty(4_000_000, 3500, YEARS, INDKOMST, "Andel", UDBETALING)
SimpleProperty(3_000_000, 4200, YEARS, INDKOMST, "Ejer", UDBETALING)
SimpleProperty(11_000_000, 5500, YEARS, INDKOMST, "Ejer", UDBETALING)
exit()
ny_andels_bolig = SimpleProperty(3_000_000, 3000, YEARS)
ejer_bolig = SimpleProperty(3_000_000, 3000, YEARS)

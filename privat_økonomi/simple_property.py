from privat_økonomi.loan import calculate_total_interest_paid
from privat_økonomi.utils import pexit


class SimpleProperty:
    """
     Samling af betydelige udgifter for enten Leje, Andel eller Ejer bolig

     TODO: Beregn
        Skat
        Renter
     """

    def __init__(self, bolig_pris, månedlig_bolig_udgift, years, income):
        """Alle beregninger er i år, med mandre andet er angivet"""
        self.bolig_pris = bolig_pris
        # Antager man ligger minimums udbetaling på 5%
        self.udbetaling = bolig_pris * 0.05
        self.lån = bolig_pris * 0.95
        self.renter_total = calculate_total_interest_paid(self.lån, 6, 10)
        self.renter = self.renter_total // years
        self.stiftelsesomkostninger = 10000

        # Omkostninger til staten
        # https://domstol.dk/tinglysningsretten/tingboegerne/tinglysningsafgifter/
        # 1.45% af det pantsikrede beløb
        self.tinglysningsafgift = self.lån * 0.0145 + 1660

        self.engangs_omkostninger = self.stiftelsesomkostninger + self.tinglysningsafgift

        #
        self.skattefradrag = self.renter
        # print(f'Total: {int(self.månedlig_ydelse_total)}/måned')


YEARS = 10
andels_bolig = SimpleProperty(1_150_000, 3000, YEARS)
ny_andels_bolig = SimpleProperty(3_000_000, 3000, YEARS)
ejer_bolig = SimpleProperty(3_000_000, 3000, YEARS)

from privat_økonomi.utils import pexit


class Property:
    """ Samling af udgifter forbundet med at eje lejlighed/rækkehus/villa, pr måned """

    def __init__(self, låne_beløb, ejendomsværdi, grundværdi):
        # Omkostninger til bank. Helt uoverskueligt, så kig altid på ÅOP!
        # https://www.findbank.dk/stiftelsesomkostninger/
        self.stiftelsesomkostninger = 0
        self.gebyrer = 0
        self.rente = 0

        # Bidrag er i realiteten = gebyrer, blot kun for realkreditlån
        self.bidrag = 0
        self.kurs = 0

        # Omkostninger til staten
        # https://domstol.dk/tinglysningsretten/tingboegerne/tinglysningsafgifter/
        # 1.45% af det pantsikrede beløb
        self.tinglysningsafgift = låne_beløb * 0.0145 + 1660

        # TODO: Der findes fradrag!
        # TODO: Meget svær at beregne. Copy paste hellere værdier fra en reel bolig
        # self.ejendomsværdiskat = calc_ejendomsværdiskat(ejendomsværdi)

        # TODO: Der findes fradrag!
        # TODO: Meget svær at beregne. Copy paste hellere værdier fra en reel bolig
        # Omkostninger til kommunen. Varierer.
        # self.grundskyld = calc_grundskyld(grundværdi)
        print(f'{self.ejendomsværdiskat=} {self.grundskyld=}')

        # Gebyr for afhenting af skrald og adgang til skraldeplads. Obligatorisk
        self.renovation = 2500 / 12

        # Omkostninger til ejendommen
        self.husleje = 0
        self.ejerudgift = 0

        # https://www.bolius.dk/saa-meget-el-vand-og-varme-bruger-en-gennemsnitsfamilie-279
        self.vand = 600

        # https://sparenergi.dk/forbruger/varme/forsta-din-varmeregning
        self.varme = 1000
        self.el = 500
        self.forsikring = 200 / 12

        # Alt vedligeholdelse, inde og udvendig
        self.vedligeholdelse = 1000

        self.månedlig_ydelse_total = \
            self.rente + \
            self.ejendomsværdiskat + \
            self.grundskyld + \
            self.renovation + \
            self.husleje + \
            self.ejerudgift + \
            self.vand + \
            self.varme + \
            self.el + \
            self.forsikring + \
            self.vedligeholdelse

        # TODO: beregn engangsomkostninger
        self.engangs_omkostninger = \
            self.stiftelsesomkostninger + \
            self.tinglysningsafgift

        print(f'Total: {int(self.månedlig_ydelse_total)}/måned')


def calc_ejendomsværdiskat(num: int):
    """ https://skat.dk/skat.aspx?oid=2242217 """
    upper_boundary = 3_040_000

    if num > upper_boundary:
        # 0.92% op til 3.04 mil
        lower_tax = upper_boundary * 0.92 / 100
        num -= upper_boundary

        # 3% af resten
        upper_tax = num * 3 / 100

        ejendomsværdiskat = lower_tax + upper_tax
    else:
        # 0.92% op til 3.04 mil
        lower_tax = num * 0.92 / 100
        ejendomsværdiskat = lower_tax

    return int(ejendomsværdiskat / 12)


def calc_grundskyld(grundværdi: int):
    """ 20 promille er et fint gennemsnit på tværs af kommuner """
    return int(grundværdi * 20 / 1000 / 12)


kim_gamle = Property(10_000_000, 3_700_000, 2_385_800)
kim_nye = Property(10_000_000, 8_471_000, 5_312_000)
# nabo_nye = Expenses(10_000_000, 5_500_000, 4_000_000)

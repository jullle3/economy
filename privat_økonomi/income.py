TAX_RATE = 0.42


class Income:
    """Calculate income after all expenditures and more"""

    def __init__(self, indkomst: int, renter=0, kørselsfradrag=0):
        """
        :param indkomst: Indkomst før skat, fradrag og uden pension
        """
        renter = int(renter)
        # TODO: Er der flere betydelige fradrag?
        self.rente_fradrag = _calc_rente_fradrag(renter)
        self.fradrag = self.rente_fradrag + kørselsfradrag
        self.skattepligtig_indkomst = indkomst - self.fradrag
        self.skat = int(self.skattepligtig_indkomst * TAX_RATE)
        self.udbetalt = indkomst - self.skat
        # Beregn den ekstra indkomst som følge af fradrag
        skat_uden_fradrag = int(indkomst * TAX_RATE)
        udbetalt_uden_fradrag = indkomst - skat_uden_fradrag
        self.ekstra_indkomst = self.udbetalt - udbetalt_uden_fradrag
        # Hvor mange procent af fradraget som ender som reel indkomst
        self.fradrag_forhold_procent = self.ekstra_indkomst / self.fradrag if self.ekstra_indkomst else 0

        ekstra_udgifter = renter

        # Den reelle pris som rentestigninger har kostet
        self.indkomst_ændring = ekstra_udgifter - self.ekstra_indkomst


def _calc_rente_fradrag(renter: int) -> int:
    # TODO: Så simpelt kan det ikke beregnes :P
    rente_fradrag = renter * 0.336
    return int(rente_fradrag)


if __name__ == "__main__":
    Income(500_000, 48000)

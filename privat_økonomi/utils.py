import pprint


def pexit(s):
    pprint.pprint(s)
    print(type(s))
    if hasattr(s, "__len__"):
        print(f"Length: {len(s)}")
    exit()


def out(
    type,
    years,
    årlig_stigning,
    rente,
    pris,
    forventet_pris,
    engangsomkostninger,
    renter,
    gevinst_efter_skat,
    boligudgift,
    total_udgifter,
    total_indtægter,
    udgifter_gns_år,
    udgifter_første_år,
    udgifter_andet_år,
):
    print(
        f"{type:<10}{years:<10}{årlig_stigning:<25}{rente:<10}{pris:<15}{forventet_pris:<15}{renter:<10}{boligudgift:<15}{engangsomkostninger:<20}{total_udgifter:<15}{total_indtægter:<18}{gevinst_efter_skat:<30}{udgifter_gns_år:<20}{udgifter_første_år:<20}{udgifter_andet_år:<20}"
    )


out(
    "Type",
    "Years",
    "Forv. årlig stigning",
    "Rente",
    "Bolig Pris",
    "Forv. pris",
    "Engangsomkostninger",
    "Renter",
    "Gevinst efter skat",
    "Boligudgift",
    "Total Udgifter",
    "Total Indtægter",
    'Udgifter gns./år',
    'Udgifter år 1',
    'Udgifter år 2',
)

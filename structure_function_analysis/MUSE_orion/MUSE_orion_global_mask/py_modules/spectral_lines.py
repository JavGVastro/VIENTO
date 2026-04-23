from dataclasses import dataclass


@dataclass(frozen=True)
class SpectralLine:
    key: str
    plot_label: str
    rest_wavelength: float
    element: str
    ion: str
    transition_id: str


LINES = {
    "Halpha": SpectralLine(
        key="Halpha",
        plot_label=r'H$\alpha$',
        rest_wavelength=6562.8,
        element="H",
        ion="H_I",
        transition_id="H_I-6563",
    ),

    "NII_6583": SpectralLine(
        key="NII_6583",
        plot_label=r'[N II]$\ \lambda$6584',
        rest_wavelength=6583.45,
        element="N",
        ion="N_II",
        transition_id="N_II-6583",
    ),

    "SII_6731": SpectralLine(
        key="SII_6731",
        plot_label=r'[S II]$\ \lambda$6731',
        rest_wavelength=6730.8,
        element="S",
        ion="S_II",
        transition_id="S_II-6731",
    ),

    "OIII_5007": SpectralLine(
        key="OIII_5007",
        plot_label=r'[O III]$\ \lambda$5007',
        rest_wavelength=5006.9,
        element="O",
        ion="O_III",
        transition_id="O_III-5007",
    ),

    "ArIII_7136": SpectralLine(
        key="ArIII_7136",
        plot_label=r'[Ar III]$\ \lambda$7136',
        rest_wavelength=7135.8,
        element="Ar",
        ion="Ar_III",
        transition_id="Ar_III-7136",
    ),

    "SIII_9069": SpectralLine(
        key="SIII_9069",
        plot_label=r'[S III]$\ \lambda$9069',
        rest_wavelength=9069.1,
        element="S",
        ion="S_III",
        transition_id="S_III-9069",
    ),
}


def get_line(key: str) -> SpectralLine:
    return LINES[key]

def print_available_lines() -> None:
    for key in LINES:
        print(key)
from dataclasses import dataclass

@dataclass(frozen=True)
class AstronomicalInstrument:
    key: str
    full_name: str
    instrument_id: str
    arcsec_per_pixel: float | None
    site: str
    telescope: str
    focus: str | None
    instrument_type: str
    wavelength_coverage: str | None
    spectral_resolution: str | None
    modes: tuple[str, ...]
    notes: str | None = None


INSTRUMENTS = {
    "MUSE": AstronomicalInstrument(
        key="MUSE",
        full_name="Multi Unit Spectroscopic Explorer",
        instrument_id="MUSE",
        arcsec_per_pixel=0.2,
        site="Paranal",
        telescope="Very Large Telescope, UT4",
        focus="Nasmyth",
        instrument_type="Integral field spectrograph, imager",
        wavelength_coverage="465–930 nm",
        spectral_resolution="From 1700 in the blue to 3400 in the red",
        modes=(),
    ),

    "FLAMES": AstronomicalInstrument(
        key="FLAMES",
        full_name="Fibre Large Array Multi Element Spectrograph",
        instrument_id="FLA",
        arcsec_per_pixel=None,
        site="Paranal",
        telescope="VLT UT2",
        focus="Nasmyth A",
        instrument_type="Multi-object fibre-fed spectrograph",
        wavelength_coverage="370–950 nm",
        spectral_resolution="GIRAFFE: R=5500–65100; UVES fibre mode: R~47000",
        modes=("MEDUSA", "IFU", "ARGUS", "UVES"),
    ),
    
    "KPNO_Echelle": AstronomicalInstrument(
        key="KPNO_Echelle",
        full_name="Echelle Spectrograph",
        instrument_id="ECH",
        arcsec_per_pixel=0.534,
        site="Kitt Peak National Observatory",
        telescope="NSF Nicholas U. Mayall 4-meter Telescope",
        focus=None,
        instrument_type="Echelle spectrograph",
        wavelength_coverage=None,
        spectral_resolution=None,
        modes=(),
        notes=(
            "Retired/legacy KPNO echelle instrument. "
            "arcsec_per_pixel kept from user metadata; "
            "other instrument-specific fields should be filled from the operation manual or papers."
        ),
),
    "LVM": AstronomicalInstrument(
        key="LVM",
        full_name="Local Volume Mapper Instrument",
        instrument_id="LVM",
        arcsec_per_pixel=37.0,
        site="Las Campanas Observatory",
        telescope="0.16 m telescope system",
        focus=None,
        instrument_type="Wide-field fibre-fed integral field spectrograph",
        wavelength_coverage="3600–9800 Å",
        spectral_resolution="R~4000",
        modes=(),
),
    "TAURUS2": AstronomicalInstrument(
        key="TAURUS2",
        full_name="Taurus-2",
        instrument_id="TAU",
        arcsec_per_pixel=0.26,
        site="Roque de los Muchachos Observatory, La Palma",
        telescope="William Herschel Telescope",
        focus=None,
        instrument_type="Imaging Fabry-Perot / tunable-filter instrument",
        wavelength_coverage=None,
        spectral_resolution=None,
        modes=(),
),
}


def get_instrument(key: str) -> AstronomicalInstrument:
    return INSTRUMENTS[key]


def print_available_instruments() -> None:
    for key in INSTRUMENTS:
        print(key)

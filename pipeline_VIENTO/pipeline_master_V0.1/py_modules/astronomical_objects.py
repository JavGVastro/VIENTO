from dataclasses import dataclass, field
import numpy as np


@dataclass(frozen=True)
class SkyPoint:
    label: str
    ra_deg: float
    dec_deg: float


@dataclass(frozen=True)
class AstronomicalObject:
    key: str
    catalog_name: str
    common_name: str
    object_id: str
    object_type: str
    distance_pc: float
    main_reference: SkyPoint | None = None
    points_of_interest: dict[str, SkyPoint] = field(default_factory=dict)

    @property
    def pc_per_arcsec(self) -> float:
        return self.distance_pc * (2 * np.pi) / (360 * 60 * 60)


OBJECTS = {
    "30Doradus": AstronomicalObject(
        key="30Doradus",
        catalog_name="NGC 2070",
        common_name="30 Doradus",
        object_id="30Dor",
        object_type="H II region",
        distance_pc=50000,
        points_of_interest={},
    ),
    
    "Orion": AstronomicalObject(
        key="Orion",
        catalog_name="M 42",
        common_name="Orion",
        object_id="M42",
        object_type="H II region",
        distance_pc=410,
#        main_reference=SkyPoint(
#            label=r'$\theta^1$ Ori C',
#            ra_deg=83.818750,
#            dec_deg=-5.3897222,
#        ),
        points_of_interest={
            "theta1 Ori C": SkyPoint(
                label=r'$\theta^1$ Ori C',
                ra_deg=83.818750,
                dec_deg=-5.3897222,
            ),
        },
    ),

    "Carina": AstronomicalObject(
        key="Carina",
        catalog_name="NGC 3372",
        common_name="Carina",
        object_id="Car",
        object_type="H II region",
        distance_pc=2130,
        points_of_interest={
            "eta Car": SkyPoint(
                label="eta Car",
                ra_deg=161.26517,
                dec_deg=-59.684425,
            ),
            "Tr 14": SkyPoint(
                label="Tr 14",
                ra_deg=160.98911,
                dec_deg=-59.547698,
            ),
            "WR 25": SkyPoint(
                label="WR 25",
                ra_deg=161.0433,
                dec_deg=-59.719735,
            ),
            "Finger": SkyPoint(
                label="Finger",
                ra_deg=161.13133,
                dec_deg=-59.664035,
            ),
        },
    ),

    "Lagoon": AstronomicalObject(
        key="Lagoon",
        catalog_name="M 8",
        common_name="Lagoon",
        object_id="M8",
        object_type="H II region",
        distance_pc=1250,
        points_of_interest={
            "HD 164536": SkyPoint(
                label="HD 164536",
                ra_deg=270.6609,
                dec_deg=-24.2554,
            ),
            "7 Sgr": SkyPoint(
                label="7 Sgr",
                ra_deg=270.7129,
                dec_deg=-24.2825,
            ),
            "Herschel 36": SkyPoint(
                label="Herschel 36",
                ra_deg=270.9180,
                dec_deg=-24.3785,
            ),
            "9 Sgr": SkyPoint(
                label="9 Sgr",
                ra_deg=270.9685,
                dec_deg=-24.3607,
            ),
            "HD 164816": SkyPoint(
                label="HD 164816",
                ra_deg=270.9869,
                dec_deg=-24.3126,
            ),
            "HD 164865": SkyPoint(
                label="HD 164865",
                ra_deg=271.0634,
                dec_deg=-24.1834,
            ),
            "M8E-IR": SkyPoint(
                label="M8E-IR",
                ra_deg=271.2244,
                dec_deg=-24.4448,
            ),
            "HD 165052": SkyPoint(
                label="HD 165052",
                ra_deg=271.2940,
                dec_deg=-24.3986,
            ),
            "HD 165246": SkyPoint(
                label="HD 165246",
                ra_deg=271.5195,
                dec_deg=-24.1955,
            ),
        },
    ),
    "N346": AstronomicalObject(
        key="N346",
        catalog_name="NGC 346",
        common_name="N346",
        object_id="N346",
        object_type="H II region",
        distance_pc=62000,
        points_of_interest={},
    ),
    "N604": AstronomicalObject(
        key="N604",
        catalog_name="NGC 604",
        common_name="NGC 604",
        object_id="N604",
        object_type="H II region",
        distance_pc=840000,
        points_of_interest={},
    ),

    "N595": AstronomicalObject(
        key="N595",
        catalog_name="NGC 595",
        common_name="NGC 595",
        object_id="N595",
        object_type="H II region",
        distance_pc=840000,
        points_of_interest={},
    ),
    "Helix": AstronomicalObject(
        key="Helix",
        catalog_name="NGC 7293",
        common_name="Helix nebula",
        object_id="N7293",
        object_type="Planetary nebula",
        distance_pc=202,
        points_of_interest={},
    ),
    "N6778": AstronomicalObject(
        key="N6778",
        catalog_name="NGC 6778",
        common_name="NGC 6778",
        object_id="N6778",
        object_type="Planetary nebula",
        distance_pc=3150,
        points_of_interest={},
    ),
     "M1_42": AstronomicalObject(
        key="M1_42",
        catalog_name="M 1-42",
        common_name="M 1-42",
        object_id="M1-42",
        object_type="Planetary nebula",
        distance_pc=3066,
        points_of_interest={},
    ),
}


def get_object(key: str) -> AstronomicalObject:
    return OBJECTS[key]


def print_available_objects() -> None:
    for key in OBJECTS:
        print(key)

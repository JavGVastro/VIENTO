import numpy as np
import astropy.units as u

def make_circles_auto(
    centro,
    radius,
    field_radius,
    *,
    ring_step_factor=2.0,
    tangential_step_factor=2.0,
    start_angle=0*u.deg,
):
    """
    Build circle subfields automatically inside a circular main field.

    Parameters
    ----------
    centro : SkyCoord
        Main center of the analysis field.
    radius : astropy quantity
        Radius of each subfield circle.
    field_radius : astropy quantity
        Radius of the main analysis field.
    ring_step_factor : float
        Radial spacing between rings in units of `radius`.
        Default = 2.0, so ring centers are at 2r, 4r, 6r, ...
    tangential_step_factor : float
        Tangential spacing target in units of `radius`.
        Default = 2.0, meaning neighboring circle centers are spaced
        by about 2r along the ring.
    start_angle : astropy quantity
        Starting angle for the first circle in each ring.

    Returns
    -------
    circles : list[dict]
        Circle catalog.
    """
    r = radius
    R = field_radius

    circles = []

    # -------------------------
    # central circle -> A
    # -------------------------
    circles.append({
        "label": "A",
        "ring": "A",
        "ring_index": 0,
        "angle_deg": None,
        "center": centro,
        "ra_deg": centro.ra.deg,
        "dec_deg": centro.dec.deg,
        "radius_arcsec": r.to(u.arcsec).value,
    })

    # Maximum ring index allowed so the full subfield stays inside the main field
    k_max = int(np.floor(((R - r) / (ring_step_factor * r)).decompose().value))

    for k in range(1, k_max + 1):
        d = ring_step_factor * k * r

        # number of circles for this ring from circumference / target spacing
        circumference = 2 * np.pi * d.to(u.arcsec).value
        target_spacing = tangential_step_factor * r.to(u.arcsec).value
        n_ring = max(1, int(np.ceil(circumference / target_spacing)))

        angles = np.linspace(
            start_angle.to(u.deg).value,
            start_angle.to(u.deg).value + 360.0,
            n_ring,
            endpoint=False
        ) * u.deg

        ring_letter = chr(ord("A") + k)   # B, C, D, ...

        for i, pa in enumerate(angles, start=1):
            c = centro.directional_offset_by(pa, d)

            circles.append({
                "label": f"{ring_letter}{i}",
                "ring": ring_letter,
                "ring_index": k,
                "angle_deg": pa.to(u.deg).value,
                "center": c,
                "ra_deg": c.ra.deg,
                "dec_deg": c.dec.deg,
                "radius_arcsec": r.to(u.arcsec).value,
            })

    return circles
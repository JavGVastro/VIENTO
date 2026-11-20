from pathlib import Path
from astropy.table import Table
from astropy.io import fits

def load_line_bundle(
    name: str,
    bundle_name: str,
    maps_dir: Path,
    *,
    return_wrapped: bool = False,
    read_header: bool = False,
) -> dict:
    """
    Load observation, structure function, and fit results from a FITS file.

    Parameters
    ----------
    name : str
        Dataset identifier; FITS filename is assumed to be f"{name}.fits"
        and the observation HDU is assumed to have extname == name.
    bundle_name : str
        Desired "variable name" for the returned bundle (e.g. "S_line").
        Since Python cannot return an object with a variable name, we carry this
        name in metadata and optionally wrap the result under this key.
    maps_dir : Path
        Directory where the FITS file is located.
    return_wrapped : bool, optional
        If True, return {bundle_name: bundle_dict}. If False, return bundle_dict.
    read_header : bool, optional
        If True, also include a 'meta' dict with selected header values.

    Returns
    -------
    dict
        Either bundle_dict or {bundle_name: bundle_dict} depending on return_wrapped.
    """
    fits_path = maps_dir / f"{name}.fits"

    # --- Load main table (obs) from HDU named exactly `name` ---
    obs_tbl = Table.read(fits_path, hdu=name)
    obs_df = obs_tbl.to_pandas()

    # --- Load other tables ---
    br_tbl = Table.read(fits_path, hdu="TABLE")
    br_df = br_tbl.to_pandas()

    fit_tbl = Table.read(fits_path, hdu="PARAMETERS")
    fit_df = fit_tbl.to_pandas()

    bundle = {
        "bundle_name": bundle_name,  # carries your desired "variable name"
        "data": name,
        "obs": obs_df,
        "Br": br_df,
        "fit": fit_df,
    }

    if read_header:
        with fits.open(fits_path) as hdul:
            hdr = hdul[0].header
        # Keep only what you actually need (add/remove keys as desired)
        header_keys = ["SIG", "SIG2", "S0", "BOX_SIZE", "PC", "PIX", "LINE", "BINSIZE"]
        bundle["meta"] = {k: hdr.get(k) for k in header_keys}

    return {bundle_name: bundle} if return_wrapped else bundle# -*- coding: utf-8 -*-

def load_line_bundle_mat(
    name: str,
    bundle_name: str,
    maps_dir: Path,
    *,
    return_wrapped: bool = False,
    read_header: bool = False,
) -> dict:
    """
    Load observation, structure function, and fit results from a FITS file.

    Parameters
    ----------
    name : str
        Dataset identifier; FITS filename is assumed to be f"{name}.fits"
        and the observation HDU is assumed to have extname == name.
    bundle_name : str
        Desired "variable name" for the returned bundle (e.g. "S_line").
        Since Python cannot return an object with a variable name, we carry this
        name in metadata and optionally wrap the result under this key.
    maps_dir : Path
        Directory where the FITS file is located.
    return_wrapped : bool, optional
        If True, return {bundle_name: bundle_dict}. If False, return bundle_dict.
    read_header : bool, optional
        If True, also include a 'meta' dict with selected header values.

    Returns
    -------
    dict
        Either bundle_dict or {bundle_name: bundle_dict} depending on return_wrapped.
    """
    fits_path = maps_dir / f"{name}.fits"
    hdul = fits.open(fits_path)
    sb = hdul['MOM0'].data.astype(float)
    vv= hdul['MOM1'].data.astype(float)
    mask= hdul['MASK'].data.astype(float)

    # --- Load main table (obs) from HDU named exactly `name` ---
    #obs_tbl = Table.read(fits_path, hdu=name)
    #obs_df = obs_tbl.to_pandas()

    # --- Load other tables ---
    br_tbl = Table.read(fits_path, hdu="TABLE")
    br_df = br_tbl.to_pandas()

    fit_tbl = Table.read(fits_path, hdu="PARAMETERS")
    fit_df = fit_tbl.to_pandas()

    bundle = {
        "bundle_name": bundle_name,  # carries your desired "variable name"
        "data": name,
        "sb":   sb,
        "vv":   vv,
        "mask": mask,
        "Br":   br_df,
        "fit":  fit_df,
    }

    if read_header:
        with fits.open(fits_path) as hdul:
            hdr = hdul[0].header
        # Keep only what you actually need (add/remove keys as desired)
        header_keys = ["SIG", "SIG2", "S0", "BOX_SIZE", "PC", "PIX", "LINE", "BINSIZE"]
        bundle["meta"] = {k: hdr.get(k) for k in header_keys}

    return {bundle_name: bundle} if return_wrapped else bundle# -*- coding: utf-8 -*-

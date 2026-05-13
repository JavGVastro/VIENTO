from pathlib import Path
from astropy.io import fits

def load_spectra_from_df(df, fits_dir, 
                         flux_col="FLUX_REDUCED", 
                         err_col="ERR_REDUCED",
                         snr_col="SNR_REDUCED"):
    """
    Load one FLAMES ADP spectrum from a FITS file.

    Parameters
    ----------
    filename : str or Path
        FITS filename or full path.
    fits_dir : str or Path, optional
        Directory containing FITS files, used only if filename is not a full path.

    Returns
    -------
    wave, flux, err : ndarray
        Wavelength, reduced flux, and reduced error arrays.
    """
    spectra = []

    for _, row in df.iterrows():
        fits_path = fits_dir / row["filename"]

        try:
            with fits.open(fits_path) as hdul:
                spec = hdul[1].data

                wave = spec["WAVE"][0]
                flux = spec[flux_col][0]
                err  = spec[err_col][0]
                snr  = spec[snr_col][0]

                spectra.append({
                    "filename": row["filename"],
                    "object": row["object"],
                    "ra_deg": row["ra_deg"],
                    "dec_deg": row["dec_deg"],
                    "wave": wave,
                    "flux": flux,
                    "err": err,
                    "snr": snr,
                })

        except Exception as e:
            print(f"Could not read {fits_path.name}: {e}")

    print(f"Loaded {len(spectra)} spectra")
    return spectra
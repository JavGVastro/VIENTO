"""
Model line-of-sight velocity for LMC

Based on Oh et al (2022) (which is really van der Marel 2022) and Grishunin et al (2024)

"""

import numpy as np

import astropy.units as u
from astropy.coordinates import SkyCoord, Angle

#
# Parameters from van der Marel et al 2022, derived from Carbon star kinematics
#

# Kinematic center of LMC, eq (37) (original 05:27.6 -69.87)
CENTER_LMC = SkyCoord(
    "5:27:36", "-69.87", unit=(u.hourangle, u.deg), frame="icrs"
)  # +/- 0.5 deg
# Inclination of disk normal from line of sight, eq (35)
INC_LMC = Angle(34.7 * u.deg)  # +/- 6.2 deg
# Position angle of line of nodes, eq (37)
THETA_LMC = Angle(129.9 * u.deg)  # +/- 6 deg
# # Position angle of transverse motion
# THETA_T_LMC = Angle(78.7 * u.deg)
# Component perpendicular to line of nodes of transverse COM velocity plus nutation/precession. Defined in eq (29). Value from eq (37)
W_TS_LMC = -402.9 * u.km / u.s  # +/- 13 km/s
# Line of sight COM velocity, eq (37)
V_SYS_LMC = 262.2 * u.km / u.s  # +/- 3.4 km/s
# Component parallel to line of nodes of transverse COM velocity, eq (43)
V_TC_LMC = 253 * u.km / u.s  # +/- 50 km/s
# Distance, eq (40)
D_LMC = 50.1 * u.kpc  # +/- 2.5 kpc
# Rotation law flat velocity
V0_ROT_LMC = 50 * u.km / u.s
# Rotation law scale
R0_ROT_LMC = 2.0 * u.kpc


def vrot_lmc_grishunin(radius, r0=0.94 * u.kpc, v_inf=61.1 * u.km / u.s):
    """In-plane rotation law for LMC

    Equation 3 of Grishunin et al (2024).  Default parameters r0,
    v_inf are from that paper but are probably inconsistent with the
    van der Marel results
    """
    return v_inf * np.tanh((radius / r0) * u.rad)


def vrot_lmc_vdM(radius, eta=1.5):
    """In-plane rotation law for LMC

    Equation (36) of van der Marel et al (2022)
    """
    x = radius / R0_ROT_LMC
    return V0_ROT_LMC * x**eta / (x**eta + 1.0)


def vrot_lmc_oh(radius):
    """In-plane rotation law for LMC

        Equation (12) of Oh et al 2022
    `"""
    x = (radius / R0_ROT_LMC).value
    return V0_ROT_LMC * np.sqrt(1 - np.arctan(x) / x)


def geometric_factor(rho, Phi):
    """Geometric factor, vdW eq (25)"""
    return (
        np.cos(INC_LMC) * np.cos(rho)
        - np.sin(INC_LMC) * np.sin(rho) * np.sin(Phi - THETA_LMC)
    ) / np.sqrt(
        np.cos(INC_LMC) ** 2 * np.cos(Phi - THETA_LMC) ** 2
        + np.sin(Phi - THETA_LMC) ** 2
    )


def cylindrical_radius(rho, Phi):
    """Cylindrical radius in disk plane, vdW eq (25)"""
    return D_LMC * np.sin(rho) / geometric_factor(rho, Phi)


def vmodel_lmc(c: SkyCoord, vrotation=vrot_lmc_vdM, rot_kws={}):
    """Model line-of-sight velocity for LMC

    Equation (24) and equation (32) of van der Marel et al (2022)
    """

    # Angular radius from center
    rho = CENTER_LMC.separation(c)
    # Position angle from center
    Phi = CENTER_LMC.position_angle(c)

    # Geometric factor
    f = geometric_factor(rho, Phi)

    # Cylindrical radius in disk plane
    R_prime = cylindrical_radius(rho, Phi)

    # Center of mass (COM) radial ...
    vrad = V_SYS_LMC * np.cos(rho)
    # ... plus (COM transverse plus precession/nutation) perpendicular to THETA_LMC ...
    vrad += W_TS_LMC * np.sin(rho) * np.sin(Phi - THETA_LMC)
    # ... plus COM transverse parallel to THETA_LMC ...
    vrad += V_TC_LMC * np.sin(rho) * np.cos(Phi - THETA_LMC)
    # ... plus rotation
    vrad += (
        -vrotation(R_prime, **rot_kws) * f * np.sin(INC_LMC) * np.cos(Phi - THETA_LMC)
    )

    return vrad

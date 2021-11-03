import numpy as np

from .longitudinal import generate_longitudinal_coordinates
from .linear_normal_form import compute_linear_normal_form
from .assemble_particles import assemble_particles
from .particles import Particles


def generate_matched_gaussian_bunch(num_particles, total_intensity_particles,
                                    nemitt_x, nemitt_y, sigma_z,
                                    particle_ref, R_matrix,
                                    circumference,
                                    alpha_momentum_compaction,
                                    rf_harmonic,
                                    rf_voltage,
                                    rf_phase,
                                    p_increment=0.,
                                    particle_class=Particles,
                                    _context=None, _buffer=None, _offset=None,
                                    ):

    zeta, delta = generate_longitudinal_coordinates(
            distribution='gaussian',
            mass0=particle_ref.mass0,
            q0=particle_ref.q0,
            gamma0=particle_ref.gamma0,
            num_particles=num_particles,
            circumference=circumference,
            alpha_momentum_compaction=alpha_momentum_compaction,
            rf_harmonic=rf_harmonic,
            rf_voltage=rf_voltage,
            rf_phase=rf_phase,
            p_increment=p_increment,
            sigma_z=sigma_z)

    assert len(zeta) == len(delta) == num_particles

    gemitt_x = nemitt_x/particle_ref.beta0/particle_ref.gamma0
    gemitt_y = nemitt_y/particle_ref.beta0/particle_ref.gamma0

    x_norm = np.sqrt(gemitt_x) * np.random.normal(size=num_particles)
    px_norm = np.sqrt(gemitt_x) * np.random.normal(size=num_particles)
    y_norm = np.sqrt(gemitt_y) * np.random.normal(size=num_particles)
    py_norm = np.sqrt(gemitt_y) * np.random.normal(size=num_particles)


    part = assemble_particles(_context=_context, _buffer=_buffer, _offset=_offset,
                      R_matrix=R_matrix,
                      particle_class=particle_class,
                      particle_ref=particle_ref,
                      zeta=zeta, delta=delta,
                      x_norm=x_norm, px_norm=px_norm,
                      y_norm=y_norm, py_norm=py_norm,
                      weight=total_intensity_particles/num_particles)
    return part

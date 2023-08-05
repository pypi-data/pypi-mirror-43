import numpy as np
import shutil
from astropy import cosmology as cosmo

from autolens.data import ccd as im
from autolens.data.array import grids, mask as msk, scaled_array
from autolens.lens import lens_data as li, lens_fit
from autolens.lens import ray_tracing
from autolens.lens.plotters import lens_fit_hyper_plotters
from autolens.model.galaxy import galaxy as g
from autolens.model.profiles import light_profiles as lp, mass_profiles as mp
from test.fixtures import *


@pytest.fixture(name='lens_fit_plotter_path')
def make_lens_fit_plotter_setup():
    return "{}/../../test_files/plotting/fit/".format(os.path.dirname(os.path.realpath(__file__)))


@pytest.fixture(name='galaxy_light')
def make_galaxy_light():
    return g.Galaxy(light=lp.EllipticalSersic(intensity=1.0), redshift=2.0)


@pytest.fixture(name='galaxy_mass')
def make_galaxy_mass():
    return g.Galaxy(mass=mp.SphericalIsothermal(einstein_radius=1.0), redshift=1.0)


@pytest.fixture(name='grid_stack')
def make_grid_stack():
    return grids.GridStack.from_shape_pixel_scale_and_sub_grid_size(shape=(100, 100), pixel_scale=0.05, sub_grid_size=2)


@pytest.fixture(name='image')
def make_image():
    image = scaled_array.ScaledSquarePixelArray(array=np.ones((3, 3)), pixel_scale=1.0)
    noise_map = im.NoiseMap(array=2.0 * np.ones((3, 3)), pixel_scale=1.0)
    psf = im.PSF(array=3.0 * np.ones((1, 1)), pixel_scale=1.0)

    return im.CCDData(image=image, pixel_scale=1.0, noise_map=noise_map, psf=psf)


@pytest.fixture(name='positions')
def make_positions():
    positions = [[[0.1, 0.1], [0.2, 0.2]], [[0.3, 0.3]]]
    return list(map(lambda position_set: np.asarray(position_set), positions))


@pytest.fixture(name='mask')
def make_mask():
    return msk.Mask.circular(shape=((3, 3)), pixel_scale=0.1, radius_arcsec=0.1)


@pytest.fixture(name='lens_data')
def make_lens_image(image, mask):
    return li.LensData(ccd_data=image, mask=mask)


@pytest.fixture(name='fit_lens_only')
def make_fit_lens_only(lens_data, galaxy_light):
    tracer = ray_tracing.TracerImagePlane(lens_galaxies=[galaxy_light], image_plane_grid_stack=lens_data.grid_stack,
                                          cosmology=cosmo.Planck15)
    return lens_fit.fit_lens_data_with_tracer(lens_data=lens_data, tracer=tracer)


@pytest.fixture(name='fit_source_and_lens')
def make_fit_source_and_lens(lens_data, galaxy_light, galaxy_mass):
    tracer = ray_tracing.TracerImageSourcePlanes(lens_galaxies=[galaxy_mass], source_galaxies=[galaxy_light],
                                                 image_plane_grid_stack=lens_data.grid_stack, cosmology=cosmo.Planck15)
    return lens_fit.fit_lens_data_with_tracer(lens_data=lens_data, tracer=tracer)


@pytest.fixture(name='hyper')
def make_hyper():
    class Hyper(object):

        def __init__(self):
            pass

    hyper = Hyper()

    hyper.hyper_model_image = np.array([[3.0, 5.0, 7.0],
                                        [9.0, 8.0, 1.0],
                                        [4.0, 0.0, 9.0]])
    hyper.hyper_galaxy_images = [np.array([[1.0, 3.0, 5.0],
                                           [7.0, 9.0, 8.0],
                                           [6.0, 4.0, 0.0]])]
    hyper.hyper_minimum_values = [0.2, 0.8]

    hyper_galaxy = g.HyperGalaxy(contribution_factor=4.0, noise_factor=2.0, noise_power=3.0)
    hyper.hyper_galaxy = g.Galaxy(light=lp.EllipticalSersic(intensity=1.0), hyper_galaxy=hyper_galaxy)
    return hyper


@pytest.fixture(name='lens_hyper_image')
def make_lens_hyper_image(image, mask, hyper):
    return li.LensDataHyper(ccd_data=image, mask=mask, hyper_model_image=hyper.hyper_model_image,
                            hyper_galaxy_images=hyper.hyper_galaxy_images,
                            hyper_minimum_values=hyper.hyper_minimum_values)


@pytest.fixture(name='fit_hyper_lens_only')
def make_fit_hyper_lens_only(lens_hyper_image, hyper):
    tracer = ray_tracing.TracerImagePlane(lens_galaxies=[hyper.hyper_galaxy],
                                          image_plane_grid_stack=lens_hyper_image.grid_stack)
    return lens_fit.hyper_fit_lens_data_with_tracer(lens_data_hyper=lens_hyper_image, tracer=tracer)


def test__fit_sub_plot_hyper_lens_only(fit_lens_only, fit_hyper_lens_only, plot_patch,
                                                                   lens_fit_plotter_path):

    lens_fit_hyper_plotters.plot_fit_subplot(fit_hyper=fit_hyper_lens_only, fit=fit_lens_only, should_plot_mask=True,
                                             extract_array_from_mask=True, zoom_around_mask=True,
                                             cb_tick_values=[1.0], cb_tick_labels=['1.0'],
                                             output_path=lens_fit_plotter_path,
                                             output_filename='hyper_lens_fit', output_format='png')

    assert lens_fit_plotter_path + 'hyper_lens_fit.png' in plot_patch.paths


def test__fit_individuals__hyper_lens_only__depedent_on_input(fit_hyper_lens_only, fit_lens_only, plot_patch,
                                                               lens_fit_plotter_path):

    lens_fit_hyper_plotters.plot_fit_individuals(fit_hyper=fit_hyper_lens_only, fit=fit_lens_only,
                                                 should_plot_mask=True, extract_array_from_mask=True,
                                                 zoom_around_mask=True,
                                                 should_plot_noise_map=True,
                                                 should_plot_model_image=True,
                                                 should_plot_chi_squared_map=True,
                                                 output_path=lens_fit_plotter_path, output_format='png')

    assert lens_fit_plotter_path + 'fit_model_image.png' in plot_patch.paths

    assert lens_fit_plotter_path + 'fit_residual_map.png' not in plot_patch.paths

    assert lens_fit_plotter_path + 'fit_hyper_chi_squared_map.png' in plot_patch.paths

    assert lens_fit_plotter_path + 'fit_hyper_noise_map.png' in plot_patch.paths

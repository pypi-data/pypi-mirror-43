=========================
SAp CTA data pipeline API
=========================

.. module:: pywicta

The library provides classes which are usable by third party tools.

.. note::

    This project is still in *beta* stage, so the API is not finalized yet.

Benchmark package
-----------------

.. toctree::
   :maxdepth: 1

   pywicta.benchmark.assess <api_benchmark_assess>

Denoising package
-----------------

.. toctree::
   :maxdepth: 1

   pywicta.denoising.wavelets_mrfilter <api_filter_wavelet_mrfilter>
   pywicta.denoising.wavelets_mrtransform <api_filter_wavelet_mrtransform>
   pywicta.denoising.tailcut <api_filter_tailcut>
   pywicta.denoising.abstract_cleaning_algorithm <api_filter_abstract_cleaning_algorithm>
   pywicta.denoising.rejection_criteria <api_filter_rejection_criteria>
   pywicta.denoising.inverse_transform_sampling <api_filter_inverse_transform_sampling>

Image package
-------------

.. toctree::
   :maxdepth: 1

   pywicta.image.hillas_parameters <api_image_hillas_parameters>
   pywicta.image.signal_to_border_distance <api_image_signal_to_border_distance>

I/O package
-----------

.. toctree::
   :maxdepth: 1

   pywicta.io.geometry_converter <api_io_geometry_converter>
   pywicta.io.images <api_io_images>
   pywicta.io.simtel <api_io_simtel>
   pywicta.io.simtel_to_fits <api_io_simtel_to_fits>

Optimization package
--------------------

.. toctree::
   :maxdepth: 1

   pywicta.optimization.bruteforce <api_optimization_bruteforce>
   pywicta.optimization.differential_evolution <api_optimization_differential_evolution>
   pywicta.optimization.saes <api_optimization_saes>
   pywicta.optimization.objectivefunc.tailcut <api_optimization_objectivefunc_tailcut>
   pywicta.optimization.objectivefunc.wavelets_mrfilter <api_optimization_objectivefunc_wavelets_mrfilter>
   pywicta.optimization.objectivefunc.wavelets_mrtransform <api_optimization_objectivefunc_wavelets_mrtransform>


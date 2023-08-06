#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

# This script is provided under the terms and conditions of the MIT license:
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__all__ = ['WaveletTransform']

"""Denoise images using the Starlet transform.

Usage
-----

    starlet.py [-h] [--type-of-filtering STRING]
                    [--filter-thresholds FLOAT LIST]
                    [--last-scale STRING]
                    [--detect-only-positive-structures]
                    [--remove-isolated-pixels]
                    [--noise-cdf-file FILE]
                    [--verbose] [--debug] [--max-images INTEGER]
                    [--telid INTEGER] [--eventid INTEGER]
                    [--camid STRING] [--benchmark STRING]
                    [--label STRING] [--plot] [--saveplot FILE]
                    [--output FILE]
                    FILE [FILE ...]

    Denoise FITS images using the Starlet Transform.

    positional arguments:
      FILE                  The files image to process (FITS).If fileargs is a
                            directory,all FITS files it contains are processed.

    optional arguments:
      -h, --help            show this help message and exit
      --type-of-filtering STRING, -f STRING
                            Type of filtering: hard_filtering,
                            ksigma_hard_filtering
      --filter-thresholds FLOAT LIST, -t FLOAT LIST
                            Thresholds used for the plane filtering.
      --last-scale STRING, -L STRING
                            Last plane treatment: keep, drop, mask
      --detect-only-positive-structures, -p
                            Detect only positive structure
      --remove-isolated-pixels
                            Suppress isolated pixels in the support (scipy
                            implementation)
      --noise-cdf-file FILE
                            The JSON file containing the Cumulated Distribution
                            Function of the noise model used to inject artificial
                            noise in blank pixels (those with a NaN value).
                            Default=None.
      --verbose, -v         Verbose mode
      --debug               Debug mode
      --max-images INTEGER  The maximum number of images to process
      --telid INTEGER       Only process images from the specified telescope
      --eventid INTEGER     Only process images from the specified event
      --camid STRING        Only process images from the specified camera
      --benchmark STRING, -b STRING
                            The benchmark method to use to assess the algorithm
                            for thegiven images
      --label STRING, -l STRING
                            The label attached to the produced results
      --plot                Plot images
      --saveplot FILE       The output file where to save plotted images
      --output FILE, -o FILE
                            The output file path (JSON)

Examples
--------
  ./starlet.py -h
  ./starlet.py ./test.fits
  ipython3 -- ./starlet.py -t 21.5,11.7 ./test.fits
"""

import argparse

from pywicta.denoising.abstract_cleaning_algorithm import AbstractCleaningAlgorithm
from pywicta.denoising.inverse_transform_sampling import EmpiricalDistribution
from pywicta.io import images

from pywi.processing.filtering import hard_filter
from pywi.processing.filtering.hard_filter import filter_planes
from pywi.processing.filtering.pixel_clusters import filter_pixels_clusters as scipy_kill_isolated_pixels
from pywi.processing.filtering.pixel_clusters import filter_pixels_clusters_stats
from pywi.processing.filtering.pixel_clusters import number_of_pixels_clusters
from pywi.processing.transform import starlet
from pywi.processing.transform.starlet import inverse_wavelet_transform
from pywi.processing.transform.starlet import wavelet_transform

from pywi.ui.argparse_commons import add_common_arguments
from pywi.ui.filter_with_starlet import add_arguments

# CONSTANTS ##################################################################

DEBUG = False

##############################################################################

# TODO: remove this redundant class (already defined in pywi.processing.compositing)
class WaveletTransform(AbstractCleaningAlgorithm):
    """The wavelet transform wrapper for ctapipe."""

    def __init__(self):
        super().__init__()
        self.label = "WT (starlet)"  # Name to show in plots

    def clean_image(self,
                    input_image,
                    type_of_filtering=hard_filter.DEFAULT_TYPE_OF_FILTERING,
                    filter_thresholds=hard_filter.DEFAULT_FILTER_THRESHOLDS,
                    last_scale_treatment=starlet.DEFAULT_LAST_SCALE_TREATMENT,
                    detect_only_positive_structures=False,
                    kill_isolated_pixels=False,
                    noise_distribution=None,
                    output_data_dict=None,
                    clusters_threshold=0,
                    **kwargs):
        """Clean the `input_image` image.

        Apply the wavelet transform, filter planes and return the reverse
        transformed image.

        Parameters
        ----------
        input_image : array_like
            The image to clean.
        type_of_filtering : str
            Type of filtering: 'hard_filtering' or 'ksigma_hard_filtering'.
        filter_thresholds : list of float
            Thresholds used for the plane filtering.
        last_scale_treatment : str
            Last plane treatment: 'keep', 'drop' or 'mask'.
        detect_only_positive_structures : bool
            Detect only positive structures.
        kill_isolated_pixels : bool
            Suppress isolated pixels in the support.
        noise_distribution : bool
            The JSON file containing the Cumulated Distribution Function of the
            noise model used to inject artificial noise in blank pixels (those
            with a NaN value).
        output_data_dict : dict
            A dictionary used to return results and intermediate results.
        clusters_threshold : float
            The threshold used to define clusters of pixels (the "level of the sea")

        Returns
        -------
            Return the cleaned image.
        """

        if DEBUG:
            print("Filter thresholds:", filter_thresholds)

        number_of_scales = len(filter_thresholds) + 1

        if not (1 < number_of_scales <= 10):
            # This range ]1,10] is a hard constraint from the starlet transform
            raise ValueError("bad number of scales: {}. Should be 1 < Nbr Scales <= 10. Check that filter_thresholds is a list of number and not a string.".format(number_of_scales))

        if DEBUG:
            print("Number of scales:", number_of_scales)

        # COMPUTE THE WAVELET TRANSFORM #######################################

        wavelet_planes = wavelet_transform(input_image,
                                           number_of_scales=number_of_scales,
                                           noise_distribution=noise_distribution)

        if DEBUG:
            for index, plane in enumerate(wavelet_planes):
                images.plot(plane, "Plane " + str(index))

        # FILTER WAVELET PLANES ###############################################

        filtered_wavelet_planes = filter_planes(wavelet_planes,
                                                method=type_of_filtering,
                                                thresholds=filter_thresholds,
                                                detect_only_positive_structures=detect_only_positive_structures)

        #if DEBUG:
        #    for index, plane in enumerate(filtered_wavelet_planes):
        #        images.plot(plane, "Filtered plane " + str(index))

        # COMPUTE THE INVERSE TRANSFORM #######################################

        cleaned_image = inverse_wavelet_transform(filtered_wavelet_planes,
                                                  last_plane=last_scale_treatment)
        if DEBUG:
            images.plot(cleaned_image, "Cleaned image")

        # KILL ISOLATED PIXELS ################################################

        kill_islands = filter_pixels_clusters_stats(cleaned_image)
        img_cleaned_islands_delta_pe, img_cleaned_islands_delta_abs_pe, img_cleaned_islands_delta_num_pixels = kill_islands
        img_cleaned_num_islands = number_of_pixels_clusters(cleaned_image)

        if output_data_dict is not None:
            output_data_dict["img_cleaned_islands_delta_pe"] = img_cleaned_islands_delta_pe
            output_data_dict["img_cleaned_islands_delta_abs_pe"] = img_cleaned_islands_delta_abs_pe
            output_data_dict["img_cleaned_islands_delta_num_pixels"] = img_cleaned_islands_delta_num_pixels
            output_data_dict["img_cleaned_num_islands"] = img_cleaned_num_islands

        if kill_isolated_pixels:
            cleaned_image = scipy_kill_isolated_pixels(cleaned_image, threshold=clusters_threshold)
            if DEBUG:
                images.plot(cleaned_image, "Cleaned image after island kill")

        return cleaned_image


def main():
    """The main module execution function.

    Contains the instructions executed when the module is not imported but
    directly called from the system command line.
    """

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Denoise FITS images with Wavelet Transform.")

    parser = add_arguments(parser)
    parser = add_common_arguments(parser, nargs="+")

    # COMMON OPTIONS

    CAM_IDS = ("ASTRICam", "CHEC", "DigiCam", "FlashCam", "NectarCam", "LSTCam")

    parser.add_argument("--cluster-threshold", type=float, metavar="FLOAT",
                        help="The threshold for the pixels clusters filtering")

    parser.add_argument("--max-images", type=int, metavar="INTEGER",
                        help="The maximum number of images to process")

    parser.add_argument("--telid", type=int, metavar="INTEGER", 
                        help="Only process images from the specified telescope")

    parser.add_argument("--eventid", type=int, metavar="INTEGER", 
                        help="Only process images from the specified event")

    parser.add_argument("--camid", metavar="STRING", 
                        help="Only process images from the specified camera: {}".format(str(CAM_IDS)))

    parser.add_argument("--benchmark", "-b", metavar="STRING", 
                        help="The benchmark method to use to assess the algorithm for the"
                             "given images")

    parser.add_argument("--label", "-l", default=None,
                        metavar="STRING",
                        help="The label attached to the produced results")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path (JSON)")

    args = parser.parse_args()

    type_of_filtering = args.type_of_filtering
    filter_thresholds_str = args.filter_thresholds
    last_scale_treatment = args.last_scale
    detect_only_positive_structures = args.detect_only_positive_structures
    remove_isolated_pixels = args.remove_isolated_pixels
    noise_cdf_file = args.noise_cdf_file

    verbose = args.verbose
    debug = args.debug
    cluster_threshold = args.cluster_threshold           # TODO: move this argument in PyWI
    max_images = args.max_images
    tel_id = args.telid
    event_id = args.eventid
    cam_id = args.camid
    benchmark_method = args.benchmark
    label = args.label
    plot = args.plot
    saveplot = args.saveplot

    input_file_or_dir_path_list = args.fileargs

    # CHECK OPTIONS #############################

    if type_of_filtering not in hard_filter.AVAILABLE_TYPE_OF_FILTERING:
        raise ValueError('Unknown type of filterning: "{}". Should be in {}'.format(type_of_filtering,
                                                                                    hard_filter.AVAILABLE_TYPE_OF_FILTERING))

    try:
        filter_thresholds = [float(threshold_str) for threshold_str in filter_thresholds_str.split(",")]
    except:
        raise ValueError('Wrong filter thresholds: "{}". Should be in a list of figures separated by a comma (e.g. "3,2,3")'.format(filter_thresholds_str))

    if last_scale_treatment not in starlet.AVAILABLE_LAST_SCALE_OPTIONS:
        raise ValueError('Unknown type of last scale treatment: "{}". Should be in {}'.format(last_scale_treatment ,
                                                                                              starlet.AVAILABLE_LAST_SCALE_OPTIONS))

    # TODO: check the noise_cdf_file value

    #############################################

    if args.output is None:
        output_file_path = "score_wavelets_benchmark_{}.json".format(benchmark_method)
    else:
        output_file_path = args.output

    if noise_cdf_file is not None:
        noise_distribution = EmpiricalDistribution(noise_cdf_file)
    else:
        noise_distribution = None

    cleaning_function_params = {
            "type_of_filtering": type_of_filtering,
            "filter_thresholds": filter_thresholds,
            "last_scale_treatment": last_scale_treatment,
            "detect_only_positive_structures": detect_only_positive_structures,
            "kill_isolated_pixels": remove_isolated_pixels,
            "noise_distribution": noise_distribution,
            "verbose": verbose,
            "cluster_threshold": cluster_threshold
        }

    cleaning_algorithm = WaveletTransform()

    if verbose:
        cleaning_algorithm.verbose = True

    if label is not None:
        cleaning_algorithm.label = label

    output_dict = cleaning_algorithm.run(cleaning_function_params,
                                         input_file_or_dir_path_list,
                                         benchmark_method,
                                         output_file_path,
                                         plot=plot,
                                         saveplot=saveplot,
                                         max_num_img=max_images,
                                         tel_id=tel_id,
                                         event_id=event_id,
                                         cam_id=cam_id,
                                         debug=debug)

if __name__ == "__main__":
    main()


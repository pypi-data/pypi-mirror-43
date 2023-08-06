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

"""
Denoise images with the tail-cut algorithm.

Note
----
    See :mod:`ctapipe.image.cleaning.tailcuts_clean`.
"""

__all__ = ["Tailcut"]

import argparse

from pywicta.denoising.abstract_cleaning_algorithm import AbstractCleaningAlgorithm

from pywicta.io import geometry_converter

from pywi.processing.filtering.pixel_clusters import filter_pixels_clusters as scipy_pixels_clusters_filtering
from pywi.processing.filtering.pixel_clusters import filter_pixels_clusters_stats
from pywi.processing.filtering.pixel_clusters import number_of_pixels_clusters

from ctapipe.image.cleaning import tailcuts_clean

class Tailcut(AbstractCleaningAlgorithm):
    """A tail-cut image cleaning wrapper."""

    def __init__(self):
        super(Tailcut, self).__init__()
        self.label = "Tailcut"  # Name to show in plots

    def clean_image(self,
                    input_img,
                    high_threshold=10.,
                    low_threshold=8.,
                    pixels_clusters_filtering="off",
                    verbose=False,
                    cam_id=None,
                    output_data_dict=None,
                    **kwargs):
        """Apply ctapipe's tail-cut image cleaning on ``input_img``.

        Note
        ----
            The main difference with :mod:`ctapipe.image.cleaning.tailcuts_clean` is that here the cleaning function
            takes 2D Numpy arrays.

        Parameters
        ----------
        input_img : array_like
            The image to clean. Should be a **2D** Numpy array.
        high_threshold : float
            The *core threshold* (a.k.a. *picture threshold*).
        low_threshold : float
            The *boundary threshold*.
        pixels_clusters_filtering : str
            Defines the method used to remove isolated pixels after the tail-cut image cleaning.
            Accepted values are: "off", "scipy" or "mars".

            - "off": don't apply any filtering after the tail-cut image cleaning.
            - "scipy": keep only the largest cluster of pixels after the tail-cut image cleaning.
              See :mod:`pywi.processing.filtering.pixel_clusters` for more information.
            - "mars": apply the same filtering than in CTA-Mars analysis, keep only *significant core pixels* that have
              at least two others *significant core pixels* among its neighbors (a *significant core pixels* is a pixel
              above the *core threshold*).

        verbose : bool
            Print additional messages if ``True``.
        cam_id : str
            The camera ID from which ``input_img`` came from: "ASTRICam", "CHEC", "DigiCam", "FlashCam", "NectarCam" or
            "LSTCam".
        output_data_dict : dict
            An optional dictionary used to transmit internal information to the caller.

        Returns
        -------
        array_like
            The ``input_img`` after tail-cut image cleaning. This is a **2D** Numpy array (i.e. it should be converted
            with :func:`pywicta.io.geometry_converter.image_2d_to_1d` before any usage in ctapipe).
        """

        if cam_id is None:
            raise Exception("cam_id have to be defined")    # TODO

        if not (pixels_clusters_filtering.lower() in ("off", "scipy", "mars")):
            raise ValueError('pixels_clusters_filtering = {}. Accepted values are: "off", "scipy" or "mars".'.format(pixels_clusters_filtering))

        # If low_threshold > high_threshold then low_threshold = high_threshold
        low_threshold = min(high_threshold, low_threshold)

        # 2D ARRAY (FITS IMAGE) TO CTAPIPE IMAGE ###############

        geom_1d = geometry_converter.get_geom1d(cam_id)
        img_1d = geometry_converter.image_2d_to_1d(input_img, cam_id)

        # APPLY TAILCUT CLEANING ##############################

        if pixels_clusters_filtering.lower() == "mars":
            if verbose:
                print("Mars pixels clusters filtering")
            mask = tailcuts_clean(geom_1d,
                                  img_1d,
                                  picture_thresh=high_threshold,
                                  boundary_thresh=low_threshold,
                                  keep_isolated_pixels=False,
                                  min_number_picture_neighbors=2)
        else:
            mask = tailcuts_clean(geom_1d,
                                  img_1d,
                                  picture_thresh=high_threshold,
                                  boundary_thresh=low_threshold,
                                  keep_isolated_pixels=True)
        img_1d[mask == False] = 0

        # CTAPIPE IMAGE TO 2D ARRAY (FITS IMAGE) ###############

        cleaned_img_2d = geometry_converter.image_1d_to_2d(img_1d, cam_id)

        # KILL ISOLATED PIXELS #################################

        img_cleaned_islands_delta_pe, img_cleaned_islands_delta_abs_pe, img_cleaned_islands_delta_num_pixels = filter_pixels_clusters_stats(cleaned_img_2d)
        img_cleaned_num_islands = number_of_pixels_clusters(cleaned_img_2d)

        if output_data_dict is not None:
            output_data_dict["img_cleaned_islands_delta_pe"] = img_cleaned_islands_delta_pe
            output_data_dict["img_cleaned_islands_delta_abs_pe"] = img_cleaned_islands_delta_abs_pe
            output_data_dict["img_cleaned_islands_delta_num_pixels"] = img_cleaned_islands_delta_num_pixels
            output_data_dict["img_cleaned_num_islands"] = img_cleaned_num_islands

        if pixels_clusters_filtering.lower() == "scipy":
            if verbose:
                print("Scipy pixels clusters filtering")
            cleaned_img_2d = scipy_pixels_clusters_filtering(cleaned_img_2d)

        return cleaned_img_2d


def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Denoise FITS images with the tailcut algorithm.")

    parser.add_argument("--high-threshold", "-T", type=float, default=0, metavar="FLOAT", 
                        help="The 'high' threshold value")

    parser.add_argument("--low-threshold", "-t", type=float, default=0, metavar="FLOAT", 
                        help="The 'low' threshold value")

    clusters_help_str = ('Defines the method used to remove isolated pixels after the tail-cut image cleaning. '
                         'Accepted values are: "off" (don\'t apply any filtering after the tail-cut image cleaning), '
                         '"scipy" (keep only the largest cluster of pixels after the tail-cut image cleaning), '
                         '"mars" (apply the same filtering than in CTA-Mars analysis, keep only significant core '
                         'pixels that have at least two others significant core pixels among its neighbors, a '
                         'significant core pixels beeing a pixel above the core threshold).')

    parser.add_argument("--clusters", metavar="STRING", default='off',
                        help=clusters_help_str)

    # COMMON OPTIONS

    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose mode")

    parser.add_argument("--debug", action="store_true",
                        help="Debug mode")

    parser.add_argument("--max-images", type=int, metavar="INTEGER", 
                        help="The maximum number of images to process")

    parser.add_argument("--telid", type=int, metavar="INTEGER", 
                        help="Only process images from the specified telescope")

    parser.add_argument("--eventid", type=int, metavar="INTEGER", 
                        help="Only process images from the specified event")

    parser.add_argument("--camid", metavar="STRING", 
                        help="Only process images from the specified camera")

    parser.add_argument("--benchmark", "-b", metavar="STRING", 
                        help="The benchmark method to use to assess the algorithm for the"
                             "given images")

    parser.add_argument("--label", "-l", default=None,
                        metavar="STRING",
                        help="The label attached to the produced results")

    parser.add_argument("--plot", action="store_true",
                        help="Plot images")

    parser.add_argument("--saveplot", default=None, metavar="FILE",
                        help="The output file where to save plotted images")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path (JSON)")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The files image to process (FITS)."
                             "If fileargs is a directory,"
                             "all FITS files it contains are processed.")

    args = parser.parse_args()

    high_threshold = args.high_threshold
    low_threshold = args.low_threshold
    pixels_clusters_filtering = args.clusters

    verbose = args.verbose
    debug = args.debug
    max_images = args.max_images
    tel_id = args.telid
    event_id = args.eventid
    cam_id = args.camid
    benchmark_method = args.benchmark
    label = args.label
    plot = args.plot
    saveplot = args.saveplot

    input_file_or_dir_path_list = args.fileargs

    if args.output is None:
        output_file_path = "score_tailcut_benchmark_{}.json".format(benchmark_method)
    else:
        output_file_path = args.output

    cleaning_function_params = {
                "high_threshold": high_threshold,
                "low_threshold": low_threshold,
                "pixels_clusters_filtering": pixels_clusters_filtering,
                "verbose": verbose
            }

    cleaning_algorithm = Tailcut()

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


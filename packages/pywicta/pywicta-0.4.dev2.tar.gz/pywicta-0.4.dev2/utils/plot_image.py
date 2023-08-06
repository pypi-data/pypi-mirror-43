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
Plot a FITS file.

Example usages:
  ./utils/plot_image.py -h
  ./utils/plot_image.py ./test.fits
  ipython3 -- ./utils/plot_image.py ./test.fits
"""

import common_functions as common

import argparse
import os
import numpy as np

from pywicta.io import images


def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Plot a FITS file.")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("--output", "-o", default=None, metavar="FILE",
                        help="The output file path (image file)")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The files image to process (FITS)."
                             "If fileargs is a directory,"
                             "all FITS files it contains are processed.")

    args = parser.parse_args()

    quiet = args.quiet
    output = args.output
    input_file_or_dir_path_list = args.fileargs

    # FETCH IMAGES ############################################################

    for input_file_or_dir_path in input_file_or_dir_path_list:

        if os.path.isdir(input_file_or_dir_path):
            input_file_path_list = common.get_fits_files_list(input_directory_path)
        else:
            input_file_path_list = [input_file_or_dir_path]

        # Parse FITS files
        for input_file_path in input_file_path_list:

            # READ THE INPUT FILE #############################################

            fits_images_dict, fits_metadata_dict = images.load_benchmark_images(input_file_path)

            input_img = fits_images_dict["input_image"]
            reference_img = fits_images_dict["reference_image"]

            if input_img.ndim != 2:
                raise Exception("Unexpected error: the input FITS file should contain a 2D array.")

            if reference_img.ndim != 2:
                raise Exception("Unexpected error: the input FITS file should contain a 2D array.")

            # ASSESS OR PRINT THE CLEANED IMAGE ###############################

            base_file_path = os.path.basename(input_file_path)
            base_file_path = os.path.splitext(base_file_path)[0]

            image_list = [input_img, reference_img] 
            title_list = ["Input image", "Reference image"] 

            if output is None:
                output = "{}.pdf".format(base_file_path)

            if not quiet:
                images.plot_list(image_list, title_list, fits_metadata_dict)

            print("Writing", output)
            images.mpl_save_list(image_list, output, title_list, fits_metadata_dict)


if __name__ == "__main__":
    main()


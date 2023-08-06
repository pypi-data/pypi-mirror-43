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

import copy
import datetime
import json
import os
import numpy as np
import random
import sys
import time
import traceback

from pywi.benchmark.metrics.refbased import mse
from pywi.processing.filtering.pixel_clusters import filter_pixels_clusters_stats
from pywi.processing.filtering.pixel_clusters import number_of_pixels_clusters
from pywi.io.images import image_generator
import pywi.io.images

###############################################################################

class AbstractCleaningAlgorithm(object):
    """A convenient optional wrapper to simplify the image cleaning analysis.

    Common processing to run and assess the image cleaning procedure on a set
    of images and save results. This class gather some common procedures to
    avoid code duplication in image cleaning modules:

    * call the cleaning algorithm on an image set;
    * assess the cleaning procedure using a set of estimators;
    * apply various pre-processing and post-processing procedures (e.g.
      geometry conversion);
    * collect and save metadata, results and intermediate values that are
      useful for analysis;
    * measure and save the execution time;
    * manage exceptions;
    * ...

    This abstract class is supposed to be inherited by the others image
    cleaning classes."""

    def __init__(self):
        self.label = "Unknown"  # Name to show in plots
        self.verbose = False    # Debug mode

    def __call__(self, *pargs, **kargs):
        return self.clean_image(*pargs, **kargs)

    def __str__(self):
        return "{}".format(self.algorithm_label)

    def run(self,
            cleaning_function_params,
            input_file_or_dir_path_list,
            benchmark_method,
            output_file_path,
            plot=False,
            saveplot=None,
            ref_img_as_input=False,     # A hack to easily produce CSV files...
            max_num_img=None,
            debug=False):
        """A convenient optional wrapper to simplify the image cleaning analysis.

        Apply the image cleaning analysis on `input_file_or_dir_path_list`,
        apply some pre-processing and post-processing procedures, collect and
        return results, intermediate values and metadata.
        
        Parameters
        ----------
        cleaning_function_params
            A dictionary containing the parameters required for the image
            cleaning method.
        input_file_or_dir_path_list
            A list of file to clean. Can be a list of simtel files, fits files
            or directories containing such files.
        benchmark_method
            The list of estimators to use to assess the image cleaning. If
            `None`, images are cleaned but nothing is returned (can be used
            with e.g. the `plot` and/or `saveplot` options).
        output_file_path
            The result file path (a JSON file).
        plot
            The result of each cleaning is plot if `True`.
        saveplot
            The result of each cleaning is saved if `True`.
        ref_img_as_input
            This option is a hack to easily produce a "flatten" CSV results
            files.
        max_num_img
            The number of images to process among the input set
            (`input_file_or_dir_path_list`).
        debug
            Stop the execution and print the full traceback when an exception
            is encountered if this parameter is `True`. Report exceptions and
            continue with the next input image if this parameter is `False`.
        
        Returns
        -------
        dict
            Results, intermediate values and metadata.
        """

        launch_time = time.perf_counter()

        if benchmark_method is not None:
            io_list = []           # The list of returned dictionaries

        for image in image_generator(input_file_or_dir_path_list,
                                     max_num_images=max_num_img):

            input_file_path = image.meta['file_path']

            if self.verbose:
                print(input_file_path)

            # `image_dict` contains metadata (to be returned) on the current image
            image_dict = {"input_file_path": input_file_path}

            try:
                # READ THE INPUT FILE #####################################

                reference_img = image.reference_image
                pixels_position = image.pixels_position

                if ref_img_as_input:
                    # This option is a hack to easily produce CSV files with
                    # the "null_ref" "cleaning" module...
                    input_img = copy.deepcopy(reference_img)
                else:
                    input_img = image.input_image

                image_dict.update(image.meta)

                if benchmark_method is not None:

                    # FETCH ADDITIONAL IMAGE METADATA #####################

                    delta_pe, delta_abs_pe, delta_num_pixels = filter_pixels_clusters_stats(reference_img)       # TODO: NaN
                    num_islands = number_of_pixels_clusters(reference_img)                                             # TODO: NaN

                    image_dict["img_ref_islands_delta_pe"] = delta_pe
                    image_dict["img_ref_islands_delta_abs_pe"] = delta_abs_pe
                    image_dict["img_ref_islands_delta_num_pixels"] = delta_num_pixels
                    image_dict["img_ref_num_islands"] = num_islands

                    image_dict["img_ref_sum_pe"] = float(np.nansum(reference_img))
                    image_dict["img_ref_min_pe"] = float(np.nanmin(reference_img))
                    image_dict["img_ref_max_pe"] = float(np.nanmax(reference_img))
                    image_dict["img_ref_num_pix"] = int( (reference_img[np.isfinite(reference_img)] > 0).sum() )

                    image_dict["img_in_sum_pe"] = float(np.nansum(input_img))
                    image_dict["img_in_min_pe"] = float(np.nanmin(input_img))
                    image_dict["img_in_max_pe"] = float(np.nanmax(input_img))
                    image_dict["img_in_num_pix"] = int( (input_img[np.isfinite(input_img)] > 0).sum() )

                # CLEAN THE INPUT IMAGE ###################################

                # Copy the image (otherwise some cleaning functions like Tailcut may change it)
                #input_img_copy = copy.deepcopy(input_img)
                input_img_copy = input_img.astype('float64', copy=True)

                cleaning_function_params["output_data_dict"] = {}

                initial_time = time.perf_counter()
                cleaned_img = self.clean_image(input_img_copy, **cleaning_function_params)   # TODO: NaN
                full_clean_execution_time_sec = time.perf_counter() - initial_time

                if benchmark_method is not None:
                    image_dict.update(cleaning_function_params["output_data_dict"])
                    del cleaning_function_params["output_data_dict"]

                # ASSESS OR PRINT THE CLEANED IMAGE #######################

                if benchmark_method is not None:

                    # ASSESS THE CLEANING #################################

                    kwargs = {}  # TODO GEOM
                    score = mse(cleaned_img, reference_img)

                    image_dict["score"] = [score]
                    image_dict["score_name"] = ["mse"]
                    image_dict["full_clean_execution_time_sec"] = full_clean_execution_time_sec

                    image_dict["img_cleaned_sum_pe"] = float(np.nansum(cleaned_img))
                    image_dict["img_cleaned_min_pe"] = float(np.nanmin(cleaned_img))
                    image_dict["img_cleaned_max_pe"] = float(np.nanmax(cleaned_img))
                    image_dict["img_cleaned_num_pix"] = int( (cleaned_img[np.isfinite(cleaned_img)] > 0).sum() )

                # PLOT IMAGES #########################################################

                if plot or (saveplot is not None):
                    image_list = [input_img, reference_img, cleaned_img] 
                    title_list = ["Input image", "Reference image", "Cleaned image"] 

                    if plot:
                        pywi.io.images.plot_list(image_list,
                                                     title_list=title_list,
                                                     metadata_dict=image.meta)

                    if saveplot is not None:
                        plot_file_path = saveplot
                        print("Saving {}".format(plot_file_path))
                        pywi.io.images.mpl_save_list(image_list,
                                                         output_file_path=plot_file_path,
                                                         title_list=title_list,
                                                         metadata_dict=image.meta)

            except Exception as e:
                print("Abort image {}: {} ({})".format(input_file_path, e, type(e)))

                if debug:
                    # The following line print the full trackback
                    traceback.print_tb(e.__traceback__, file=sys.stdout)

                if benchmark_method is not None:

                    # http://docs.python.org/2/library/sys.html#sys.exc_info
                    exc_type, exc_value, exc_traceback = sys.exc_info() # most recent (if any) by default

                    '''
                    Reason this _can_ be bad: If an (unhandled) exception happens AFTER this,
                    or if we do not delete the labels on (not much) older versions of Py, the
                    reference we created can linger.

                    traceback.format_exc/print_exc do this very thing, BUT note this creates a
                    temp scope within the function.
                    '''

                    error_dict = {
                                  'filename': exc_traceback.tb_frame.f_code.co_filename,
                                  'lineno'  : exc_traceback.tb_lineno,
                                  'name'    : exc_traceback.tb_frame.f_code.co_name,
                                  'type'    : exc_type.__name__,
                                  #'message' : exc_value.message
                                  'message' : str(e)
                                 }

                    del(exc_type, exc_value, exc_traceback) # So we don't leave our local labels/objects dangling
                    # This still isn't "completely safe", though!

                    #error_dict = {"type": str(type(e)),
                    #              "message": str(e)}

                    image_dict["error"] = error_dict

            finally:
                if benchmark_method is not None:
                    io_list.append(image_dict)

        if benchmark_method is not None:
            error_list = [image_dict["error"] for image_dict in io_list if "error" in image_dict]
            print("{} images aborted".format(len(error_list)))

            # GENERAL EXPERIMENT METADATA
            output_dict = {}
            output_dict["benchmark_execution_time_sec"] = str(time.perf_counter() - launch_time)
            output_dict["date_time"] = str(datetime.datetime.now())
            output_dict["class_name"] = self.__class__.__name__
            output_dict["algo_code_ref"] = str(self.__class__.clean_image.__code__)
            output_dict["label"] = self.label
            output_dict["cmd"] = " ".join(sys.argv)
            output_dict["algo_params"] = cleaning_function_params

            if "noise_distribution" in output_dict["algo_params"]:
                del output_dict["algo_params"]["noise_distribution"]  # not JSON serializable...

            output_dict["benchmark_method"] = benchmark_method
            output_dict["system"] = " ".join(os.uname())
            output_dict["io"] = io_list

            with open(output_file_path, "w") as fd:
                json.dump(output_dict, fd, sort_keys=True, indent=4)  # pretty print format

            return output_dict

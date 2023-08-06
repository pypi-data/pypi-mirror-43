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

__all__ = ['ObjectiveFunction']

import numpy as np

from pywi.ui.filter_with_mrfilter import WaveletTransform
from pywi.benchmark.metrics.refbased import mse


def norm_angle_diff(angle_in_degrees):
    """Normalize the difference of 2 angles in degree.

    This function is used to normalize the "delta psi" angle.
    """
    return np.abs(np.mod(angle_in_degrees + 90, 180) - 90.)


# OPTIMIZER ##################################################################

class ObjectiveFunction:

    def __init__(self, input_files, noise_distribution=None, max_num_img=None, aggregation_method="mean"):
        self.call_number = 0

        # Init the wavelet class
        self.cleaning_algorithm = WaveletTransform()

        # Make the image list
        self.input_files = input_files
        self.max_num_img = max_num_img

        self.noise_distribution = noise_distribution

        self.aggregation_method = aggregation_method  # "mean" or "median"

        print("aggregation method:", self.aggregation_method)

        # PRE PROCESSING FILTERING ############################################

        # TODO...


    def __call__(self, sigma_list):
        self.call_number += 1

        aggregated_score = np.inf

        try:
            k_sigma_noise_threshold = ",".join([str(sigma) for sigma in sigma_list])

            algo_params_var = {
                        "k_sigma_noise_threshold": k_sigma_noise_threshold
                    }

            benchmark_method = "delta_psi"          # TODO

            label = "WT_{}".format(self.call_number)
            self.cleaning_algorithm.label = label

            output_file_path = "score_wavelets_optim_{}.json".format(self.call_number)

            algo_params = {
                        "coef_detection_method": 1,
                        "correction_offset": False,
                        "detect_only_positive_structure": False,
                        "epsilon": None,
                        "first_detection_scale": None,
                        "input_image_scale": "linear",
                        #"k_sigma_noise_threshold": "2,2,3,3",
                        "filter_pixels_clusters": True,
                        "mask_file_path": None,
                        #"mrfilter_directory": "/dev/shm/.jd",
                        "noise_distribution": self.noise_distribution,
                        "noise_model": 3,
                        "number_of_iterations": None,
                        "number_of_scales": 4,
                        "offset_after_calibration": None,
                        "precision": None,
                        "support_file_name": None,
                        "suppress_isolated_pixels": True,
                        "suppress_last_scale": True,
                        "suppress_positivity_constraint": False,
                        "tmp_files_directory": "/dev/shm/.jd",
                        "type_of_filtering": None,
                        "type_of_filters": None,
                        "type_of_multiresolution_transform": None,
                        "type_of_non_orthog_filters": None,
                        "verbose": False
                    }

            algo_params.update(algo_params_var)

            # TODO: randomly make a subset fo self.input_files
            input_files = self.input_files

            output_dict = self.cleaning_algorithm.run(algo_params,
                                                      input_file_or_dir_path_list=input_files,
                                                      benchmark_method=benchmark_method,
                                                      output_file_path=output_file_path,
                                                      max_num_img=self.max_num_img)

            score_list = []

            # Read and compute results from output_dict
            for image_dict in output_dict["io"]:

                # POST PROCESSING FILTERING #######################################

                # >>>TODO<<<: Filter images: decide wether the image should be used or not ? (contained vs not contained)
                # TODO: filter these images *before* cleaning them to avoid waste of computation...

                # >>>TODO<<<: Filter images by energy range: decide wether the image should be used or not ?
                # TODO: filter these images *before* cleaning them to avoid waste of computation...

                ###################################################################

                # GET THE CLEANED IMAGE SCORE

                raise NotImplementedError()

            # Compute the mean
            if self.aggregation_method == "mean":
                aggregated_score = np.array([score_list]).mean()
            elif self.aggregation_method == "median":
                aggregated_score = np.array([score_list]).median()
            else:
                raise ValueError("Unknown value for aggregation_method: {}".format(self.aggregation_method))

            # TODO: save results in a JSON file (?)
            print(algo_params_var, aggregated_score, self.aggregation_method)
        except Exception as e:
            print(e)

        return float(aggregated_score)


if __name__ == "__main__":
    # Test...

    #func = ObjectiveFunction(input_files=["/Users/jdecock/astri_data/fits/gamma/"])
    #func = ObjectiveFunction(input_files=["./testset/gamma/astri/tel1/"])
    func = ObjectiveFunction(input_files=["/Volumes/ramdisk/flashcam/fits/gamma/"])

    sigma_list = [2, 2, 3, 3]

    score = func(sigma_list)


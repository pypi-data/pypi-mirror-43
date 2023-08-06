#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:42:00 2013
@author: Joel

Description:
Prepare the data for processing
    - Read in the spreadsheet
    - Prepare the format of the output spreadsheets
    - Prepare variables  to be used later
    - Find the most extreme cartesian coordinates for the cells in order to
        set the axes of the WellPatterning plots to the same min and max values
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import numpy as np
import pandas as pd


def load_sample_data(self):
    sample_path = ('https://gitlab.com/stemcellbioengineering/'
                   'context-explorer/raw/master/sample-data/ce-sample.csv')
    self.data = pd.read_csv(sample_path, sep=',')


def load_field_layout(self, radio_button_text):
    if radio_button_text == 'Spiral':
        self.fieldlookuptable = np.array([
            [57, 58, 59, 60, 61, 62, 63, 64, 65],
            [56, 31, 32, 33, 34, 35, 36, 37, 66],
            [55, 30, 13, 14, 15, 16, 17, 38, 67],
            [54, 29, 12,  3,  4,  5, 18, 39, 68],
            [53, 28, 11,  2,  1,  6, 19, 40, 69],
            [52, 27, 10,  9,  8,  7, 20, 41, 70],
            [51, 26, 25, 24, 23, 22, 21, 42, 71],
            [50, 49, 48, 47, 46, 45, 44, 43, 72],
            [81, 80, 79, 78, 77, 76, 75, 74, 73], ])
    elif radio_button_text == 'Meander/Snake':
        self.fieldlookuptable = np.array([
            [1,  2,  3,  4,  5,  6,  7,  8,  9],
            [18, 17, 16, 15, 14, 13, 12, 11, 10],
            [19, 20, 21, 22, 23, 24, 25, 26, 27],
            [36, 35, 34, 33, 32, 31, 30, 29, 28],
            [37, 38, 39, 40, 41, 42, 43, 44, 45],
            [54, 53, 52, 51, 50, 49, 48, 47, 46],
            [55, 56, 57, 58, 59, 60, 61, 62, 63],
            [72, 71, 70, 69, 68, 67, 66, 65, 64],
            [73, 74, 75, 76, 77, 78, 79, 80, 81], ])
    elif radio_button_text == 'Row-wise':
        self.fieldlookuptable = np.array([
            [1,  2,  3,  4,  5,  6,  7,  8,  9],
            [10, 11, 12, 13, 14, 15, 16, 17, 18],
            [19, 20, 21, 22, 23, 24, 25, 26, 27],
            [28, 29, 30, 31, 32, 33, 34, 35, 36],
            [37, 38, 39, 40, 41, 42, 43, 44, 45],
            [46, 47, 48, 49, 50, 51, 52, 53, 54],
            [55, 56, 57, 58, 59, 60, 61, 62, 63],
            [64, 65, 66, 67, 68, 69, 70, 71, 72],
            [73, 74, 75, 76, 77, 78, 79, 80, 81], ])
    elif radio_button_text == 'Mid-snake':
        self.fieldlookuptable = np.array([
            [2,  3,  4,  5,  6,  7,  8,  9, 10],
            [19, 18, 17, 16, 15, 14, 13, 12, 11],
            [20, 21, 22, 23, 24, 25, 26, 27, 28],
            [37, 36, 35, 34, 33, 32, 31, 30, 29],
            [38, 39, 40, 41, 1, 42, 43, 44, 45],
            [54, 53, 52, 51, 50, 49, 48, 47, 46],
            [55, 56, 57, 58, 59, 60, 61, 62, 63],
            [72, 71, 70, 69, 68, 67, 65, 65, 64],
            [73, 74, 75, 76, 77, 78, 79, 80, 81], ])
    else:
        self.fieldlookuptable = np.ones([9, 9]).astype(int)


def preprocessing(self, radio_button_text):
    # Makes it easy to always reference 'Condition' when plotting elsewhere
    # instead of having to check if it is empty and then use the well labels
    if 'Condition' not in self.data.columns:
        self.data['Condition'] = self.data['Well']
    # This needs to happen after clicking the preprocess button
    # So can't have it in the compute_field_size function
    self.pixsize = self.spinBox_field_size.value()
    # Set pixsize to the value in the spinbox whether this was just calculated
    # or prespecified.
    # The given x and y coordinates from imaging instruments can be relative
    # to each field. The below transforms the coordinates to be relative to
    # each well depending on which scanning pattern was chosen.
    self.data['LeftPixsize'] = self.data['Left']
    self.data['TopPixsize'] = self.data['Top']
    load_field_layout(self, radio_button_text)
    if radio_button_text != 'Stitched image':
        self.tp('Computing well coordinates from field coordinates...')
        self.tp('Chosen layout:')
        print(self.fieldlookuptable)
        x_coordinates = np.zeros(len(self.data))
        y_coordinates = np.zeros(len(self.data))
        field_col_name = self.comboBox_field_col.currentText()
        for field_num, field in enumerate(self.data[field_col_name]):
            x_coordinates[field_num] = np.where(
                self.fieldlookuptable == field)[0]
            y_coordinates[field_num] = np.where(
                self.fieldlookuptable == field)[1]
        self.data.TopPixsize = self.data.Top + self.pixsize * x_coordinates
        self.data.LeftPixsize = self.data.Left + self.pixsize * y_coordinates
    self.tp('Done')

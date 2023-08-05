# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 03 22:29:21 2013
@author: Joel

Description:
Main file. Calls the GUI and grabs the status of checkboxes and line edits.
Holds the outline for the analysis process.
"""
import os
import sys
import logging
import operator
from time import time
import traceback as tb
from numbers import Number
from datetime import datetime
from itertools import product

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from natsort import natsorted
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QTableWidgetItem, QFileDialog)

# To print version string on startup
from ._version import get_versions
# Import the interface layouts from the file created with the QtDesigner
# import .gui.context_explorer_design as context_explorer_design
# import .gui.visual_clustering_gui as visual_clustering_gui
from .gui import context_explorer_design
from .gui import visual_clustering_gui
# Import the necessary functions from my scripts
from .data_processing import preprocessing
# from .plot_colonies import plot_colonies
from .plot_colonies import plot_wells_solocpu
from .cluster_cells import cluster_cells_multicpu
from .visual_clustering import done
from .visual_clustering import interactive_clustering
from .visual_clustering import plot_int_clust_results
from .intensity_distributions import prep_histograms
from .intensity_distributions import prep_scatter
from .colony_overlays import prep_colony_overlays
# Import the settings from last time the program ran
# If the program is run for the first time, then skip this step as the settings
# file does not exist yet.
# When the compiled program looks for refs it looks in /library.zip first. If
# the settings file is present there, it won't load from anywhere else.
# Therefore, it is crucial to exclude the settings file in the py2exe setup
# script.  If the program is started from the shortcut (as it most often will
# be), the path to the 'dist' directory where the settings file is kept  needs
# to be added to the system path. If the script is run from an itnerpreterer or
# the program is started from within the directory, this still works and just
# adds an empty path which does no harm.
sys.path.append(os.path.join(os.getcwd() + os.sep, 'dist'))
try:
    from .default_settings import default_directory
except ImportError:
    pass
    # print('You are running ContextExplorer for the first time, have fun!')


class MainWindow(QMainWindow, context_explorer_design.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(os.path.join(os.path.dirname(__file__),
                                       'icons/ce-icon-keep-white.png')),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.tabWidget.setCurrentIndex(0)
        self.pushButton_load_csv.clicked.connect(self.load_csv)
        self.pushButton_assign_columns.clicked.connect(self.assign_columns)
        self.actionExit.triggered.connect(self.close)
        self.pushButton_visual_clustering.clicked.connect(
                self.show_clustering_window)
        self.pushButton_plot_histograms.clicked.connect(
                lambda: prep_histograms(self))
        self.pushButton_plot_scatter.clicked.connect(
                lambda: prep_scatter(self))
        self.pushButton_agg_col_plot.clicked.connect(
                lambda: prep_colony_overlays(self))
        self.pushButton_clear_layout.clicked.connect(
                self.tableWidget_plate_layout.clear)
        self.pushButton_clear_layout.clicked.connect(
            self.change_plate_layout_table)
        self.pushButton_calc_well_coord.clicked.connect(self.calc_well_coord)
        self.pushButton_assign_layout.clicked.connect(self.update_plate_layout)
        self.table = self.tableWidget_plate_layout
        self.clip = QApplication.clipboard()
        if (os.path.basename(os.getcwd()) != 'dist' and
                os.path.isdir(os.getcwd() + os.sep + 'dist')):
            os.chdir(os.getcwd() + os.sep + 'dist')
        self.load_default_settings()
        self.comboBox_scatter_scale_y.hide()
        self.comboBox_scatter_scale_x.hide()
        self.label_xmax_3.hide()
        self.label_xmax_4.hide()
        self.checkBox_agg_col_exclude_cells.hide()
        # Hide the last 2 tabs.
        self.tabWidget.removeTab(self.tabWidget.count() - 1)  # zero indexed
        self.tabWidget.removeTab(self.tabWidget.count() - 1)
        # self.listWidget.hide()
        # self.checkBox_no_plots.hide()
        # self.checkBox_skip_coldetection.hide()
        # self.pushButton_analyze.hide()
        self.groupBox_12.hide()
        plt.ioff()  # turn off interactive plots so that figures don't pop up
        self.pushButton_identify_colonies.clicked.connect(
            self.cluster_cells_multicpu_wrapper)
        self.pushButton_plot_wells.clicked.connect(
            lambda: plot_wells_solocpu(self))
        # self.pushButton_update_well_plot_color.clicked.connect(
        #         self.update_well_plot_color)
        self.label_7.hide()
        self.label_10.hide()
        self.label_11.hide()
        self.label_12.hide()
        self.label_13.hide()
        self.label_14.hide()
        self.label_16.hide()
        self.label_17.hide()
        self.lineEdit_epsilon.hide()
        self.lineEdit_min_pts.hide()
        self.lineEdit_min_size.hide()
        self.lineEdit_min_density.hide()
        self.lineEdit_min_roundness.hide()
        self.lineEdit_max_size.hide()
        self.lineEdit_max_density.hide()
        self.lineEdit_max_roundness.hide()
        self.comboBox_well_plot_save_as.addItems(['.jpg', '.pdf', '.png'])
        self.comboBox_hist_scale.addItems(['linear', 'log'])
        self.comboBox_scatter_scale_x.addItems(['linear', 'log'])
        self.comboBox_scatter_scale_y.addItems(['linear', 'log'])
        self.comboBox_agg_level.addItems(['Colony', 'Condition'])
        self.comboBox_plate_layout.addItems(
            ['24 wells', '96 wells', '384 wells'])
        self.comboBox_plate_layout.currentIndexChanged.connect(
            self.change_plate_layout_table)
        self.comboBox_plate_layout.setCurrentText('96 wells')
        # I use these lists of comboboxes in the `boolen_column` function
        self.boolean_comp_op_combos = [  # comparison operators
            self.comboBox_bool_comp_op_1, self.comboBox_bool_comp_op_2,
            self.comboBox_bool_comp_op_3, self.comboBox_bool_comp_op_4]
        for bool_comp_op in self.boolean_comp_op_combos:
            bool_comp_op.addItems(['>', '<', '=', '≠'])
        # Initialize `well_colony_vertices`, to avoid cumbersome if-expression
        # later on
        self.well_colony_vertices = False
        self.pushButton_add_col_bool.clicked.connect(self.add_column)
        self.pushButton_add_col_apply.clicked.connect(self.add_column_apply)
        self.pushButton_delete_column.clicked.connect(self.delete_column)
        self.pushButton_rename_column.clicked.connect(self.rename_column)
        self.pushButton_delete_outside_cells.clicked.connect(
            self.delete_outside_cells)
        self.pushButton_view_data.clicked.connect(self.view_data)
        self.pushButton_save_data.clicked.connect(self.save_data)
        self.pushButton_save_agg_data.clicked.connect(self.save_agg_data)
        self.checkBox_bool_1.stateChanged.connect(self.change_bool_state_1)
        self.checkBox_bool_2.stateChanged.connect(self.change_bool_state_2)
        self.checkBox_bool_3.stateChanged.connect(self.change_bool_state_3)
        self.checkBox_bool_4.stateChanged.connect(self.change_bool_state_4)
        self.pushButton_view_col_data_types.clicked.connect(
            self.view_column_data_types)
        # Disable field layout
        self.radioButton_stitched.clicked.connect(
            lambda x: self.comboBox_field_col.setEnabled(False))
        self.radioButton_stitched.clicked.connect(
            lambda x: self.label_42.setEnabled(False))
        self.radioButton_stitched.clicked.connect(
            lambda x: self.spinBox_field_size.setEnabled(False))
        self.radioButton_stitched.clicked.connect(
            lambda x: self.label_field_size.setEnabled(False))
        # Enable field layout
        rdio_btns = [self.radioButton_row, self.radioButton_snake,
                     self.radioButton_mid_snake, self.radioButton_spiral]
        for rdio_btn in rdio_btns:
            rdio_btn.clicked.connect(
                lambda x: self.comboBox_field_col.setEnabled(True))
            rdio_btn.clicked.connect(
                lambda x: self.label_42.setEnabled(True))
            rdio_btn.clicked.connect(
                lambda x: self.spinBox_field_size.setEnabled(True))
            rdio_btn.clicked.connect(
                lambda x: self.label_field_size.setEnabled(True))
        print('\ncontext-explorer version {}\n'
              .format(get_versions()['version']))
        # Only allow the use of sequential color maps
        sequential_cmaps = [
            'inferno', 'viridis', 'plasma', 'magma', 'cividis', 'Greys',
            'Purples', 'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr',
            'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu',
            'PuBuGn', 'BuGn', 'YlGn']
        self.comboBox_agg_col_hb_cmap.addItems(sequential_cmaps)

    def change_plate_layout_table(self, num_wells):
        num_wells = int(self.comboBox_plate_layout.currentText().split()[0])
        self.plate_rows = int((num_wells / 1.5) ** (1/2))
        self.plate_cols = int(num_wells / self.plate_rows)
        self.tableWidget_plate_layout.setColumnCount(self.plate_cols)
        self.tableWidget_plate_layout.setRowCount(self.plate_rows)
        # Restore the labels on the headers
        well_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                        'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
        self.plate_well_letters = well_letters[:self.plate_rows]
        self.table.setVerticalHeaderLabels(self.plate_well_letters)
        self.well_labels = [
            label + str(num) for label, num in product(
                self.plate_well_letters, range(1, self.plate_cols + 1))]

    def calc_well_coord(self):
        # Find which radio button is selected
        radio_buttons = [self.radioButton_stitched, self.radioButton_row,
                         self.radioButton_snake, self.radioButton_spiral,
                         self.radioButton_mid_snake]
        radio_button = self.radioButton_stitched
        i = 0
        while not radio_button.isChecked():
            radio_button = radio_buttons[i]
            i += 1
        preprocessing(self, radio_button.text())

    def delete_column(self):
        col_to_delete = self.comboBox_delete_column.currentText()
        self.data = self.data.drop(col_to_delete, axis=1)
        self.tp('Deleted {}\n'.format(col_to_delete))
        self.update_column_combo_boxes()
        return None

    def rename_column(self):
        col_to_rename = self.comboBox_rename_column.currentText()
        new_col_name = self.lineEdit_new_col_name_rename.text()
        self.data = self.data.rename(columns={col_to_rename: new_col_name})
        self.tp('Renamed {} to {}\n'.format(col_to_rename, new_col_name))
        self.update_column_combo_boxes()
        self.lineEdit_new_col_name_rename.clear()
        return None

    def delete_outside_cells(self):
        if 'Colony' in self.data.columns:
            self.data = self.data.loc[self.data['Colony'] != '-1']
            self.tp('Cells deleted')
        else:
            self.tp('Cannot delete cells before colonies have been identified')
        return None

    def change_bool_state_1(self):
        if self.checkBox_bool_1.isChecked():
            self.comboBox_bool_col_1.setEnabled(True)
            self.comboBox_bool_comp_op_1.setEnabled(True)
            self.lineEdit_bool_value_1.setEnabled(True)
        else:
            self.comboBox_bool_col_1.setEnabled(False)
            self.comboBox_bool_comp_op_1.setEnabled(False)
            self.lineEdit_bool_value_1.setEnabled(False)
        return None

    def change_bool_state_2(self):
        if self.checkBox_bool_2.isChecked():
            self.comboBox_bool_col_2.setEnabled(True)
            self.comboBox_bool_comp_op_2.setEnabled(True)
            self.lineEdit_bool_value_2.setEnabled(True)
        else:
            self.comboBox_bool_col_2.setEnabled(False)
            self.comboBox_bool_comp_op_2.setEnabled(False)
            self.lineEdit_bool_value_2.setEnabled(False)
        return None

    def change_bool_state_3(self):
        if self.checkBox_bool_3.isChecked():
            self.comboBox_bool_col_3.setEnabled(True)
            self.comboBox_bool_comp_op_3.setEnabled(True)
            self.lineEdit_bool_value_3.setEnabled(True)
        else:
            self.comboBox_bool_col_3.setEnabled(False)
            self.comboBox_bool_comp_op_3.setEnabled(False)
            self.lineEdit_bool_value_3.setEnabled(False)
        return None

    def change_bool_state_4(self):
        if self.checkBox_bool_4.isChecked():
            self.comboBox_bool_col_4.setEnabled(True)
            self.comboBox_bool_comp_op_4.setEnabled(True)
            self.lineEdit_bool_value_4.setEnabled(True)
        else:
            self.comboBox_bool_col_4.setEnabled(False)
            self.comboBox_bool_comp_op_4.setEnabled(False)
            self.lineEdit_bool_value_4.setEnabled(False)
        return None

    def save_agg_data(self):
        self.tp('Saving...')
        date = datetime.fromtimestamp(time()).strftime('%Y%m%d-%H%M%S')
        agg_level = self.comboBox_agg_level.currentText()
        agg_metrics = [np.mean]  # np.median, np.std]
        agg_base_name = 'aggregated-data-{}-{}.csv'.format(agg_level, date)
        agg_path = os.path.join(self.ce_dir_name, agg_base_name)
        if agg_level == 'Colony':
            if 'Colony' in self.data.columns:
                agg_data = (self.data
                                .groupby(['Condition', 'Well', 'Colony'])
                                .agg(agg_metrics).reset_index())
                agg_data.columns = [col[0] + col[1].capitalize() for col in
                                    agg_data.columns.values]
                agg_data.to_csv(agg_path, index=False, float_format='%.2f')
            else:
                self.tp('Cannot save aggregated colony data before cells have '
                        'been clustered into colonies.')
                return None
        elif agg_level == 'Condition':
            if 'Condition' in self.data.columns:
                agg_data = (self.data
                                .groupby(['Condition'])
                                .agg(agg_metrics).reset_index())
                agg_data.columns = [col[0] + col[1].capitalize() for col in
                                    agg_data.columns.values]
                agg_data.to_csv(agg_path, index=False, float_format='%.2f')
            else:
                self.tp('Cannot save aggregated condition data before cells '
                        'have been assigned conditions in the plate layout')
                return None
        self.tp('Data saved to {}'.format(agg_path))
        return None

    def save_data(self):
        self.tp('Saving...')
        date = datetime.fromtimestamp(time()).strftime('%Y%m%d-%H%M%S')
        file_path = os.path.join(self.ce_dir_name,
                                 'cell-data{}.csv'.format(date))
        self.data.to_csv(file_path, index=False, float_format='%.2f')
        self.tp('Data saved to {}'.format(file_path))
        return None

    def view_data(self):
        self.tp('Selected data:')
        # Negative values can be used to specify the last row
        row_min = self.spinBox_row_min.value()
        row_max = self.spinBox_row_max.value()
        if self.checkBox_view_data_all_cols.isChecked():
            col_name = self.data.columns
        else:
            col_name = self.comboBox_view_data_col.currentText()
        # Allow pandas to display the however many rows and cols are specified
        with pd.option_context("display.max_rows", self.data.shape[0],
                               'display.max_columns', self.data.shape[1]):
            print('{}\n'.format(self.data[col_name].iloc[row_min:row_max]))
        return None

    def view_column_data_types(self):
        width = max([len(col) for col in self.data.columns]) + 5
        self.tp('Column data types:')
        for col in self.data.columns:
            # For mixed data
            if len(self.data[col].apply(type).unique()) > 1:
                print('{0: <{1}}mix of {2}({3})'
                      .format(col, width, ' and '
                              .join(self.data[col]
                                    .apply(lambda x: str(type(x))
                                           .split("'")[1])
                                    .unique()), self.data[col].dtype))
            # All other cases have only 1 dtype so it is safe to check only 1
            # element
            elif isinstance(self.data[col][0], Number):
                print('{0: <{1}}number   ({2})'.format(
                    col, width, str(self.data[col].dtype)))
            elif isinstance(self.data[col][0], str):
                print('{0: <{1}}text     ({2})'.format(
                    col, width, str(self.data[col].dtype)))
            elif isinstance(self.data[col][0], np.bool_):
                print('{0: <{1}}boolean  ({2})'.format(
                    col, width, str(self.data[col].dtype)))
            # For any other type of dtype
            else:
                print('{0: <{1}}{2} ({3})'.format(col, width, str(type(
                    self.data[col][0])).split("'")[1], self.data[col].dtype))
        print('')
        return None

    def add_column_apply(self):
        '''
        Evaluates a user expression and applies it to a column to create a new
        column with the results.
        '''
        # Discussions on how to make eval safer:
        # http://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
        # http://lybniz2.sourceforge.net/safeeval.html
        # "Of course in most cases (desktop programs) the user can't do any
        # more than they could do by writing their own python script, but in
        # some applications (web apps, kiosk computers), this could be a risk."
        # That quote has a valid point, the user can at most wreck their own
        # machine in my case, and only if they really try to. It was still
        # interesting to learn abotu eval safety issues.
        self.tp('Adding new column...')
        apply_str = self.lineEdit_transformation_apply.text()
        new_col_name = self.lineEdit_new_col_name_apply.text()
        apply_col = self.comboBox_add_col_apply.currentText()
        # Create a dictionary for builin functions
        safe_user_funcs = {
            'log10': np.log10, 'log2': np.log2, 'abs': abs, 'len': len}
        # Remove builtin functions and only offer access to the explicity
        # specified functions.
        # The ** are for exapnding the items within those dictionaries and
        # combining it into a new dictionary with the surroundinf {}. This is
        # done since I can't specify `x` other than in the lambda expression.
        try:
            self.data[new_col_name] = (
                self.data[apply_col]
                    .apply(lambda x: eval(apply_str, {'__builtins__': None},
                                          {**safe_user_funcs, **{'x': x}})))
            self.update_column_combo_boxes()
            self.tp('Added column {}.\n'.format(new_col_name))
        except TypeError:
            self.tp(
                'ERROR. Possible reasons:\n1.You are trying to perform a '
                'numerical operation on a text column or vice versa. Check '
                'the column data types.\n2.You are trying to use an unknown '
                'function. The available functions are {}.\n'.format(
                    ', '.join([func for func in safe_user_funcs])))
        except SyntaxError:
            self.tp('Expression syntax incorrect. Expression string empty?\n')
        self.lineEdit_new_col_name_apply.clear()
        return None

    def add_column(self):
        self.tp('Adding new column...')
        new_col_name = self.lineEdit_new_col_name.text()
        comp_list = []
        if self.checkBox_bool_1.isChecked():
            comp_list.append([
                self.comboBox_bool_col_1.currentText(),
                self.comboBox_bool_comp_op_1.currentText(),
                self.lineEdit_bool_value_1.text()])
        if self.checkBox_bool_2.isChecked():
            comp_list.append([
                self.comboBox_bool_col_2.currentText(),
                self.comboBox_bool_comp_op_2.currentText(),
                self.lineEdit_bool_value_2.text()])
        if self.checkBox_bool_3.isChecked():
            comp_list.append([
                self.comboBox_bool_col_3.currentText(),
                self.comboBox_bool_comp_op_3.currentText(),
                self.lineEdit_bool_value_3.text()])
        if self.checkBox_bool_4.isChecked():
            comp_list.append([
                self.comboBox_bool_col_4.currentText(),
                self.comboBox_bool_comp_op_4.currentText(),
                self.lineEdit_bool_value_4.text()])
        comp_op_dict = {
            '>': operator.gt, '<': operator.lt,
            '=': operator.eq, '≠': operator.ne}
        bool_results = []
        res_comb_df = pd.Series(np.ones(self.data.shape[0]), dtype=bool)
        self.tp('Condition:')
        for comp_col, comp_op, comp_value in comp_list:
            if comp_value == '':
                comp_value = '[Empty]'
            self.tp('{} {} {}'.format(comp_col, comp_op, comp_value))
            if comp_value.isdigit():
                comp_value = float(comp_value)
            try:
                res = comp_op_dict[comp_op](self.data[comp_col], comp_value)
            except TypeError:
                # Try to print a helpful error message
                width = len(comp_col) + 1
                # For mixed data
                if len(self.data[comp_col].apply(type).unique()) > 1:
                    comp_col_print = (
                        '{0: <{1}}mix of {2} ({3})'
                        .format(comp_col, width, ' and '
                                .join(self.data[comp_col]
                                      .apply(lambda x: str(type(x))
                                             .split("'")[1])
                                      .unique()),
                                self.data[comp_col].dtype))
                # All other cases have only 1 dtype so it is safe to check only
                # 1 element
                elif isinstance(self.data[comp_col][0], Number):
                    comp_col_print = '{0: <{1}}number ({2})'.format(
                        comp_col, width, self.data[comp_col].dtype)
                elif isinstance(self.data[comp_col][0], str):
                    comp_col_print = '{0: <{1}}text ({2})'.format(
                        comp_col, width, self.data[comp_col].dtype)
                elif isinstance(self.data[comp_col][0], np.bool_):
                    comp_col_print = '{0: <{1}}boolean ({2})'.format(
                        comp_col, width, self.data[comp_col].dtype)
                # For any other dtype
                else:
                    comp_col_print = '{0: <{1}}{2} ({3})'.format(
                        comp_col, width, str(type(self.data[comp_col][0]))
                        .split("'")[1], self.data[comp_col].dtype)
                self.tp(
                    'ERROR: The values in the {0} column are of a different '
                    'type than comparison value.'.format(comp_col))
                self.tp(
                    'Comparison value data type: {0: <{1}}{2}'
                    .format(comp_value, width,
                            str(type(comp_value)).split("'")[1]))
                self.tp('          Column data type: {0}\n'
                        .format(comp_col_print))
                break
            # Abbreviate True/False to facilitate use in figure legends
            res_comb_df = res_comb_df & res
            tf_res = ['T' if x else 'F' for x in res]
            bool_results.append(tf_res)

        # Only create the column if the comparison above was valid
        if 'res' in locals():
            bool_tuples = list(zip(*bool_results))
#             self.data[new_col_name] = bool_tuples
            # Compress tuples to facilitate use in figure legends
#             self.data[new_col_name] = self.data[new_col_name].str.join('')
            self.data[new_col_name] = res_comb_df
            self.tp('Added column {}.'.format(new_col_name))
            self.update_column_combo_boxes()
            # Save paramters so it is possible to keep track of what conditino
            # the True/False value in a column represents
            list_to_save = list_to_save = [('ColumnName', new_col_name)]
            list_to_save.extend([(x[0], x[2]) for x in comp_list])
            # Easier to make it into a data frame than including new imports
            # just to save this list.
            date = datetime.fromtimestamp(time()).strftime('%Y%m%d-%H%M%S')
            pd.DataFrame(list_to_save).to_csv(
                os.path.join(self.ce_dir_name, 'add-column-params-{}.csv'
                             .format(date)), header=False, index=False)
            #  Need to delete, otherwise `res` is kept in `locals()` for the
            #  next runand ruins the conditional above
            del res
        self.lineEdit_new_col_name.clear()
        print('')
        return None

    def cluster_cells_multicpu_wrapper(self):
        # Record all the params specified in the gui
        self.cluster_params = {}
        self.cluster_params['eps'] = float(self.lineEdit_epsilon.text())
        self.cluster_params['min_samples'] = float(
            self.lineEdit_min_pts.text())
        self.cluster_params['min_size'] = float(self.lineEdit_min_size.text())
        self.cluster_params['max_size'] = float(self.lineEdit_max_size.text())
        self.cluster_params['min_density'] = float(
            self.lineEdit_min_density.text())
        self.cluster_params['max_density'] = float(
            self.lineEdit_max_density.text())
        self.cluster_params['min_roundness'] = float(
            self.lineEdit_min_roundness.text())
        self.cluster_params['max_roundness'] = float(
            self.lineEdit_max_roundness.text())
        self.well_colony_vertices = cluster_cells_multicpu(
            self, self.cluster_params)
        self.update_column_combo_boxes()
        # Set sane default values on the comboBoxes after clustering
        if self.comboBox_agg_col_hb_x.currentIndex() == 0:
            self.comboBox_agg_col_hb_x.setCurrentText('XRelativeCentroid')
        if self.comboBox_agg_col_hb_y.currentIndex() == 0:
            self.comboBox_agg_col_hb_y.setCurrentText('YRelativeCentroid')
        if self.comboBox_agg_col_line_x.currentIndex() == 0:
            self.comboBox_agg_col_line_x.setCurrentText('NormDistBorder')
        return None

    def update_well_plot_color(self):
        self.comboBox_well_plot_color.clear()
        self.comboBox_well_plot_color.addItems(self.data.columns)
        return None

    def tp(self, string):
        '''
        tp = time_print, prefaces the string with the current time.
        More convenient under self, so it needn't be passed around everywhere.
        '''
        current_time = datetime.now().strftime('[%H:%M:%S]')
        if string[0] == '\n':
            print('\n{} {}'.format(current_time, string[1:]))
        else:
            print('{} {}'.format(current_time, string))
        return None

    def update_plate_layout(self):
        self.plate_layout_dict = {}
        # Go through all rows and columns
        self.tp('\nUpdating plate layout...')
        for row, well_letter in enumerate(self.plate_well_letters):
            for col in range(self.plate_cols):
                # Append the values to the list. If there is an empty cell,
                # move on to the next.
                try:
                    self.plate_layout_dict[well_letter + str(col+1)] = (
                        str(self.table.item(row, col).text()))
                except AttributeError:
                    self.plate_layout_dict[well_letter + str(col+1)] = ''
        # Since the data_preprocessing already sets ['Condition'] = ['Well'],
        # it only need to be updated if the user has specified conditions
        if not all([plate_label == '' for plate_label in
                    self.plate_layout_dict.values()]):
            self.data['Condition'] = self.data['Well'].apply(
                    lambda x: self.plate_layout_dict[x])
        self.tp('Done')

    def load_default_settings(self):
        # Always define `default_dir`, allows for brevity in the `load_csv` def
        self.default_dir = os.getcwd()
        self.default_dir = default_directory
        # If the settings file has been imported
        if 'default_settings' in sys.modules.keys():
            if hasattr(self, 'default_directory'):
                self.default_dir = default_directory
            # if hasattr(default_settings, 'EpsDistance'):
            #     self.lineEdit_epsilon.setText(
            #         str(default_settings.EpsDistance))
            # if hasattr(default_settings, 'MaxColonyRoundness'):
            #     self.lineEdit_max_roundness.setText(
            #         str(default_settings.MaxColonyRoundness))
            # if hasattr(default_settings, 'MaxColonySize'):
            #     self.lineEdit_max_size.setText(
            #         str(default_settings.MaxColonySize))
            # if hasattr(default_settings, 'MaxColonyDensity'):
            #     self.lineEdit_max_density.setText(
            #         str(default_settings.MaxColonyDensity))
            # if hasattr(default_settings, 'MinColonyRoundness'):
            #     self.lineEdit_min_roundness.setText(
            #         str(default_settings.MinColonyRoundness))
            # if hasattr(default_settings, 'MinColonySize'):
            #     self.lineEdit_min_size.setText(
            #         str(default_settings.MinColonySize))
            # if hasattr(default_settings, 'MinColonyDensity'):
            #     self.lineEdit_min_density.setText(
            #         str(default_settings.MinColonyDensity))
            # if hasattr(default_settings, 'IQR'):
            #     self.lineEdit_iqr.setText(str(default_settings.IQR))

    def keyPressEvent(self, e):
        # This function must be named 'keyPressEvent'. It captures all
        # keypresses and checks if they meet any of the specific keypresses
        # listed in the if-conditions. e = event
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            selected = self.table.selectedRanges()
            # Enables copying into multiple cells of the QtTableWidget from
            # excel and tab separated text files.
            if e.key() == QtCore.Qt.Key_V:  # paste
                first_row = selected[0].topRow()
                first_col = selected[0].leftColumn()
                # copied text is split by '\n' and '\t' to paste to the cells
                for r, row in enumerate(self.clip.text().split('\n')):
                    for c, text in enumerate(row.split('\t')):
                        self.table.setItem(
                            first_row+r, first_col+c, QTableWidgetItem(text))
                # Resize the column width to fit the names of the conditions.
                self.table.resizeColumnsToContents()
                self.plate_layout = []
                # Go through all rows and columns
                for row in range(0, 8):
                    for col in range(0, 12):
                        # Append the values to the list. If there is an empty
                        # cell, move on to the next.
                        try:
                            self.plate_layout.append(
                                str(self.table.item(row, col).text()))
                        except AttributeError:
                            self.plate_layout.append("")
                # Filter out empty items from the list. Some empty cells seems
                # to be read to the list and not filtered in the previous step
                # so that is why this is needed.
#                self.plate_layout = [item for item
#                    in self.plate_layout if item != '']
                # Set the dictionary key of the currently selected item to the
                # current plate layout
#                 self.all_plate_layouts[
#                    str(self.listWidget.currentItem().text())]
                # = self.plate_layout
#                print(self.plate_layout)
            # This is to copy from the table to somewhere else. Will probably
            # not be used that much
            elif e.key() == QtCore.Qt.Key_C:  # copy
                s = ""
                for r in range(selected[0].topRow(),
                               selected[0].bottomRow()+1):
                    for c in range(selected[0].leftColumn(),
                                   selected[0].rightColumn()+1):
                        try:
                            s += str(self.table.item(r, c).text()) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n"  # eliminate last '\t'
                self.clip.setText(s)

    def show_clustering_window(self):
        # Open the window. When no file is selected, print an error message
        if self.file_path == '':
            self.tp('No file selected. Load a file before optimizing the '
                    'clustering parameters.')
        else:
            # Assign the ClusteringWindow class to a variable
            # (self.clustering_window) in the main window of the application.
            # Values from the clustering window can be reached even after it is
            # closed by typing for example:
            # self.clustering_window.doubleSpinBox_distance.value()
            self.clustering_window = ClusteringWindow(self)
            # Display the window as a non-modal dialog. To display as a modal
            # dialog, use 'exec_' instead of 'show'.
            self.clustering_window.show()
            self.clustering_window.data_cluster = self.data.copy()
            self.clustering_window.spinBox_resolution.setValue(256)
            self.clustering_window.spinBox_resolution.setKeyboardTracking(
                False)
            self.clustering_window.spinBox_resolution.valueChanged.connect(
                self.plot_colony_clusters_wrapper)
            # Set the eps and minPts parameters to the ones in the main window.
            self.clustering_window.doubleSpinBox_distance.setValue(
                float(self.lineEdit_epsilon.text()))
            self.clustering_window.doubleSpinBox_min_points.setValue(
                float(self.lineEdit_min_pts.text()))
            # Set the sliders to these values as well
            self.clustering_window.horizontalSlider_distance.setValue(
                float(self.lineEdit_epsilon.text()))
            self.clustering_window.horizontalSlider_min_points.setValue(
                float(self.lineEdit_min_pts.text()))
            # Set the min and max size to the values in the main window.
            self.clustering_window.lineEdit_min_density.setText(
                str(self.lineEdit_min_density.text()))
            self.clustering_window.lineEdit_max_density.setText(
                str(self.lineEdit_max_density.text()))
            self.clustering_window.lineEdit_min_roundness.setText(
                str(self.lineEdit_min_roundness.text()))
            self.clustering_window.lineEdit_max_roundness.setText(
                str(self.lineEdit_max_roundness.text()))
            self.clustering_window.lineEdit_min_size.setText(
                str(self.lineEdit_min_size.text()))
            self.clustering_window.lineEdit_max_size.setText(
                str(self.lineEdit_max_size.text()))
#            self.clustering_window.lineEdit_ch1_min.setText(
#                str(self.lineEdit_ch1_min.text()))
#            self.clustering_window.lineEdit_ch1_max.setText(
#                str(self.lineEdit_ch1_max.text()))
#            self.clustering_window.lineEdit_ch2_min.setText(
#                str(self.lineEdit_ch2_min.text()))
#            self.clustering_window.lineEdit_ch2_max.setText(
#                str(self.lineEdit_ch2_max.text()))
#            self.clustering_window.lineEdit_ch3_min.setText(
#                str(self.lineEdit_ch3_min.text()))
#            self.clustering_window.lineEdit_ch3_max.setText(
#                str(self.lineEdit_ch3_max.text()))
            # Redraw plot when enter is pressed in a filter value box
            (self.clustering_window.lineEdit_min_density.returnPressed
                .connect(self.plot_int_clust_results_wrapper))
            (self.clustering_window.lineEdit_max_density.returnPressed
                .connect(self.plot_int_clust_results_wrapper))
            (self.clustering_window.lineEdit_min_roundness.returnPressed
                .connect(self.plot_int_clust_results_wrapper))
            (self.clustering_window.lineEdit_max_roundness.returnPressed
                .connect(self.plot_int_clust_results_wrapper))
            (self.clustering_window.lineEdit_min_size.returnPressed
                .connect(self.plot_int_clust_results_wrapper))
            (self.clustering_window.lineEdit_max_size.returnPressed
                .connect(self.plot_int_clust_results_wrapper))
            # (self.clustering_window.doubleSpinBox_min_points.valueChanged
            #     .connect(self.plot_colony_clusters_wrapper))
            # (self.clustering_window.doubleSpinBox_distance.valueChanged
            #     .connect(self.plot_colony_clusters_wrapper))
#            self.clustering_window.lineEdit_ch1_min.returnPressed.connect(
#                self.plot_colony_clusters_wrapper())
#            self.clustering_window.lineEdit_ch1_max.returnPressed.connect(
#                self.plot_colony_clusters_wrapper())
#            self.clustering_window.lineEdit_ch2_min.returnPressed.connect(
#                self.plot_colony_clusters_wrapper())
#            self.clustering_window.lineEdit_ch2_max.returnPressed.connect(
#                self.plot_colony_clusters_wrapper())
#            self.clustering_window.lineEdit_ch3_min.returnPressed.connect(
#                self.plot_colony_clusters_wrapper())
#            self.clustering_window.lineEdit_ch3_max.returnPressed.connect(
#                self.plot_colony_clusters_wrapper())
            # Connect all the buttons to their respective functions
            # One way to pass an argument with a function in a button connect,
            # is to use lambda. Another is with
            # button1.clicked.connect(partial(self.on_button, 1))
            # See
            # http://eli.thegreenplace.net/2011/04/25/passing-extra-arguments-to-pyqt-slot/
            # Dont really need this plot button, just plot automatically from
            # the beginning
    #        self.clustering_window.pushButton_plot.clicked.connect(self.plot_colony_clusters_wrapper())
            # Populate the well spin box with the unique well values and replot
            # when the well in the spinbox value is changed.
            self.clustering_window.comboBox_wells.addItems(
                natsorted(self.clustering_window.data_cluster['Well']
                          .astype(str)
                          .unique()))
            self.clustering_window.comboBox_wells.activated.connect(
                self.plot_colony_clusters_wrapper)
            # Populate the color spin box with the column names and replot
            # when the column in the spinbox value is changed.
            self.clustering_window.comboBox_color.addItems(
                natsorted(self.clustering_window.data_cluster
                          .select_dtypes([np.number])
                          .columns))
            self.clustering_window.comboBox_color.activated.connect(
                self.plot_colony_clusters_wrapper)

            # Link the sliders to the spinboxes so that one updates when the
            # value is changed in the other.
            (self.clustering_window.horizontalSlider_distance.sliderMoved
                .connect(self.clustering_window.doubleSpinBox_distance
                         .setValue))
            (self.clustering_window.horizontalSlider_min_points.sliderMoved
                .connect(self.clustering_window.doubleSpinBox_min_points
                         .setValue))
            # Turning off keyboard tracking causes the signal only to be
            # omitted when the enter key is pressed, focus is lost, or arrows
            # are clicked, rather than as soon as a value is entered.
            (self.clustering_window.doubleSpinBox_distance.
                setKeyboardTracking(False))
            (self.clustering_window.doubleSpinBox_min_points.
                setKeyboardTracking(False))
            (self.clustering_window.doubleSpinBox_distance.valueChanged
                .connect(self.clustering_window.horizontalSlider_distance
                         .setValue))
            (self.clustering_window.doubleSpinBox_min_points.valueChanged
                .connect(self.clustering_window.horizontalSlider_min_points
                         .setValue))
            # self.clustering_window.doubleSpinBox_top_edge.setKeyboardTracking(False)
            # self.clustering_window.doubleSpinBox_bottom_edge.setKeyboardTracking(False)
            # self.clustering_window.doubleSpinBox_left_edge.setKeyboardTracking(False)
            # self.clustering_window.doubleSpinBox_right_edge.setKeyboardTracking(False)
            # self.clustering_window.doubleSpinBox_top_edge.valueChanged.connect(
            #     self.plot_colony_clusters_wrapper)
            # self.clustering_window.doubleSpinBox_bottom_edge.valueChanged.connect(
            #     self.plot_colony_clusters_wrapper)
            # self.clustering_window.doubleSpinBox_left_edge.valueChanged.connect(
            #     self.plot_colony_clusters_wrapper)
            # self.clustering_window.doubleSpinBox_right_edge.valueChanged.connect(
            #     self.plot_colony_clusters_wrapper)

            # Replot when the sliders are moved (and since they are linked also
            # when the value in the spinboxes change.
            (self.clustering_window.horizontalSlider_distance.sliderReleased
                .connect(self.plot_colony_clusters_wrapper))
            (self.clustering_window.horizontalSlider_min_points.sliderReleased
                .connect(self.plot_colony_clusters_wrapper))
            # Set the layout to the matplotlib widget canvas to tight.
            self.clustering_window.widget_matplotlib.canvas.fig.tight_layout()
            # Exit when the done-button is clicked
            self.clustering_window.pushButton_done.clicked.connect(
                lambda: done(self))
            # Run the plot function as the window opens.
            self.plot_colony_clusters_wrapper()
        return None

    def plot_colony_clusters_wrapper(self):
        # Read in values from the gui
        int_clust_color_col = str(
            self.clustering_window.comboBox_color.currentText())
        self.int_clust_db, self.int_clust_data = (
                interactive_clustering(self, int_clust_color_col))
        self.plot_int_clust_results_wrapper()

    def plot_int_clust_results_wrapper(self):
        visual_plot_params = {}
        visual_plot_params['min_roundness'] = float(
            self.clustering_window.lineEdit_min_roundness.text())
        visual_plot_params['max_roundness'] = float(
            self.clustering_window.lineEdit_max_roundness.text())
        visual_plot_params['min_size'] = float(
            self.clustering_window.lineEdit_min_size.text())
        visual_plot_params['max_size'] = float(
            self.clustering_window.lineEdit_max_size.text())
        visual_plot_params['min_density'] = float(
            self.clustering_window.lineEdit_min_density.text())
        visual_plot_params['max_density'] = float(
            self.clustering_window.lineEdit_max_density.text())
        visual_plot_params['ch1_min'] = float(
            self.clustering_window.lineEdit_ch1_min.text())
        visual_plot_params['ch1_max'] = float(
            self.clustering_window.lineEdit_ch1_max.text())
        visual_plot_params['ch2_min'] = float(
            self.clustering_window.lineEdit_ch2_min.text())
        visual_plot_params['ch2_max'] = float(
            self.clustering_window.lineEdit_ch2_max.text())
        visual_plot_params['ch3_min'] = float(
            self.clustering_window.lineEdit_ch3_min.text())
        visual_plot_params['ch3_max'] = float(
            self.clustering_window.lineEdit_ch3_max.text())
        visual_plot_params['top_edge'] = (
            self.clustering_window.doubleSpinBox_top_edge.value() / 100)
        visual_plot_params['bottom_edge'] = (
            self.clustering_window.doubleSpinBox_bottom_edge.value() / 100)
        visual_plot_params['left_edge'] = (
            self.clustering_window.doubleSpinBox_left_edge.value() / 100)
        visual_plot_params['right_edge'] = (
            self.clustering_window.doubleSpinBox_right_edge.value() / 100)
        plot_int_clust_results(self, self.int_clust_db, self.int_clust_data,
                               visual_plot_params)

    def update_column_combo_boxes(self, exclude_cols=[]):
        '''
        Refill the column list for all comboboxes. Should be run every time a
        new column is added/deleted to the data frame and when a new data frame
        is loaded.
        '''
        all_columns_combos = [
            self.comboBox_well_plot_color,
            self.comboBox_bool_col_1, self.comboBox_bool_col_2,
            self.comboBox_bool_col_3, self.comboBox_bool_col_4,
            self.comboBox_view_data_col, self.comboBox_delete_column,
            self.comboBox_add_col_apply, self.comboBox_rename_column,
            self.comboBox_x_col, self.comboBox_y_col,
            self.comboBox_well_col]
        all_columns_combos = [
            cb for cb in all_columns_combos if cb not in exclude_cols]
        all_columns = self.data.columns.sort_values()
        for combo_box in all_columns_combos:
            previous_item = combo_box.currentText()
            combo_box.clear()
            combo_box.addItems(all_columns)
            # If the previous item has been removed, this gracefully selects
            # the next
            combo_box.setCurrentText(previous_item)
        # Numerical only
        numerical_columns_combos = [
            self.comboBox_hist_col,
            self.comboBox_scatter_col_x, self.comboBox_scatter_col_y,
            self.comboBox_agg_col_line_x, self.comboBox_agg_col_line_y,
            self.comboBox_agg_col_hb_y, self.comboBox_agg_col_hb_x,
            self.comboBox_agg_col_hb_color, self.comboBox_field_col]
        numerical_columns_combos = [
            cb for cb in numerical_columns_combos if cb not in exclude_cols]
        numerical_columns = [
            col for col in self.data.columns.sort_values() if
            self.data[col].dtype == int or self.data[col].dtype == float]
        for combo_box in numerical_columns_combos:
            previous_item = combo_box.currentText()
            combo_box.clear()
            combo_box.addItems(numerical_columns)
            # If the previous item has been removed, this gracefully selects
            # the next
            combo_box.setCurrentText(previous_item)
        self.comboBox_scatter_col_y.setCurrentIndex(1)
        return None

    def standardize_well_names(self, well_str):
        '''
        Standardize well names by removing leading zeros (A01 --> A1)
        '''
        if well_str[1] == '0':
            return well_str[0] + well_str[2]
        else:
            return well_str

    def load_csv(self):
        '''
        Read the selected csv-file into a pandas data frame.
        '''
        # All that is needed for multiple files is to add an "s":
        # getOpenFileNames
        self.file_path = QFileDialog.getOpenFileName(
            self, "Open File Dialog", directory=self.default_dir,
            filter="CSV-files (*.csv)")[0]
        value_sep = self.lineEdit_value_sep.text()
        dec_sep = self.lineEdit_decimal_sep.text()
        com_prefix = self.lineEdit_comment_prefix.text()
        thousands_sep = self.lineEdit_thousands_sep.text()
        if len(thousands_sep) < 1:
            thousands_sep = None
        # self.file_path = ('/home/joel/edu/phd/ce/src/context-explorer/'
        #                   'sample-data/ce-sample.csv')
        if self.file_path == '':
            self.tp('No file selected')
            self.label_open_file.setText('No file selected')
        else:
            self.tp('Loading data...')
            # It is much faster to have the separator fixed and allow only for
            # csv-files
            self.data = pd.read_csv(
                self.file_path, engine='c', sep=value_sep,
                thousands=thousands_sep, decimal=dec_sep, comment=com_prefix,
                skipinitialspace=True)
            # Drop any columns without values
            self.data.dropna(inplace=True, axis=1, how='all')
            self.label_open_file.setText(self.file_path)
            self.tp('Loaded {}'.format(self.file_path))
            self.tp((
                'There are {} rows and {} columns in this dataframe'.format(
                    self.data.shape[0], self.data.shape[1])))
            self.tp('Displaying the first three rows for all columns:')
            print(self.data.head(3))
            # Create a directory for all the analyses files
            base_name = os.path.basename(os.path.splitext(self.file_path)[0])
            dir_name = os.path.dirname(os.path.splitext(self.file_path)[0])
            self.ce_dir_name = os.path.join(
                dir_name, 'CE-{}'.format(base_name))
            if not os.path.exists(self.ce_dir_name):
                os.mkdir(self.ce_dir_name)
            # Don't replace the default directory with an empty line if the
            # user cancels the open dialogue
            if not self.file_path == []:
                # Save the settings as soon as the open file dialog is closed
                # so that the new directory is opened were the 'open' button to
                # be clicked again
                self.default_dir = os.path.dirname(self.file_path)
            # Clear the plate layout when a new file is opened
#            self.tableWidget_plate_layout.clear()
            # Reset the field resolution value so that it is recalculated later
            # and not mistaken for user input, which prevents the calculation
            self.spinBox_resolution.setValue(0)
            self.update_column_combo_boxes()
            # Set default combobox values for data from CellProfiler,
            # cellomics, or that has previously been run through CE.
            if 'WellId' in self.data.columns:
                self.comboBox_well_col.setCurrentText('WellId')
            elif 'Metadata_Well' in self.data.columns:
                self.comboBox_well_col.setCurrentText('Metadata_Well')
            elif 'Well' in self.data.columns:
                self.comboBox_well_col.setCurrentText('Well')
            if 'XCentroid' in self.data.columns:
                self.comboBox_x_col.setCurrentText('XCentroid')
            elif 'AreaShape_Center_X' in self.data.columns:
                self.comboBox_x_col.setCurrentText('AreaShape_Center_X')
            elif 'LeftPixSize' in self.data.columns:
                self.comboBox_x_col.setCurrentText('LeftPixSize')
            if 'YCentroid' in self.data.columns:
                self.comboBox_y_col.setCurrentText('YCentroid')
            elif 'AreaShape_Center_Y' in self.data.columns:
                self.comboBox_y_col.setCurrentText('AreaShape_Center_Y')
            elif 'TopPixSize' in self.data.columns:
                self.comboBox_y_col.setCurrentText('TopPixSize')
            if 'FieldNumber' in self.data.columns:
                self.comboBox_field_col.setCurrentText('FieldNumber')
            elif 'Metadata_Field' in self.data.columns:
                self.comboBox_field_col.setCurrentText('Metadata_Field')
            elif 'Field' in self.data.columns:
                self.comboBox_field_col.setCurrentText('Field')
            self.groupBox_cols.setEnabled(True)
            # Disable the field column selection since the default is stitched
            self.comboBox_field_col.setEnabled(False)
            self.label_42.setEnabled(False)
            self.spinBox_field_size.setEnabled(False)
            self.label_field_size.setEnabled(False)
            self.tp('Done')
        return None

    def compute_field_size(self):
        if self.data.Top.max() <= 256 and self.data.Left.max() <= 256:
            self.spinBox_field_size.setValue(256)
        elif self.data.Top.max() <= 512 and self.data.Left.max() <= 512:
            self.spinBox_field_size.setValue(512)
        elif self.data.Top.max() <= 1024 and self.data.Left.max() <= 1024:
            self.spinBox_field_size.setValue(1024)
        elif self.data.Top.max() <= 2048 and self.data.Left.max() <= 2048:
            self.spinBox_field_size.setValue(2048)

    def assign_columns(self):
        self.data = self.data.rename(columns={
            self.comboBox_well_col.currentText(): 'Well',
            self.comboBox_x_col.currentText(): 'Left',
            self.comboBox_y_col.currentText(): 'Top'})
        self.data['Well'] = self.data['Well'].apply(
            self.standardize_well_names)
        self.groupBox_tile_pattern.setEnabled(True)
        self.update_column_combo_boxes(exclude_cols=[
            self.comboBox_x_col, self.comboBox_y_col, self.comboBox_well_col])
        self.compute_field_size()
        self.tp('Done')


class ClusteringWindow(QMainWindow, visual_clustering_gui.Ui_MainWindow):
    """Customization for Qt Designer created window"""
    def __init__(self, MainWindow):
        # initialization of the superclass
        super().__init__()
        # setup the GUI --> function generated by pyuic4
        self.setupUi(self)
        self.lineEdit_ch1_min.hide()
        self.lineEdit_ch1_max.hide()
        self.lineEdit_ch2_min.hide()
        self.lineEdit_ch2_max.hide()
        self.lineEdit_ch3_min.hide()
        self.lineEdit_ch3_max.hide()
        self.groupBox.hide()
        self.label_8.hide()
        self.label_9.hide()
        self.label_18.hide()
        self.spinBox_resolution.hide()
        self.label_3.hide()


def main():
    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook
    # Set the exception hook to the wrapping function
    sys.excepthook = my_exception_hook
    # Show gui
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
    return None


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    # print(exctype, value, traceback)
    logger.exception('{} {} {}'.format(
        exctype, value, tb.format_tb(traceback)))
    # Alternative log formatting
    # for l in tb.format_tb(traceback)[0].split('\n'):
    #     logger.exception(l)
    # logger.exception('{} {}'.format(
    #     exctype, value))
    # Show the output from the standard except hook
    sys._excepthook(exctype, value, traceback)
    issue_url = (
        'https://gitlab.com/stemcellbioengineering/context-explorer/issues')
    no_data_msg_1 = (
        'AttributeError("\'MainWindow\' object has no attribute \'data\'",)')
    no_data_msg_2 = (
        'AttributeError("\'MainWindow\' object has no attribute '
        '\'file_path\'",)')
    if repr(value) == no_data_msg_1 or repr(value) == no_data_msg_2:
        # This is a known error so no need to exit the program, it will behave
        # well after loading in the data
        print('\nIt appears that you did not load a data set, please select '
              'a data set before using the functions within context-explorer.'
              '\nIf you did that already and still see this error, please '
              'open an issue at {} to receive help. Please include the full '
              'traceback error message from above or the entire content of '
              'the log file at {}.'.format(issue_url, log_filepath))
    else:
        print('\nThe program crashed. Please read the error message above and '
              'visit the online issue list at {} to see if this error has '
              'already reported. If not, open a new issue to receive help. '
              'Please include the full traceback error message from above or '
              'the entire content of the the log file at {}.'
              .format(issue_url, log_filepath))
        # Since this represent unknown errors there is no guarantee that the
        # application will be well-behaved after encountering this error.
        # Exiting program is the only reasonable thing.
        sys.exit(1)


# Logging
log_dir = os.path.join(os.getcwd(), 'log')
os.makedirs(log_dir, exist_ok=True)
time_str = datetime.now().strftime('%Y%m%d-%H%M%S')
log_filepath = '{}.log'.format(os.path.join(log_dir, time_str))
logging.captureWarnings(True)
logger = logging.getLogger('py.warnings')
hdlr = logging.FileHandler(log_filepath)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

# Run main application when the file is executed, but not when it is imported
if __name__ == '__main__':
    main()

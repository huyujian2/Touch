# Copyright 2018 Google Inc. All Rights Reserved.
# Author:  stukru@google.com

import re
from collections import OrderedDict
import os
import threading


__version__ = '2.0.9'


"""
MeasurementLimitsCollection v2.0.9:
  -Changed "inf" to "+inf" to match Clifford formatting.
  
MeasurementLimitsCollection v2.0.8:
  -Fixed validator string return when both low limit and high limit are None.  Now will return inf for this situation.
  -Validator rule check will ignore spaces now between operator and variable.
  
MeasurementLimitsCollection v2.0.7:
  -Always show CoF limits in validator string even if the CoF limits did not need to be looked up.
  -Fixed iteration bug.
  
MeasurementLimitsCollection v2.0.6:
  -Fixed bug when CoF limit columns do not exist in limits file where exception would occur when trying to convert CoF
  limit values to numeric.
  
MeasurementLimitsCollection v2.0.5:
  -Added support for continue on fail (CoF) limits.
  
MeasurementLimitsCollection v2.0.4:
  -Allow for regular expression match of measurement name to support same limits applied to different measurement
   results.
  
MeasurementLimitsCollection v2.0.3:
  -Moved RandomAccessFile to its own file random_access_file.py.
  -During validation __call__, raise detailed ValueError if limits not found.
   
MeasurementLimitsCollection v2.0.2:
  -Row selectors are now stored in OrderedDict so queries return multiple limits in same order that they are listed in
  the limits file.
  -Added API to get version from limits file.

MeasurementLimitsCollection v2.0.1:
  -Removed sku from default selectors.

MeasurementLimitsCollection v2.0.0:
  -Generic selectors using **kwargs.
  -Support for multi-up test system (multiple DUTs tested at same time) by having different selectors for each DUT.

MeasurementLimitsCollection v1.0.13:
  -Updated python documentation per Google standard.
  -Updated RandomAccessFile class to version 2.4 to merge with RandomAccessFile class used in Clifford Log Viewer.

MeasurementLimitsCollection v1.0.12:
  -Added support to add comments to the file by skipping rows that start with #.

MeasurementLimitsCollection v1.0.11:
  -ValidatorWithLimitFile.__str__:  Check if self._limits is not None before accessing self._limits.Low_Limit and
  self._limits.High_Limit.

MeasurementLimitsCollection v1.0.10:
  -Fixed bug where limit value of 0 would be converted to None in MeasurementLimits class.
  -Added validator class to work with Clifford.
  -Fixed bug during lookup of one limits set for a given measure_name where it would not find the first limit in the
  file at row index 0 due to if condition of "if row_index:" instead of proper way of "if row_index is not None:".

MeasurementLimitsCollection v1.0.9:
  -Added Test_Mode column selector.

MeasurementLimitsCollection v1.0.8:
  -Fixed issue where getting phase limits search was searching phase name using "contains" instead of "exact match".

MeasurementLimitsCollection v1.0.7:
  -Updated exception message when base limits are missing.

MeasurementLimitsCollection v1.0.6:
  -Ability to get all phase limits with product and SKU selector.
  -Only use .get API function now for all limit queries.

MeasurementLimitsCollection v1.0.5:
  -Fixed for newline characters \r\n to support in Windows and Linux.

MeasurementLimitsCollection v1.0.4:
  -Use splitlines if row delimiter is \r, \n or \r\n.

MeasurementLimitsCollection v1.0.3:
  -Fixed caching issue when caching individual cell values that makes complete row in cache.

MeasurementLimitsCollection v1.0.2:
  -Fixed exception error if last line in file is blank.

MeasurementLimitsCollection v1.0.1:
  -Added support to cache limit rows that were retrieved so subsequent lookups do not have to access the file.

MeasurementLimitsCollection v1.0.0:
  -Initial release
"""


thread_local_data = threading.local()


class ValidatorWithLimitFile(object):
  """
  Clifford measurement result validator which gets limits from a csv file.  Limits can be selected based on product,
  SKU and test_mode (production, debug, etc.).  Also, this validator checks if the measurement value (result) is
  within a valid range and also allow for a text message value which is a detailed error message on why the
  measurement or phase failed.  If the value (result) is a text message, then this validator will indicate the
  measurement failed except if the value is equal to 'NOT_TESTED' which indicates the measurement was skipped so this
  value will be set as a pass.
  """

  def __init__(self, phase_name, measure_name, is_cof_limits=False):
    """
    Initialize ValidatorWithLimitFile object.

    Args:
      phase_name:  Phase name this limit validator is associated with.
      measure_name:  Measurement name this limit validator is associated with.
      is_cof_limits:  Flag indicating if these are continue on fail (CoF) limits; set to True for CoF limits.
    """
    self.phase_name = phase_name
    self.measure_name = measure_name
    self._limits = None
    self._validation_type = None
    self._validator_rule = None
    self._search_pattern = None
    self._outcome = None
    self.is_cof_limits = is_cof_limits
    self.is_cof_limits_enabled = False

  def __call__(self, value):
    """
    This will be invoked by Clifford to test if the measurement passed or failed.

    Args:
      value:  Measurement value to evaluate if it passed or failed.

    Returns:
      True if measurement value passed; otherwise, false if it failed.
    """
    self.get_limits()
    return self.validate(value)

  def get_limits(self):
    """
    Get the limits from the limits file based on selectors.
    """
    self.is_cof_limits_enabled = ValidatorWithLimitFile.limits_collection.is_cof_limits_enabled
    # If these are CoF limits and CoF limits are disabled, no need to lookup limits since they are not used
    if self.is_cof_limits and not self.is_cof_limits_enabled:
      return None

    # Get limit selectors
    limit_selectors = None
    if hasattr(thread_local_data, 'test_data'):
      limit_selectors = thread_local_data.test_data.measurement_limit_selectors
      if limit_selectors is not None:
        # Save thread_local_data.test_data limits selectors in global limit selectors for case when test_data one is
        # not available
        ValidatorWithLimitFile._limit_selectors = limit_selectors
    if limit_selectors is None:
      # Use global limit selectors if not available in thread_local_data.test_data
      limit_selectors = ValidatorWithLimitFile._limit_selectors
    if limit_selectors is None:
      limit_selectors = {}
    limit_selectors['phase_name'] = self.phase_name
    limit_selectors['measurement_name'] = self.measure_name

    # Get limits from limits file
    self._limits = ValidatorWithLimitFile.limits_collection.get(**limit_selectors)
    if self._limits is None:
      raise ValueError("Limits not found for phase='{0}', measurement name='{1}'.".format(self.phase_name,
                                                                                          self.measure_name))
    # If CoF limits are enabled and this validator is CoF limits, then transfer CoF limits to normal limits properties
    if self.is_cof_limits and self.is_cof_limits_enabled:
      self._limits.low_limit = self._limits.cof_low_limit
      self._limits.high_limit = self._limits.cof_high_limit

    # Check what validation type is being done based on the validation rule
    self._validator_rule = self._limits.validator_rule
    if self._validator_rule:  # Remove whitespace
      self._validator_rule = self._validator_rule.replace(" ", "")
    self._validation_type = "unknown"
    if '<=x<=' in self._validator_rule:
      self._validation_type = "range"
    elif '<=x' in self._validator_rule:
      self._validation_type = "range"
      self._limits.high_limit = None
    elif 'x<=' in self._validator_rule:
      self._validation_type = "range"
      self._limits.low_limit = None
    elif 're.search' in self._validator_rule:
      self._validation_type = 'regular_expression'

  def validate(self, value):
    """
    Validate a measurement value against the limits.

    Args:
      value:  Measurement value to validate against limits.

    Returns:
      True if measurement value passed limits; otherwise, False if failed.
    """
    validation_result = False

    # If these are CoF limits and CoF limits are disabled, return good validation since these limits are not used
    if self.is_cof_limits and not self.is_cof_limits_enabled:
      return True

    # Perform the validation
    if self._validation_type == 'range':
      if type(value) is str:
        if value == 'NOT_TESTED':
          validation_result = True
        else:
          validation_result = False
      elif self._limits.low_limit is not None and value < self._limits.low_limit:
        validation_result = False
      elif self._limits.high_limit is not None and value > self._limits.high_limit:
        validation_result = False
      else:
        validation_result = True
    elif self._validation_type == 'regular_expression':
      self._search_pattern = self._limits.search_pattern
      re_search_result = re.search(self._search_pattern, value)
      if re_search_result is None:
        validation_result = False
      else:
        validation_result = True

    return validation_result

  def __str__(self):
    """
    String representation of this validator object.  This will be displayed in the Clifford UI validator column.

    Returns:
      String representation of this validator object.
    """
    if self._limits is None:
      self.get_limits()

    # If these are CoF limits and CoF limits are disabled, return blank validator string since these limits are not used
    if self.is_cof_limits and not self.is_cof_limits_enabled:
      return ''

    if self._limits is None:
      return 'No limits found'
    elif self._validation_type == 'range':
      if self._limits.low_limit is not None and self._limits.high_limit is None:
        return '{0} <= x'.format(self._limits.low_limit)
      elif self._limits.low_limit is None and self._limits.high_limit is not None:
        return 'x <= {0}'.format(self._limits.high_limit)
      elif self._limits.low_limit is None and self._limits.high_limit is None:
        return '-inf <= x <= +inf'
      else:
        return '{0} <= x <= {1}'.format(self._limits.low_limit, self._limits.high_limit)
    elif self._validation_type == 'regular_expression':
      return "'x' matches {0}".format(self._search_pattern)

  """
  Limits collection object.  Holds all limits loaded from the limits file.
  """
  limits_collection = None

  """
  List of limit selectors such as product, SKU and test mode.
  """
  _limit_selectors = None

  @classmethod
  def load_limits_collection(cls, file_path, selector_columns=None, selection_rules=None, is_cof_limits_enabled=False):
    """
    Load the limits collection from the limits file.  This must be done before doing any limit validation in each
    validator instance __call__ method.

    Args:
      file_path:  Limits file path to load.
    """
    cls.limits_collection = MeasurementLimitsCollection(selector_columns=selector_columns,
                                                        selection_rules=selection_rules,
                                                        is_cof_limits_enabled=is_cof_limits_enabled)
    cls.limits_collection.load(file_path=file_path)

  @classmethod
  def assign_limit_selectors(cls, test_data):
    """
    Assign the limit selectors to use for each limit lookup done during limit validation in the __call__ method.  This
    assignment is usually called at the start of testing after the DUT product and SKU is known from either retrieving
    from the DUT itself or from a config file.

    Args:
      selectors:  Selectors are named parameters where the parameter name must match the column name in the limits file
          and the value is the matching criteria to select the proper limits row to retrieve.  For example, a limits
          file may have selectors (column names) of phase_name, measurement_name, product, sku and test_mode.  The call
          would then be the following:
          limits_collection.get(product='B1', sku='ROW', test_mode='production', phase_name='Current_Drain', 'Off_Current')
    """
    thread_local_data.test_data = test_data


class MeasurementLimitsCollection(object):
  """
  Manages a collection of measurement limits.  Limits are loaded from a delimited file and are accessed using a random
  access file.  This gives the ability to have a very small memory footprint even with thousands of limits.  Limits can
  be retrieved based on selectors such as phase name and measurement name.  The retrieved limits are passed back as a
  MeasurementLimits object type.
  """
  def __init__(self, selector_columns=None, selection_rules=None, is_cof_limits_enabled=False):
    """
    Initialize the measurement limits collection object.
    """
    self._limits_file = None

    self.is_cof_limits_enabled = is_cof_limits_enabled

    # If a new limit selector is needed, then add it to this list and update the get method
    self._selector_columns = selector_columns
    if self._selector_columns is None:
      self._selector_columns = ['product', 'test_mode', "phase_name", "measurement_name"]

    # Set the name of the phase and measurement columns since these columns are required in the selectors
    self._PHASE_NAME = 'phase_name'
    self._MEAS_NAME = 'measurement_name'
    self._HIGH_LIMIT = 'high_limit'
    self._LOW_LIMIT = 'low_limit'
    self._COF_HIGH_LIMIT = 'cof_high_limit'
    self._COF_LOW_LIMIT = 'cof_low_limit'
    for column_name in self._selector_columns:
      if 'phase_' in column_name.lower():
        self._PHASE_NAME = column_name
      elif 'measurement_' in column_name.lower():
        self._MEAS_NAME = column_name

    self._numeric_columns = {self._LOW_LIMIT: 'float', self._HIGH_LIMIT: 'float', self._COF_LOW_LIMIT: 'float',
                             self._COF_HIGH_LIMIT: 'float'}

    self.selection_rules = selection_rules
    if self.selection_rules is None:
      self.selection_rules = [['product', 'test_mode', self._PHASE_NAME, self._MEAS_NAME],
                              ['product', self._PHASE_NAME, self._MEAS_NAME],
                              ['test_mode', self._PHASE_NAME, self._MEAS_NAME],
                              [self._PHASE_NAME, self._MEAS_NAME]]

  def __len__(self):
    """
    Total measurement limits available from the limits file that was loaded.

    Returns:
      Total measurement limits available from the limits file that was loaded.
    """
    if self._limits_file:
      return len(self._limits_file)

    return 0

  def __iter__(self):
    """
    Return the iterable object.

    Returns:
      This object.
    """
    return self

  def __next__(self):  # For python 3.x
    """
    Iteration.

    Returns:
      Next limits object for iteration.
    """
    return next()

  def next(self):
    """
    Iteratation.

    Returns:
      Next limits object for iteration.
    """
    cells = iter(self._limits_file).next()
    return MeasurementLimits(self._limits_file.column_names, cells)

  def load(self, file_path):
    """
    Load the limits file.

    Args:
      file_path:  Limits file path to load.
    """
    self._limits_file = RandomAccessFile()
    self._limits_file.load(file_path=file_path, row_delimiter='\r\n', column_delimiter=',', has_header_row=True, columns_to_create_row_selectors=self._selector_columns, numeric_columns=self._numeric_columns)
    # Update the numeric columns for high/low limits after loading the file to check the column names
    for column_name in self._limits_file.column_names:
      if 'cof_high_limit' in column_name.lower():
        self._COF_HIGH_LIMIT = column_name
      elif 'cof_low_limit' in column_name.lower():
        self._COF_LOW_LIMIT = column_name
      elif 'high_limit' in column_name.lower():
        self._HIGH_LIMIT = column_name
      elif 'low_limit' in column_name.lower():
        self._LOW_LIMIT = column_name
    self._numeric_columns = {self._LOW_LIMIT: 'float', self._HIGH_LIMIT: 'float', self._COF_LOW_LIMIT: 'float',
                             self._COF_HIGH_LIMIT: 'float'}
    self._limits_file.numeric_columns = self._numeric_columns

  def get_version(self):
    """
    Get the version of the measurement limits file.

    Return:
        Version of the measurement limits file.
    """
    if self._limits_file:
      return self._limits_file.version
    return None

  def get(self, **selectors):
    """
    Get measurement limits from the limits file based on selectors.  Selectors are named parameters where the parameter
    name must match the column name in the limits file and the value is the matching criteria to select the proper
    limits row to retrieve.  For example, a limits file may have selectors (column names) of phase_name,
    measurement_name, product, sku and test_mode.  The call would then be the following:
    limits_collection.get(product='B1', sku='ROW', test_mode='production', phase_name='Current_Drain', 'Off_Current')

    Args:
      selectors:  See description above.

    Returns:
      Limits object found. Or list of limits if multiple limits were found based on the selection critiera.  None if
      limits not found based on input selectors.
    """
    limits = None
    phase_name = selectors.get(self._PHASE_NAME)
    measurement_name = selectors.get(self._MEAS_NAME)

    if phase_name and measurement_name:
      limits = self._get_limits(selectors)
      # If limits not found, then check for limits allowing for measurement name to match a regular expression to allow
      # for common limits that are applied across different measurement results such as using different channels
      if limits is None:
        rows = self._limits_file.get_rows_from_cell_selectors(phase_name=phase_name)
        for row in rows:
          next_measurement_name = row[self._limits_file.get_column_index(self._MEAS_NAME)]
          if re.search(next_measurement_name, measurement_name):
            selectors[self._MEAS_NAME] = next_measurement_name
            limits = self._get_limits(selectors)
            break
    elif phase_name:
      limits = []
      # Get all measurement names for a given test phase
      rows = self._limits_file.get_rows_from_cell_selectors(phase_name=phase_name)
      measurement_names = {}
      for row in rows:
        measurement_name = row[self._limits_file.get_column_index(self._MEAS_NAME)]
        if measurement_name not in measurement_names:
          measurement_names[measurement_name] = measurement_name
          selectors[self._MEAS_NAME] = measurement_name
          limits.append(self._get_limits(selectors))
    else:
      raise ValueError("MeasurementLimitsCollection.get error:  Selectors must contain phase_name parameter.")

    return limits

  def _get_limits(self, selectors):
    """
    Get limits based on defined selectors that define column values the limits must match in order to be selected.
    :param selectors:  Dictionary of selectors where the key is column name and the value is the limit row value in that
        column that must match in order to be selected.  Set to None or leave the column name out of the selectors list
        to ignore this column for selecting.
    :return:  Limits object that was selected.
    """
    limits = None
    cells = None
    for selection_rule in self.selection_rules:
      selectors_based_on_rule = {}
      for column_name in selection_rule:
        cell_value = selectors.get(column_name)
        if cell_value is not None:
          selectors_based_on_rule[column_name] = cell_value
      cells = self._limits_file.get_row_from_cell_selectors(**selectors_based_on_rule)
      if cells is not None:
        break
    # Convert the list of cell values to a MeasurementLimits object for easier access of each limit attribute
    if cells:
      limits = MeasurementLimits(self._limits_file.column_names, cells)
    return limits

  def destroy(self):
    """
    Destroy this measurements limits collection by freeing any resources and deleting cache files.
    """
    if self._limits_file:
      self._limits_file.destroy()


class MeasurementLimits(object):
  """
  Contains information about limits for one measurement.
  """

  def __init__(self, limit_attributes, limit_values):
    """
    Initialize the MeasurementLimits object.

    Args:
      limit_attributes:  List of limit attributes to create.  This is usually the column names from the limits file.
      limit_values:  List of limit attribute values associated with each attribute in the limit_attributes list.
    """
    if len(limit_attributes) != len(limit_values):
      raise ValueError("MeasurementLimits initialize error: Total limit attributes = {0} and total limit values = {1}.  These totals must match.".format(len(limit_attributes), len(limit_values)))

    self._limit_attributes = limit_attributes
    self._limit_values = limit_values

    # Attributes are dynamically created based on column names in limit file
    for limit_attribute, limit_value in zip(limit_attributes, limit_values):
      if not isinstance(limit_value, float) and not limit_value:
        limit_value = None
      setattr(self, limit_attribute, limit_value)

  def __str__(self):
    """
    String representation of this object.

    Returns:
      String representation of this object.
    """
    obj_str = None

    for attribute_index in range(0, len(self._limit_attributes)):
      if obj_str is None:
        obj_str = "{0}={1}".format(self._limit_attributes[attribute_index], self._limit_values[attribute_index])
      else:
        obj_str = "{0}, {1}={2}".format(obj_str, self._limit_attributes[attribute_index], self._limit_values[attribute_index])

    return obj_str


class RandomAccessFile(object):
  """
  Create random access file from existing file or memory data.
  Version 2.5:  Separated into own file random_access_file.py.  Added rows_as_dictionary property to allow support to
                return rows as a dictionary instead of a list where key is column name and value is cell value.
  Version 2.4:  Updated to work with both measurement limits and Clifford Log Viewer.
  Version 2.3:  Updated python documentation per Google standard.
  Version 2.2:  Added support to add comments to the file by skipping rows that start with #.
  Version 2.1:  Added cache support for get row lookups.
  Version 2.0:  Changes to support row selectors.
  """
  def __init__(self, file_path=None, row_delimiter='\n', column_delimiter='\t'):
    """
    Initialize RandomAccessFile object.

    Args:
      file_path:  File path of random access file.  Set to None to define file path later when loading.
      row_delimiter:  Delimiter for a row.
      column_delimiter:  Delimiter for a column.
    """
    self.file_path = file_path
    self.row_delimiter = row_delimiter
    self.column_delimiter = column_delimiter
    self._file = None
    self._VERSION_MARKER = "version"
    self.version = None

    self._column_name_to_index_map = {}
    self._column_index_to_name_map = []
    self.numeric_columns = {}
    self._row_selector_columns = None

    self.max_cache_rows_allowed = 100  # Set to None for unlimited cache capacity
    self._cache = {}

    self._filters = None
    self._is_filter_on = False
    self._iteration_row_index = 0

    self._index_table = []  # Active index table in use which can be either _file_index_table or _filter_index_table
    self._file_index_table = []  # Complete file index table (no filtering)
    self._filter_index_table = []  # Filtered index table which will be a reduced table of _file_index_table
    self._filter_to_file_row_map = None
    self.row_selector_dictionary = None

    self.total_found_cells = 0
    self.found_cells = None
    self.first_found_cell = None

    self._rows_as_dictionary = False

  def __len__(self):
    """
    Total count of viewable rows (rows that satisfy the set filter expression).

    Returns:
      Total count of viewable rows (rows that satisfy the set filter expression).
    """
    if self._index_table is None:
      return 0

    return len(self._index_table)

  def __iter__(self):
    return self

  def __next__(self):  # For python 3.x
    return next()

  def next(self):
    if self._iteration_row_index < len(self):
      cells = self.get_row(self._iteration_row_index)
      self._iteration_row_index += 1
    else:
      self._iteration_row_index = 0  # Reset so it can iterated again
      raise StopIteration()

    return cells

  def __getitem__(self, item):
    return self.get_row(item)

  @property
  def rows_as_dictionary(self):
    return self._rows_as_dictionary

  @rows_as_dictionary.setter
  def rows_as_dictionary(self, value):
    self._rows_as_dictionary = value

  @property
  def column_names(self):
    """
    Get column names.

    Returns:
      List of column names.
    """
    return self._column_index_to_name_map

  def load(self, file_path, row_delimiter='\n', column_delimiter='\t', has_header_row=True,
           columns_to_create_row_selectors=None, numeric_columns=None):
    """
    Load a file and index it for random access based on a row and column delimiter.

    Args:
      file_path:  File path to index as random access.
      row_delimiter:  Delimiter for a row.
      column_delimiter:  Delimiter for a column.
      has_header_row:  Set to True if file has a header row; otherwise, set to False.
      columns_to_create_row_selectors:  List of column names to create selector lookup dictionary for looking up a row
          based on values in these columns.  Set to None if not using.
      numeric_columns:  Dictionary of column names that are numeric.  Each dictionary key is the column name and the
          dictionary value is the type of numeric for this column which can be 'int', 'float' or 'numeric string'.
          Values of 'int' or 'float' are converted to these defined types while 'numeric string' will be left as a
          string but for find operations, it will be treated as numeric.  Example is {'Line#': 'int', 'Price': 'float'}.
          Set to None if no numeric columns.
    """
    ra_data = []
    header = None
    data_file = open(file_path, "r")
    data = data_file.read()
    if row_delimiter == '\r' or row_delimiter == '\n' or row_delimiter == '\r\n':
      rows = data.splitlines()
    else:
      rows = data.split(row_delimiter)
    data = None

    for row in rows:
      if row:
        if row.startswith('#'):  # Skip rows that start with # since these are comment rows
          if len(row) > 1:
            comment_row = row[1:].strip()  # Remove comment marker # and leading/trailing white space
            if comment_row.lower().startswith(self._VERSION_MARKER):
              version_cells = comment_row.split(column_delimiter)
              if len(version_cells[0]) > len(self._VERSION_MARKER):
                # Version is in 1st cell (example "# Version 1.2.3,,,,,,,")
                self.version = version_cells[0][len(self._VERSION_MARKER):].strip()
              if len(version_cells[1]) > 0:
                # Version is in second cell (example "# Version,1.2.3,,,,,,")
                if self.version is None:
                  self.version = version_cells[1]
                else:
                  self.version = "{0}{1}".format(self.version, version_cells[1])
        else:
          cells = row.split(column_delimiter)
          if has_header_row and header is None:
            header = cells
            self._create_column_mapping(header)
          else:
            ra_data.append(cells)

    rows = None

    ra_file_path = file_path + ".rac"
    self.create(file_path=ra_file_path, data=ra_data, row_delimiter=row_delimiter, column_delimiter=column_delimiter,
                column_names=header, numeric_columns=numeric_columns, columns_to_create_row_selectors=columns_to_create_row_selectors)

  def save(self, file_path, delimiter):
    """
    Save the current filtered data to defined file path.

    Args:
      file_path:  File path to save the filtered data to.
      delimiter:  Delimiter for the file.
    """
    with open(file_path, "w") as data_file:
      for row_index in range(0, len(self._index_table)):
        row_cells = self.get_row(row_index)
        file_row = row_cells[0]
        for col in range(1, len(row_cells)):
          file_row = "{0}{1}{2}".format(file_row, delimiter, row_cells[col])

        data_file.write("{0}{1}".format(file_row, self.row_delimiter))

  def _create_column_mapping(self, column_names):
    """
    Create column mapping of column names to column indexes.

    Args:
      column_names:  List of column names.
    """
    self._column_index_to_name_map = column_names
    if column_names is None:
      self._column_name_to_index_map = None
    else:
      self._column_name_to_index_map = {}
      for column_index in range(0, len(column_names)):
        self._column_name_to_index_map[column_names[column_index]] = column_index

  def get_column_index(self, column_name):
    """
    Get the column index for a given column name.
    :param column_name:  Column name to get its index for.
    :return:  Column index.
    """
    return self._column_name_to_index_map.get(column_name)

  def create(self, file_path, data, row_delimiter='\n', column_delimiter='\t', column_names=None,
             numeric_columns=None, columns_to_create_row_selectors=None):
    """
    Create a random access file from existing data.

    Args:
      file_path:  File path of the random access file to create.
      data:  File data to create random access file for.  The data should be in row/column format as a list of lists
          where outer list is the row list and the inner lists are columns.
      row_delimiter:  Delimiter for a row.
      column_delimiter:  Delimiter for a column.
      column_names:  List of column names used to access data by the column names instead of column indexes.
      numeric_columns:  Dictionary of column names that are numeric.  Each dictionary key is the column name and the
          dictionary value is the type of numeric for this column which can be 'int', 'float' or 'numeric string'.
          Values of 'int' or 'float' are converted to these defined types while 'numeric string' will be left as a
          string but for find operations, it will be treated as numeric.  Example is {'Line#': 'int', 'Price': 'float'}.
          Set to None if no numeric columns.
      columns_to_create_row_selectors:  List of column names to create selector lookup dictionary for looking up a row
          based on values in these columns.  Set to None if not using.
    """
    self.file_path = file_path
    self.row_delimiter = row_delimiter
    self.column_delimiter = column_delimiter
    self._file = open(file_path, "w")
    self._file_index_table = []
    self.row_selector_dictionary = OrderedDict()

    self._create_column_mapping(column_names)
    self.numeric_columns = numeric_columns
    is_windows = False
    if os.name == "nt":
      is_windows = True

    for row in data:
      cell_indexes = []
      for cell in row:
        index = self._file.tell()
        cell_indexes.append(index)
        data_to_write = "{0}{1}".format(cell, self.column_delimiter)
        self._file.write(data_to_write)
      # TODO:  Check if better way to handle carriage return and line feed between Windows and Linux
      if is_windows and self.row_delimiter == "\r\n":
        self._file.write("\n")
      else:
        self._file.write(self.row_delimiter)

      # Create additional selector lookup table based on cell values defined in list of specified columns
      if columns_to_create_row_selectors and self._column_index_to_name_map:
        selector_values = {}
        for column_name in columns_to_create_row_selectors:
          column_index = self._column_name_to_index_map.get(column_name)
          if column_index is None:
            raise ValueError("Create random access file error during creation of row selectors:  Column name '{0}' does not exist in data.".format(column_name))
          elif column_index > (len(row) - 1):
            # This row does not have one of the selector columns so must skip it for row selector lookup
            break
          selector_value = row[column_index]
          selector_values[column_name] = selector_value
        if len(selector_values) > 0:
          row_key = RowSelector(columns_to_create_row_selectors, selector_values)
          if row_key not in self.row_selector_dictionary:
            self.row_selector_dictionary[row_key] = len(self._file_index_table)
          else:
            raise ValueError("Create random access file error during creation of row selectors:  Row selector key '{0}' has duplicate entries in the data.".format(row_key))

      # Set the last index in a row as the index of the end of the row
      cell_indexes.append(self._file.tell() - 2)
      self._file_index_table.append(cell_indexes)

    self._row_selector_columns = columns_to_create_row_selectors
    self._index_table = self._file_index_table
    self.close()

  def close(self):
    """
    Close the random access file.  This does NOT delete the file.
    """
    if self._file is not None:
      self._file.close()
      self._file = None

  def destroy(self):
    """
    Destroy this instance of a random access file by deleting the file.  You can no longer use this instance after
    executing this function.
    """
    self.close()
    try:
      os.remove(self.file_path)
    except Exception:
      pass  # Ignore any errors

  def open(self):
    """
    Open the random access file.
    """
    if self._file is None:
      self._file = open(self.file_path, "r")

  def _save_cells_to_cache(self, row_index, column_index, cells):
    """
    Save a cell values to the cache so subsequent lookups can use this cache value instead of getting from the file.
    Either one cell can be saved or a complete row of cells.

    Args:
      row_index:  Row index of the cell or cells to save to cache.  The complete row of cells will be saved if
          column_index is set to -1.
      column_index:  Column index from the cell.  If saving a complete row to cache, then set this to -1.
      cells:  Can be either one cell value or list of cell values for complete row to save.
    """
    if self.max_cache_rows_allowed is None or len(self._cache) < self.max_cache_rows_allowed:
      # If filter is on, then need to convert filter table row index to complete file table row index
      if self._is_filter_on:
        row_index = self._filter_to_file_row_map[row_index]

      if column_index == -1:  # Saving complete row of cell values
        self._cache[row_index] = cells
      else:  # Saving one cell value
        if row_index not in self._cache:
          self._cache[row_index] = {}
        self._cache[row_index][column_index] = cells
        # If adding last cell to cache to make complete row, convert dictionary to list
        if len(self._cache[row_index]) + 1 == len(self._index_table[row_index]):
          cache_list = []
          for col_index in range(0, len(self._cache[row_index])):
            cache_list.append(None)
          for col_index, val in self._cache[row_index].iteritems():
            cache_list[col_index] = val
          self._cache[row_index] = cache_list

  def _get_cells_from_cache(self, row_index, column_index):
    """
    Get cell values from cache.

    Args:
      row_index:  Row index to get cache cell values for.
      column_index:  Column index to get cache cell value for.  If -1, then list of all cell values for the row are
          retrieved.

    Returns:
      One cell value from cache if retrieving one cell value or complete row cell values if retrieving complete
      row when column_index is set to -1.  Returns None if cell is not available in cache.
    """
    cells = None
    file_row_index = row_index

    # If filter is on, then need to convert filter table row index to complete file table row index
    if self._is_filter_on:
      file_row_index = self._filter_to_file_row_map[row_index]

    if file_row_index in self._cache:  # Row is in the cache table
      cells = self._cache[file_row_index]

      # Check if complete row is in cache (note, +1 for cells length since index table has extra entry for end of row)
      is_complete_row_in_cache = False
      if (len(cells) + 1) == len(self._index_table[row_index]):
        is_complete_row_in_cache = True

      if column_index == -1:  # Getting cell values of complete row
        if not is_complete_row_in_cache:
          cells = None
      else:  # Getting one cell value
        if is_complete_row_in_cache and column_index < len(cells):
          return cells[column_index]
        elif column_index in cells:
          return cells[column_index]
        else:
          cells = None

    return cells

  def get_cell(self, row_index, column_index):
    """
    Get a cell value from the random access file.  Note, this will leave the file open.  Call the close function to
    close the file.

    Args:
      row_index:  Row index of the cell to get its value from.
      column_index:  Column index of the cell to get its value from.


    Returns:
      Value for cell at location (row, col).
    """
    # Allow for negative indexing from end of row or column
    if row_index < 0:
      row_index = len(self._index_table) + row_index
    if column_index < 0:
      column_index = len(
        self._index_table[row_index]) - 1 + column_index  # -1 is because extra column for end of row marker

    # If cell is in the cache, then return it instead of reading from the file
    cell_value = self._get_cells_from_cache(row_index, column_index)

    # Read cell value from file if not in cache
    if cell_value is None:
      self.open()

      if column_index < len(self._index_table[row_index]) - 1:
        next_index = self._index_table[row_index][column_index + 1] - 1  # Remove column delimiter
      else:
        # Column index is out of range for this row, so return cell value of None
        return None
        #raise ValueError("Column index {0} is out of range.  Maximum column index allowed is {1}.".format(column_index, len(self._index_table[row_index]) - 1))

      # Move file pointer to the start of the cell to get
      self._file.seek(self._index_table[row_index][column_index])
      if next_index == -1:  # Read to the end of the file
        cell_value = self._file.read()
      else:
        cell_value = self._file.read(next_index - self._index_table[row_index][column_index])

      # Store the read cell value in the cache if the cache is not at its limit yet
      self._save_cells_to_cache(row_index, column_index, cell_value)

    return cell_value

  def get_rows_from_cell_selectors(self, **cell_selectors):
    """
    Get a row based on matching cell values in the row.  This is available only if the random access file was created
    with columns_to_create_row_selectors in create method.

    Args:
      cell_selectors:  List of cell values that row must match in order to be chosen to return values for.  The cell
          values correspond to the columns that were defined in columns_to_create_row_selectors when creating the random
          access file.

    Returns:
      List of the cell values for the selected row based on the cell selectors.  None if could not find the row.
    """
    if self._is_filter_on:
      raise ValueError("get_rows_from_cell_selectors does not support lookup when filters are on.")

    row_key = RowSelector(self._row_selector_columns, cell_selectors)
    found_row_indexes = [value for key, value in self.row_selector_dictionary.iteritems() if key == row_key]

    rows = []
    for row_index in found_row_indexes:
      rows.append(self.get_row(row_index))

    return rows

  def get_row_from_cell_selectors(self, **cell_selectors):
    """
    Get a row based on matching cell values in the row.  This is available only if the random access file was created
    with columns_to_create_row_selectors in create method.

    Args:
      cell_selectors:  List of cell values that row must match in order to be chosen to return values for.  The cell
          values correspond to the columns that were defined in columns_to_create_row_selectors when creating the random
          access file.

    Returns:
      List of the cell values for the selected row based on the cell selectors.  None if could not find the row.
    """
    if self._is_filter_on:
      raise ValueError("get_row_from_cell_selectors does not support lookup when filters are on.")

    cells = None
    row_key = RowSelector(self._row_selector_columns, cell_selectors)
    row_index = self.row_selector_dictionary.get(row_key)
    if row_index is not None:
      cells = self.get_row(row_index)

    return cells

  def get_row(self, row_index):
    """
    Get the data in format of list of cell values for a specified row of the random access file.  Note, this will
    leave the file open.  Call the close function to close the file.

    Args:
      row_index:  Row index to get the row data for.

    Returns:
      List of the cell values for the specified row index.
    """
    self.open()

    if row_index < len(self._index_table):
      # Get row of cells from cache if exists
      cells = self._get_cells_from_cache(row_index, -1)

      # Read row of cells from file if not in cache
      if cells is None:
        # Move file pointer to the start of the row to get
        self._file.seek(self._index_table[row_index][0])
        # Read the entire row from the file
        row = self._file.read(self._index_table[row_index][-1] - self._index_table[row_index][0] - 1)
        # Split the row into cells to return as a list of cells
        cells = row.split(self.column_delimiter)

        # Convert cell values in defined numeric columns to float
        if self.numeric_columns is not None:
          for column_name, numeric_type in self.numeric_columns.iteritems():
            column_index = self._column_name_to_index_map.get(column_name)
            if column_index is not None and column_index < len(cells):
              try:
                if numeric_type == 'float':
                  cells[column_index] = float(cells[column_index])
                elif numeric_type == 'int':
                  cells[column_index] = int(cells[column_index])
              except ValueError:
                pass

        # Save the cell values for this row to cache so subsequent calls can return cache values instead of accessing file
        self._save_cells_to_cache(row_index=row_index, column_index=-1, cells=cells)

      if self.rows_as_dictionary:
        cells_as_dict = {}
        for column_index in range(0, len(self._column_index_to_name_map)):
          cells_as_dict[self._column_index_to_name_map[column_index]] = cells[column_index]
        return cells_as_dict
    else:
      raise ValueError(
        "Row index {0} is out of range.  Total viewing rows is {1}.".format(row_index, len(self._index_table)))

    return cells

  def get_total_rows(self):
    """
    Get the total data rows contained in this random access file.  Filtering does not affect this value - this value
    will always return the total rows of data contained in this random access file.  Use get_total_viewable_rows to
    get the total rows that are currently viewable based on the set filters - rows that meet the filter criteria.

    Returns:
      Total rows of data contained in this random access file.
    """
    if self._file_index_table is None:
      return 0
    else:
      return len(self._file_index_table)

  def get_total_viewable_rows(self):
    """
    Get the total data rows that are viewable based on the set filter which are rows that meet the filter criteria.

    Returns:
      Total viewable data rows.
    """
    if self._index_table is None:
      return 0
    else:
      return len(self._index_table)

  def set_filter(self, filter_expressions, exact_match):
    """
    Set filter so only specific rows will be accessed.

    Args:
      filter_expressions:  List of regular expression patterns to match for filtering where each list entry is a tuple
          of the following format (column_name, regular expression patter to match).
      exact_match:  Set to True for exact match; otherwise, False will do a "contains" search.
    """
    self._index_table = self._file_index_table
    self._filter_index_table = []
    self._filter_to_file_row_map = []
    self._filters = filter_expressions
    for row_index in range(0, len(self._index_table)):
      does_row_match_filter = True
      for filter_expression in filter_expressions:
        column_index = self._column_name_to_index_map[filter_expression[0]]
        cell_value = self.get_cell(row_index, column_index)

        if exact_match:
          search_pattern = "\\b{0}\\b".format(filter_expression[1])
        else:
          search_pattern = filter_expression[1]

        if cell_value is None or not re.search(search_pattern, cell_value):
          does_row_match_filter = False
          break
      if does_row_match_filter:
        self._filter_index_table.append(self._index_table[row_index])
        self._filter_to_file_row_map.append(row_index)

    self._index_table = self._filter_index_table
    self.found_cells = None
    self.first_found_cell = None
    self.total_found_cells = 0
    self._iteration_row_index = 0  # Reset so it can iterated again
    self._is_filter_on = True

  def clear_filter(self):
    """
    Clear the filter setting.
    """
    self._index_table = self._file_index_table
    self._filters = None
    self._filter_to_file_row_map = None
    self.found_cells = None
    self.first_found_cell = None
    self.total_found_cells = 0
    self._iteration_row_index = 0  # Reset so it can iterated again
    self._is_filter_on = False

  def clear_find(self):
    """
    Clear the data of the last find that was run.
    """
    self.found_cells = None
    self.first_found_cell = None
    self.total_found_cells = 0

  def find_all(self, text_to_find, match_case, exact_match):
    """
    Find all cells in the random access file that match a specific search criteria.

    Args:
      text_to_find:  Text to find.
      match_case:   Set to True to match case.
      exact_match:  Set to True to find exact match.

    Returns:
      Dictionary of found cells where key is the row index of found cells and the value is dictionary of columns of the
      found cells in that row index.
    """
    self.clear_find()

    if not match_case:
      text_to_find = text_to_find.lower()

    for row_index in range(0, len(self)):
      found_cells_in_row = None
      row = self.get_row(row_index)
      column_index = 0
      for cell in row:
        is_found_cell = False
        exact_match_search = exact_match
        is_string = True

        # Check if this column has numeric values in it
        column_name = self._column_index_to_name_map[column_index]
        if column_name in self.numeric_columns:
          is_string = False

        # Check if this cell matches find criteria
        if not is_string:
          exact_match_search = True
        elif not match_case:
          cell = cell.lower()
        if exact_match_search and cell == text_to_find:
          is_found_cell = True
        elif not exact_match_search and text_to_find in cell:
          is_found_cell = True

        # If this cell is a found cell, add it to the dictionary of found cells in this row
        if is_found_cell:
          self.total_found_cells += 1
          if found_cells_in_row is None:
            found_cells_in_row = OrderedDict()
          found_cells_in_row[column_index] = self.total_found_cells
          if self.first_found_cell is None:
            self.first_found_cell = (row_index, column_index)

        column_index = column_index + 1

      # If there were any found cells in this row, add the dictionary to the overall found cells dictionary
      if found_cells_in_row is not None:
        if self.found_cells is None:
          self.found_cells = OrderedDict()
        self.found_cells[row_index] = found_cells_in_row

    return self.found_cells


class RowSelector(object):
  """
  Row selector which is used to determine if a row matches a specific selector criteria where the selector is specific
  matching values for defined columns.
  """

  def __init__(self, column_names, selectors):
    """
    Row selector constructor.
    :param column_names:  List of column names used for row selection.
    :param selectors:  Dictionary of selector values where key is column name and value is the cell value in that
        column.
    """
    self.column_names = column_names
    self.selectors = selectors

  def __hash__(self):
    """
    Calculate hash for this selector object; used for dictionary key.
    :return:  Hash integer value.
    """
    hash_key = self.__str__()
    return hash(hash_key)

  def __str__(self):
    """
    Create string representation of this selector object.
    :return:  String representation of this selector object.
    """
    hash_key = None
    for column_name in self.column_names:
      cell_value = self.selectors.get(column_name)
      if cell_value is None or len(cell_value) == 0:
        cell_value = 'None'
      if hash_key is None:
        hash_key = cell_value
      else:
        hash_key = "{0}::{1}".format(hash_key, cell_value)
    return hash_key

  def __eq__(self, comparing_selector):
    """
    Check if this selector object is equal to another selector object.
    :param comparing_selector:  Selector object to compare with this selector object.
    :return:  True is the selector objects are equal; otherwise, False if not equal.
    """
    return RowSelector.is_equal(self.selectors, comparing_selector.selectors, self.column_names, True)

  @staticmethod
  def is_equal(selector1, selector2, selection_rule, allow_wildcards=True):
    """
    Check if two row selectors are equal to each other.
    :param selector1:  Selector 1 to compare with selector 2.
    :param selector2:  Selector 2 to compare with selector 1.
    :param selection_rule:  Selection rules to follow for comparison.  This is list of column names which are the keys
    in the selectors to retrieve values for and perform comparison.  If a selector has a column entry that is not in
    this selection_rule list, then it is ignored in the equals comparison.
    :param allow_wildcards:  Set to true to allow wildcards in each selector column.  A wildcard is when the column is
    not in the selector list or its value is set to None.
    :return:  True if selector 1 and 2 are equal to each other; otherwise, false.
    """
    is_equal = True
    for column_name in selection_rule:
      cell_value1 = selector1.get(column_name)
      cell_value2 = selector2.get(column_name)
      if allow_wildcards:
        if cell_value1 and cell_value2 and cell_value1 != cell_value2:
          is_equal = False
          break
      else:
        if cell_value1 and cell_value2 and cell_value1 == cell_value2:
          is_equal = True
        elif not cell_value1 and not cell_value2:
          is_equal = True
        else:
          is_equal = False
          break
    return is_equal


if __name__ == "__main__":
  # Example usage of MeasurementLimitsCollection
  print("Limits file C:\\temp\\Measurement_Limits_File_Example.csv")
  limits_collection = MeasurementLimitsCollection(selector_columns=['product', 'sku', 'test_mode', "phase_name", "measurement_name"],
                                                  selection_rules=[['product', 'sku', 'test_mode', 'phase_name', 'measurement_name'],
                                                                   ['product', 'sku', 'phase_name', 'measurement_name'],
                                                                   ['product', 'test_mode', 'phase_name', 'measurement_name'],
                                                                   ['product', 'phase_name', 'measurement_name'],
                                                                   ['test_mode', 'phase_name', 'measurement_name'],
                                                                   ['phase_name', 'measurement_name']])
  limits_collection.load("C:\\temp\\Measurement_Limits_File_Example.csv")
  print("Limits file version = {0}".format(limits_collection.get_version()))

  selectors = [('sensitivity', 'max_SNR_20N', 'B1', None, None),
               ('sensitivity', 'max_SNR_20N', 'B1', 'X', None),
               ('sensitivity', 'max_SNR_20N', 'B1', 'Japan', None),
               ('sensitivity', 'max_SNR_20N', 'B1', 'Japan', 'debug'),
               ('sensitivity', 'max_SNR_20N', 'B1', 'Japan', 'production'),
               ('sensitivity', 'max_SNR_20N', 'C1', 'Japan', 'debug'),
               ('sensitivity', 'max_SNR_20N', 'X', 'Japan', 'debug'),
               ('current_drain', 'on_current', None, None, None),
               ('sensitivity', None, None, None, None),
               ('sensitivity', None, 'B1', None, None),
               ('sensitivity', None, 'B1', 'Japan', None),
               ('sensitivity', None, 'B1', 'Japan', 'debug'),
               ('sensitivity', None, 'C1', 'Japan', None),
               ('sensitivity', None, 'X', 'Japan', None),
               ('lte_power', None, 'B1', 'Japan', 'debug'),
               ('lte_power', None, 'C1', 'Japan', 'debug'),
               ('lte_power', None, 'C1', 'Row', 'production'),
               ('lte_power', None, 'C1', 'Row', 'local'),
               ('current_drain', 'tx_current', None, None, None),
               ('sensitivity', 'max_SNR_20N', None, None, None),
               ('sensitivity', 'max_SNR_20N', 'B1', None, None),
               ('sensitivity', 'max_SNR_20N', 'X', 'Brazil', None),
               ('sensitivity', 'max_SNR_20N', 'C1', 'Row', None),
               ('sensitivity', 'max_SNR_20N', 'C1', 'Japan', None),
               ('sensitivity', 'max_SNR_20N', 'C1', 'Japan', 'debug'),
               ('sensitivity', 'max_SNR_20N', 'B1', 'Japan', 'debug'),
               ('lte_power', 'max_power', 'B1', None, 'debug'),
               ('lte_power', 'max_power', None, None, 'debug'),]

  for selector in selectors:
    phase = selector[0]
    measurement = selector[1]
    product = selector[2]
    sku = selector[3]
    test_mode = selector[4]
    if measurement:
      print("Limits for measurement '{0}' in test phase '{1}' where product='{2}', sku='{3}', test_mode='{4}':".format(measurement, phase, product, sku, test_mode))
      limits = limits_collection.get(phase_name=phase, measurement_name=measurement, product=product, sku=sku, test_mode=test_mode)
      print(limits)
    else:
      print("All limits for test phase '{0}' where product='{1}', sku='{2}', test_mode='{3}':".format(phase, product, sku, test_mode))
      phase_limits = limits_collection.get(phase_name=phase, product=product, sku=sku, test_mode=test_mode)
      print ("Total limits = {0}".format(len(phase_limits)))
      for limits in phase_limits:
        print(limits)
    print('')

  # ValidatorWithLimit testing
  test_data = MeasurementLimits(['measurement_limit_selectors'], [[]])
  ValidatorWithLimitFile.load_limits_collection(file_path="C:\\temp\\Measurement_Limits_File_Example.csv",
                                                selector_columns=['product', 'sku', 'test_mode', "phase_name", "measurement_name"])
  ValidatorWithLimitFile.assign_limit_selectors(test_data)
  validator = ValidatorWithLimitFile(phase_name='current_drain', measure_name='on_current')
  val_result = validator(9020)
  validator = ValidatorWithLimitFile(phase_name='test_initialization', measure_name='dut_software_version')
  val_result = validator('1.4.10')

  # Iterate the complete limits file
  print ("All limits in file:")
  print ("Total limits = {0}".format(len(limits_collection)))
  for limits in limits_collection:
    print(limits)
  print('')

  # Iterate the complete limits file again to make sure iteration resetting works
  print ("All limits in file:")
  print ("Total limits = {0}".format(len(limits_collection)))
  for limits in limits_collection:
    print(limits)

  # Limit check a result to test that float numeric types are returned in the low and high limits
  print('')
  limits = limits_collection.get(phase_name='current_drain', measurement_name='on_current')
  reading = 10000
  if reading >= limits.low_limit and reading <= limits.high_limit:
    print("phase=current_drain; measurement=on_current; reading=1000; Limit check=PASSED")
  else:
    print("phase=current_drain; measurement=on_current; reading=1000; Limit check=FAILED")

  # Destroy the measurement limits collection which will close the file and delete the cache file
  limits_collection.destroy()

  pass


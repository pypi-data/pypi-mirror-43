"""
    date_simple.py - Wrapper module which provides a simplified interface to a
    few of the date functions of the standard distribution datetime module.

    Author: Rexford Cristal, rexford.cristal@gmail.com
    Last Modified: 03/06/2019
"""

import datetime

DATEFORMATS = {'YYYY-MM-DD':'%Y-%m-%d', 'MM/DD/YYYY':'%m/%d/%Y', 'DD-Mon-YY':'%d-%b-%y', 'YYYYMMDD':'%Y%m%d'}

def get_date_object(date=None):
    """ takes an optional string date and returns a date object """

    if date:
        if isinstance(date, str):
            return try_format(date)
        raise TypeError("'date' argument must be a string")
    return datetime.date.today()

def get_date_string(date_object=None, format='YYYY-MM-DD'):
    """ takes an optional date object and returns a formatted string """

    if date_object:
        if isinstance(date_object, datetime.date):
            if format in DATEFORMATS:
                return date_object.strftime(DATEFORMATS[format])
            raise ValueError("'{}' is not a valid format".format(format))
        raise TypeError("'date_object' argument must be a date object")
    return datetime.date.today().strftime('%Y-%m-%d')

def try_format(user_string_date):
    """ returns a date object if the string date format is valid """

    for format in ['%Y-%m-%d', '%m/%d/%Y', '%d-%b-%y', '%Y%m%d']:
        try:
            return datetime.datetime.strptime(user_string_date, format).date()
        except ValueError:
            pass
    raise ValueError("'{}' is not a valid date string".format(user_string_date))

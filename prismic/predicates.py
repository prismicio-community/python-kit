# -*- coding: utf-8 -*-

"""
prismic.predicates
~~~~~~~~~~~

This module provides helpers to write predicates to query Prismic

"""
import datetime


def at(fragment, value):
    return ['at', fragment, value]

def not_(fragment, value):
    return ['not', fragment, value]

def any(fragment, values):
    return ['any', fragment, values]

def in_(fragment, values):
    return ['in', fragment, values]

def fulltext(fragment, values):
    return ['fulltext', fragment, values]


def similar(fragment, value):
    return ['similar', fragment, value]


def gt(fragment, value):
    return ['number.gt', fragment, value]


def lt(fragment, value):
    return ['number.lt', fragment, value]


def in_range(fragment, before, after):
    return ['number.inRange', fragment, before, after]


def date_before(fragment, before):
    return ['date.before', fragment, __to_timestamp(before)]


def date_after(fragment, after):
    return ['date.after', fragment, __to_timestamp(after)]


def date_between(fragment, before, after):
    return ['date.between', fragment, __to_timestamp(before), __to_timestamp(after)]


def day_of_month(fragment, day):
    return ['date.day-of-month', fragment, day]


def day_of_month_after(fragment, day):
    return ['date.day-of-month-after', fragment, day]


def day_of_month_before(fragment, day):
    return ['date.day-of-month-before', fragment, day]


def day_of_week(fragment, day):
    return ['date.day-of-week', fragment, day]


def day_of_week_after(fragment, day):
    return ['date.day-of-week-after', fragment, day]


def day_of_week_before(fragment, day):
    return ['date.day-of-week-before', fragment, day]


def month(fragment, month):
    return ['date.month', fragment, month]


def month_before(fragment, month):
    return ['date.month-before', fragment, month]


def month_after(fragment, month):
    return ['date.month-after', fragment, month]


def year(fragment, year):
    return ['date.year', fragment, year]


def hour(fragment, hour):
    return ['date.hour', fragment, hour]


def hour_before(fragment, hour):
    return ['date.hour-before', fragment, hour]


def hour_after(fragment, hour):
    return ['date.hour-after', fragment, hour]


def near(fragment, latitude, longitude, radius):
    return ['geopoint.near', fragment, latitude, longitude, radius]


def __to_timestamp(input):
    if isinstance(input, datetime.date) or isinstance(input, datetime.datetime):
        return (input - datetime.datetime(1970, 1, 1)).total_seconds() * 1000
    return input

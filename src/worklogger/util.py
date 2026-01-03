"""util - Module for utility functions shared between worklogger submodules"""

import datetime


def timedelta_hours(delta: datetime.timedelta) -> int:
    """Get how many hours are in the timedelta"""
    return delta.days * 24 + delta.seconds // 3600


def timedelta_mins(delta: datetime.timedelta) -> int:
    """Get how many minutes in final hour of timedelta"""
    return (delta.seconds % 3600) // 60

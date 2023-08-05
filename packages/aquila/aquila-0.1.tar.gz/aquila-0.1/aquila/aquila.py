#!/usr/bin/env python3

"""
ASCII Splash screen for SHYCD Software.
"""

from colored import attr, fg
from pendulum import now

__version__ = "0.0.1"

h = "--"
hs = " "

shycd_logo_len = 17

# Bold normal white.
bw = attr("bold") + fg(231)
# Bold normal green.
blg = attr("bold") + fg(10)
# Bold normal yellow.
by = attr("bold") + fg(11)
# Bold normal sky blue.
bsb = attr("bold") + fg(14)
# Style reset.
sr = attr("reset")


def __date_string():
    return now(tz="local").to_rfc1036_string()


def signum(
    title,
    shycd_space_width=13,
    title_space=None,
    date_space=None,
    show_parameters=False
        ):
    """

    :param title: Title.
    :param shycd_space_width:  (Default value = 13)
        Automatically assigned if default.
    :param title_space:  (Default value = None)
        Automatically assigned if default.
    :param date_space:  (Default value = None)
        Automatically assigned if default.
    :param show_parameters:  (Default value = False) Testing purposes.

    """
    ss = " " * shycd_space_width

    h_space = len(h) + len(hs)
    floor_medium_width = (2 * shycd_space_width + shycd_logo_len) // 2

    if not title_space:
        title_space = " " * (
            floor_medium_width - len(title) // 2 - h_space
            )
    else:
        title_space = " " * title_space

    date = __date_string()

    if not date_space:
        date_space = " " * (floor_medium_width - len(date) // 2)
    else:
        date_space = " " * date_space

    logo = f"{ss}   {blg}-x-{by}SHYCD{blg}-x-\n"\
           f"{ss} -x{by}-{bsb}    o    {by}-{blg}x-\n"\
           f"{ss}-x{by}-{bsb}           {by}-{blg}x-\n"\
           f"{ss}-x{by}-{bsb}        o  {by}-{blg}x-\n"\
           f"{ss}-x{by}-{bsb}           {by}-{blg}x-\n"\
           f"{ss} -x{by}-{bsb} o  o  o {by}-{blg}x-\n"\
           f"{ss}   --{by}-{blg}xx{by}x{blg}xx{by}-{blg}--\n"\
           f"{ss}     .--x--."

    title_line = f"{bw}{title_space}{h}{hs}{title}{hs}{h}"
    date_line = f"{date_space}{date}{sr}"

    if show_parameters:
        logo_width = 17
        print("--- Aquila parameters ---")
        print(f"· shycd_space_width: {shycd_space_width}")
        print(f"· logo_width: {logo_width}")
        print(f"· len(date) {len(date)}")
        print(f"· len(title) {len(title)}")
        print(f"· len(date_space) {len(date_space)}")
        print(f"· len(title_space) {len(title_space)}")
        print(
            "· 2 * shycd_space_width + logo_width: "
            f"{2 * shycd_space_width + logo_width}"
            )
        print(
            "· 2 * len(date_space) + len(date): "
            f"{2 * len(date_space) + len(date)}"
            )
        print(f"Middle point: {(2 * shycd_space_width + logo_width) / 2}")

    return f"\n{logo}\n{title_line}\n\n{date_line}\n"

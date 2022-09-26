from . import FLGallery, utils
from .templateGlobals import template_globals
from .localization import strings

import locale
from datetime import datetime
from pytz import timezone
from flask import render_template, abort, redirect, url_for

LOCALE = 'pt_BR'  # 'en_US'
TIMEZONE = 'America/Sao_Paulo'

D_FORMAT = '%Y-%m-%d %H:%M:%S UTC%z'
locale.setlocale(locale.LC_TIME, LOCALE + '.UTF-8')  # locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')


def return_page(month, year, dirs, curtime=datetime.now(timezone(TIMEZONE))):
    # https://stackoverflow.com/a/28446432 | https://lokalise.com/blog/date-time-localization/
    m_str = utils.short_date(m=int(month)).strftime('%B').title()

    # Get previous and next months
    # TODO: Fix this, very flawed
    prev_m = str(int(month) - 1).zfill(2)
    next_m = str(int(month) + 1).zfill(2)

    if not (year, prev_m) in dirs:
        prev_m = '00'

    if not (year, next_m) in dirs:
        next_m = '00'

    # print(prev_m, next_m)

    return render_template("main.html",
                           pictures=utils.get_pics(int(year), int(month)), month=month, year=year,
                           month_name=m_str, now_time=curtime.strftime(D_FORMAT), prev_month=prev_m, next_month=next_m)


@FLGallery.route("/")
def homepage():
    cur_time = datetime.now(timezone(TIMEZONE))

    y = cur_time.strftime('%Y')
    m = cur_time.strftime('%m')

    # Use these for testing and whatnot
    # y = '2023'
    # m = '04'

    v_dirs = utils.get_valid_dirs()

    if (y, m) not in v_dirs:  # If the (month, year) combination doesn't exist...
        y, m = utils.get_closest_match((int(y), int(m)), v_dirs)  # ...get closest match.

    if (y, m) == (0, 0):
        # print(y, m)
        abort(404)

    return return_page(m, y, v_dirs, cur_time)


@FLGallery.route("/<y>/<m>")
def year_month(y, m):
    v_dirs = utils.get_valid_dirs()

    # If the month argument is not in the range of >0 = x = 13< and/or is longer > 2 digits...
    if int(m) not in range(1, 13) or len(m) > 2 or \
            (y, m) not in v_dirs:  # ...and/or the (month, year) combination don't exist...
        abort(404)  # Return "404: Page not Found".

    # If month argument is only one digit long...
    if len(m) == 1:
        # ...redirect to proper URL format:
        return redirect(url_for('flgallery.year_month', y=y, m=m.zfill(2)), code=301)  # "301: Moved permanently"

    return return_page(m, y, v_dirs)


@FLGallery.context_processor
def context():
    # If LOCALE is not a key in strings
    if LOCALE not in strings:
        lang = "en_US"
    else:
        lang = LOCALE

    # | operator merges the two dicts
    return template_globals | strings[lang]

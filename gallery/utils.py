try:
    from . import FLGallery
    sta_fo = FLGallery.static_folder
except ImportError:
    # Eww hacks :puke_emoji:
    sta_fo = 'static'
from datetime import date
from pathlib import Path


def get_pics(year, month):
    out = []
    _dir = Path(FLGallery.static_folder).joinpath(f"{year}/{str(month).zfill(2)}/")

    # print(Path.cwd())

    # sorted() is used here to enforce that the images will appear
    # in the same order, no matter what OS the server is running on
    for p in sorted(Path('.').joinpath(_dir).glob('*.jpg')):
        out.append(p.name)

    return out


def get_valid_dirs():
    _list = []

    for child in Path(sta_fo).glob('*/*/'):
        # Get all directories containing at least one file
        if child.is_dir() and len([x for x in child.iterdir() if x.is_file()]) != 0:
            p = child.parts  # Get tuple with all "parts" of the path
            pl = len(p) - 1  # Get index to last item of tuple

            _year = p[pl - 1]
            _month = p[pl]
            _list.append((_year, _month))

    return _list


def get_closest_match(_tuple, _list):
    """Find the closest match to tuple in _list"""
    # https://www.geeksforgeeks.org/python-how-to-get-subtraction-of-tuples/
    # https://stackoverflow.com/a/12141207

    # TODO: Prove this behavior works as intended IRL (aka wait one month and see if it breaks catastrophycally)
    # It very likely will break lol
    #
    #
    # If server is (somehow) being ran before any of the dates accesible, it should return 404
    # Ex: Server time is 2003-02, earliest accesible data is from 2022-05 --> Return 404
    #
    # If server is being run after the latest accesible date, it should return the latest date
    # Ex: Server time is 2023-06, latest accessible data is from 2022-06 --> Return data from 2022-06
    prev_result = (float('inf'), float('inf'))
    index = None

    for _index, l_tuple in enumerate(_list):
        subtraction = tuple(map(lambda l, m: int(l) - int(m), l_tuple, _tuple))

        # If the subtraction tuple contains a positive number (greater than 0)
        if len([x for x in subtraction if x >= 0]) == 0:
            # print(f"[x for x in {subtraction} if x > 0]: {[x for x in subtraction if x > 0]}")
            continue  # ...skip this iteration. (don't show data from the future)

        abs_sub = tuple([abs(x) for x in subtraction])
        # print(subtraction, abs_sub)
        # print(f"{abs_sub} < {prev_result}: {abs_sub < prev_result}")
        if abs_sub < prev_result:
            prev_result = abs_sub
            index = _index
            # print(index)

    if index is not None:
        # print(_list)
        # print(_list[index])
        return _list[index]
    else:
        return 0, 0


def short_date(y=1900, m=1, d=1):
    """ Shorthand for datetime.date, for doing "month number -> month name" conversions and what not"""
    return date(y, m, d)

from utils import get_valid_dirs
from pathlib import Path
from PIL import Image


def gen_thumbnails(year, month):
    # TODO: Check if script is being run from the right directory before doing anything
    _dir = f"static/{year}/{str(month).zfill(2)}/*.jpg"

    for p in Path('.').glob(_dir):
        t_path = p.parent.joinpath('t/')
        o_path = t_path.joinpath(p.name).__str__()

        # If thumbnail directory doesn't exist yet...
        if not t_path.is_dir():
            t_path.mkdir()

        if Path(o_path).is_file() and (getattr(Path(o_path).stat(), 'st_mtime') > getattr(p.stat(), 'st_mtime')):
            print(f'WARN: A thumbnail for "{p.name}" already exists, and it seems to be up-to-date.')
            continue  # Break out of this iteration of the for loop

        # https://stackoverflow.com/a/60883103
        with Image.open(p) as img:
            if img.size[0] > img.size[1]:
                shorter = img.size[1]
            else:
                shorter = img.size[0]

            left = int(img.size[0] / 2 - shorter / 2)
            upper = int(img.size[1] / 2 - shorter / 2)
            right = left + shorter
            lower = upper + shorter

            img = img.crop((left, upper, right, lower))
            img.thumbnail((300, 300), reducing_gap=2.0)

            print(f'DONE: Thumbnail succesfully generated for "{p.name}"')
            img.save(o_path)


if __name__ == '__main__':
    # TODO: Check for orphaned thumbnails and delete them
    print(f'INFO: The current working directory is "{Path.cwd()}".')

    L = get_valid_dirs('.')
    # print(L)

    for i in L:
        gen_thumbnails(*i)

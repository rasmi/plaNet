from __future__ import division

import os
import glob
from PIL import Image

def resize(image, size=256):
    """
    Crops a centered square and scales down to desired size.
    """

    im = Image.open(image)
    print im.size
    # Scale the smaller side down to size=256.
    smaller_side, smaller_side_res = min(enumerate(im.size), key=lambda s: s[1])
    larger_side, larger_side_res = max(enumerate(im.size), key=lambda s: s[1])

    print smaller_side_res, larger_side_res
    # Remove images that are too small.
    if smaller_side < size:
        os.remove(image)

    # Calculate how much to trim to get a square image.
    scaling_factor = smaller_side_res / size
    new_large_side_res = larger_side_res / scaling_factor
    crop_amount = larger_side_res - size
    trim = int((crop_amount/2)/scaling_factor)
    print trim
    if larger_side:
        # Height is larger, trim vertically.
        box = (0, 0 + trim, smaller_side_res, larger_side_res - trim)
    else:
        # Width is larger, trim horizontally.
        box = (0 + trim, 0, larger_side_res - trim, smaller_side_res)

    print box
    # Resize and crop.
    im = im.crop(box)
    im = im.resize((size, size))
    im.save(image, 'JPEG')
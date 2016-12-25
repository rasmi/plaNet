from __future__ import division

import os
import math
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

    # Calculate how much scaling to get to a properly sized image on the smaller side.
    scaling_factor = smaller_side_res / size
    new_large_side_res = int(larger_side_res / scaling_factor)

    if larger_side:
        # Height is larger, scale limit horizontally.
        im = im.resize((size, new_large_side_res))
    else:
        # Height is larger, scale limit vertically.
        im = im.resize((new_large_side_res, size))

    # Trim the rest to reach size on the larger end
    crop_amount = new_large_side_res - size
    if crop_amount % 2 == 0:
        pad = 0
    else:
        pad = 1
    trim = math.floor(crop_amount/2)

    if larger_side:
        # Height is larger, trim vertically.
        box = (0, 0 + trim + pad, size, new_large_side_res - trim)
    else:
        # Width is larger, trim horizontally.
        box = (0 + trim + pad, 0, new_large_side_res - trim, size)

    print box
    # Crop.
    im = im.crop(box)
    
    im.save(image, 'JPEG')
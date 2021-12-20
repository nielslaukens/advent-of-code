import typing

import numpy
import scipy.ndimage

from tools import numpy_tools

with open("20.input.txt", "r") as f:
    lines = [
        line.strip()
        for line in f.readlines()
    ]
    lines = [
        [
            char == '#'
            for char in line
        ]
        for line in lines
    ]

image_enhancement_algorithm = lines[0]
assert lines[1] == []
image = numpy.array(lines[2:], dtype=bool)


def enhance_once(image: numpy.ndarray, background: bool) -> typing.Tuple[numpy.ndarray, bool]:
    def process_pixel(footpr):
        # I don't understand why, but footpr is of dtype=float
        binary_number = ''.join([str(bit) for bit in footpr.astype(int).tolist()])
        number = int(binary_number, 2)
        enhanced_pixel = image_enhancement_algorithm[number]
        return enhanced_pixel

    enhanced_image = scipy.ndimage.generic_filter(
        numpy.pad(image, pad_width=1, mode='constant', constant_values=background),
        # ^ add explicit border to allow the image to extend
        footprint=numpy.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
        function=process_pixel,
        mode='constant', cval=background,
    )
    return enhanced_image, image_enhancement_algorithm[511 if background else 0]

print(numpy_tools.str_highlight_value(image.astype(int), 1))
enhanced_image, background = enhance_once(image, background=False)
print(numpy_tools.str_highlight_value(enhanced_image.astype(int), 1))
enhanced_image, background = enhance_once(enhanced_image, background)
print(numpy_tools.str_highlight_value(enhanced_image.astype(int), 1))

assert background is False
print(f"{numpy.sum(enhanced_image)} pixels are lit")

#!/usr/bin/env python
__version__ =  '1.0'
__licence__ = 'FreeBSD License'
__author__ =  'Robert Gawron'
import sys
import Image
import math
import random
import logging

def get_offset(a, b):
 
    mask = ((-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2),
            (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
            (-2,  0), (-1,  0), (0,  0), (1,  0), (2,  0),
            (-2,  1), (-1,  1), (0,  1), (1,  1), (2,  1),
            (-2, -2), (-1,  2), (0,  2), (1,  2), (2,  2))

    mask1 = ((-1, -1), (0, -1), (1, -1),
            (-1,  0), (0,  0), (1,  0),
            (-1,  1), (0,  1), (1,  1))



    width, height = a.size
    frame = 5#len(mask) # TODO is it needed?
    x_start = random.randrange(frame, width - frame)
    y_start = random.randrange(frame, height - frame)


    best_match = 0, 0
    first_check = True
    smallest_difference = 0

    for (x_init, y_init) in mask:
        x, y = x_start + x_init, y_start + y_init
        difference = 0
        local_best_match = 0, 0

        for (x_delta, y_delta) in mask:
            x_checked, y_checked = x + x_delta, y + y_delta
            p1, p2 = a.getpixel((x, y)), b.getpixel((x_checked, y_checked))
            difference += abs(p1[0] - p2[0])

            if first_check or smallest_difference >= difference:
                first_check = False
                smallest_difference = difference
                local_best_match = x_delta, y_delta

        best_match = best_match[0] + local_best_match[0], best_match[1] + local_best_match[1]

    return best_match[0]/len(mask), best_match[1]/len(mask)


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    assert(len(sys.argv) == 3)

    files = sys.argv[1], sys.argv[2]
    logging.info(files)

    images = map(Image.open, files)
    assert(images[0].size == images[1].size)

    samples_amount = 50# TODO magic number

    width, height = images[0].size
    images[0] = images[0].resize((width*2, height*2)) 
    images[1] = images[1].resize((width*2, height*2)) 

    x, y = 0, 0
    for i in range(samples_amount):
        xn, yn = get_offset(images[0], images[1])
        x, y = x + xn, y + yn

    x, y = (x / samples_amount), (y / samples_amount)

    print "the offset between %s and %s is (%2d, %2d)" % (files[0], files[1], x, y)

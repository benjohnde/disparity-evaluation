#!/usr/bin/env python

import sys
import os
import subprocess
import time
import multiprocessing
from functools import partial

config = {
    'algorithms': range(6),
    'cmd': '/Users/bjohn/git/thesis/disparity-evaluation/1_DisparityAlgorithm/bin/DisparityAlgorithm',
    'datasets': [
        {
            'path': '/Users/bjohn/Desktop/datasets/svddd/',
            'sequences': ['03-apple']
        }
    ]
}

def mkdirs(path):
    if not os.path.exists(path): os.makedirs(path)
    return

def getListOfImages(path):
    images = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            if not f.startswith('.'):
                images.append(f)
    images.sort()
    return images

# execute algorithms
def execute(path, a, image):
    current = multiprocessing.current_process()
    worker = current._identity[0]
    leftImagePath = os.path.join(path, 'left', image)
    rightImagePath = os.path.join(path, 'right', image)
    resultImagePath = os.path.join(path, 'computed', str(a))
    resultImagePath = os.path.join(resultImagePath, os.path.splitext(image)[0] + '.exr')
    f = os.path.basename(resultImagePath)
    if os.path.isfile(resultImagePath):
        print 'skipping ' + f
        return
    print 'processing ' + f
    # Usage: <identifier> <algorithmId> <left> <right> <out>
    subprocess.call([config['cmd'], str(worker), str(a), leftImagePath, rightImagePath, resultImagePath])
    return

# setup pool for processing parallelism for one sequence
def createPool(path, a):
    pool = 4
    if a == 0:
        pool = 2
    if a == 1:
        pool = 2
    if a == 9:
        pool = 2
    print 'creating pool (' + str(pool) + ') for sequence: ' + path + ', algorithm: ' + str(a)
    mkdirs(os.path.join(path, 'computed', str(a)))
    start = time.time()
    p = multiprocessing.Pool(pool)
    f = partial(execute, path, a)
    images = getListOfImages(os.path.join(path, 'left')) # only read left directory
    p.map(f, images)
    p.close()
    p.join()
    end = time.time()
    delta = "%.2f" % (end - start)
    print delta + ' seconds runtime (sequence: ' + path + ', algorithm: ' + str(a) + ')'

# create all the things
for a in config['algorithms']:
    for d in config['datasets']:
        for s in d['sequences']:
            path = os.path.join(d['path'], s)
            createPool(path, a)

exit(0)

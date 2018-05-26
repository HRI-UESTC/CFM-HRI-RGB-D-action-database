# !/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'FesianXu'
__date__ = 2018 / 3 / 23
__version__ = ''


root_path = './home/fesian/data/testdemo/'
save_path = './home/fesian/data/mats/'

import numpy as np
import scipy.io as sio
import os


'''
This script is used to read the raw skeleton files saved in .txt formation and then save them
to a more compact file in .mat formation which could easily read in MATLAB and python.
'''


def read_skel(file_path):
  nframes = 0
  with open(file_path, 'r') as f:
    for line in f:
      if '#' in line:
        nframes += 1

  mat = np.zeros(shape=(nframes, 25, 3), dtype=np.float32)
  inner_loop_counter = 0
  inner_clip_counter = -1
  is_start = False

  with open(file_path, 'r') as f:

    for line in f:
      if is_start:
        inner_loop_counter += 1
        if inner_loop_counter % 3 == 1:
          split_loc = line.split(' ')

          bias = int(inner_loop_counter/3)
          mat[inner_clip_counter, bias, 0] = float(split_loc[0])
          mat[inner_clip_counter, bias, 1] = float(split_loc[1])
          mat[inner_clip_counter, bias, 2] = float(split_loc[2])

        if inner_loop_counter % 75 == 0:
          is_start = False

      if '#' in line:
        inner_clip_counter += 1
        inner_loop_counter = 0
        is_start = True
  return mat

counter = 0
for each_1f in os.listdir(root_path):
  path_1f = root_path+'/'+each_1f
  for each_2f in os.listdir(path_1f):
    path_2f = path_1f+'/'+each_2f
    for each_3f in os.listdir(path_2f):
      path_3f = path_2f+'/'+each_3f
      for each_file in os.listdir(path_3f):
        file_name = path_3f+'/'+each_file
        mat = read_skel(file_name)
        save_file_name = save_path+each_file[0:-4]+'.mat'
        sio.savemat(save_file_name, {'skel':mat})
        counter += 1
        print(counter)


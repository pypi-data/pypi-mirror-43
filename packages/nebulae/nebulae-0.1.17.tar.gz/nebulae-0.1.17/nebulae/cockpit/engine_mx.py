#!/usr/bin/env python
'''
engine_mx
Created by Seria at 12/02/2019 3:45 PM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========
   
'''
# -*- coding:utf-8 -*-
import mxnet as mx
from ..toolkit.utility import getAvailabelGPU

class EngineMX(object):
    '''
    Param:
    device: 'gpu' or 'cpu'
    available_gpus
    gpu_mem_fraction
    if_conserve
    least_mem
    '''
    def __init__(self, param):
        self.param = param
        # look for available gpu devices
        if self.param['device'].lower() == 'gpu':
            if self.param['if_conserve']:
                from os import environ
                environ['MXNET_GPU_MEM_POOL'] = int(100 * self.param['gpu_mem_fraction'])
            if not self.param['available_gpus']:
                gpus = getAvailabelGPU(self.param['ngpus'], self.param['least_mem'])
                if gpus < 0:
                    raise Exception('No available gpu', gpus)
            else:
                gpus = self.param['available_gpus'].split(',')
            self.config_proto.gpu_options.visible_device_list = gpus
            print('+' + ((24 + len(gpus)) * '-') + '+')
            print('| Reside in Device: \033[1;36mGPU-%s\033[0m |' % gpus)
            print('+' + ((24 + len(gpus)) * '-') + '+')
        elif self.param['device'].lower() == 'cpu':
            print('+' + (23 * '-') + '+')
            print('| Reside in Device: \033[1;36mCPU\033[0m |')
            print('+' + (23 * '-') + '+')
        else:
            raise KeyError('Given device should be either cpu or gpu.')
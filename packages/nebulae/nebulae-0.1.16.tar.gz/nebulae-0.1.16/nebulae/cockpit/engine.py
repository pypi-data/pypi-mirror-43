#!/usr/bin/env python
'''
engine
Created by Seria at 23/11/2018 2:36 PM
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
from ..law import Law

def Engine(config=None, device=None, num_gpus=1, least_mem=2048,
           available_gpus='', gpu_mem_fraction=1, if_conserve=True):
    if config is None:
        param = {'device': device, 'num_gpus': num_gpus, 'least_mem': least_mem,
                 'available_gpus': available_gpus, 'gpu_mem_fraction': gpu_mem_fraction, 'if_conserve': if_conserve}
    else:
        config['num_gpus'] = config.get('num_gpus', num_gpus)
        config['least_mem'] = config.get('least_mem', least_mem)
        config['available_gpus'] = config.get('available_gpus', available_gpus)
        config['gpu_mem_fraction'] = config.get('gpu_mem_fraction', gpu_mem_fraction)
        config['if_conserve'] = config.get('if_conserve', if_conserve)
        param = config

    core = Law.CORE.upper()
    if core == 'TENSORFLOW':
        from .engine_tf import EngineTF
        return EngineTF(param)
    else:
        raise ValueError('NEBULAE ERROR ⨷ %s has not been a supported core.' % core)
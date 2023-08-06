#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Juan Montesinos"
__copyright__ = "Copyright 2018"
__version__ = "0.1"
__maintainer__ = "Juan Montesinos"
__email__ = "juanfelipe.montesinos@upf.edu"
__status__ = "Stable"


import numpy as np
from .flowlib import *
from .flowlib import flow_to_image,scale_image
import multiprocessing as mp
import matplotlib.pyplot as plt
import imageio
from functools import partial
from .interactive_flow import window

__all__=['npflow']
class npflow(np.ndarray):

    def __new__(cls, inp,UNKNOWN_FLOW_THRESH=1e7,SMALLFLOW=0.0,LARGEFLOW=1e8,*args,**kwargs):
        if isinstance(inp,np.ndarray):
            x = inp
        elif isinstance(inp,list) or isinstance(inp,tuple) or isinstance(inp,str):
            x = read_flow(inp,*args,**kwargs)
        shape = x.shape
        dimensions = len(shape)
        if dimensions == 4 or dimensions == 3:           
            obj = np.asarray(x).view(cls)
            obj.UNKNOWN_FLOW_THRESH = UNKNOWN_FLOW_THRESH
            obj.SMALLFLOW = SMALLFLOW
            obj.LARGEFLOW = LARGEFLOW
            obj.isflow = (dimensions == 3)  
            obj.N = shape[0] if dimensions == 4 else 1
            obj.idx = 0
            obj.idx_o = 0
            obj.idx_f = obj.N
            obj.step = 1
            return obj
        else:
            raise Exception('Wrong input dimensions')
    def __array_finalize__(self, obj):
        if obj is None: return
        dimensions = len(self.shape)
        self.UNKNOWN_FLOW_THRESH = getattr(obj, 'UNKNOWN_FLOW_THRESH', None)
        self.SMALLFLOW = getattr(obj, 'SMALLFLOW', None)
        self.LARGEFLOW = getattr(obj, 'LARGEFLOW', None)
        self.isflow = (dimensions == 3)  
        self.N = self.shape[0] if dimensions == 4 else 1
        self.idx = 0
        self.idx_o = 0
        self.idx_f = self.N
        self.step = getattr(obj, 'step', None)
        # We do not need to return anything    
    def __setiter__(self,start=None,end=None,step=None):
        self.idx_o = start if start is not None else 0
        self.idx_f = end if end is not None else self.N
        self.step = step if step is not None else self.step
        self.idx = self.idx_o
    def __call__(self,x=None):
        if isinstance(x,int):
            return self if self.isflow else self[x,...]
        elif isinstance(x,tuple):
            self.__setiter__(*x)
        else:
            return self.view(np.ndarray)  
    def __iter__(self):
        return self
    def __next__(self):
        if self.idx < self.idx_f:
            self.idx += self.step
            return self if self.isflow else self[self.idx-1,...]
            
        else:
            self.__setiter__(self.idx_o,self.idx_f,self.step)
            raise StopIteration
            
    def __len__(self):
        return self.N
    def fp2int(self,precision,ui=8):
        if (self.dtype == np.float64) or (self.dtype == np.float) or (self.dtype == np.float32):
            return fp2int(self,ui=ui)
        return self
    def int2fp(self,precision,ui=8):
        if (self.dtype == np.dtype('uint'+str(ui))):
            return int2fp(self,ui=ui,precision=precision)     
    def asimage(self,path=None,display = False):
        if path is None:
            return flow_to_image(self, display=False)
        else:
            flow = flow_to_image(self, display=False)
            imageio.imwrite(path,flow)
            return flow
    def save_as_stream(self,path,**kwargs):
        imageio.mimsave(path,[i.asimage() for i in self],**kwargs)
    def interactive(self):
        game = window(self,'hola')
        self = game.main()        
    def resize(self,new_size,**kwargs):
        return npflow(FlowResize(new_size,self,**kwargs))
    def display(self,idx=None):
        if self.isflow:
            plt.imshow(self.asimage())
        else:
            plt.imshow(self[idx].asimage())
    def scale(self,new_range,dtype=np.uint8):
        return scale_image(self,new_range).astype(dtype)
    def write(self,filename,idx=None,workers=mp.cpu_count(),**kwargs):
        if self.isflow:
            write_flow(self.__call__(),filename,**kwargs)
        else:
            
            if isinstance(filename,str) and isinstance(idx,int):
                write_flow(self[idx,...],filename,**kwargs)
            else:
                idx = idx if isinstance(idx,list) else list(range(self.N))
                flow = self.__call__()
                pool = mp.Pool()
                results = [pool.apply_async(partial(write_flow,**kwargs), args =(flow[i,...],file)) for i,file in zip(idx,filename)]
                pool.close()
    def mag(self):
        if self.isflow:
            return np.linalg.norm(self[...,:2],axis=2)
        else:
            return np.linalg.norm(self[...,:2],axis=3)
                               
    def see_and_listen(self):
        from sklearn.mixture import GaussianMixture
        from sklearn.decomposition import PCA
        if self.isflow:
            raise Exception('Not available for single optical flow, use video sequence')
        sum_mag = self.mag().sum(0)
#       To implement more than 1 player per video
        predictions = sum_mag>(sum_mag.mean()+sum_mag.std()).astype(bool)
        ux = []
        uy = []
        for flow in self:
            ux.append(flow[...,0][predictions].mean())
            uy.append(flow[...,1][predictions].mean())
        ux = np.stack(ux)
        uy = np.stack(uy)
        u = np.stack([ux,uy],axis=1)
        self.pca = PCA(n_components=1)
        self.pca.fit(u)
        return sum_mag,self.pca.transform(u)[:,0]/np.linalg.norm(self.pca.components_)
d='/media/jfm/SlaveSSD/flowfusion_16npy/cello/cello11_288to295'
f = npflow(d,precision=16)
s,v=f.see_and_listen()
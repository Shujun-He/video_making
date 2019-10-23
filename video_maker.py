import cv2
import os
import numpy as np
from tqdm import tqdm

class video_maker:
    '''
    Video maker class, which makes videos from images,
    with the option to cut the images
    Args:
        images: image paths to play sequentially in a video
        cut: cut ratio in order of top, bottom, left, right
    '''
    def __init__(self,images,cut,frames_per_image=None,format='MP4V',fps=24,resolution=(1080,1920),
                 force_resolution=False):
        self.images=images
        self.frames_per_image=frames_per_image
        if frames_per_image is None:
            self.frames_per_image=np.ones(len(self.images),dtype='int32')
        self.format=format
        self.fps=fps
        self.resolution=resolution
        self.cut=cut
        self.force_resolution=force_resolution
    def _initilize_video(self,video_name):
        '''
        Initilizes the video writer and the size and
        width of the video
        '''
        if not self.force_resolution:
            height, width, layers = cv2.imread(self.images[0]).shape
            self.resolution=[int(height*(1-self.cut[0]-self.cut[1])),
                             int(width*(1-self.cut[2]-self.cut[3])),
                             ]
        print(self.resolution)
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        self.video = cv2.VideoWriter(video_name, 0, self.fps, (self.resolution[1],self.resolution[0]))
        return self
    def writeimages2vidoe(self,video_name):
        '''
        Writes the images contained by the maker to a video
        Args:
            name of the output video file
        '''
        self._initilize_video(video_name)
        for i in tqdm(range(len(self.images))):
            image=self.images[i]
            rgb=cv2.imread(image)
            rgb=image_processing.trim_image(rgb,self.cut)
            rgb=image_processing.resize_image(rgb,self.resolution)
            for j in range(self.frames_per_image[i]):
                self.video.write(rgb)
        cv2.destroyAllWindows()
        self.video.release() 
        return self
          
class image_processing:
    def resize_image(image,dim):
        resized = cv2.resize(image, (dim[1],dim[0]), interpolation = cv2.INTER_AREA)
        return resized
    def trim_image(image,cut):
        height, width, layers = image.shape
        ver_start=int(height*cut[0])
        ver_end=int(height-height*cut[1])        
        hor_start=int(width*cut[2])
        hor_end=int(width-width*cut[3])
        trimmed_image=image[ver_start:ver_end,hor_start:hor_end,]
        return trimmed_image

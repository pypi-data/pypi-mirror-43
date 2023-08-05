Master: [![CircleCI](https://circleci.com/gh/JenioPY/compimg/tree/master.svg?style=svg&circle-token=08abd49c539289429775861727cae51269c6db2c)](https://circleci.com/gh/JenioPY/compimg/tree/master) 
Develop: [![CircleCI](https://circleci.com/gh/JenioPY/compimg/tree/develop.svg?style=svg&circle-token=08abd49c539289429775861727cae51269c6db2c)](https://circleci.com/gh/JenioPY/compimg/tree/develop)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Documentation Status](https://readthedocs.org/projects/compimg/badge/?version=latest)](https://compimg.readthedocs.io/en/latest/?badge=latest)


## Introduction
##### For full documentation visit [documentation site](https://compimg.readthedocs.io).
Image similarity metrics are often used in image quality assessment for performance
evaluation of image restoration and reconstruction algorithms. They require two images:
- test image (image of interest)
- reference image (image we compare against)  

Such metrics produce numerical value.
 
Such methods are are widely called full/reduced-reference methods for 
assessing image quality.

`compimg` package is all about calculating similarity between images. 
It provides image similarity metrics (PSNR, SSIM etc.) that are widely used 
to asses image quality.

```python
import numpy as np
from compimg.similarity import SSIM
some_grayscale_image = np.ones((20,20), dtype=np.uint8)
identical_image = np.ones((20,20), dtype=np.uint8)
result = SSIM().compare(some_grayscale_image, identical_image)
# result == 1.0
```

## Features  
- common metrics for calculating similarity of one image to another 
- only `numpy` as a dependency

## Installation
`compimg` is available on PyPI. You can install it using pip:  
`pip install compimg`

## Note 
Keep in mind that metric are not aware of what you are passing. If 
metric relies on intensity values and you have YCbCr image you should pass
only the first channel to the computing routine.

## Help
If you have any problems or questions please post an issue.
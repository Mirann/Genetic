from features import surf_features
from filesworker import get_dmc_image
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image

file = "D:\\CanserImages\\Nodule\\1.3.6.1.4.1.14519.5.2.1.6279.6001.102790687459702089070957161759.dcm"
ds = get_dmc_image(file)
kp, des = surf_features(ds.pixel_array)
print(len(kp))
# img = fromarray(ds.pixel_array)


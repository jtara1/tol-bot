import numpy as np
import matplotlib.pyplot as plt

from skimage.io import imsave, imread
from skimage import data
from skimage.color import rgb2gray
from skimage.feature import match_template


image = imread('trees_ss 8.jpg')
image = rgb2gray(image)
#coin = image[170:220, 75:130]
coin = imread('trees_ss 8 crop.jpg')
coin = rgb2gray(coin)

result = match_template(image, coin)
ij = np.unravel_index(np.argmax(result), result.shape)
x, y = ij[::-1]

fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(8, 3))

ax1.imshow(coin)
ax1.set_axis_off()
ax1.set_title('template')

ax2.imshow(image)
ax2.set_axis_off()
ax2.set_title('image')
# highlight matched region
hcoin, wcoin = coin.shape
rect = plt.Rectangle((x, y), wcoin, hcoin, edgecolor='r', facecolor='none')
ax2.add_patch(rect)

ax3.imshow(result)
ax3.set_axis_off()
ax3.set_title('`match_template`\nresult')
# highlight matched region
ax3.autoscale(False)
ax3.plot(x, y, 'o', markeredgecolor='r', markerfacecolor='none', markersize=10)

plt.show()
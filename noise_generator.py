import numpy as np
import matplotlib.pyplot as plt

# Define the size of the texture
width, height = 256, 256

# Generate random noise
noise = np.random.rand(height, width)

# Create the figure and axes without a border
fig, ax = plt.subplots(figsize=(5, 5), dpi=100)
ax.imshow(noise, cmap='gray')
ax.axis('off')  # Hide the axes

# Remove the padding around the image
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

plt.show()
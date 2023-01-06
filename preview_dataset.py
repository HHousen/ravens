from ravens.dataset import Dataset
from matplotlib import pyplot as plt
import h5py

with h5py.File("test_data.h5", "r") as f:
    for i in range(0, 10*3, 3):
        image = f["color"][i]
        plt.imshow(image, interpolation='nearest')
        plt.show()

# dataset = Dataset("place-red-in-green-train")

# image = dataset.sample()["segm"]

# plt.imshow(image[2].squeeze(), interpolation='nearest')
# plt.show()
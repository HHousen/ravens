# Ravens - Transporter Networks

Fork of [google-research/ravens](https://github.com/google-research/ravens) to generate custom dataset.

## Installation

**Step 1.** Recommended: install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) with Python 3.7.

```shell
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -u
echo $'\nexport PATH=~/miniconda3/bin:"${PATH}"\n' >> ~/.profile  # Add Conda to PATH.
source ~/.profile
conda init
```

**Step 2.** Create and activate Conda environment, then install GCC and Python packages.

```shell
git clone git@github.com:HHousen/ravens.git
cd ~/ravens
conda create --name ravens python=3.7 -y
conda activate ravens
conda install h5py tqdm
pip install -r requirements.txt
pip install -e .
```

## Getting Started

Generate the dataset by running `python ravens/demos.py --assets_root=./ravens/environments/assets/ --task=place-red-in-green --mode=train --n=70000`. This will create a h5py file called `raven_robot_data.h5` with the datasets color (image data), segm (segmentation maps), and num_objects_on_table (number of objects present on the table in the image).

The `preview_dataset.py` script will cycle though the images in the generated `raven_robot_data.h5` dataset file using matplotlib.

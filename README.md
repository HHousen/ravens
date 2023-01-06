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

### Exact Commands

1. Training Data (first chunk): `python ravens/demos.py --assets_root=./ravens/environments/assets/ --task=place-red-in-green --mode=train --start_seed=-2 --n=11667`.
2. Training Data (second chunk): `python ravens/demos.py --assets_root=./ravens/environments/assets/ --task=place-red-in-green --mode=train --start_seed=23332 --n=11667`.
3. Evaluation/Test Data: `python ravens/demos.py --assets_root=./ravens/environments/assets/ --task=place-red-in-green --mode=test --start_seed=-1 --n=5000`.
4. Merge Training Data Chunk: `python merge.py`.
5. Rename: `mv ravens_robot_data_train_0.h5 ravens_robot_data_train.h5 && mv ravens_robot_data_test_1.h5 ravens_robot_data_test.h5`.

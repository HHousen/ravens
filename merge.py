import h5py
from tqdm import tqdm, trange

with h5py.File("ravens_robot_data_train_0.h5", "r+") as f1, h5py.File("ravens_robot_data_train_23334.h5", "r") as f2:
    for key in tqdm(f2.keys(), "Keys"):
        for idx in trange(len(f2[key])//2000, desc="idx"):
            value = f2[key][idx*2000:idx*2000+2000]
            f1[key].resize((f1[key].shape[0] + value.shape[0]), axis=0)
            f1[key][-value.shape[0] :] = value
        
        value = f2[key][idx*2000+2000:]
        f1[key].resize((f1[key].shape[0] + value.shape[0]), axis=0)
        f1[key][-value.shape[0] :] = value


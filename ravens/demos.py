# coding=utf-8
# Copyright 2022 The Ravens Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Data collection script."""

import os
import random
import h5py
from tqdm import tqdm

from absl import app
from absl import flags

import numpy as np

from ravens import tasks
from ravens.dataset import Dataset
from ravens.environments.environment import ContinuousEnvironment
from ravens.environments.environment import Environment

flags.DEFINE_string('assets_root', '.', '')
flags.DEFINE_string('data_dir', '.', '')
flags.DEFINE_bool('disp', False, '')
flags.DEFINE_bool('shared_memory', False, '')
flags.DEFINE_string('task', 'towers-of-hanoi', '')
flags.DEFINE_string('mode', 'train', '')
flags.DEFINE_integer('n', 1000, '')
flags.DEFINE_bool('continuous', False, '')
flags.DEFINE_integer('steps_per_seg', 3, '')

FLAGS = flags.FLAGS


def main(unused_argv):

  # Initialize environment and task.
  env_cls = ContinuousEnvironment if FLAGS.continuous else Environment
  env = env_cls(
      FLAGS.assets_root,
      disp=FLAGS.disp,
      shared_memory=FLAGS.shared_memory,
      hz=480)
  task = tasks.names[FLAGS.task](continuous=FLAGS.continuous)
  task.mode = FLAGS.mode

  # Initialize scripted oracle agent and dataset.
  agent = task.oracle(env, steps_per_seg=FLAGS.steps_per_seg)
  dataset = Dataset(os.path.join(FLAGS.data_dir, f'{FLAGS.task}-{task.mode}'))

  # Train seeds are even and test seeds are odd.
  seed = dataset.max_seed
  if seed < 0:
    seed = -1 if (task.mode == 'test') else -2

  # Determine max steps per episode.
  max_steps = task.max_steps
  if FLAGS.continuous:
    max_steps *= (FLAGS.steps_per_seg * agent.num_poses)

  # Collect training data from oracle demonstrations.
  with h5py.File("raven_robot_data.h5", "w") as f:
    for idx in tqdm(range(FLAGS.n)):
      seed += 2
      np.random.seed(seed)
      random.seed(seed)
      env.set_task(task)
      obs, num_objects_on_table = env.reset()
      color = np.array(obs["color"])
      segm = np.array(obs["segm"])
      entry = {"color": color, "segm": segm, "num_objects_on_table": np.array([num_objects_on_table])}

      for key, value in entry.items():
        if idx == 0:
          f.create_dataset(
              key,
              data=value,
              dtype=value.dtype,
              maxshape=(None, *value.shape[1:]),
              compression="gzip",
              chunks=True,
          )
        else:
          f[key].resize((f[key].shape[0] + value.shape[0]), axis=0)
          f[key][-value.shape[0] :] = value

if __name__ == '__main__':
  app.run(main)

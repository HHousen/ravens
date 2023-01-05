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

"""Sorting Task."""

import os
import random
import numpy as np
from ravens.tasks.task import Task
from ravens.utils import utils

import pybullet as p


class PlaceRedInGreen(Task):
  """Sorting Task."""

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.max_steps = 10
    self.pos_eps = 0.05

  def reset(self, env):
    super().reset(env)
    num_total_objects = np.random.randint(3, 9)
    num_objects = [0] * 3
    for _ in range(num_total_objects):
      idx = np.random.randint(0, 3)
      num_objects[idx] += 1
    n_bowls = num_objects[0]
    n_blocks = num_objects[1]
    n_boxes = num_objects[2]
    if n_boxes > 2:
      left_over = n_boxes - 2
      n_boxes = 2
      split = left_over // 2
      n_blocks += split
      n_bowls += split
      if left_over % 2 != 0:
        n_blocks += 1

    for _ in range(n_boxes):
      # Add container box.
      zone_size = self.get_random_size(0.10, 0.15, 0.12, 0.15, 0.05, 0.05)
      zone_pose = self.get_random_pose(env, zone_size)
      container_template = 'container/container-template.urdf'
      half = np.float32(zone_size) / 2
      replace = {'DIM': zone_size, 'HALF': half}
      container_urdf = self.fill_template(container_template, replace)
      obj_id = env.add_object(container_urdf, zone_pose, 'fixed')
      if obj_id is None:
        num_total_objects -= 1
        continue
      color = random.choice(list(utils.COLORS.values()))
      p.changeVisualShape(obj_id, -1, rgbaColor=color + [1])
      os.remove(container_urdf)

    # Add bowls.
    bowl_urdf = 'bowl/bowl.urdf'
    for _ in range(n_bowls):
      bowl_size = self.get_random_size(0.13, 0.15, 0.13, 0.15, 0, 0)
      bowl_pose = self.get_random_pose(env, bowl_size)
      obj_id = env.add_object(bowl_urdf, bowl_pose, 'fixed')
      if obj_id is None:
        num_total_objects -= 1
        continue
      color = random.choice(list(utils.COLORS.values()))
      p.changeVisualShape(obj_id, -1, rgbaColor=color + [1])

    # Add blocks.
    block_urdf = 'stacking/block.urdf'
    for _ in range(n_blocks):
      block_size = self.get_random_size(0.09, 0.13, 0.09, 0.13, 0.09, 0.13)
      block_pose = self.get_random_pose(env, block_size)
      block_id = env.add_object(block_urdf, block_pose)
      if block_id is None:
        num_total_objects -= 1
        continue
      color = random.choice(list(utils.COLORS.values()))
      p.changeVisualShape(block_id, -1, rgbaColor=color + [1])

    return num_total_objects

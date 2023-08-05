# coding=utf-8
# Copyright 2018 The TF-Agents Authors.
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

"""A DDPG Agent.

Implements the Deep Deterministic Policy Gradient (DDPG) algorithm from
"Continuous control with deep reinforcement learning" - Lilicrap et al.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import tensorflow as tf


from tf_agents.agents import tf_agent
from tf_agents.environments import trajectory
from tf_agents.policies import actor_policy
from tf_agents.policies import ou_noise_policy
from tf_agents.utils import eager_utils
from tf_agents.utils import nest_utils
import tf_agents.utils.common as common_utils
import gin.tf


class DdpgInfo(collections.namedtuple(
    'DdpgInfo', ('actor_loss', 'critic_loss'))):
  pass


@gin.configurable
class DdpgAgent(tf_agent.TFAgent):
  """A DDPG Agent."""

  def __init__(self,
               time_step_spec,
               action_spec,
               actor_network,
               critic_network,
               actor_optimizer=None,
               critic_optimizer=None,
               ou_stddev=1.0,
               ou_damping=1.0,
               target_update_tau=1.0,
               target_update_period=1,
               dqda_clipping=None,
               td_errors_loss_fn=None,
               gamma=1.0,
               reward_scale_factor=1.0,
               gradient_clipping=None,
               debug_summaries=False,
               summarize_grads_and_vars=False,
               train_step_counter=None,
               name=None):
    """Creates a DDPG Agent.

    Args:
      time_step_spec: A `TimeStep` spec of the expected time_steps.
      action_spec: A nest of BoundedTensorSpec representing the actions.
      actor_network: A tf_agents.network.Network to be used by the agent. The
        network will be called with call(observation, step_type).
      critic_network: A tf_agents.network.Network to be used by the agent. The
        network will be called with call(observation, action, step_type).
      actor_optimizer: The optimizer to use for the actor network.
      critic_optimizer: The optimizer to use for the critic network.
      ou_stddev: Standard deviation for the Ornstein-Uhlenbeck (OU) noise added
        in the default collect policy.
      ou_damping: Damping factor for the OU noise added in the default collect
        policy.
      target_update_tau: Factor for soft update of the target networks.
      target_update_period: Period for soft update of the target networks.
      dqda_clipping: when computing the actor loss, clips the gradient dqda
        element-wise between [-dqda_clipping, dqda_clipping]. Does not perform
        clipping if dqda_clipping == 0.
      td_errors_loss_fn:  A function for computing the TD errors loss. If None,
        a default value of  elementwise huber_loss is used.
      gamma: A discount factor for future rewards.
      reward_scale_factor: Multiplicative scale for the reward.
      gradient_clipping: Norm length to clip gradients.
      debug_summaries: A bool to gather debug summaries.
      summarize_grads_and_vars: If True, gradient and network variable summaries
        will be written during training.
      train_step_counter: An optional counter to increment every time the train
        op is run.  Defaults to the global_step.
      name: The name of this agent. All variables in this module will fall
        under that name. Defaults to the class name.
    """
    tf.Module.__init__(self, name=name)
    self._actor_network = actor_network
    self._target_actor_network = self._actor_network.copy(
        name='TargetActorNetwork')

    self._critic_network = critic_network
    self._target_critic_network = self._critic_network.copy(
        name='TargetCriticNetwork')

    self._actor_optimizer = actor_optimizer
    self._critic_optimizer = critic_optimizer

    self._ou_stddev = ou_stddev
    self._ou_damping = ou_damping
    self._target_update_tau = target_update_tau
    self._target_update_period = target_update_period
    self._dqda_clipping = dqda_clipping
    self._td_errors_loss_fn = (
        td_errors_loss_fn or common_utils.element_wise_huber_loss)
    self._gamma = gamma
    self._reward_scale_factor = reward_scale_factor
    self._gradient_clipping = gradient_clipping
    self._update_target = self._get_target_updater(self._target_update_tau,
                                                   self._target_update_period)

    policy = actor_policy.ActorPolicy(
        time_step_spec=time_step_spec, action_spec=action_spec,
        actor_network=self._actor_network, clip=True)
    collect_policy = actor_policy.ActorPolicy(
        time_step_spec=time_step_spec, action_spec=action_spec,
        actor_network=self._actor_network, clip=False)
    collect_policy = ou_noise_policy.OUNoisePolicy(
        collect_policy,
        ou_stddev=self._ou_stddev,
        ou_damping=self._ou_damping,
        clip=True)

    super(DdpgAgent, self).__init__(
        time_step_spec,
        action_spec,
        policy,
        collect_policy,
        train_sequence_length=2 if not self._actor_network.state_spec else None,
        debug_summaries=debug_summaries,
        summarize_grads_and_vars=summarize_grads_and_vars,
        train_step_counter=train_step_counter)

  def _initialize(self):
    common_utils.soft_variables_update(
        self._critic_network.variables,
        self._target_critic_network.variables, tau=1.0)
    common_utils.soft_variables_update(
        self._actor_network.variables,
        self._target_actor_network.variables, tau=1.0)

  def _get_target_updater(self, tau=1.0, period=1):
    """Performs a soft update of the target network parameters.

    For each weight w_s in the original network, and its corresponding
    weight w_t in the target network, a soft update is:
    w_t = (1- tau) x w_t + tau x ws

    Args:
      tau: A float scalar in [0, 1]. Default `tau=1.0` means hard update.
      period: Step interval at which the target networks are updated.
    Returns:
      A callable that performs a soft update of the target network parameters.
    """
    with tf.name_scope('update_targets'):
      def update():
        # TODO(kbanoop): What about observation normalizer variables?
        critic_update = common_utils.soft_variables_update(
            self._critic_network.variables,
            self._target_critic_network.variables, tau)
        actor_update = common_utils.soft_variables_update(
            self._actor_network.variables,
            self._target_actor_network.variables, tau)
        return tf.group(critic_update, actor_update)

      return common_utils.Periodically(update, period,
                                       'periodic_update_targets')

  def _experience_to_transitions(self, experience):
    transitions = trajectory.to_transition(experience)

    # Remove time dim if we are not using a recurrent network.
    if not self._actor_network.state_spec:
      transitions = tf.nest.map_structure(lambda x: tf.squeeze(x, [1]),
                                          transitions)

    time_steps, policy_steps, next_time_steps = transitions
    actions = policy_steps.action
    return time_steps, actions, next_time_steps

  def _train(self, experience, weights=None):
    time_steps, actions, next_time_steps = self._experience_to_transitions(
        experience)

    # TODO(kbanoop): Apply a loss mask or filter boundary transitions.
    critic_loss = self.critic_loss(time_steps, actions, next_time_steps,
                                   weights=weights)
    actor_loss = self.actor_loss(time_steps, weights=weights)

    def clip_and_summarize_gradients(grads_and_vars):
      """Clips gradients, and summarizes gradients and variables."""
      if self._gradient_clipping is not None:
        grads_and_vars = eager_utils.clip_gradient_norms_fn(
            self._gradient_clipping)(
                grads_and_vars)

      if self._summarize_grads_and_vars:
        # TODO(kbanoop): Move gradient summaries to train_op after we switch to
        # eager train op, and move variable summaries to critic_loss.
        for grad, var in grads_and_vars:
          with tf.name_scope('Gradients/'):
            if grad is not None:
              tf.compat.v2.summary.histogram(
                  name=grad.op.name, data=grad, step=self.train_step_counter)
          with tf.name_scope('Variables/'):
            if var is not None:
              tf.compat.v2.summary.histogram(
                  name=var.op.name, data=var, step=self.train_step_counter)
      return grads_and_vars

    eager_utils.create_train_op(
        critic_loss,
        self._critic_optimizer,
        global_step=self.train_step_counter,
        transform_grads_fn=clip_and_summarize_gradients,
        variables_to_train=self._critic_network.trainable_weights,
    )

    eager_utils.create_train_op(
        actor_loss,
        self._actor_optimizer,
        global_step=None,
        transform_grads_fn=clip_and_summarize_gradients,
        variables_to_train=self._actor_network.trainable_weights,
    )

    self._update_target()

    total_loss = actor_loss + critic_loss

    # TODO(kbanoop): Compute per element TD loss and return in loss_info.
    return tf_agent.LossInfo(total_loss,
                             DdpgInfo(actor_loss, critic_loss))

  def critic_loss(self,
                  time_steps,
                  actions,
                  next_time_steps,
                  weights=None):
    """Computes the critic loss for DDPG training.

    Args:
      time_steps: A batch of timesteps.
      actions: A batch of actions.
      next_time_steps: A batch of next timesteps.
      weights: Optional scalar or element-wise (per-batch-entry) importance
        weights.
    Returns:
      critic_loss: A scalar critic loss.
    """
    with tf.name_scope('critic_loss'):
      target_actions, _ = self._target_actor_network(
          next_time_steps.observation, next_time_steps.step_type)
      target_critic_net_input = (next_time_steps.observation, target_actions)
      target_q_values, _ = self._target_critic_network(
          target_critic_net_input, next_time_steps.step_type)

      td_targets = tf.stop_gradient(
          self._reward_scale_factor * next_time_steps.reward +
          self._gamma * next_time_steps.discount * target_q_values)

      critic_net_input = (time_steps.observation, actions)
      q_values, _ = self._critic_network(critic_net_input,
                                         time_steps.step_type)

      critic_loss = self._td_errors_loss_fn(td_targets, q_values)
      if nest_utils.is_batched_nested_tensors(
          time_steps, self.time_step_spec, num_outer_dims=2):
        # Do a sum over the time dimension.
        critic_loss = tf.reduce_sum(input_tensor=critic_loss, axis=1)
      if weights is not None:
        critic_loss *= weights
      critic_loss = tf.reduce_mean(input_tensor=critic_loss)

      with tf.name_scope('Losses/'):
        tf.compat.v2.summary.scalar(
            name='critic_loss', data=critic_loss, step=self.train_step_counter)

      if self._debug_summaries:
        td_errors = td_targets - q_values
        common_utils.generate_tensor_summaries('td_errors', td_errors,
                                               self.train_step_counter)
        common_utils.generate_tensor_summaries('td_targets', td_targets,
                                               self.train_step_counter)
        common_utils.generate_tensor_summaries('q_values', q_values,
                                               self.train_step_counter)

      return critic_loss

  def actor_loss(self, time_steps, weights=None):
    """Computes the actor_loss for DDPG training.

    Args:
      time_steps: A batch of timesteps.
      weights: Optional scalar or element-wise (per-batch-entry) importance
        weights.
      # TODO(kbanoop): Add an action norm regularizer.
    Returns:
      actor_loss: A scalar actor loss.
    """
    with tf.name_scope('actor_loss'):
      actions, _ = self._actor_network(time_steps.observation,
                                       time_steps.step_type)
      critic_net_input = (time_steps.observation, actions)
      q_values, _ = self._critic_network(critic_net_input,
                                         time_steps.step_type)
      actions = tf.nest.flatten(actions)
      dqdas = tf.gradients(ys=[q_values], xs=actions)
      actor_losses = []
      for dqda, action in zip(dqdas, actions):
        if self._dqda_clipping is not None:
          dqda = tf.clip_by_value(dqda, -1 * self._dqda_clipping,
                                  self._dqda_clipping)
        loss = common_utils.element_wise_squared_loss(
            tf.stop_gradient(dqda + action), action)
        if nest_utils.is_batched_nested_tensors(
            time_steps, self.time_step_spec, num_outer_dims=2):
          # Sum over the time dimension.
          loss = tf.reduce_sum(input_tensor=loss, axis=1)
        if weights is not None:
          loss *= weights
        loss = tf.reduce_mean(input_tensor=loss)
        actor_losses.append(loss)

      actor_loss = tf.add_n(actor_losses)
      with tf.name_scope('Losses/'):
        tf.compat.v2.summary.scalar(
            name='actor_loss', data=actor_loss, step=self.train_step_counter)

    return actor_loss

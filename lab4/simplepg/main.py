#!/usr/bin/env python

"""
This project was developed by Rocky Duan, Peter Chen, Pieter Abbeel for the Berkeley Deep RL Bootcamp, August 2017. Bootcamp website with slides and lecture videos: https://sites.google.com/view/deep-rl-bootcamp/.

Copyright 2017 Deep RL Bootcamp Organizers.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""


from collections import defaultdict
import numpy as np
import gym
import click
from simplepg.simple_utils import gradient_check, log_softmax, softmax, weighted_sample, include_bias, test_once, nprs
import tests.simplepg_tests


##############################
# Methods for Point-v0
##############################

def point_get_logp_action(theta, ob, action):
    """
    :param theta: A matrix of size |A| * (|S|+1)
    :param ob: A vector of size |S|
    :param action: A vector of size |A|
    :return: A scalar
    """
    ob_1 = include_bias(ob)
    mean = theta.dot(ob_1)
    zs = action - mean
    return -0.5 * np.log(2 * np.pi) * theta.shape[0] - 0.5 * np.sum(np.square(zs))


def point_get_grad_logp_action(theta, ob, action):
    """
    :param theta: A matrix of size |A| * (|S|+1)
    :param ob: A vector of size |S|
    :param action: A vector of size |A|
    :return: A matrix of size |A| * (|S|+1)
    
    This implementation is based on suggested from
    function point_get_logp_action.
    
    The only difference is in the computation of the
    returned results. Refer to the lab instructions,
    part 3.3
    """
    ob1 = include_bias(ob)
    mean = theta.dot(ob1)
    zs = action - mean
    return np.outer(zs, ob1)


def point_get_action(theta, ob, rng=np.random):
    """
    :param theta: A matrix of size |A| * (|S|+1)
    :param ob: A vector of size |S|
    :return: A vector of size |A|
    """
    ob_1 = include_bias(ob)
    mean = theta.dot(ob_1)
    return rng.normal(loc=mean, scale=1.)


def point_test_grad_impl():
    # check gradient implementation
    rng = nprs(42)
    test_ob = rng.uniform(size=(4,))
    test_act = rng.uniform(size=(4,))
    test_theta = rng.uniform(size=(4, 5))
    # Check that the shape matches
    assert point_get_grad_logp_action(
        test_theta, test_ob, test_act).shape == test_theta.shape
    gradient_check(
        lambda x: point_get_logp_action(
            x.reshape(test_theta.shape), test_ob, test_act),
        lambda x: point_get_grad_logp_action(
            x.reshape(test_theta.shape), test_ob, test_act).flatten(),
        test_theta.flatten()
    )


##############################
# Methods for Cartpole-v0
##############################

def compute_logits(theta, ob):
    """
    :param theta: A matrix of size |A| * (|S|+1)
    :param ob: A vector of size |S|
    :return: A vector of size |A|
    """
    ob_1 = include_bias(ob)
    logits = ob_1.dot(theta.T)
    return logits


def cartpole_get_logp_action(theta, ob, action):
    """
    :param theta: A matrix of size |A| * (|S|+1)
    :param ob: A vector of size |S|
    :param action: An integer
    :return: A scalar
    """
    return log_softmax(compute_logits(theta, ob))[action]


def cartpole_get_grad_logp_action(theta, ob, action):
    """
    :param theta: A matrix of size |A| * (|S|+1)
    :param ob: A vector of size |S|
    :param action: An integer
    :return: A matrix of size |A| * (|S|+1)
    """
    # Create empty array for storing actions
    a = np.zeros(theta.shape[0])
    
    # Set current action
    a[action] = 1
    
    # Compute the softmax probability of the actions
    # Refer to p. 3.6 softmax formula
    softmax_prob = softmax(compute_logits(theta, ob))
    
    ob1 = include_bias(ob)
    # Compute the return gradient similarly as for the point example
    
    return np.outer(a - softmax_prob, ob1)


def cartpole_get_action(theta, ob, rng=np.random):
    """
    :param theta: A matrix of size |A| * (|S|+1)
    :param ob: A vector of size |S|
    :return: An integer
    """
    return weighted_sample(compute_logits(theta, ob), rng=rng)


def cartpole_test_grad_impl():
    # check gradient implementation
    rng = nprs(42)
    test_ob = rng.uniform(size=(4,))
    test_act = rng.choice(4)
    test_theta = rng.uniform(size=(4, 5))
    # Check that the shape matches
    assert cartpole_get_grad_logp_action(
        test_theta, test_ob, test_act).shape == test_theta.shape
    gradient_check(
        lambda x: cartpole_get_logp_action(
            x.reshape(test_theta.shape), test_ob, test_act),
        lambda x: cartpole_get_grad_logp_action(
            x.reshape(test_theta.shape), test_ob, test_act).flatten(),
        test_theta.flatten()
    )


def compute_entropy(logits):
    """
    :param logits: A matrix of size N * |A|
    :return: A vector of size N
    """
    logp = log_softmax(logits)
    return -np.sum(logp * np.exp(logp), axis=-1)


@click.command()
@click.argument("env_id", type=str, default="Point-v0")
@click.option("--batch_size", type=int, default=2000)
@click.option("--discount", type=float, default=0.99)
@click.option("--learning_rate", type=float, default=0.1)
@click.option("--n_itrs", type=int, default=100)
@click.option("--render", type=bool, default=False)
@click.option("--use-baseline", type=bool, default=True)
@click.option("--natural", type=bool, default=False)
@click.option("--natural_step_size", type=float, default=0.01)
def main(env_id, batch_size, discount, learning_rate, n_itrs, render, use_baseline, natural, natural_step_size):
    # Check gradient implementation

    rng = np.random.RandomState(42)

    if env_id == 'CartPole-v0':
        cartpole_test_grad_impl()
        env = gym.make('CartPole-v0')
        obs_dim = env.observation_space.shape[0]
        action_dim = env.action_space.n
        get_action = cartpole_get_action
        get_grad_logp_action = cartpole_get_grad_logp_action
    elif env_id == 'Point-v0':
        point_test_grad_impl()
        from simplepg import point_env
        env = gym.make('Point-v0')
        obs_dim = env.observation_space.shape[0]
        action_dim = env.action_space.shape[0]
        get_action = point_get_action
        get_grad_logp_action = point_get_grad_logp_action
    else:
        raise ValueError(
            "Unsupported environment: must be one of 'CartPole-v0', 'Point-v0'")

    env.seed(42)
    timestep_limit = env.spec.timestep_limit

    # Initialize parameters
    theta = rng.normal(scale=0.1, size=(action_dim, obs_dim + 1))

    # Store baselines for each time step.
    baselines = np.zeros(timestep_limit)

    # Policy training loop
    for itr in range(n_itrs):
        # Collect trajectory loop
        n_samples = 0
        grad = np.zeros_like(theta)
        episode_rewards = []

        # Store cumulative returns for each time step
        all_returns = [[] for _ in range(timestep_limit)]

        all_observations = []
        all_actions = []

        while n_samples < batch_size:
            observations = []
            actions = []
            rewards = []
            ob = env.reset()
            done = False
            # Only render the first trajectory
            render_episode = n_samples == 0
            # Collect a new trajectory
            while not done:
                action = get_action(theta, ob, rng=rng)
                next_ob, rew, done, _ = env.step(action)
                observations.append(ob)
                actions.append(action)
                rewards.append(rew)
                ob = next_ob
                n_samples += 1
                if render and render_episode:
                    env.render()
            # Go back in time to compute returns and accumulate gradient
            # Compute the gradient along this trajectory
            R = 0.
            for t in reversed(range(len(observations))):
                def compute_update(discount, R_tplus1, theta, s_t, a_t, r_t, b_t, get_grad_logp_action):
                    """
                    :param discount: A scalar
                    :param R_tplus1: A scalar
                    :param theta: A matrix of size |A| * (|S|+1)
                    :param s_t: A vector of size |S|
                    :param a_t: Either a vector of size |A| or an integer, depending on the environment
                    :param r_t: A scalar
                    :param b_t: A scalar
                    :param get_grad_logp_action: A function, mapping from (theta, ob, action) to the gradient (a 
                    matrix of size |A| * (|S|+1) )
                    :return: A tuple, consisting of a scalar and a matrix of size |A| * (|S|+1)
                    """
                    # Use the formula from the lab instructions, part 3.4
                    R_t = discount * R_tplus1 + r_t
                    # Compute the single gradient contribution by formula from step 3.3
                    pg_theta = get_grad_logp_action(theta, s_t, a_t) * (R_t - b_t)
                    return R_t, pg_theta

                # Test the implementation, but only once
                test_once(compute_update)

                R, grad_t = compute_update(
                    discount=discount,
                    R_tplus1=R,
                    theta=theta,
                    s_t=observations[t],
                    a_t=actions[t],
                    r_t=rewards[t],
                    b_t=baselines[t],
                    get_grad_logp_action=get_grad_logp_action
                )
                all_returns[t].append(R)
                grad += grad_t

            episode_rewards.append(np.sum(rewards))
            all_observations.extend(observations)
            all_actions.extend(actions)

        def compute_baselines(all_returns):
            """
            :param all_returns: A list of size T, where the t-th entry is a list of numbers, denoting the returns 
            collected at time step t across different episodes
            :return: A vector of size T
            """
            baselines = np.zeros(len(all_returns))
            for t in range(len(all_returns)):
                # Use trajectories from previous episodes to compute the baseline
                if len(all_returns[t]) > 0:
                    # We need to check do we have any trajectories at all
                    # If not the default value of zero will be remaining
                    baselines[t] = np.mean(all_returns[t])
            return baselines

        if use_baseline:
            test_once(compute_baselines)
            baselines = compute_baselines(all_returns)
        else:
            baselines = np.zeros(timestep_limit)

        # Roughly normalize the gradient
        grad = grad / (np.linalg.norm(grad) + 1e-8)

        if not natural:

            theta += learning_rate * grad
        else:
            def compute_fisher_matrix(theta, get_grad_logp_action, all_observations, all_actions):
                """
                :param theta: A matrix of size |A| * (|S|+1)
                :param get_grad_logp_action: A function, mapping from (theta, ob, action) to the gradient (a matrix 
                of size |A| * (|S|+1) )
                :param all_observations: A list of vectors of size |S|
                :param all_actions: A list of vectors of size |A|
                :return: A matrix of size (|A|*(|S|+1)) * (|A|*(|S|+1)), i.e. #columns and #rows are the number of 
                entries in theta
                """
                d = len(theta.flatten())
                F = np.zeros((d, d))
                
                # Compute for each action 
                for i in range(len(all_actions)):
                    # First compute the inner value of the action gradient and make theta a flattened vector
                    grads = get_grad_logp_action(theta, all_observations[i], all_actions[i]).flatten()
                    # Accumulate the inner product of the gradient
                    F += np.outer(grads, grads.T)
                    
                # Compute the mean (expected value)    
                F /= len(all_actions)
                return F

            def compute_natural_gradient(F, grad, reg=1e-4):
                """
                :param F: A matrix of size (|A|*(|S|+1)) * (|A|*(|S|+1))
                :param grad: A matrix of size |A| * (|S|+1)
                :param reg: A scalar
                :return: A matrix of size |A| * (|S|+1)
                """
                # First ensure that Fisher inf. matrix is positive definite
                F_inv = np.linalg.inv(F + reg * np.eye(*F.shape))
                
                # Compute natural gradient with flattened version
                natural_grad = F_inv.dot(grad.flatten())
                
                # Reshape back to the g shape
                natural_grad = natural_grad.reshape(grad.shape)
                
                return natural_grad

            def compute_step_size(F, natural_grad, natural_step_size):
                """
                :param F: A matrix of size (|A|*(|S|+1)) * (|A|*(|S|+1))
                :param natural_grad: A matrix of size |A| * (|S|+1)
                :param natural_step_size: A scalar
                :return: A scalar
                """
                
                # Flatten the natural gradient again
                natural_grad = natural_grad.flatten()
                
                # The computation is performed on accordance with
                # Formula from the solution footnote
                denominator = natural_grad.T.dot(F).dot(natural_grad)
                nominator = 2 * natural_step_size
                
                step_size = np.sqrt(nominator / denominator)
                
                return step_size

            test_once(compute_fisher_matrix)
            test_once(compute_natural_gradient)
            test_once(compute_step_size)

            F = compute_fisher_matrix(theta=theta, get_grad_logp_action=get_grad_logp_action,
                                      all_observations=all_observations, all_actions=all_actions)
            natural_grad = compute_natural_gradient(F, grad)
            step_size = compute_step_size(F, natural_grad, natural_step_size)
            theta += step_size * natural_grad

        if env_id == 'CartPole-v0':
            logits = compute_logits(theta, np.array(all_observations))
            ent = np.mean(compute_entropy(logits))
            perp = np.exp(ent)

            print("Iteration: %d AverageReturn: %.2f Entropy: %.2f Perplexity: %.2f |theta|_2: %.2f" % (
                itr, np.mean(episode_rewards), ent, perp, np.linalg.norm(theta)))
        else:
            print("Iteration: %d AverageReturn: %.2f |theta|_2: %.2f" % (
                itr, np.mean(episode_rewards), np.linalg.norm(theta)))


if __name__ == "__main__":
    main()

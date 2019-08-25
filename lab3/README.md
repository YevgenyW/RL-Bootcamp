## How to test this lab work

This README provides commands to quickly test the results of the homeworks.

**NOTE: Before testing the lab work be sure that you completed all pre-lab setup of your local environment. Make sure Docker is started and Docker Daemon is reachable**

### DQN Update


To test run:

```bash
./docker_run.sh simpledqn/main.py GridWorld-v0
```

To visualize run in separate terminal:

```bash
./docker_run.sh simpledqn/main.py --render True GridWorld-v0
```

Or alternatively:

```bash
./docker_run.sh viskit/frontend.py data/local/dqn_gridworld
```

*If your implementation is correct, you should observe steady improvement in the AverageReturn metric, achieving an average return of 1 after about 10 iterations*

### Double DQN update

We can switch on the Double DQN mode by turning on a command-line flag:

```bash
./docker_run.sh simpledqn/main.py --double True GridWorld-v0
```

*Although double Q-learning is more stable, its performance gain on this simple Gridworld problem is not obvious.*

### Learning Pong with RAM observation

To test run:

```bash
./docker_run.sh simpledqn/main.py --double --render True Pong-ram-v0
```

To visualize:

```bash
./docker_run.sh viskit/frontend.py data/local/dqn_pong
```

*The AverageReturn should go from approximately −18 to approximately −11 in 50 iterations, but you should start to see learning progress in the first couple minutes*










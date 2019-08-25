## How to test this lab work

This README provides commands to quickly test the results of the homeworks.

**NOTE: Before testing the lab work be sure that you completed all pre-lab setup of your local environment. Make sure Docker is started and Docker Daemon is reachable**

### Policy Gradient (part 3)

Without using Time-Dependent baseline

```bash
./docker_run.sh simplepg/main.py Point-v0 --render True --use-baseline False
```

With usage of Time-Dependent baseline

```bash
./docker_run.sh simplepg/main.py Point-v0 --render True
```

Cartpole discrete actions gradient testing

```bash
./docker_run.sh simplepg/main.py CartPole-v0 --render True
```

Natural Gradient

```bash
 ./docker_run.sh simplepg/main.py CartPole-v0 --natural True
```

### Advanced Policy Gradient (part 4)

```bash
./docker_run.sh experiments/run_pg_cartpole.py
```

To visualize the result run this in separate terminal

```bash
./docker_run.sh scripts/sim_policy.py data/local/pg-cartpole
```

Or in other way run

```bash
./docker_run.sh viskit/frontend.py data/local/pg-cartpole
```

And visit [this link](http://localhost:5000/)

You can find detailed variables explanation in the lab instructions (at the end of part 4)

### Trust Region Policy Optimization (TRPO)

Discrete policy testing

```bash
./docker_run.sh experiments/run_trpo_cartpole.py
```

Continious Pendulum policy

```bash
./docker_run.sh experiments/run_trpo_pendulum.py
```

Roboschool Cheetah continious policy (requires a lot of time to train)

```bash
./docker_run.sh experiments/run_trpo_half_cheetah.py
```

For visualizations instructions refer to lab instructions (part 5.3)






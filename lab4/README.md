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

*Your algorithm should be able to achieve an average return of above -25 in around 30 iterations, and above -21 in around 60 iterations.*

Cartpole discrete actions gradient testing

```bash
./docker_run.sh simplepg/main.py CartPole-v0 --render True
```

*After correctly implementing the method, your code should be able to im- prove its performance (the desired average return should be above 180).*

Natural Gradient

```bash
 ./docker_run.sh simplepg/main.py CartPole-v0 --natural True
```

*After completing these methods, you should observe much more stable performance improvement.*

### Advanced Policy Gradient (part 4)

```bash
./docker_run.sh experiments/run_pg_cartpole.py
```

*Within 100 iterations you should be able to achieve an average return close to 200.*

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

*You should observe that the average return quickly converges to the op- timal value 200. *

Continious Pendulum policy

```bash
./docker_run.sh experiments/run_trpo_pendulum.py
```

*Your implementation should be able to achieve an average return of at least around −180 after training for 100 iterations *

Roboschool Cheetah continious policy (requires a lot of time to train)

```bash
./docker_run.sh experiments/run_trpo_half_cheetah.py
```

* This environment requires much more time to train. You should be able to achieve an average return of around 200 after 100 iterations, 1000 after 400 iterations, and 2000 after 2500 iterations (your actual result may vary).*

For visualizations instructions refer to lab instructions (part 5.3)

### A2C

Pong agent policy with partially trained policy

```bash
 ./docker_run.sh experiments/run_a2c_pong_warm_start.py
```

*If your implementation is correct, you should observe the average return rising from −21 to −13 in 10 epochs, 0 in 20 epochs, and around 20 in 30 epochs*

Breakout agent from scratch

```bash
./docker_run.sh experiments/run_a2c_breakout.py
```

*Although reaching convergence can take quite long (a few thousands of epochs in our experience), progress can be observed from very early on. With a proper implementation you should observe the average return im- proving from around 1 to around 10 after 50 epochs.*

Pong agent from scratch

```bash
./docker_run.sh experiments/run_a2c_pong.py
```

*This can take a few hours before you see any signs of life. In our experience, the performance stayed at around −20 during the first 300 up to even 700 epochs. Then, it will gradually improve to around 20 in a few hundred more epochs. *





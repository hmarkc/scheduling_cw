# Instructions

<!-- README files with minimal instructions to compile and use your code -->

Set up:

    pip install -r requirements.txt

To test Tabu/RVNS algorithms, run the <code>main.py</code> file using the following arguments:

    usage: main.py [-h] [-method METHOD] [-env ENV] [-L L] [-gamma GAMMA] [-K K] [-debug DEBUG] [-seed SEED] [-opt]

    options:
      -h, --help      show this help message and exit
      -method METHOD  the method to use: tabu or rvns
      -env ENV        the environment to use: theo or vm
      -L L            the length of the tabu list
      -gamma GAMMA    the gamma parameter
      -K K            the number of iterations to run the algorithm for
      -debug DEBUG    the level of debug messages to print
      -seed SEED      the seed to use for random number generation
      -opt            whether to optimize the RVNS schedule by local search

Run Tabu algorithm with 120000 iterations, $\gamma$=10, $L$=20:

    python main.py -method tabu -K 120000 -gamma 10 -L 20

Run RVNS algorithm with 2000 iterations, $seed$=3

    python main.py -method rvns -K 2000 -seed 3

Run the optimized RVNS algorithm (with the extra refinement step) with 500 iterations, $seed$=3

    python main.py -method rvns -K 500 -seed 3 -opt

<code>experiment.ipynb</code> contains all the experiments used to generate the graphs in the report. Run it sequentially to repeat all the experiments.

Execution of question 2.1 is in <code>2_1_output.txt</code>, question 2.2 in <code>2_2_output.txt</code>, question 3.2 in <code>3_2_output.txt</code>, and question 3.3 in <code>3_3_output.txt</code>.

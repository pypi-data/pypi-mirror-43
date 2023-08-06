# BigMPI4py

BigMPI4py is a module developed based on Lisando Dalcin's implementation of Message Passing 
Interface (MPI for short) for python, MPI4py (https://mpi4py.readthedocs.io), which allows for
parallelization of data structures within python code. 

Although many of the common cases of parallelization can be solved with MPI4py alone, there
are cases were big data structures cannot be distributed across cores within MPI4py 
infrastructure. This limitation is well known for MPI4py and happens due to the fact that MPI 
calls have a buffer limitation of 2GB entries. 

In order to solve this problem, some solutions exist, like dividing the datasets in "chunks" that
satisfy the data size criterion, or using other MPI implementations such as BigMPI 
(https://github.com/jeffhammond/BigMPI). BigMPI requires both understanding
the syntax of BigMPI, as well as having to adapt python scripts to BigMPI, which can be 
difficult and requires knowledge of C-based programming languages, of which many users have a 
lack of. Then, the "chunking" strategy can be used in Python, but has to be adapted manually for 
data types and, in many cases, the number of elements that each node will receive which, in order
to circumvent the 2 GB problem, can be difficult.

BigMPI4py adapts the "chunking" strategy of data, being able to automatically distribute 
the most common python
data types used in python, such as numpy arrays, pandas dataframes, lists, nested lists, 
or lists of 
arrays and dataframes. Therefore, users of BigMPI4py can automatically parallelize their 
pipelines by calling BigMPI4py's functions with their data.

So far, BigMPI4py implements certain MPI's collective communication operations, like
`MPI.Comm.scatter()`, `MPI.Comm.bcast()`, `MPI.Comm.gather()` or `MPI.Comm.allgather()`, which 
are the most commonly used ones in parallelization.  BigMPI4py also implements point-to-point 
communication operation `MPI.Comm.sendrecv()`.

BigMPI4py also detects whether a vectorized parallelization using `MPI.Comm.Scatterv()` and 
`MPI.Comm.Gatherv()` operations can be used, saving time for object communication. 

Check out the tutorial notebook to see how to use BigMPI4py, with many examples inside!
Also, you can look at the Docker containers with conda and pip installation in `Registry` section on the left.

## How to install BigMPI4py

BigMPI4py works on MPI4py, and MPI4py works on MPI, which is an external program. When installing BigMPI4py by conda you won't need to install anything.
If you prefer to install BigMPI4py via pip, you will have to install MPI first.

### Installing via conda

In order to install pip via conda run this command on the terminal:
 `conda install -c alexmascension bigmpi4py` 

### Installing via pip

BigMPI4py can be installed via pip with:

`pip install bigmpi4py`

MPI must be installed. You can install MPI (and other related libraries) with:

`apt-get install libopenmpi2 openmpi-bin openmpi-common openssh-client openssh-server libopenmpi-dev`

## How to use the notebook

You can download the notebook in any location of your computer. After installing
BigMPI4py, go to the directory where you have downloaded the notebook via the
console, and run

`jupyter notebook`

This will prompt a window where you can run the tutorial. Mind that some files
will be generated in a folder at the same directory where you downloaded the 
notebook.

## Error troubleshooting

Most of the errors when running BigMPI4py or MPI4py derive from problems with MPI. Please, make sure no ovelapping versions of MPI exist.
When installing BigMPI4py through conda, OpenMPI v3.0 is installed, so if you already have some version of MPI installed, it is possible
that MPI reports some error when running. Then install BigMPI4py via pip, or uninstall any MPI installed, and reinstall BigMPI4py.

When running BigMPI4py through conda it is possible that this error appears:

```
--------------------------------------------------------------------------
The value of the MCA parameter "plm_rsh_agent" was set to a path
that could not be found:

  plm_rsh_agent: ssh : rsh

Please either unset the parameter, or check that the path is correct
--------------------------------------------------------------------------
```

If that happens, installing `openssh` should solve the problem:
`apt-get install openssh-client openssh-server`

## Cite us

You can look up our paper in bioRxiv to see how the software works.
https://www.biorxiv.org/content/early/2019/01/17/517441

If you find this software useful, please cite us:

Alex M. Ascensión and Marcos J. Araúzo-Bravo. BigMPI4py: Python module for parallelization of Big Data objects; bioRxiv, (2019). doi: 10.1101/517441. 


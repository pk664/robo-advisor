# robo-advisor

A Python application that ... describe ... 

# Prerequisites 

  + Anaconda 3.7+
  + Python 3.7+
  + Pip

## Installation

Fork this [remote repository](http://github.com/pk664/robo-advisor) under your own control, then "clone" or download your remote copy onto your local computer.


After cloning the repo, navigate there from the command-line:

```sh
cd robo-advisor
```

Use Anaconda to create and activate a new virtual environment, perhaps called "stocks-env":

```sh
conda create -n stocks-env python=3.8
conda activate stocks-env
```

From inside the virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

> NOTE: if this command throws an error like "Could not open requirements file: [Errno 2] No such file or directory", make sure you are running it from the repository's root directory, where the requirements.txt file exists (see the initial `cd` step above)

## Usage

Run the game script by executing the following command: 

```py
python app/robo_advisor.py

> NOTE: if you see an error like "ModuleNotFoundError: No module named '...'", 
it's because the given package isn't installed, so run the `pip` command above to ensure that 
package has been installed into the virtual environment. 

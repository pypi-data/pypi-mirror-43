# abp 0.6.3
Python port of Anders and Briegel' s [method](https://arxiv.org/abs/quant-ph/0504117) for fast simulation of Clifford circuits.

## Usage

```python
import abp
from abp.util import xyz
g = abp.GraphState()
g.add_qubit("alice", position=xyz(0, 0, 0))
g.add_qubit("bob", position=xyz(0, 0, 0))
g.act_hadamard("alice")
g.act_hadamard("bob")
g.act_cz("alice", "bob")
g.push() # Sends for visualization
```

## Demo

![Demo video](doc/abp.mp4)

## Installation

Install from source

```shell
$ git clone http://gitlab.psiquantum.lan/pete/abp
$ cd abp
$ virtualenv env
$ source env/bin/activate
$ python setup.py develop 
```

## Documentation
You can read the full documentation [here](https://peteshadbolt.co.uk/static/abp/). You can also build it locally using Sphinx with `make doc`.

To install Sphinx on OSX, use `pip install sphinx`. If after doing so `make doc` still does not work, some OSX users may also need to install `sphinxcontrib-napoleon` by running `pip install sphinxcontrib-napoleon`.

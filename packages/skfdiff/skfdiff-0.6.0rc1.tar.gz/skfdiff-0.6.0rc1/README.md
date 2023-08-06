# Scikit-fdiff / skfdiff (formerly Triflow)

|                                                                       master                                                                       |                                                                     dev                                                                      |
| :------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------: |
| [![pipeline status](https://gitlab.com/celliern/scikit-fdiff/badges/master/pipeline.svg)](https://gitlab.com/celliern/scikit-fdiff/commits/master) | [![pipeline status](https://gitlab.com/celliern/scikit-fdiff/badges/dev/pipeline.svg)](https://gitlab.com/celliern/scikit-fdiff/commits/dev) |
| [![coverage report](https://gitlab.com/celliern/scikit-fdiff/badges/master/coverage.svg)](https://gitlab.com/celliern/scikit-fdiff/commits/master) | [![coverage report](https://gitlab.com/celliern/scikit-fdiff/badges/dev/coverage.svg)](https://gitlab.com/celliern/scikit-fdiff/commits/dev) |

- [Scikit-fdiff / skfdiff (formerly Triflow)](#scikit-fdiff--skfdiff-formerly-triflow)
  - [Installation](#installation)
    - [External requirements](#external-requirements)
    - [via PyPI](#via-pypi)
    - [via github](#via-github)
    - [via anaconda (strongly advised for windows users)](#via-anaconda-strongly-advised-for-windows-users)
  - [Introduction](#introduction)
    - [Rational](#rational)
  - [Model writing](#model-writing)
    - [Example](#example)
      - [1D advection / diffusion system, Dirichlet boundary](#1d-advection--diffusion-system-dirichlet-boundary)
      - [2D advection / diffusion system, mixed dirichlet / periodic boundary](#2d-advection--diffusion-system-mixed-dirichlet--periodic-boundary)
  - [News / TODO / Roadmad](#news--todo--roadmad)
    - [NEWS](#news)
    - [ROADMAP / TODO LIST](#roadmap--todo-list)
    - [License](#license)

## Installation

### External requirements

This library is written for python &gt;= 3.5.

On v0.6.0, it is possible to choose between numpy and numba
(which provide similar features). numpy will be slower but with
no compilation time, which is handy for testing and prototyping.
On other hand, numba use a JIT compilation, and give access to
faster and parallized routines in the cost of an extra dependency
and a warm-up time.

### via PyPI

```bash
pip install skfdiff[numba,interactive]
```

will install the package and

```bash
pip install skfdiff --upgrade
```

will update an old version of the library.

### via github

You can install the latest version of the library
using pip and the github repository:

```bash
pip install git+git://github.com/locie/skfdiff.git
```

### via anaconda (strongly advised for windows users)

```bash
conda install -c conda-forge -c celliern skfdiff
```

## Introduction

### Rational

The aim of this library is to have a (relatively) easy way to write
transient dynamic systems with 1D finite difference discretization, with
fast temporal solvers.

The main two parts of the library are:

- symbolic tools defining the spatial discretization, with boundary
    taking into account in a separated part
- a fast temporal solver written in order to use the sparsity of the
    finite difference method to reduce the memory and CPU usage during
    the solving

Moreover, extra tools are provided and the library is written in a
modular way, allowing an easy extension of these different parts (see
the plug-in module of the library.)

The library fits well with an interactive usage (in a jupyter notebook).
The dependency list is actually larger, but on-going work target a
reduction of the stack complexity.

## Model writing

All the models are written as function generating the F
vector and the Jacobian matrix of the model defined as ``dtU = F(U)``.

The symbolic model is written as a simple mathematic equation. For
example, a diffusion advection model can be written as:

```python
from skfdiff import Model

equation_diff = "k * dxxU - c * dxU"
dependent_var = "U"
physical_parameters = ["k", "c"]

model = Model(equation_diff, dependent_var,
              physical_parameters)
```

### Example

#### 1D advection / diffusion system, Dirichlet boundary

```python
>>> import pylab as pl
>>> import numpy as np
>>> from skfdiff import Model, Simulation

>>> model = Model("k * dxxU - c * dxU",
...               "U(x)", ["k", "c"],
...               boundary_conditions={("U", "x"): ("dirichlet", "dirichlet")}
...               )

>>> x, dx = np.linspace(0, 1, 200, retstep=True)
>>> U = np.cos(2 * np.pi * x * 5)

# The fields are ``xarray.Dataset`` objects, and all the
# tools / methods available in the ``xarray`` lib can be
# applied to the skfdiff.Fields.
>>> fields = model.Fields(x=x, U=U, k=0.001, c=0.3)

# fix the boundary values for the dirichlet condition
>>> fields["U"][0] = 1
>>> fields["U"][-1] = 0

>>> t = 0
>>> dt = 5E-1
>>> tmax = 2.5

>>> simul = Simulation(model, fields, dt, tmax=tmax)

# The containers are in-memory or persistant
# xarray Dataset with all or some time-steps available.
>>> container = simul.attach_container()
>>> simul.run()
(2.5, <xarray.Dataset>
 Dimensions:  (x: 200)
 Coordinates:
   * x        (x) float64 0.0 ... 1.0
 Data variables:
     U        (x) float64 ...
     k        float64 0.001
     c        float64 0.3)

>>> for t in container.data.t:
...     fig = pl.figure()
...     plot = container.data["U"].sel(t=t).plot()

```

#### 2D advection / diffusion system, mixed robin / periodic boundary

```python
>>> import pylab as pl
>>> import numpy as np
>>> from skfdiff import Model, Simulation

# some specialized scheme as the upwind scheme as been implemented.
# as the problem as a strong advective component, we can use it
# to reduce the numerical instabilities.
# the dirichlet condition mean that the boundary will stay fix,
# keeping the initial value.
>>> model = Model("k * (dxxU + dyyU) - (upwind(cx, U, x, 2) + upwind(cy, U, y, 2))",
...               "U(x, y)", ["k", "cx", "cy"],
...               boundary_conditions={("U", "x"): ("dxU - (U - sin(y) * cos(t))", "dxU - 5"),
...                                    ("U", "y"):  "periodic"})

>>> x = np.linspace(0, 10, 56)
>>> y = np.linspace(-np.pi, np.pi, 32)

>>> U = np.zeros((x.size, y.size))
>>> fields = model.Fields(x=x, y=y, U=U, k=0.001, cx=0.8, cy=0.3)

>>> dt = 1.
>>> tmax = 15.

>>> simul = Simulation(model, fields, dt, tmax=tmax, tol=5E-1)
>>> container = simul.attach_container()

>>> simul.run()
(15.0, <xarray.Dataset>
 Dimensions:  (x: 56, y: 32)
 Coordinates:
   * x        (x) float64 0.0 ... 10.0
   * y        (y) float64 -3.142 ... 3.142
 Data variables:
     U        (x, y) float64 ...
     k        float64 0.001
     cx       float64 0.8
     cy       float64 0.3)

>>> for t in np.linspace(0, tmax, 5):
...     fig = pl.figure()
...     plot = container.data["U"].sel(t=t, method="nearest").plot()

```

## News / TODO / Roadmad

### NEWS

v0.6.0: This is a huge step for the software, and a lot of the API modification
is expected. Beside that, the software name change (some other skfdiff was there
before this one). All change will not be documented : they are numerous and it
should be considered as a new, more capable and performant software.
As the main improvement :

- Real arbitrary boundary condition: complex boundary conditions are properly
  dealt with and the domain where they sould be applied are automaticaly
  detected by the solver.
- Arbitrary dimension: the software is now able to deal with 2D / 3D (and more)
  and not only 1D cases.
- Auxiliary definition allow the user to define intermediary variables, making
  the model writing easier.
- The core dependencies have been decreased, and there is the possibility the
  select some extra dependency. In particular, theano is not mendatory anymore,
  allowing easier installation (especially for windows users).
- skfdiff[interactive] allow interactive work with the jupyter notebook.
- skfdiff[numba] make the numba backend available if the non-python dep of
  numba are available on the computer (see the numba doc).

v0.5.1:

- remove some model arguments (simplify, fdiff_jac) that was undocumented.
- make Simulation, Fields, Container, Model pickables in order to improve
  multiprocessing usage of the library

v0.5.0:

- WARNING: some part of the API has changed:
  - Simulation signature has changed. ``t`` arg is now optional (with t=0) as
    default and ``physical_parameters`` is now ``parameters``.
  - The displays have been completely rewritten, and the previous API is
    depreciated. Users are encouraged to modify their scripts or to stick to
    the ^0.4 skfdiff versions.
- move schemes from plugins to core
- backends: remove tensorflow, add numpy which is way slower but has no
  compilation overhead.
- displays and containers are connected to the simulation via `streamz`
- add post-processing.
- real-time display is now based on [Holoviews](https://holoviews.org/).
  Backward compatibility for display is broken and users are encouraged
  to modify their scripts or to stick to the ^0.4 skfdiff versions.
- use poetry to manage dependencies.
- use `tqdm` to display simulation update.

v0.4.12:

- give user choice of backend
  - get out tensorflow backend (not really efficient for
  increased maintenance cost)
  - give access to theano and numpy backend
- upwind scheme support
- using xarray as fields backend, allowing easy post process and save
- update display and containers
- adding repr string to all major classes

v0.4.7:

- adding tensor flow support with full testing
- adding post-processing in bokeh fields display

### ROADMAP / TODO LIST

The following items are linked to a better use of solid external libs:

- change all the display and container workflow:
  - ~~use streamz to allow pipeline like way to add display / probing / post-process~~
  - ~~use holoviews as main way to do real-time plotting~~
  - ~~use xarray multi netcdf files to reduce IO lack of performance~~
- better use of external solving lib:
  - merge skfdiff.plugins.schemes and scipy.integrate.OdeSolver API
  - ~~use scipy.integrate.solve_ivp for skfdiff temporal scheme solving (making it more robust)~~
  - main goal is to have better two-way integration with scipy

These are linked to the skfdiff core

- ~~build a robust boundary condition API ~~
- ~~work on dimension extension, allowing 2D resolution and more~~
- allow heterogeneous grid (variable with different dimensions)
  - ~~internal computation that deal heterogeneous grid~~
  - aggregation function (mean, integrate, min/max, localized probe)
- ~~allow auxiliary function to make some complex model easier to write~~
- allow a choice on the finite difference scheme, on a global way or term by term (core implemented, need user api)
- test and propose other backends (Cython, ~~numba~~, pythran?)
- work on adaptive spatial and temporal mesh

These are "behind-the scene" that are important for code maintainability

- ~~make a class that is able to deal with boundary condition logic and complexity~~
- ~~change the name of the package~~
- ~~Use appveyor for windows tests~~
- ~~use the gitlab continuous deployment to build and upload the doc.~~

These are far away but can be very interesting:

- implement continuation algorithm working with skfdiff (separate project?)

### License

This project is licensed under the term of the [MIT license](LICENSE)
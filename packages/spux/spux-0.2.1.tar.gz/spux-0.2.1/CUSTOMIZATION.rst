
.. _CUSTOMIZATION:

=============
Customization
=============

This section discusses the peculiarities of coupling your model with the framework
(the most common use case of SPUX),
including some guidelines on writing a custom posterrior sampler
or a custom likelihood module and using it within SPUX.
You are welcome to browse through the results of the models already coupled to spux in the :ref:`gallery`.

Adding your model
-----------------

In order to implement your own model, first you can take a look at the base Model class at
`spux/models/model.py <https://gitlab.com/siam-sc/spux/tree/master/spux/models/model.py>`_.
There, extensive comments describe the requirements and also additional helper variables
available within all model methods.

You will need to create a new file with your model class derived from this base :code:`Model` class.
To have an idea what is required, take a look at the code
for the Randomwalk model used in :ref:`tutorial`.

Taking into account additional requirements for respective drivers (see :ref:`installation`),
start from the template corresponding to the required programming language:

* Python: `spux/models/randomwalk.py <https://gitlab.com/siam-sc/spux/tree/master/spux/models/randomwalk.py>`_, `examples/hydro/hydro.py <https://gitlab.com/siam-sc/spux/tree/master/examples/hydro/hydro.py>`_
* Fortran: `examples/superflex/superflex.py <https://gitlab.com/siam-sc/spux/tree/master/examples/superflex/superflex.py>`_
* Java: `examples/prey-predator/ibm.py <https://gitlab.com/siam-sc/spux/tree/master/spux/models/ibm.py>`_

You will need to modify two mandatory methods:

* :code:`init (self, input, parameters)` - initialize model for the specified input and parameters
* :code:`run (self, time)` - run model until the specified time

In the method declarations above, the arguments have the following meanings:

* :code:`input` - an optional arbitraty object specified in the :code:`likelihood` (default is :code:`None`)
* :code:`parameters` - a :code:`pandas.Dataframe` object with model parameters (as in the :code:`prior` of the :code:`sampler`)
* :code:`time` - an entry from the :code:`index` of the :code:`pandas.Dataframe` object :code:`data` specified in the :code:`likelihood`

If you model is not written in pure Python (or R?), you will need to specify custom methods for model serialization
into its binary representation (state) and a corresponding de-serialization:

* :code:`save (self)` - save and return a binary array representing the current state of the model
* :code:`load (self, state)` - load model using the binary array representing its required state
* :code:`state (self, size)` - return a custom empty array of required size (default: :code:`bytearray`)

For most common programming languages, SPUX contains built-in driver modules which in
`spux/drivers <https://gitlab.com/siam-sc/spux/tree/master/spux/drivers/>`_,
which can be used to implement the above routines quickly and efficiently.
We recomment to look at the provided example modes in
`examples/ <https://gitlab.com/siam-sc/spux/tree/master/examples/>`_.

Adding your distribution
------------------------

The easiest way to specify a multivariate distribution is to use a tensor
`spux/distributions/tensor.py <https://gitlab.com/siam-sc/spux/tree/master/spux/distributions/tensor.py>`_
of selected univariate distributions from the :code:`scipy.stats` module; see an example in :ref:`tutorial`.

An example of how to have a joint parameters distribution with correlations,
possibly by selecting a multivariate distribution from the :code:`scipy.stats` module,
can be found in
`spux/distributions/multivariate.py <https://gitlab.com/siam-sc/spux/tree/master/spux/distributions/multivariate.py>`_.

Adding your error
-----------------

One custom scenario would be when the predictions or the data need to be transformed
before the density of the distribution can be evaluated.
To support this, you can provide a custom :code:`transform (self, data, parameters)` method in the error class
which returns a new copy of the data with the required transformations already in place.

For an example, look at the :code:`error.py` in
`examples/hydro/error.py <https://gitlab.com/siam-sc/spux/tree/master/examples/hydro/error.py>`_.

Adding your sampler
-------------------

Work in progress.

Adding your likelihood
----------------------

Work in progress.

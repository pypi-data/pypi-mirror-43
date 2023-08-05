pyveu -- Value Error Unit
=================================

The python package pyveu (Value Error Unit) handles real-life experimental
data which includes uncertainties and physical units. The package implements
arithmetic operations and many mathematical functions for physical quantities.
Gaussian error propagation is used to calculate the uncertainty of derived
quantities.

The package is built with the day-to-day requirements of people working a
laboratory kept in mind. The package offers an imperative programming style,
which means that the operations are evaluated when they are typed
interactively in python, giving researchers the freedom and flexibility they
need.


Quickstart
==========

Install the package using pip

.. code-block:: console

   $ pip install pyveu


The working horse of the package is the `pyveu.Quantity
<https://pyveu.readthedocs.io/en/latest/api_reference.html#quantity>`_ class. It can be
used to convert units, for example, it can convert meter per second into kilometer
per hour.

>>> from pyveu import Quantity
>>> speed = Quantity("32 +- 3 m / s")
>>> speed.str("km / hr")
'(115 +- 11) km / hr'

Quantities from a measurement usually come with a measurement uncertainty. The
class `pyveu.Quantity
<https://pyveu.readthedocs.io/en/latest/api_reference.html#quantity>`_ propagates the uncertainty automatically.

>>> time = Quantity("3.23 +- 0.1 min")
>>> distance = speed * time
>>> distance.str("km")
'(6.2 +- 0.6) km'

Links
=====

 * `GitLab Repository <https://gitlab.sauerburger.com/frank/pyveu>`_
 * `Documentation <https://pyveu.readthedocs.io/>`_
 * `pyveu on PyPi <https://pypi.org/project/pyveu>`_

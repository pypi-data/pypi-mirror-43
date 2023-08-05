
.. |bs| replace:: **bgsignature**

BGSignature
===========

|bs| is a package used to compute signatures.

The most basic type of computation is the computation
of the counts of the different k-mers (e.g. 3 or 5).
This computation can be done for a set of mutations,
for a set of regions or for a set of mutation
that fall within certain regions.


|bs| consists of 3 tools:

- **count**: count different k-mers
- **frequency**: divide the counts by the total counts
- **normalize**: divide the counts by counts obtained
  separately and normalize the results.

**Advanced features** include:

- ability to group the counts (e.g. group mutations by sample)
- normalize the counts by the context taken from a regions file
- collapse (add together) reverse complementary sequences



Installation
------------

This project is a Python package
and can be installed with ``pip``.
Download the source code, get into this
project directory and execute:

.. code:: bash

   pip install .


Usage
-----

Command line interface
**********************

The 3 tools can be called using

- *bgsignature count*
- *bgsignature frequency*
- *bgsignature normalize*

Some examples:

- getting help:

    .. code:: bash

       bgsignature -h
       bgsignature frequency -h

- count triplets in mutation that fall in certain regions using hg38:

    .. code:: bash

       bgsignature count -m my/muts/file -r my/regions/file
       -g hg38 -o my/output.json --cores 4


Python
******

Alternative, the command line options have an equivalent in Python:

.. code:: python

   from bgsignature import count, relative_frequency, normalize

that accept similar parameters except the output.
The return object can be used as a dictionary.

If you already have your files loaded in Python
you can use directly count function
in the corresponding module.
E.g.:

.. code:: python

   from bgsignature.count import mutation
   mutation.count(mutations, 'hg38', 3)

In addition, you can also
use the the "low-level" functions that
do the count (``count_all``
and ``count_group``)
which are much simple and do not
perform any kind of parallelization.
E.g.:

.. code:: python

   from bgsignature.count import mutation
   mutation.count_all(mutations, 'hg38', 3)
   # or to group mutations by sample
   mutation.count_group(mutations, 'hg38', 3, 'SAMPLE')


The return object can be normalized to 1,
using the ``sum1()`` method
or divided by some normalization counts
using the ``normalize()`` method.



Important
---------

There are some behavioural characteristics that
must be taken into account:

- |bs| filters out mutations whose reference nucleotide
  (as provided in the file), and the
  corresponding one in the reference genome do not match.

- when using the ``collapse`` option (enabled by default),
  |bs| does not remove one of the collapsed sequences but keeps both.
  This means that you need to manually remove the ones you
  are not interested in.

- when using ``bgsignature.count.mutation.count``
  or ``bgsignature.count.region.count`` function
  and a number of ``cores`` for paralelization,
  the ``chunk`` parameter must be selected
  adequately, as a it can have a huge impact on performance.

File formats
------------

Mutations file
**************

Tab separated file
(can be compressed into ``gz``, ``bgz`` or ``xz`` formats)
with a header and at least these columns:
``CHROMOSOME``, ``POSITION``, ``REF``, ``ALT``.
In addition, ``SAMPLE``, ``CANCER_TYPE`` and ``SIGNATURE``
are optional columns that can be used for
grouping the signature.


Regions file
************

Tab separated file
(can be compressed into ``gz``, ``bgz`` or ``xz`` formats)
with a header and at least these columns:
``CHROMOSOME``, ``START``, ``END``, ``ELEMENT``.
In addition, ``SYMBOL``, and ``SEGMENT``
are optional columns that can be used for
grouping the signature.



Support
-------

If you are having issues, please let us know.
You can contact us at: bbglab@irbbarcelona.org

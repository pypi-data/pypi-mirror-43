pl-z2labelmap
=============

.. image:: https://badge.fury.io/py/pl-z2labelmap.svg
    :target: https://badge.fury.io/py/pl-z2labelmap

.. image:: https://travis-ci.org/FNNDSC/pl-z2labelmap.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/pl-z2labelmap

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-z2labelmap

.. contents:: Table of Contents


Abstract
--------

zlabelmap.py generates FreeSurfer labelmaps from z-score vector files. Essentially the script consumes an input text vector file of 

.. code::

    <str_structureName> <float_lh_zScore> <float_rh_zScore>

and creates a FreeSurfer labelmap where <str_structureName> colors correspond to the z-score (normalized between 0 and 255).

Currently, only the 'aparc.a2009s' FreeSurfer segmentation is fully supported, however future parcellation support is planned.

Negative z-scores and positive z-scores are treated in the same manner but have sign-specific color specifications.

Positive and negative z-Scores can be assigned some combination of the chars 'RGB' to indicate which color dimension will reflect the z-Score. For example, a 
    
.. code::

    --posColor R --negColor RG

will assign positive z-scores shades of 'red' and negative z-scores shades of 'yellow' (Red + Green = Yellow).

Synopsis
--------

.. code::

    python z2labelmap.py                                            \
        [-v <level>] [--verbosity <level>]                          \
        [--random]                                                  \
        [-p <f_posRange>] [--posRange <f_posRange>]                 \
        [-n <f_negRange>] [--negRange <f_negRange>]                 \
        [-P <'RGB'>] [--posColor <'RGB'>]                           \
        [-N  <'RGB'> [--negColor <'RGB'>]                           \
        [-s <f_scaleRange>] [--scaleRange <f_scaleRange>]           \
        [-l <f_lowerFilter>] [--lowerFilter <f_lowerFilter>]        \
        [-u <f_upperFilter>] [--upperFilter <f_upperFilter>]        \
        [-z <zFile>] [--zFile <zFile>]                              \
        [--version]                                                 \
        [--man]                                                     \
        [--meta]                                                    \
        <inputDir>                                                  \
        <outputDir> 

Run
----

This ``plugin`` can be run in two modes: natively as a python package or as a containerized docker image.

Using PyPI
~~~~~~~~~~

To run from PyPI, simply do a 

.. code:: bash

    pip install z2labelmap


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the host ``$(pwd)/out`` directory is world writable!*

Now, prefix all calls with 

.. code:: bash

    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-z2labelmap z2labelmap.py                          \

Thus, getting on-line help is:

.. code:: bash

    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-z2labelmap z2labelmap.py                          \
            --man                                                       \
            /incoming /outgoing

Brief example
~~~~~~~~~~~~~

* To create a sample/random z-score file and analyze this created file:

.. code::

    mkdir in out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing  \
            fnndsc/pl-z2labelmap z2labelmap.py                      \
            --random                                                \
            --posRange 3.0 --negRange -3.0                          \
            /incoming /outgoing

In this example, z-scores range between 0.0 and (+/-) 3.0.

* To analyze a file already located at 'in/zfile.csv', apply a scaleRange and also filter out the lower 80\% of z-scores:

.. code::
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing  \
            fnndsc/pl-z2labelmap z2labelmap.py                      \
            --scaleRange 2.0 --lowerFilter 0.8                      \
            --negColor B --posColor R                               \
            /incoming /outgoing

* Assuming a file called 'zfile.csv' in the <inputDirectory> that ranges in z-score between 0.0 and 3.0, use the --scaleRange to reduce the apparent brightness of the map by 50 percent and also remove the lower 80 percent of zscores (this has the effect of only showing the brightest 20 percent of zscores). 

.. code:: 

    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing  \
            fnndsc/pl-z2labelmap z2labelmap.py                      \
            --scaleRange 2.0 --lowerFilter 0.8                      \
            --negColor B --posColor R                               \
            /incoming /outgoing

Command line arguments
----------------------

.. code::

        <inputDir>
        Required argument.
        Input directory for plugin.

        <outputDir>
        Required argument.
        Output directory for plugin.

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--random]
        If specified, generate a z-score file based on <posRange> and <negRange>.

        [-p <f_posRange>] [--posRange <f_posRange>]
        Positive range for random max deviation generation.

        [-n <f_negRange>] [--negRange <f_negRange>]
        Negative range for random max deviation generation.

        [-P <'RGB'>] [--posColor <'RGB'>]
        Some combination of 'R', 'G', B' for positive heat.

        [-N  <'RGB'> [--negColor <'RGB'>]
        Some combination of 'R', 'G', B' for negative heat.

        [-s <f_scaleRange>] [--scaleRange <f_scaleRange>]
        Scale range for normalization. This has the effect of controlling the
        brightness of the map. For example, if this 1.5 the effect
        is increase the apparent range by 50% which darkens all colors values.

        [-l <f_lowerFilter>] [--lowerFilter <f_lowerFilter>]
        Filter all z-scores below (normalized) <lowerFilter> to 0.0.

        [-u <f_upperFilter>] [--upperFilter <f_upperFilter>]
        Filter all z-scores above (normalized) <upperFilter> to 0.0.

        [-z <zFile>] [--zFile <zFile>]
        z-score file to read (relative to input directory). Defaults to 'zfile.csv'.

        [--version]
        If specified, print version number. 
        
        [--man]
        If specified, print (this) man page.

        [--meta]
        If specified, print plugin meta data.


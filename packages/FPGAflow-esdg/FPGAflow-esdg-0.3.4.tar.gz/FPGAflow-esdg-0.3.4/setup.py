# -*- coding: utf8 -*-
"""

************
``setup.py``
************

`BSD`_ © 2018-2019 Science and Technology Facilities Council & contributors

.. _BSD: _static/LICENSE


"""

import setuptools

if __name__ == "__main__":
    with open("README.rst", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="FPGAflow-esdg",
        version="0.3.4",
        author="Electronic System Design Group",
        author_email="fpgaflow@stfc.ac.uk",
        description="FPGAFlow scripted tool-flow for FPGA firmware development",
        long_description=long_description,
        long_description_content_type="text/x-rst",
        url="https://bitbucket.org/mjroberts/fpgaflow",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 2.7",
            "License :: OSI Approved :: BSD License",
            "Operating System :: POSIX :: Linux",
        ],
    )

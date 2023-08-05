import setuptools

setuptools.setup(
    name="python-bitvavo-api",
    version="1.0.0",
    author="Bitvavo",
    description="This is the python wrapper for the Bitvavo API",
    url="https://github.com/bitvavo/python-bitvavo-api",
    packages=setuptools.find_packages(),
    install_requires=[
        'websocket-client>=0.53.0',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
    ],
)
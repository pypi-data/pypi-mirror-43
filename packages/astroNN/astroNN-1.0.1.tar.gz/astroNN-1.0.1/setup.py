import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='astroNN',
    version='1.0.1',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Astronomy'],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'astropy',
        'h5py',
        'matplotlib',
        'astroquery',
        'pandas',
        'seaborn',
        'scikit-learn',
        'tqdm',
        'packaging'],
    extras_require={
        "keras": ["keras>=2.2.4"],
        "tensorflow": ["tensorflow>=1.13.1"],
        "tensorflow-gpu": ["tensorflow-gpu>=1.13.1"],
        "tensorflow-probability": ["tensorflow-probability>=0.6.0"]},
    url='https://github.com/henrysky/astroNN',
    project_urls={
        "Bug Tracker": "https://github.com/henrysky/astroNN/issues",
        "Documentation": "http://astronn.readthedocs.io/",
        "Source Code": "https://github.com/henrysky/astroNN",
    },
    license='MIT',
    author='Henry Leung',
    author_email='henrysky.leung@mail.utoronto.ca',
    description='Deep Learning for Astronomers with Tensorflow',
    long_description=long_description
)

# see if user really has tensorflow as tensorflow is not a strict requirement
try:
    import tensorflow
except ImportError:
    print("=======================================================================")
    print("Tensorflow not found, please install tensorflow or tensorflow_gpu manually!")
    print("=======================================================================")

try:
    import tensorflow_probability
except ImportError:
    print("=======================================================================")
    print("tensorflow_probability not found, please install tensorflow_probability manually!")
    print("=======================================================================")

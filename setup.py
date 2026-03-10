from setuptools import setup, find_packages

setup(
    name='blackboxml',
    version='0.5.0',
    author='Stuart Asiimwe',
    author_email='stuartgabriel@ymail.com',
    description='ML experiment tracking. Local, lightweight, framework-agnostic.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/stuartasiimwe7/blackboxml',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'click',
    ],
    extras_require={
        'keras': ['tensorflow>=2.0.0'],
    },
    entry_points={
        'console_scripts': [
            'bbml=blackboxml.cli:main',
        ],
    },
    python_requires='>=3.10',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)

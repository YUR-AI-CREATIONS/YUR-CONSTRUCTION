"""
Setup script for BID-ZONE
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text() if readme_file.exists() else ''

# Read requirements
requirements_file = Path(__file__).parent / 'requirements.txt'
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip() 
        for line in requirements_file.read_text().split('\n')
        if line.strip() and not line.startswith('#')
    ]

setup(
    name='bid-zone',
    version='1.0.0',
    description='Enterprise Construction Estimating Platform',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='YUR AI CREATIONS',
    license='MIT',
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'bid-zone=main:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Office/Business',
        'Topic :: Scientific/Engineering',
    ],
    keywords='construction estimating ai csi cost-estimation',
)

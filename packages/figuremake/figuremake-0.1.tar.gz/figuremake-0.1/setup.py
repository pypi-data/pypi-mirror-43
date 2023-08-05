from setuptools import setup, find_packages

setup(
    name="figuremake",
    version="0.1",
    description="Create black and white PNGs",
    author="Andrew Hoetker",
    author_email="ahoetker@me.com",
    url="https://github.com/ahoetker/figuremake",
    packages=find_packages(),
    install_requires=[
        "Click",
        "Pillow"
    ],
    entry_points='''
        [console_scripts]
        figuremake=figuremake.main:cli
    ''',
)

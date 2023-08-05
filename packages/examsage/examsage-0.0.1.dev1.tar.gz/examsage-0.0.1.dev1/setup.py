from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="examsage",
    version="0.0.1.dev1",
    author="Michael Barnard",
    author_email="mbarnard10@ivytech.edu",
    description="A tool for write math exams using sagemath and LaTeX. This is my first package and is intended as a learning exercise. In other words, expect nothing to work.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        'examsage',
    ],
    license="MIT",
    zip_safe=False,
)
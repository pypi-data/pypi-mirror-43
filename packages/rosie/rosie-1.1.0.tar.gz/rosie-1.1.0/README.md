# A Python Module for Rosie Pattern Language

* Python package for Rosie Pattern Language, to enable `pip install rosie`.

* Requires a Rosie installation.  See the
[Rosie repository](https://gitlab.com/rosie-pattern-language/rosie).

### Instruction for creating a PyPI package

Test the installation locally

	pip install -e .

Build the source distribution

    python setup.py sdist

Upload to PyPI:

	twine upload dist/*



"""
Sanic OpenAPI extension.
"""
import re
import pathlib
from setuptools import setup

module_init_path = pathlib.Path.cwd() / "sanic_openapi3e" / "__init__.py"
assert module_init_path.exists()
with open(str(module_init_path)) as fp:
    try:
        version = re.findall(
            r"""^__version__ = ['"]([^'"]+)['"]\r?$""", fp.read(), re.M
        )[0]
    except IndexError:
        raise RuntimeError(
            "Unable to determine version from {}".format(module_init_path)
        )

module_readme = pathlib.Path.cwd() / "README.md"
with open(str(module_readme)) as fp:
    long_description = fp.read()
    long_description_content_type = "text/markdown"

setup(
    name="sanic-openapi3e",
    version=version,
    url="https://github.com/endafarrell/sanic-openapi",
    license="MIT",
    author="Enda Farrell",
    author_email="enda.farrell@gmail.com",
    description="OpenAPI v3 support for Sanic. Document and describe all parameters, including sanic path params. python 3.5+",
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    packages=["sanic_openapi3e"],
    package_data={"sanic_openapi3e": ["ui/*"]},
    platforms="any",
    install_requires=["sanic>=0.6.0", "loguru"],
    extras_require={"testing": ["pytest", "pytest-cov"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)

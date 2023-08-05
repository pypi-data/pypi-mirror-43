import io

from setuptools import find_packages, setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="asu",
    version="0.2.4",
    url="https://github.com/aparcar/attendedsysupgrade-server",
    license="",
    maintainer="Paul Spooren",
    maintainer_email="mail@aparcar.org",
    description="Create sysupgrade images for OpenWrt on demand",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask", "pyodbc", "pyyaml"],
)

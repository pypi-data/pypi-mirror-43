from setuptools import find_packages, setup

setup(
    name="jkutils",
    version="0.6",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["requests==2.19.1", "kazoo==2.5.0"],
)

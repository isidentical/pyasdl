from setuptools import setup

setup(
    intall_requires=["pegen==0.0", "typing_extensions"],
    packages=["pyasdl"],
    package_data={"pyasdl": ["static/asdl.gram"]},
)

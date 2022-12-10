import setuptools

exec(open('vtk_helper/_version.py').read())

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    install_requires = [line.strip('\n') for line in f.readlines()]

setuptools.setup(
    name="vtk_helper",
    version=__version__,
    author="Petr Valenta",
    author_email="petr.valenta@email.com",
    description="A library for easy manipulation with VTK files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    url="https://github.com/valenpe7/vtk_helper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

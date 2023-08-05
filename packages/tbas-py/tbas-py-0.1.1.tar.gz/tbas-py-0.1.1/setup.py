import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tbas-py",
    version="0.1.1",
    author="Eric Hennenfent",
    author_email="ecapstone@gmail.com",
    description="Python interpreter for Tis But A Scratch (Brainfuck derivative)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ehennenfent/tbas_python",
    packages=setuptools.find_packages(),
    keywords='tbas',
    entry_points={
            'console_scripts': ['tbas=tbas.interpreter:main',
                                'tbas-gui=tbas.ui:main'],
        }
)

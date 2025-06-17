from setuptools import setup, find_packages

from pkg_resources import parse_requirements

with open("requirements.txt", encoding="utf-8") as fp:
    install_requires = [str(requirement) for requirement in parse_requirements(fp)]

setup(
    name="Chan-Theory",
    version="0.1.0",
    author="Yuhao Lian",
    author_email="lianyuhao@ieee.org",
    description="A short description of your package",
    long_description="eds sdk for python",
    license="Apache License, Version 2.0",
    url="https://github.com/YuhaoLian/Chan-Theory",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GRU License",
        "Operating System :: OS Independent",
    ],

    include_package_data=True,  # 一般不需要
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'test = test.help:main'
        ]
    }
)
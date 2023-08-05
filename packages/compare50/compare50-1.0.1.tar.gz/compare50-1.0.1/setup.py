from setuptools import setup, find_packages

setup(
    author="CS50",
    author_email="sysadmins@cs50.harvard.edu",
    classifiers=[
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.6",
        "Topic :: Education",
        "Topic :: Utilities"
    ],
    license="GPLv3",
    description="This is compare50, with which you can compare files for similarities.",
    install_requires=["attrs>=18", "intervaltree", "lib50", "numpy", "pygments", "jinja2", "termcolor", "tqdm"],
    extras_require = {
        "develop": ["sphinx", "sphinx_rtd_theme", "line_profiler"]
    },
    keywords=["compare", "compare50"],
    name="compare50",
    python_requires=">=3.5",
    packages=find_packages(exclude=["tests"]),
    scripts=["bin/compare50"],
    url="https://github.com/cs50/compare50",
    version="1.0.1",
    include_package_data=True,
)

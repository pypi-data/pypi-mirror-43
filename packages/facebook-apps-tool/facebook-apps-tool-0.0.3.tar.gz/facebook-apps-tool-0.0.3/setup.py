from setuptools import setup, find_packages

readme = open("README.rst").read()

install_requires = [
    "Click~=7.0",
    "PyYAML~=3.13",
    "facebook-py-sdk~=1.1",
    "six",
    'typing;python_version<"3.5"',
]
tests_require = ["coveralls", "pytest", "pytest-cov"]

setup(
    name="facebook-apps-tool",
    version="0.0.3",
    description="Facebook Apps Tools",
    long_description=readme,
    license="MIT",
    author="Zeta Hernandez",
    author_email="zetahernandez@gmail.com",
    url="https://github.com/zetahernandez/facebook_apps_tool",
    packages=find_packages(),
    install_requires=["facebook-py-sdk", "six", 'typing;python_version<"3.5"'],
    tests_require=tests_require,
    extras_require={"testing": tests_require},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    entry_points="""
        [console_scripts]
        fbtool=fbtool.cli:cli
    """,
)

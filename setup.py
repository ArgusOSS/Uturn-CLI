from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="uturn-cli",
    version="0.0.1",
    author="0x0elliot",
    author_email="adityanrsinha@gmail.com",
    description="CLI utility for Uturn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UturnOSS/Uturn-CLI",
    packages=find_packages(),
    install_requires=["click", "colorama"],
    setup_requires=[],
    include_package_data=True,
    entry_points="""
        [console_scripts]
        uturn-cli=uturn_cli.cli:commands
    """,
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Systems Administration"
    ],
    python_requires=">=3.6",
    license="MIT" # maybe change?
)

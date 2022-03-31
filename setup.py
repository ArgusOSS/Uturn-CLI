from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Uturn",
    version="1.0",
    author="0x0elliot",
    author_email="PLACEHOLDER",
    description="PLACEHOLDER",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Uturn/uturn-cli",
    packages=find_packages(),
    install_requires=["click", "colorama"],
    setup_requires=[],
    include_package_data=True,
    entry_points="""
        [console_scripts]
        uturn-cli=cli:commands
    """,
    classifiers=[
        ""
    ],
    python_requires=">=3.6",
    license="MIT" # maybe change?
)

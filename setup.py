from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()
setup(
    name="dismake",
    version="0.0.4",
    author="Pranoy Majumdar",
    author_email="officialpranoy2@gmail.com",
    description="None",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PranoyMajumdar/dismake",
    project_urls={"Homepage": "https://github.com/PranoyMajumdar/dismake"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.9",
    license="MIT",
    install_requires=[
        "fastapi",
        "pydantic",
        "httpx",
        "uvicorn",
        "PyNaCl",
        "rich",
    ],
)

from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()


setup(
    name="dismake",
    version="0.0.14",
    author="Pranoy Majumdar",
    author_email="officialpranoy2@gmail.com",
    description="None",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Apptic-Development/dismake",
    project_urls={"Homepage": "https://github.com/Apptic-Development/dismake"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.9",
    license="MIT",
    entry_points={"console_scripts": ["dismake=dismake.cli:main"]},
    package_data={"templates": ["templates/*"]},
    install_requires=[
        "fastapi==0.95.1",
        "httpx==0.24.0",
        "pydantic==1.10.7",
        "PyNaCl==1.5.0",
        "rich==13.3.5",
        "typing_extensions==4.5.0",
        "uvicorn==0.22.0",
    ],
)


print("Successfully installed dismake")

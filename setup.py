from setuptools import setup

with open("README.md", "r") as file:
    long_description = file.read()


setup(
    name="dismake",
    version="0.0.23",
    author="Pranoy Majumdar",
    author_email="officialpranoy2@gmail.com",
    description="None",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Apptic-Development/dismake",
    project_urls={"Homepage": "https://github.com/Apptic-Development/dismake"},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    packages=[
        "dismake",
        "dismake.models",
        "dismake.ui",
        "dismake.types",
    ],
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

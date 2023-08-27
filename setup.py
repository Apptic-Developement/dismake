from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

with open("requirements/requirements.txt", "r") as f:
    requirements = f.read().splitlines()
setup(
    name="dismake",
    version="1.0.0a1",
    author="Pranoy Majumdar",
    author_email="officialpranoy2@gmail.com",
    description="🚀 Dismake is a framework for building stateless Discord bots with Slash Commands, built on top of FastAPI.",
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
    packages=find_packages(),
    python_requires=">=3.8",
    license="MIT",
    entry_points={"console_scripts": ["dismake=dismake.cli:main"]},
    install_requires=requirements,
)


print("Successfully installed dismake")

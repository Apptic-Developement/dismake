from setuptools import setup

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()
setup(
    name="dismake",
    version="1.0.0",
    description="Dismake is a powerful Discord HTTP interactions API wrapper designed for Python developers. Whether you're using Flask, Django, or any other Python web framework, Dismake has you covered.",
    author="Pranoy Majumdar <officialpranoy@gmail.com>",
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: AsyncIO",
        "Framework :: aiohttp",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    install_requires=requirements
)
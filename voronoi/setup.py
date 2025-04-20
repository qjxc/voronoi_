from setuptools import setup, find_packages

setup(
    name="voronoi",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "PyQt5>=5.15.0",
    ],
    python_requires=">=3.8",
    author="Your Name",
    author_email="your.email@example.com",
    description="A modular Voronoi diagram visualization tool",
    long_description="A modular Voronoi diagram visualization tool with infinite tiling and smooth interaction",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/voronoi",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
) 
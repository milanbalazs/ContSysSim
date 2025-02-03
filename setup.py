from setuptools import setup, find_packages

setup(
    name="container_simulation",
    version="1.0.0",
    author="Milan Balazs",
    author_email="milanbalazs@example.com",  # TODO: Fix it
    description=(
        "A SimPy-based Containerized environment (Eg.: Docker Swarm) "
        "simulation with VMs and Containers"
    ),
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/milanbalazs/container-simulation",
    packages=find_packages(where="src"),  # Discover packages inside `src`
    package_dir={"": "src"},  # Define src as the package directory
    install_requires=[
        "simpy>=4.1.1",  # Required package for simulation
        "matplotlib>=3.8.2",  # Required for visualizations
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    include_package_data=True,
    # entry_points={
    #     "console_scripts": [
    #         "run_simulation=examples.multi_node:MultiNodeSimulation",
    #     ],
    # },
    keywords="Container Containerized Docker Swarm SimPy Simulation",
)

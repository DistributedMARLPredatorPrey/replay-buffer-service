from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="replay-buffer-service",
    version="1.1.1",
    description="Replay buffer service",
    url="https://distributedmarlpredatorprey.github.io/replay-buffer-service/",
    author="Luca Fabri",
    author_email="luca.fabri1999@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    zip_safe=False,
)

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="replay-buffer-service",
    description="Replay buffer service",
    url="#",
    author="Luca Fabri",
    author_email="luca.fabri1999@gmail.com",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="src.test",
    install_requires=requirements,
    zip_safe=False,
    python_requires="==3.11.6",
    package_data={
        "src.main.service": ["resources/*"],
    },
)

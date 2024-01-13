from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="replay-buffer-service",
    description="Replay buffer service",
    url="#",
    author="Luca Fabri",
    author_email="luca.fabri1999@gmail.com",
    packages=find_packages(),
    # package_dir={"": "src"},
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="src.test",
    install_requires=requirements,
    zip_safe=False,
    python_requires="==3.11.6",
    entry_points={
        "console_scripts": ["replay-buffer=src.main:main"],
    },
    package_data={
        "src.main": ["conf/https/*"],  # adjust the path based on your actual structure
        "src.main.service": ["resources/*"],
    },
)

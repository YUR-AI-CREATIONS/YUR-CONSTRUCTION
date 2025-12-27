from setuptools import setup, find_packages

setup(
    name="bid-zone",
    version="1.0.0",
    description="Construction Estimating and Land Procurement Due Diligence Software",
    author="YUR AI CREATIONS",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        line.strip()
        for line in open("requirements.txt")
        if line.strip() and not line.startswith("#")
    ],
)

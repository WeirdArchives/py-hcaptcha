import setuptools

with open("requirements.txt") as fp:
    requirements = fp.read().splitlines()

setuptools.setup(
    name="py-hcaptcha",
    author="h0nda",
    description="hCaptcha interaction library",
    url="https://github.com/h0nde/py-hcaptcha",
    packages=setuptools.find_packages(),
    classifiers=[],
    install_requires=requirements,
    include_package_data=True
)
from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="discord_i18n",
    author="Clutter Development",
    version="1.0.1",
    license="MIT",
    description="A simple I18N handler for Discord bots.",
    install_requires=requirements,
    python_requires=">=3.10",
    py_modules=["discord_i18n"],
    packages=["discord_i18n"],
)

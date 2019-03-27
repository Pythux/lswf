from setuptools import setup

setup(
    name='lswf',
    version='1.0',
    description='lower ssd write frequency',
    author='Pythux',
    # author_email='',
    packages=['lswf'],  # same as name
    # install_requires=[],  # external packages as dependencies
    # scripts=[
    #     'lswf/app',
    #     ]
)

# install in dev mode (link to the current folder)
# pip install -e .

#? pip uninstall will not delete scripts,
# wich will raise FileNotFound if renamed/deplaced/deleted

from setuptools import setup

setup(
    name='lswf',
    version='1.0',
    description='lower ssd write frequency',
    author='Pythux',
    # author_email='',
    packages=[
        'lswf',
        'lswf.core',
        'lswf.data_access',
        'lswf.lib',
        'lswf.models',
    ],  # same as name
    install_requires=[
        'jsonschema',
        'crud-vanilla @ git+https://github.com/Pythux/py_CRUD_vanilla.git',
        'tools @ git+https://github.com/Pythux/py_tools.git',
        'patcher @ git+https://github.com/Pythux/patcher.git',
    ],  # external packages as dependencies
    # scripts=[
    #     'lswf/app',
    #     ]
    entry_points={
        'console_scripts': [
            'lswf = lswf.__main__:main'
        ]
    },
)

# install in dev mode (link to the current folder)
# pip install -e .

# pip uninstall will not delete scripts,
# wich will raise FileNotFound if renamed/deplaced/deleted

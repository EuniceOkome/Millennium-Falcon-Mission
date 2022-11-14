from setuptools import setup

setup(
    name="give-me-the-odds",
    version='0.1',
    py_modules=['CLI'],
    install_requires=[
        'click', 'numpy', 'pandas', 'pathlib'
    ],
    entry_points='''
        [console_scripts]
        give-me-the-odds=CLI:result
    ''',
)
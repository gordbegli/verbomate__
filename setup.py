from setuptools import setup, find_packages

setup(
    name='verbomate',  # Replace with your chosen package name
    version='0.1.6',  # Initial version number
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'verbomate=verbomate.main:main',
        ],
    },
    # Additional metadata like author, description, license, classifiers, etc.
    author='Gabriel Gordbegli',
    author_email='gabe@gordbegli.com',
    description='Generate and run python scripts from your command line',
    license='MIT',  # Choose the appropriate license
    url='https://github.com/gordbegli/verbomate',  # Optional: Link to your project's repository
    install_requires=[
        'requests',  
        'openai', 
        'argparse',
    ],
)


from setuptools import setup, find_packages

setup(
    name='verbomate',  # Replace with your chosen package name
    version='0.1.0',  # Initial version number
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'verbomate=verbomate.main:main',
        ],
    },
    # Additional metadata like author, description, license, classifiers, etc.
    author='Your Name',
    author_email='your.email@example.com',
    description='A utility to fetch and execute a script from an API',
    license='MIT',  # Choose the appropriate license
    #url='https://github.com/yourusername/myutility',  # Optional: Link to your project's repository
    install_requires=[
        'requests',  # List any other dependencies your package needs here
        'openai', # OpenAI API
    ],
)


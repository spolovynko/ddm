from setuptools import setup, find_packages

setup(
    name='greet',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['python-dotenv'],
    entry_points={
        'console_scripts': [
            'greet=greet.main:main',
            'greet-setup=greet.post_install:configure_env_path'  # Install `greet-setup` command
        ],
    },
)

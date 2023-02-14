from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = 'Planet CLI tool to adquire and download \
      imagery using DATA API and ORDER API.'

setup(
        name='Planet CLI tool',
        version='0.0.2',
        author='Jorge Herrera',
        author_email='herreram.jahm@gmail.com',
        url='',
        description='Planet CLI tool.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        license='MIT',
        packages=find_packages(),
        entry_points={
            'console_scripts': [
                'planet_cli = planet_cli_tool.main:main'
            ]
        },
        classifiers=(
            "Programming Language :: Python :: 3",
            "License :: MIT License",
            "Operating System :: OS Independent",
        ),
        keywords='planet COG order data api',
        install_requires=requirements,
        zip_safe=False
)

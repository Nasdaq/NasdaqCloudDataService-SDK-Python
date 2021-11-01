from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get long description from README
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='ncdssdk',
    version='0.2.0',
    description='A Python SDK for developing applications to access the NCDS API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nasdaq',
    classifiers=[
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3.9',
    ],
    keywords='Nasdaq, NCDS, ncdssdk',
    packages=find_packages(),
    python_requires='>=3.9, <4',
    install_requires=open("requirements.in").readlines(),

    include_package_data=True,
    # We could possibly use entry_points parameter with console_scripts here to specify the NCDSSession script

    project_urls={  # Optional
        'Source': 'https://github.com/Nasdaq/NasdaqCloudDataService-SDK-Python',
    },
)
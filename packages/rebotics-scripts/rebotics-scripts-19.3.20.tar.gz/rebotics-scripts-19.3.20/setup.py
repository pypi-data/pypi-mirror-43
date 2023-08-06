"""
Collection of scripts for rebotics
"""
from setuptools import find_packages, setup

__VERSION__ = '19.3.20'

requirements = [
    'click',
    'fake_useragent',
    'ffmpeg-python',
    'numpy',
    'ratelimit',
    'requests',
    'requests[socks]',
    'PySocks',
    'tqdm',
    'xlrd',
    'pandas',
    'six',
]


setup(
    name='rebotics-scripts',
    version=__VERSION__,
    url='http://retechlabs.com/',
    license='BSD',
    author='Malik Sulaimanov',
    author_email='malik@retechlabs.com',
    description='Collection of scripts for rebotics',
    long_description=__doc__,
    packages=[
        'sdk',
        'scripts',
    ],
    package_dir={
        '': '.',
        'sdk': 'sdk',
    },
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'rebotics = scripts.cli:main',
            'api = scripts.api_v4_client:api',
            'retailer = scripts.api_v4_client:api',
            'dataset-api = scripts.dataset_api_client:api',
            'dataset = scripts.dataset_api_client:api',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        # 'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

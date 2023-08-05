import setuptools

setuptools.setup(
    name='libknot',
    version='2.8.0',
    description='Python bindings for libknot',
    author='Daniel Salzman',
    author_email='daniel.salzman@nic.cz',
    url='https://gitlab.labs.nic.cz/knot/knot-dns',
    license='GPL-3.0',
    packages=['libknot'],
    classifiers=[ # See https://pypi.org/classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: Name Service (DNS)',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Systems Administration',
    ]
)

from setuptools import setup

setup(
    name="mbootstrap",
    version="0.0.1",
    scripts=['scripts/mbootstrap.py'],
    install_requires=['gitpython', 'pyyaml'],
    entry_points={
        'console_scripts': ['mbootstrap=mbootstrap:main'],
    },
    author="Markus Hutzler",
    description="Mini Bootstrap Script",
    license="bsd-3-clause",
    keywords="bootstrap git",
    url="https://gitlab.com/mbootstrap/mbootstrap",
    project_urls={
        "Bug Tracker": "https://gitlab.com/mbootstrap/mbootstrap/issues",
        "Documentation": "https://gitlab.com/mbootstrap/mbootstrap/",
        "Source Code": "https://gitlab.com/mbootstrap/mbootstrap/",
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)

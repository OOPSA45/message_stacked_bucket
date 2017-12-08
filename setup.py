from setuptools import setup, find_packages

setup(
    name="message stacked bucket",
    version='0.1.2',
    description='Messenger client + server with lots of bugs',
    url='https://github.com/EnricoChi/message_stacked_bucket',
    author="MuromatiO",
    author_email="enricoseo@gmail.com",
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'SQLAlchemy',
        'pillow',
        'PyQt5'
    ],
    python_requires=">=3",
    packages=[
        'message stacked bucket',
        'message stacked bucket/a_client',
        'message stacked bucket/a_client/db',
        'message stacked bucket/b_server',
        'message stacked bucket/b_server/db',
        'message stacked bucket/c_gui',
        'message stacked bucket/d_jim',
        'message stacked bucket/e_temeplate_func',
        'message stacked bucket/log',
        'message stacked bucket/tests',
    ],
    package_data={
        "message stacked bucket/a_client/db": ["max.db", "sax.db", "aax.db"],
        "message stacked bucket/b_server/db": ["server.db"],
        "message stacked bucket/c_gui": ["MymessForm.ui"],
    }
)

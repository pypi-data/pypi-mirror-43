import setuptools
from face_api import __version__, __author__, __email__

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'numpy',
    'Pillow',
    'grpcio',
    'tensorflow',
    'tensorflow-serving-api',
    'dlib',
    'click'
]

setuptools.setup(
    name="face_api",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="Package for Face API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.ai.game.tw",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    data_files=[('bitmap', ['imgs/coco1.png', 'imgs/coco7.png', 'imgs/nocole1.png', 'imgs/nocole7.png'])],
    entry_points={
        'console_scripts': [
            'ex_img2fes=face_api.ex_img2fes:main',
            'ex_imgs2conf_matrix=face_api.ex_imgs2conf_matrix:main',
        ]
    },    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

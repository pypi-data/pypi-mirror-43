"""
Copyright 2019 Archie Shahidullah

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='gliaml',
      version='0.1.0',
      description='GliaML - Python Machine Learning Library',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      keywords='machine learning neural networks',
      url='https://github.com/Archiecool4/GliaML',
      download_url='https://github.com/Archiecool4/GliaML',
      author='Archie Shahidullah',
      author_email='archie@caltech.edu',
      license='http://www.apache.org/licenses/LICENSE-2.0',
      packages=['gliaml'],
      install_requires=['numpy'],
      include_package_data=True,
      zip_safe=False)

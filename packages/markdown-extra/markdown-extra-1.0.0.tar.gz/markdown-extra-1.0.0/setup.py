import os

from setuptools import setup

project_dir = os.path.dirname(os.path.abspath(__file__))


setup(
    name='markdown-extra',
    version='1.0.0',
    description='Set of extensions for markdown',
    long_description=open(os.path.join(project_dir, 'README.rst')).read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/Nicals/markdown-meta',
    author='Nicolas Appriou',
    author_email='nicolas.appriou@gmail.com',
    license='MIT',
    packages=['markdown_extra'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    keywords='markdown yaml',
    install_requires=[
        'markdown',
        'pyYAML',
    ],
    extras_require={
        'tests': ['mock;python_version<"3.3"', 'pytest'],
        'docs': ['sphinx'],
    },
)

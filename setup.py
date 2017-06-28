from setuptools import setup, find_packages

with open('requirements.txt', mode='r') as requirements:
    install_requires = [line.strip() for line in requirements]

setup(
    name='Flask Blagging',
    description='A simple Flask based blogging engine',
    version='0.1.0',
    author='Drew Bednar',
    author_email='drew@androiddrew.com',
    url='https://github.com/androiddrew/blag-fork',
    license='MIT',
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'blog_manager=manage:manager.run'
        ],
    }
)

import setuptools

with open('README.md', 'r') as fh:
	long_description = fh.read()

setuptools.setup(
	name='food',
	version='0.0.4',
	author='mat',
	author_email='fake@email.lol',
	description='yum',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://repl.it/@mat1',
	packages=setuptools.find_packages(),
	install_requires='',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
)
import setuptools

with open('README.md', 'r') as fh:
	long_description = fh.read()

setuptools.setup(
	name='repltalk',
	version='0.4.16',
	author='mat',
	author_email='mat@matdoes.dev',
	description='Uses the Repl Talk api to do stuff. info below',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://www.matdoes.dev',
	packages=setuptools.find_packages(),
	install_requires='aiohttp',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
)
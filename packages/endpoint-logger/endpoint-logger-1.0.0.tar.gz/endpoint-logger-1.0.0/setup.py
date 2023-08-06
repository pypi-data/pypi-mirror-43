from setuptools import setup


def readme():
	with open("readme.md") as f:
		return f.read()


setup(
	name = "endpoint-logger",
	version = "1.0.0",
	description = "A Python package used to track Flask API endpoint access. (Built in Python 3)",
	url = "https://github.com/M69k65y/endpoint-logger",
	author = "M69k65y",
	license = "MIT",
	packages = ["endpoint_logger"],
	zip_safe=False,
	install_requires = [
		"flask"
	],
	classifiers = [
		"Development Status :: 3 - Alpha",
		"Framework :: Flask",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3"
	],
	keywords = "flask endpoint logger logging",
	long_description = readme(),
	long_description_content_type = "text/markdown"
)
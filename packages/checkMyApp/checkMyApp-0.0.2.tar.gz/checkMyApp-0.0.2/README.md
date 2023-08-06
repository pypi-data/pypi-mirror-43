# checkMyApp
python tool to check project structure and setup file

# Building (wheel)
python setup.py sdist bdist_wheel

# Usage
Got to the folder where setup.py resides and run: "checkMyApp"

# Example
(root@machine)# checkMyApp

CheckMyApp report for python packaging
Legend:	Warning		Error		OK

Please note:
This tools uses python's 'exec' function in order to parse setup.py
This can be dangerous if you'r not familiar with the code inside setup.py.

Please approve the usage of the tool by typing 'yes' (or CTRL+c to cancel): yes
*	packages are not declared with 'find_packages()'
*	Couldn't load the following requirements:
 ['absl-py==0.2.1', 'alabaster==0.7.9', 'anaconda-client==1.6.0', 'anaconda-navigator==1.5', 'anaconda-project==0.4.1', 'argcomplete==1.0.0', 'astor==0.6.2', 'astroid==1.4.9', 'astropy==1.3', 'Babel==2.3.4', 'backports-abc==0.5', 'backports.shutil-get-terminal-size==1.0.0', 'beautifulsoup4==4.5.3', 'bitarray==0.8.1', 'blaze==0.10.1', 'bleach==1.5.0', 'bokeh==0.12.4', 'boto==2.45.0', 'Bottleneck==1.2.0', 'cffi==1.9.1', 'chardet==2.3.0', 'chest==0.2.3', 'click==6.7', 'cloudpickle==0.2.2', 'clyent==1.2.2', 'colorama==0.3.7', 'configobj==5.0.6', 'contextlib2==0.5.4', 'cryptography==1.7.1', 'cycler==0.10.0', 'Cython==0.25.2', 'cytoolz==0.8.2', 'dask==0.13.0', 'datashape==0.5.4', 'decorator==4.0.11', 'dill==0.2.5', 'docutils==0.13.1', 'et-xmlfile==1.0.1', 'fastcache==1.0.2', 'Flask==0.12', 'Flask-Cors==3.0.2', 'future==0.17.1', 'gast==0.2.0', 'gevent==1.2.1', 'greenlet==0.4.11', 'grpcio==1.12.0', 'h5py==2.6.0', 'HeapDict==1.0.0', 'html5lib==0.9999999', 'idna==2.2', 'imagesize==0.7.1', 'ipykernel==4.5.2', 'ipython==5.1.0', 'ipython-genutils==0.1.0', 'ipywidgets==5.2.2', 'isort==4.2.5', 'itsdangerous==0.24', 'jdcal==1.3', 'jedi==0.9.0', 'Jinja2==2.9.4', 'jsonschema==2.5.1', 'jupyter==1.0.0', 'jupyter-client==4.4.0', 'jupyter-console==5.0.0', 'jupyter-core==4.2.1', 'Keras==2.1.6', 'keras-tqdm==2.0.1', 'lazy-object-proxy==1.2.2', 'llvmlite==0.15.0', 'locket==0.2.0', 'lxml==3.7.2', 'Markdown==2.6.11', 'MarkupSafe==0.23', 'matplotlib==2.0.0', 'mistune==0.7.3', 'mpmath==0.19', 'multipledispatch==0.4.9', 'murmurhash3==2.3.5', 'nbconvert==4.2.0', 'nbformat==4.2.0', 'networkx==1.11', 'nltk==3.2.2', 'nose==1.3.7', 'notebook==4.3.1', 'numba==0.30.1', 'numexpr==2.6.1', 'numpy==1.14.3', 'numpydoc==0.6.0', 'odo==0.5.0', 'openpyxl==2.4.1', 'pandas==0.20.2', 'partd==0.3.7', 'pathlib2==2.2.0', 'patsy==0.4.1', 'pep8==1.7.0', 'pexpect==4.2.1', 'pickleshare==0.7.4', 'Pillow==4.0.0', 'ply==3.9', 'prompt-toolkit==1.0.9', 'protobuf==3.5.2.post1', 'psutil==5.0.1', 'ptyprocess==0.5.1', 'py==1.4.32', 'pyasn1==0.1.9', 'pycosat==0.6.1', 'pycparser==2.17', 'pycrypto==2.6.1', 'pycurl==7.43.0', 'pyflakes==1.5.0', 'Pygments==2.1.3', 'pylint==1.6.4', 'pyOpenSSL==16.2.0', 'pyparsing==2.1.4', 'pytest==3.0.5', 'python-dateutil==2.6.0', 'pytz==2016.10', 'PyYAML==3.12', 'pyzmq==16.0.2', 'QtAwesome==0.4.3', 'qtconsole==4.2.1', 'QtPy==1.2.1', 'redis==2.10.5', 'requests==2.12.4', 'rope-py3k==0.9.4.post1', 'scandir==1.4', 'scikit-image==0.12.3', 'scikit-learn==0.18.1', 'scipy==0.18.1', 'seaborn==0.7.1', 'simplegeneric==0.8.1', 'singledispatch==3.4.0.3', 'six==1.10.0', 'snowballstemmer==1.2.1', 'sockjs-tornado==1.0.3', 'Sphinx==1.5.1', 'spyder==3.1.2', 'SQLAlchemy==1.1.5', 'statsmodels==0.6.1', 'sympy==1.0', 'tables==3.3.0', 'tensorboard==1.8.0', 'tensorflow==1.8.0', 'termcolor==1.1.0', 'terminado==0.6', 'toolz==0.8.2', 'tornado==4.4.2', 'tqdm==4.23.3', 'traitlets==4.3.1', 'unicodecsv==0.14.1', 'vertica-python==0.8.0', 'wcwidth==0.1.7', 'Werkzeug==0.11.15', 'widgetsnbextension==1.2.6', 'wrapt==1.10.8', 'xlrd==1.0.0', 'XlsxWriter==0.9.6', 'xlwt==1.2.0']

(This means that the modules doesn't exists in the machine you'r running the script on it doesn't necessary means that the package won't after packaging.

*	The following module(s) seems to be required under 'install_requires' but not in use in the code:
	set(['six', 'cloudpickle', 'Flask', 'cffi', 'ipython-genutils', 'absl-py', 'networkx', 'numexpr', 'tables', 'wrapt', 'Keras', 'termcolor', 'Jinja2', 'blaze', 'sympy', 'itsdangerous', 'xlwt', 'pathlib2', 'openpyxl', 'backports.shutil-get-terminal-size', 'alabaster', 'MarkupSafe', 'scipy', 'bleach', 'Pillow', 'decorator', 'contextlib2', 'jupyter-client', 'pyOpenSSL', 'scikit-learn', 'psutil', 'mpmath', 'greenlet', 'nose', 'h5py', 'cycler', 'QtAwesome', 'Werkzeug', 'anaconda-client', 'gevent', 'jsonschema', 'odo', 'bitarray', 'xlrd', 'click', 'multipledispatch', 'seaborn', 'murmurhash3', 'redis', 'ptyprocess', 'docutils', 'jedi', 'Pygments', 'qtconsole', 'chardet', 'cytoolz', 'matplotlib', 'ply', 'ipython', 'pickleshare', 'mistune', 'nbformat', 'boto', 'numpydoc', 'spyder', 'pyparsing', 'astropy', 'terminado', 'requests', 'llvmlite', 'pyasn1', 'lazy-object-proxy', 'HeapDict', 'dill', 'snowballstemmer', 'pycparser', 'toolz', 'tensorboard', 'jupyter-console', 'prompt-toolkit', 'astor', 'pexpect', 'backports-abc', 'bokeh', 'Flask-Cors', 'isort', 'pyzmq', 'SQLAlchemy', 'Sphinx', 'imagesize', 'widgetsnbextension', 'et-xmlfile', 'pylint', 'pytz', 'jupyter-core', 'tensorflow', 'python-dateutil', 'jdcal', 'Markdown', 'pycurl', 'keras-tqdm', 'QtPy', 'future', 'locket', 'statsmodels', 'sockjs-tornado', 'configobj', 'Cython', 'ipykernel', 'Babel', 'argcomplete', 'grpcio', 'wcwidth', 'numba', 'dask', 'singledispatch', 'lxml', 'partd', 'cryptography', 'rope-py3k', 'fastcache', 'patsy', 'html5lib', 'chest', 'pytest', 'nbconvert', 'Bottleneck', 'XlsxWriter', 'PyYAML', 'clyent', 'protobuf', 'datashape', 'tornado', 'scikit-image', 'ipywidgets', 'anaconda-navigator', 'notebook', 'colorama', 'traitlets', 'beautifulsoup4', 'gast', 'astroid', 'jupyter', 'pycrypto', 'pyflakes', 'simplegeneric', 'pycosat', 'vertica-python', 'pep8', 'unicodecsv', 'anaconda-project', 'idna', 'nltk', 'scandir'])
*	Alternatively, you can replace you required module list with the following:
	['tqdm==4.23.3', 'numpy==1.14.3', 'py==1.4.32', 'pandas==0.20.2']

# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['opensoundscape']

package_data = \
{'': ['*'],
 'opensoundscape': ['config/*',
                    'init/*',
                    'model_fit/*',
                    'model_fit/model_fit_algo/template_matching/*',
                    'predict/*',
                    'predict/predict_algo/template_matching/*',
                    'scripts/*',
                    'spect_gen/*',
                    'spect_gen/spect_gen_algo/template_matching/*',
                    'utils/*',
                    'view/*']}

install_requires = \
['docopt==0.6.2',
 'librosa==0.6.2',
 'llvmlite==0.27.0',
 'matplotlib==3.0.2',
 'numba==0.42.0',
 'numpy==1.15.4',
 'opencv-python-headless==4.0.0.21',
 'pandas==0.23.4',
 'pymongo==3.7.2',
 'pyqt5>=5.12,<6.0',
 'scikit-image==0.14.1',
 'scipy==1.2.0',
 'toolz>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['opensoundscape = opensoundscape.console:run',
                     'opso_dump_cross_corrs = '
                     'opensoundscape.scripts.dump_cross_correlations:run',
                     'opso_find_high_cross_corrs = '
                     'opensoundscape.scripts.find_high_cross_correlations:run',
                     'opso_find_important_templates = '
                     'opensoundscape.scripts.find_important_templates:run',
                     'opso_generate_images = '
                     'opensoundscape.scripts.generate_images:run',
                     'opso_raven_selections_to_template_db = '
                     'opensoundscape.scripts.raven_selections_to_template_db:run']}

setup_kwargs = {
    'name': 'opensoundscape',
    'version': '0.3.0.1',
    'description': 'Open source, scalable acoustic classification for ecology and conservation',
    'long_description': "Opensoundscape\n---\n\n### Installation\n\nWe recommend you run Opensoundscape into a Python 3.7 virtual environment. If\nyou don't already have Python installed you can use [the Anaconda\ndistribution](https://www.anaconda.com/distribution/#download-section). Simply\nselect your platform (Windows, macOS, or Linux) and download a Python 3.7\n64-bit installer. You will also need to run a MongoDB server which is used to\nstore data for Opensoundscape. The documentation for this process is available\n[here](https://docs.mongodb.com/manual/installation/#mongodb-community-edition).\nThe documentation also explains how to start the service on various platforms.\n\nNow, you can get Opensoundscape via\n[PyPI](https://pypi.org/project/opensoundscape/0.3.0.1).  I will show the\n`conda` commands below, but we use `virtualenvwrapper` internally.\n\n1. Create the environment and install Opensoundscape: `conda create --name\n   opensoundscape python=3.7 opensoundscape=0.3.0.1`\n2. Activate the environment: `conda activate opensoundscape`\n3. Check if everything worked: `opensoundscape -h`\n4. Deactivate the environment when finished: `conda deactivate`\n\n### Singularity Container\n\nCurrently, Singularity is only working on Linux. The developers recently showed\na development version which works on\n[macOS](https://www.linkedin.com/feed/update/urn:li:activity:6505987087735623680/).\nYou can pull our container from\n[here](https://cloud.sylabs.io/library/_container/5c7d4c0f5cf3490001ca7987).\n\n1. Get the container: `singularity pull\n   library://barrymoo/default/opensoundscape:0.3.0.1`\n2. Check if Opensoundscape can run: `singularity run --app opensoundscape\n   opensoundscape_0.3.0.1.sif -h`\n3. Check if MongoDB can run: `singularity run --app mongodb\n   opensoundscape_0.3.0.1.sif -h`\n\n### Quick Start Guide\n\nGoing to run through a quick example of running Opensoundscape. First, we need\nsome data\n\n- The [CLO-43SD-AUDIO](https://datadryad.org/resource/doi:10.5061/dryad.j2t92)\n  dataset:\n\n```\ncd ~/Downloads\nwget https://datadryad.org/bitstream/handle/10255/dryad.111783/CLO-43SD-AUDIO.tar.gz\ntar -xzf CLO-43SD-AUDIO.tar.gz\nrm CLO-43SD-AUDIO.tar.gz\n```\n\n- Download our training & prediction split of a subset of the CLO-43SD dataset:\n\n```\ncd ~/Downloads/CLO-43SD-AUDIO/\nwget https://raw.github.com/rhine3/opso-support/master/clo-43sd-train-small.csv\nwget https://raw.github.com/rhine3/opso-support/master/clo-43sd-predict-small.csv\n```\n\n- Make a new directory to run Opensoundscape in, using `~/clo-43sd` below\n\n```\ncd ~/clo-43sd\nwget https://raw.github.com/rhine3/opso-support/master/opso-test-small.ini\n```\n\n- Edit the `.ini` to reflect the absolute path of your `Downloads` folder, e.g.\n  with `vim`: `vim opso-test-small.ini`\n- Start the MongoDB daemon in another terminal: `mongod --config\n  /usr/local/etc/mongod.conf`\n- Run Opensoundscape:\n\n```\nopensoundscape init -i opso-test-small.ini\nopensoundscape spect_gen -i opso-test-small.ini > spect-gen-output-small.txt\nopensoundscape model_fit -i opso-test-small.ini > model-fit-output-small.txt\nopensoundscape predict -i opso-test-small.ini > predict-output-small.txt\n```\n\n### Contributions\n\nContributions are highly encouraged! Our development workflow is a combination\nof `virtualenvwrapper` and `poetry`. \n\n- Get [poetry](https://poetry.eustace.io/docs/#installation)\n- Get\n  [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html)\n- Link `poetry` and `virtualenvwrapper`, add something like the following to\n  your `~/.bashrc` (don't forget to source it!)\n\n```\n# virtualenvwrapper + poetry\nexport WORKON_HOME=~/.cache/pypoetry/virtualenvs\nsource /usr/bin/virtualenvwrapper_lazy.sh\n```\n\n- Fork the github repository, and clone it\n    - We use `black` pre-commit hooks for formatting\n- Build the virtual environment for opensoundscape: `poetry install`\n- Activate your opensoundscape environment: `workon opensoundscape-py3.7`\n- Check Opensoundscape runs: `opensoundscape -h`\n- To go back to your system's Python: `deactivate`\n- Running the tests: `poetry run pytest tests`\n",
    'author': 'Justin Kitzes',
    'author_email': 'justin.kitzes@pitt.edu',
    'url': 'https://github.com/jkitzes/opensoundscape',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

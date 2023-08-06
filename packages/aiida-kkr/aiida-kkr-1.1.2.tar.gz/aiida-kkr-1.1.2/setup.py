# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiida_kkr',
 'aiida_kkr.calculations',
 'aiida_kkr.data',
 'aiida_kkr.parsers',
 'aiida_kkr.tests',
 'aiida_kkr.tools',
 'aiida_kkr.workflows']

package_data = \
{'': ['*'],
 'aiida_kkr': ['cmdline/*'],
 'aiida_kkr.tests': ['files/*',
                     'files/interpol/*',
                     'files/kkr/import_calc_old_style/*',
                     'files/kkr/kkr_run_dos_output/*',
                     'files/kkr/kkr_run_slab_nosoc/*',
                     'files/kkr/kkr_run_slab_soc_mag/*',
                     'files/kkr/kkr_run_slab_soc_simple/*',
                     'files/kkr/outputfiles/*',
                     'files/kkr/parse_Nan_result/*',
                     'files/kkr/parser_3Dsymmetries/*',
                     'files/kkrimp_parser/test1/*',
                     'files/mod_pot/test1/*',
                     'files/mod_pot/test2/*',
                     'files/voronoi/*']}

install_requires = \
['aiida-core==1.0.0a4',
 'ase',
 'bumpversion',
 'masci-tools',
 'pgtest',
 'pytest-cov>=2.5.0,<3.0.0',
 'seekpath',
 'sphinx',
 'sphinx_rtd_theme']

setup_kwargs = {
    'name': 'aiida-kkr',
    'version': '1.1.2',
    'description': 'AiiDA plugin for the KKR code',
    'long_description': "[![Documentation Status](https://readthedocs.org/projects/aiida-kkr/badge/?version=latest)](https://aiida-kkr.readthedocs.io/en/latest/?badge=latest)\n[![Build Status](https://travis-ci.org/JuDFTteam/aiida-kkr.svg?branch=master)](https://travis-ci.org/JuDFTteam/aiida-kkr)\n[![codecov](https://codecov.io/gh/JuDFTteam/aiida-kkr/branch/master/graph/badge.svg)](https://codecov.io/gh/JuDFTteam/aiida-kkr)\n[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)\n[![GitHub version](https://badge.fury.io/gh/JuDFTteam%2Faiida-kkr.svg)](https://badge.fury.io/gh/JuDFTteam%2Faiida-kkr)\n[![PyPI version](https://badge.fury.io/py/aiida-kkr.svg)](https://badge.fury.io/py/aiida-kkr)\n\n\n# aiida-kkr\n\nAiiDA plugin for the KKR codes plus workflows and utility.\n\n## Features\n\n* KKR calculations for bulk and interfaces\n* treatment of alloys using VCA or CPA\n* self-consistency, DOS and bandstructure calculations\n* extraction of magnetic exchange coupling parameters (*J_ij*, *D_ij*)\n* impurity embedding solving the Dyson equation\n* ~~import old calculations using the calculation importer~~ (only working with aiida-core<1.0, i.e. in aiida-kkr v0.1.2)\n\n\n# Installation\n\n```shell\n$ git clone https://github.com/JuDFTteam/aiida-kkr\n\n$ cd aiida-kkr\n$ pip install -e .  # also installs aiida, if missing (but not postgres)\n$ reentry scan -r aiida  \n$ verdi quicksetup  # better to set up a new profile\n$ verdi calculation plugins  # should now show kkr.* entrypoints\n```\n\n# Usage and Documentation\n\nSee http://aiida-kkr.readthedocs.io for user's guide and API reference.\n\n# Contribting guide\n\n* \n",
    'author': 'Philipp R\xc3\xbcssmann',
    'author_email': 'p.ruessmann@fz-juelich.de',
    'url': 'https://github.com/JuDFTteam/aiida-kkr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)

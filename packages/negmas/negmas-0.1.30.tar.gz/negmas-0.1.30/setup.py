# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['negmas',
 'negmas.apps',
 'negmas.apps.scml',
 'negmas.external',
 'negmas.scripts',
 'negmas.tests']

package_data = \
{'': ['*'],
 'negmas': ['logs/*'],
 'negmas.tests': ['config/*',
                  'data/10issues/*',
                  'data/AMPOvsCity/*',
                  'data/Laptop/*',
                  'data/Laptop1Issue/*',
                  'data/LaptopConv/*',
                  'data/LaptopConv1D/*',
                  'data/fuzzyagent/*',
                  'data/scenarios/anac/y2010/EnglandZimbabwe/*',
                  'data/scenarios/anac/y2010/ItexvsCypress/*',
                  'data/scenarios/anac/y2010/Travel/*',
                  'data/scenarios/other/S-1NIKFRT-1/*',
                  'scml/*']}

install_requires = \
['Click>=6.0',
 'PyYAML==5.1b1',
 'colorlog>=4.0,<5.0',
 'hypothesis>=4.9,<5.0',
 'inflect>=2.1,<3.0',
 'matplotlib>=3.0,<4.0',
 'numpy>=1.16,<2.0',
 'pandas>=0.24.1,<0.25.0',
 'progressbar2>=3.39,<4.0',
 'py4j>=0.10.8,<0.11.0',
 'pytest-cov>=2.6,<3.0',
 'pytest-runner>=4.4,<5.0',
 'scipy>=1.2,<2.0',
 'setuptools>=40.8,<41.0',
 'stringcase>=1.2,<2.0',
 'tabulate>=0.8.3,<0.9.0',
 'typing>=3.6,<4.0',
 'typing_extensions>=3.7,<4.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses'], 'dask': ['distributed']}

entry_points = \
{'console_scripts': ['negmas = scripts.negmas:cli']}

setup_kwargs = {
    'name': 'negmas',
    'version': '0.1.30',
    'description': 'NEGotiations Managed by Agent Simulations',
    'long_description': "NegMAS\n******\n\n\n.. .. image:: https://img.shields.io/pypi/v/negmas/svg\n..         :target: https://pypi.python.org/pypi/negmas\n\n.. .. image:: https://img.shields.io/travis/yasserfarouk/negmas/svg\n..         :target: https://travis-ci.org/yasserfarouk/negmas\n\n.. .. image:: https://readthedocs.org/projects/negmas/badge/?version=latest\n..         :target: https://negmas/readthedocs.io/en/latest/?badge=latest\n..         :alt: Documentation Status\n\n\n\nA python library for managing autonomous negotiation agents in simulation environments. The name ``negmas`` stands for\neither NEGotiation MultiAgent System or NEGotiations Managed by Agent Simulations (your pick).\n\nIntroduction\n============\n\nThis package was designed to help advance the state-of-art in negotiation research by providing an easy-to-use yet\npowerful platform for autonomous negotiation targeting situated simultaneous negotiations.\nIt grew out of the NEC-AIST collaborative laboratory project.\n\nBy *situated* negotiations, we mean those for which utility functions are not pre-ordained by fiat but are a natural\nresult of a simulated business-like process.\n\nBy *simultaneous* negotiations, we mean sessions of dependent negotiations for which the utility value of an agreement\nof one session is affected by what happens in other sessions.\n\nThe documentation is available at: documentation_\n\n.. _documentation: http://www.yasserm.com/negmas/index.html\n\nMain Features\n=============\n\nThis platform was designed with both flexibility and scalability in mind. The key features of the NegMAS package are:\n\n#. The public API is decoupled from internal details allowing for scalable implementations of the same interaction\n   protocols.\n#. Supports agents engaging in multiple concurrent negotiations.\n#. Provides support for inter-negotiation synchronization either through coupled utility functions or through central\n   *control* agents.\n#. The package provides sample negotiators that can be used as templates for more complex negotiators.\n#. The package supports both mediated and unmediated negotiations.\n#. Supports both bilateral and multilateral negotiations.\n#. Novel negotiation protocols and simulated *worlds* can be added to the package as easily as adding novel negotiators.\n#. Allows for non-traditional negotiation scenarios including dynamic entry/exit from the negotiation.\n#. A large variety of built in utility functions.\n#. Utility functions can be active dynamic entities which allows the system to model a much wider range of dynamic ufuns\n   compared with existing packages.\n#. A distributed system with the same interface and industrial-strength implementation is being created allowing agents\n   developed for NegMAS to be seemingly employed in real-world business operations.\n\nTo use negmas in a project\n\n.. code-block:: python\n\n    import negmas\n\nThe package was designed for many uses cases. On one extreme, it can be used by an end user who is interested in running\none of the built-in negotiation protocols. On the other extreme, it can be used to develop novel kinds of negotiation\nagents, negotiation protocols, multi-agent simulations (usually involving situated negotiations), etc.\n\nRunning existing negotiators/negotiation protocols\n==================================================\n\nUsing the package for negotiation can be as simple as the following code snippet:\n\n.. code-block:: python\n\n    from negmas import SAOMechanism, AspirationNegotiator, MappingUtilityFunction\n    session = SAOMechanism(outcomes=10, n_steps=100)\n    negotiators = [AspirationNegotiator(name=f'a{_}') for _ in range(5)]\n    for negotiator in negotiators:\n        session.add(negotiator, ufun=MappingUtilityFunction(lambda x: random.random() * x[0]))\n\n    session.run()\n\nIn this snippet, we created a mechanism session with an outcome-space of *10* discrete outcomes that would run for *10*\nsteps. Five agents with random utility functions are then created and *added* to the session. Finally the session is\n*run* to completion. The agreement (if any) can then be accessed through the *state* member of the session. The library\nprovides several analytic and visualization tools to inspect negotiations. See the first tutorial on\n*Running a Negotiation* for more details.\n\nDeveloping a negotiator\n=======================\n\nDeveloping a novel negotiator slightly more difficult by is still doable in few lines of code:\n\n.. code-block:: python\n\n    from negmas.negotiators import Negotiator\n    class MyAwsomeNegotiator(Negotiator):\n        def __init__(self):\n            # initialize the parents\n            Negotiator.__init__(self)\n            MultiNegotiationsMixin.__init__(self)\n\n        def respond_(self, offer, state):\n            # decide what to do when receiving an offer @ that negotiation\n            pass\n\n        def propose_(self, state):\n            # proposed the required number of proposals (or less) @ that negotiation\n            pass\n\nBy just implementing `respond_()` and `propose_()`. This negotiator is now capable of engaging in alternating offers\nnegotiations. See the documentation of `Negotiator` for a full description of available functionality out of the box.\n\nDeveloping a negotiation protocol\n=================================\n\nDeveloping a novel negotiation protocol is actually even simpler:\n\n.. code-block:: python\n\n    from negmas.mechanisms import Mechanism\n\n    class MyNovelProtocol(Mechanism):\n        def __init__(self):\n            super().__init__()\n\n        def step_(self):\n            # one step of the protocol\n            pass\n\nBy implementing the single `step_()` function, a new protocol is created. New negotiators can be added to the\nnegotiation using `add()` and removed using `remove()`. See the documentation for a full description of\n`Mechanism` available functionality out of the box [Alternatively you can use `Protocol` instead of `Mechanism`].\n\n\nRunning a world simulation\n==========================\n\nThe *raison d'être* for NegMAS is to allow you to develop negotiation agents capable of behaving in realistic\n*business like* simulated environments. These simulations are called *worlds* in NegMAS. Agents interact with each other\nwithin these simulated environments trying their maximize some intrinsic utility function of the agent through several\n*possibly simultaneous* negotiations.\n\nThe `situated` module provides all that you need to create such worlds. An example can be found in the `scml` package.\nThis package implements a supply chain management system in which factory managers compete to maximize their profits in\na market with only negotiations as the means of securing contracts.\n\n\nAcknowledgement\n===============\n\n.. _Genius: http://ii.tudelft.nl/genius\n\nNegMAS tests use scenarios used in ANAC 2010 to ANAC 2018 competitions obtained from the Genius_ Platform. These domains\ncan be found in the tests/data and notebooks/data folders.\n",
    'author': 'Yasser Mohammad',
    'author_email': 'yasserfarouk@gmail.com',
    'url': 'https://github.com/yasserfarouk/negmas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

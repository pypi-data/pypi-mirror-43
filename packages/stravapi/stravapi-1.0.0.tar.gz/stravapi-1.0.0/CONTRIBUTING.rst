============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Submit Feedback
~~~~~~~~~~~~~~~

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.


Development Workflow
====================

The workflow supports the following steps

 * lint
 * test
 * build
 * document
 * upload
 * graph

These actions are supported out of the box by the corresponding scripts under _CI/scripts directory with sane defaults based on best practices.
Sourcing setup_aliases.ps1 for windows powershell or setup_aliases.sh in bash on Mac or Linux will provide with handy aliases for the shell of all those commands prepended with an underscore.

The bootstrap script creates a .venv directory inside the project directory hosting the virtual environment. It uses pipenv for that.
It is called by all other scripts before they do anything. So one could simple start by calling _lint and that would set up everything before it tried to actually lint the project

Once the code is ready to be delivered the _tag script should be called accepting one of three arguments, patch, minor, major following the semantic versioning scheme.
So for the initial delivery one would call

    $ _tag --minor

which would bump the version of the project to 0.1.0 tag it in git and do a push and also ask for the change and automagically update HISTORY.rst with the version and the change provided.


So the full workflow after git is initialized is:

 * repeat as necessary (of course it could be test - code - lint :) )
   * code
   * lint
   * test
 * commit and push
 * develop more through the code-lint-test cycle
 * tag (with the appropriate argument)
 * build
 * upload (if you want to host your package in pypi)
 * document (of course this could be run at any point)


Important Information
=====================

This template is based on pipenv. In order to be compatible with requirements.txt so the actual created package can be used by any part of the existing python ecosystem some hacks were needed.
So when building a package out of this **do not** simple call

    $ python setup.py sdist bdist_egg

**as this will produce an unusable artifact with files missing.**
Instead use the provided build and upload scripts that create all the necessary files in the artifact.


Get Started!
------------

Ready to contribute? Here's how to set up `stravapi` for local development.
Using of pipenv is highly recommended.

1. Clone your fork locally::

    $ git clone https://github.com/wefner/stravapi

2. Install your local copy into a virtualenv. Assuming you have pipenv installed, this is how you set up your clone for local development::

    $ cd stravapi/
    $ pipenv install --ignore-pipfile

3. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.
   Do your development while using the CI capabilities and making sure the code passes lint, test, build and document stages.


4. Commit your changes and push your branch to the server::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

5. Submit a merge request

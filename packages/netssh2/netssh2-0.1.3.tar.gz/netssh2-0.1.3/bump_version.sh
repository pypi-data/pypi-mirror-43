#$/bin/bash

# This script creates new tag with changelog and uploads the new version to pypi

# Creating new tag for gitchangelog
sed -i -E 's/__version__ = .[0-9]+\.[0-9]+\.[0-9]./__version__ = \"'"$1"'\"/g' netssh2/__init__.py;
git commit netssh2/__init__.py -m "Version bump to $1";
git tag -a $1 -m '$2';
# Updating changelog
gitchangelog;
git tag -d $1;
git reset --soft HEAD~1;
# Updating MANIFEST.IN
rm -f MANIFEST.in
check-manifest -c;
# Version bump commit
git commit netssh2/__init__.py CHANGELOG.rst MANIFEST.in -m "Version bump to $1";
git tag -a $1 -m '$2';
git push --follow-tags;

# TODO: Add wheel generation
# PYPI:
rm -rf dist;
sudo python setup.py sdist;
twine check dist/* && twine upload dist/*;

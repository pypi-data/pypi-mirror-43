Changelog
=========

0.1.2 (2019-03-26)
------------------
- Add automatic MANIFEST.in updating to bump_version.sh.
  No need to run manually 'check-manifest -c'
- Add manifest file to include everything to built packages.
- Add script for automated version bumping.
  This includes:
   - creating new tag
   - bumping version with commit,
   - updating changelog (need 'pip install gitchangelog')
   - pushing to pypi

  Usage:
  ./bump_version $VERSION $TAG_MESSAGE
  ./bump_version 0.1.0 "Alpha release."
- Add .gitignore.

0.1.1 (2019-03-26)
------------------
- Fix date of 0.0.1 release.
- Fix docs link in README.
- Add changelog to documentation.
- Add license metadata setup.py.
- Add changelog to setup.py long description (pypi).
- Have only GPL v3 on PyPi.

0.1.0 (2019-03-26)
------------------
- Add changelog.
- Improve README.
- Add pypi identifiers to setup.py.
- Add RST docs to be generated with sphinx using 'make html'.
- Fix python envs in tox.
- Add code coverage to tox test.
- Change command prompt too if changing prompt of existing session.
- Add basic tests for tox.
- Cleanup when disconnecting.
- Add messages to assertions.
- Catch error when given invalid hostname.
  This prevents from retrying the socket connection again and again.
- Add linting CI.

0.0.1 (2019-03-21)
------------------
- Basic implementation of netssh2 to work with paralel SSH and interactive shell.
- Add license.
- Initial commit.


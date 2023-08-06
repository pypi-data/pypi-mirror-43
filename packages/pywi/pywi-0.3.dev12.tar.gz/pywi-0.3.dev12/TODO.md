# TODO

- [ ] Add the package "pipeline" (or another name) in witch parts of the "ui" package will migrate
- [ ] Improve the Makefile. see: python3 setup.py --help-commands. Among the interesting options:
    - [ ] python3 setup.py clean --help
    - [ ] python3 setup.py install_data --help
    - [ ] python3 setup.py bdist_rpm --help
    - [ ] python3 setup.py bdist_wininst --help
    - [ ] python3 setup.py check --help
    - [ ] python3 setup.py upload --help
    - [ ] python3 setup.py develop --help
    - [ ] python3 setup.py dist_info --help
    - [ ] python3 setup.py saveopts --help
    - [ ] python3 setup.py test --help
    - [ ] python3 setup.py upload_docs --help
    - [ ] python3 setup.py ptr --help
    - [ ] python3 setup.py pytest --help
- [ ] Finish the refactoring from the former "datapipe" project
    - [ ] grep -ri denoising .
    - [ ] grep -r wavelets_mrfilter .
    - [x] grep -r wavelets_mrtransform .
    - [x] grep -r abstract_cleaning_algorithm .
    - [ ] grep -ri cta pywi docs
    - [ ] grep -ri fits pywi docs
    - [ ] grep -ri geom pywi docs
    - [ ] grep -ri event pywi docs
    - [ ] grep -ri kill pywi docs (warning: it requires to update pywi-cta too)
    - [ ] grep -ri tel pywi docs
    - [ ] grep -ri pe pywi docs
    - [ ] grep -ri tailcut pywi docs
- [ ] Make a conda package for Linux, MacOSX and Windows + update the installation instructions
- [ ] Fix the unittests
- [x] Use Travis CI for continuous integration
- [ ] Use AppVeyor (https://www.appveyor.com/) for continuous integration on
      Windows systems (see
      https://conda.io/docs/user-guide/tasks/use-conda-with-travis-ci.html#appveyor
      and https://packaging.python.org/guides/supporting-windows-using-appveyor/)

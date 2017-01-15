Introduction
============

Jimbo is a simple configuration management tool for Artifactory.


Usage
=====
Install and use jimbo::

    git clone https://github.com/ruhe/jimbo
    pip install jimbo
    jimbo run --url http://127.0.0.1:8081/artifactory \
              --username admin --password password \
              --config-file jimbo/conf/example.yaml


Run jimbo without installation::

    git clone https://github.com/ruhe/jimbo
    cd jimbo
    tox -e venv -- jimbo run --url http://127.0.0.1:8081/artifactory \
                             --username admin --password password \
                             --config-file conf/example.yaml

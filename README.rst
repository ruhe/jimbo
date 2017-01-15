Introduction
============

Jimbo is a simple configuration management tool for Artifactory.

Configuration
=============
Configuration file defines list of repositories that jimbo should manage. Only
most important fields should be set, everything else will be set from
defaults_.

Here's an example of configuration file contents::

  local:
    - key: docker-dev-local
      packageType: docker
      description: Local repository for Docker images
      enableDockerSupport: true
      maxUniqueTags: 100

  remote:
    - key: docker-remote-dockerhub
      packageType: docker
      description: Remote Docker repository for DockerHub (local file cache)
      url: "https://registry-1.docker.io/"
      enableDockerSupport: true

    - key: docker-remote-quay
      packageType: docker
      description: Remote Docker repository for quay.io (local file cache)
      url: "https://quay.io/repository"
      enableDockerSupport: true

Usage
=====
Install and use jimbo::

    git clone https://github.com/ruhe/jimbo
    pip install jimbo
    # Copy and edit sample cofiguration file
    cp jimbo/conf/example.yaml jimbo/conf/repositories.yaml
    vim jimbo/conf/repositories.yaml

    # Run jimbo command
    jimbo run --url http://127.0.0.1:8081/artifactory \
              --username admin --password password \
              --config-file jimbo/conf/example.yaml


Run jimbo without installation::

    git clone https://github.com/ruhe/jimbo
    cd jimbo
    # Copy and edit sample cofiguration file
    cp conf/example.yaml conf/repositories.yaml
    vim conf/repositories.yaml
    
    # Run jimbo command    
    tox -e venv -- jimbo run --url http://127.0.0.1:8081/artifactory \
                             --username admin --password password \
                             --config-file conf/example.yaml

.. _defaults: https://github.com/ruhe/jimbo/tree/master/jimbo/defaults

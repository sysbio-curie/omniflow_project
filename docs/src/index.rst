==================
Neko
==================

   :target: https://github.com/sysbio-curie/Neko/actions/workflows/build.yaml
   :alt: Tests

.. image:: https://img.shields.io/readthedocs/omniflow_project
   :target: https://sysbio-curie.github.io/Neko/
   :alt: Documentation

Package to extract, visualize, convert and study interactions from database into executable activity flow based model.
Neko, is based on `Omnipath <https://github.com/saezlab/omnipath>`_, `Pypath <https://github.com/saezlab/pypath>`_ and `Atopo <https://github.com/druglogics/atopo>`_.

This is a work-in-progress package made in collaboration with Dénes Turei and Asmund Flobak.

Current contributors: Marco Ruscone, Eirini Tsirvouli, Andrea Checcoli, Dénes Turei.

Installation:

All the dependencies are listed in the pyproject.toml file. To install the package, you can use the following command:

.. code-block:: bash

    pip install .

CURRENT FEATURES:

version 0.9.1
--------------

- Network creation and manipulation: The package allows for the creation of a network of nodes and edges, with various methods for enrichment analysis. This includes adding and removing nodes and edges, loading a network from a SIF (Simple Interaction Format) file, and adding paths to the edge list of the network.
- Connection of nodes: The package provides several methods to connect nodes in the network. This includes connecting all nodes, connecting a subgroup of nodes, connecting all nodes of a network object, and connecting subcomponents of a network object.
- Connection of genes to phenotype: The package provides a method to connect genes to a phenotype based on provided parameters. This includes retrieving phenotype markers, identifying unique Uniprot genes, and connecting them to the network. There is also an option to compress the network by substituting specified genes with the phenotype name.

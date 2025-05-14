.. POGG documentation master file, created by
   sphinx-quickstart on Thu Mar  6 14:06:07 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

POGG documentation
==================

POGG (Precision-Oriented Graphical Generator) is a python package designed to convert structured data (e.g. directed graphs or tables) into plain English text. It does this by building Minimal Recursion Semantic (MRS) structures from scratch and then sends them to the English Resource Grammar (ERG) which generates English strings for those semantic structures.

API Reference
--------------

.. toctree::
   :maxdepth: 1
   :caption: General Configuration Module

   pogg_config.py <pogg/pogg.pogg_config.rst>

.. toctree::
   :maxdepth: 1
   :caption: Semantic Composition Modules

   semantic_algebra.py <pogg/semantic_composition/pogg.semantic_composition.semantic_algebra.rst>


Educational Primers
--------------------

The following pages provide some primers for background knowledge that is helpful to understand when using POGG.

.. toctree::
   :maxdepth: 1
   :caption: Education

   English Resource Grammar (ERG) <education/erg.rst>
   Minimal Recursion Semantics (MRS) <education/mrs.rst>


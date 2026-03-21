.. POGG documentation master file, created by
   sphinx-quickstart on Thu Mar  6 14:06:07 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

POGG documentation
==================

POGG (Precision-Oriented Graphical Generator) is a python package designed to convert structured data (e.g. directed graphs or tables) into plain English text. It does this by building Minimal Recursion Semantic (MRS) structures from scratch and then sends them to the English Resource Grammar (ERG) which generates English strings for those semantic structures.

TODO
-----
:doc:`Click here for a list of pages that have not been created yet. <TODO/TODO>`

API Reference
--------------

.. toctree::
   :maxdepth: 1
   :caption: Configuration

   Configuration Module <apidocs/pogg/pogg.pogg_config>

.. toctree::
   :maxdepth: 1
   :caption: PyDelphin Extensions

   my_delphin <apidocs/pogg/pogg.my_delphin.my_delphin>
   sementcodecs <apidocs/pogg/pogg.my_delphin.sementcodecs>

.. toctree::
   :maxdepth: 1
   :caption: Semantic Composition Modules

   sement_util <apidocs/pogg/pogg.semantic_composition.sement_util>
   semantic_algebra <apidocs/pogg/pogg.semantic_composition.semantic_algebra>
   semantic_composition <apidocs/pogg/pogg.semantic_composition.semantic_composition>

.. toctree::
   :maxdepth: 1
   :caption: Semantic Composition Mixins

   single_word_constructions <apidocs/pogg/pogg.semantic_composition.composition_mixins.single_word_constructions>
   base_constructions <apidocs/pogg/pogg.semantic_composition.composition_mixins.base_constructions>


.. toctree::
   :maxdepth: 1
   :caption: Lexicon

   Lexicon Builder Classes <apidocs/pogg/pogg.lexicon.lexicon_builder>

.. toctree::
   :maxdepth: 1
   :caption: Data Handling

   Graph Utilities <apidocs/pogg/pogg.data_handling.graph_util>
   POGGDataset <apidocs/pogg/pogg.data_handling.pogg_dataset>

.. toctree::
   :maxdepth: 1
   :caption: Graph to SEMENT module

   Graph to SEMENT <apidocs/pogg/pogg.graph_to_SEMENT.graph_to_SEMENT>


.. toctree::
   :maxdepth: 1
   :caption: Evaluation and Reporting

   Evaluation <apidocs/pogg/pogg.evaluation.evaluation>
   Reporting <apidocs/pogg/pogg.evaluation.reporting>

.. toctree::
   :maxdepth: 1
   :caption: POGG Routine

   POGG Routine <apidocs/pogg/pogg.pogg_routine>




Usage Examples
---------------

.. toctree::
   :maxdepth: 1
   :caption: Usage Examples

   Configuration Module Example <usage_nbs/pogg/pogg_config_usage>

   SEMENT class Examples <usage_nbs/pogg/my_delphin/my_delphin_usage>
   sementcodecs Examples <usage_nbs/pogg/my_delphin/sementcodecs_usage>

   POGGDataset Examples <usage_nbs/pogg/data_handling/pogg_dataset_usage>
   Graph Util Examples <usage_nbs/pogg/data_handling/graph_util_usage>

   SEMENT Util Examples <usage_nbs/pogg/semantic_composition/sementutil_usage>
   SemanticAlgebra class Examples <usage_nbs/pogg/semantic_composition/SemanticAlgebra_usage>

   Lexicon Builder Examples <usage_nbs/pogg/lexicon/lexicon_builder_usage>

   Graph to SEMENT Examples <usage_nbs/pogg/graph_to_SEMENT/POGGGraphConverter_usage>

   Evaluation Examples <usage_nbs/pogg/evaluation/evaluation_usage>
   Reporting Examples <usage_nbs/pogg/evaluation/reporting_usage>
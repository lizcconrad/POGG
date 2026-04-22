import json
import os

import pogg.semantic_composition.base_constructions
from pogg.lexicon.lexicon_builder import POGGLexiconUtil, POGGLexicon
from pogg.semantic_composition.semantic_algebra import SemanticAlgebra
from pogg.pogg_config import POGGCompositionConfig
from pogg.semantic_composition.base_constructions import SemanticComposition
import inspect

pogg_config = POGGCompositionConfig("../data/config.yml")

lexicon_directory = "/Users/lizcconrad/Documents/PhD/POGG/data_handling/perplexity/development/lexicons/HealTheTrees/"

# POGGLexiconUtil.initialize_lexicon_directory("HealTheTrees", lexicon_directory)
# lexicon_name = "HealTheTrees"

POGGLexiconUtil.update_lexicon_files(lexicon_directory)






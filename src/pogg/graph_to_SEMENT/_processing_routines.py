import copy
import inspect
import networkx as nx
from pathlib import Path

from pogg.evaluation import POGGDataPointEvaluation
from pogg_semantics.pogg_config import POGGCompositionConfig
from pogg_semantics.my_delphin import SEMENT
from pogg_semantics.semantic_composition import SemanticComposition, SemCompTracer, SemAlgTracer, SEMENTUtil


class SEMENTProcessingRoutines:
    # functions static
    @staticmethod
    def apply_default_variable_properties(sem_comp: SemanticComposition, data_point_evaluation: POGGDataPointEvaluation):
        for sement in data_point_evaluation.original_data_point_SEMENTs:
            new_sement = sem_comp.universal_singular(sement)
            data_point_evaluation.modified_data_point_SEMENTs.append(new_sement)
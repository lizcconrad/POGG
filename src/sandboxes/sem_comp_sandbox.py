from pogg.pogg_config import POGGConfig
from pogg.semantic_composition.base_constructions import SemanticComposition
from pogg.semantic_composition.semantic_algebra import SemanticAlgebra
import pogg.semantic_composition.sement_util as sement_util
import pogg.my_delphin.sementcodecs as sementcodecs


pogg_config = POGGConfig("../data/config.yml")
sem_alg = SemanticAlgebra(pogg_config)
sem_comp = SemanticComposition(sem_alg)

probably = sem_comp.adjective("_probable_a_1")
sleep = sem_comp.verb("_sleep_v_1")

probably_sleeps = sem_alg.op_scopal_argument_index(probably, sleep, "ARG1")

str = sementcodecs.encode(probably_sleeps, indent=True)

overwrite = sement_util.overwrite_eqs(probably_sleeps)

overwrite_str = sementcodecs.encode(overwrite, indent=True)

print(str)
print(overwrite_str)
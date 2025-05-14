import yaml
from delphin import semi

class _VarIterator:
    """
    Iterator to help with creating handles, indices, and variables in SEMENTs

    e.g. The ``ARG0`` of the ``_cake_n_1`` predicate may have a value of ``x1``, the ``1`` comes from this iterator.
    Every time a new variable is introduced the current value of the iterator is used and the iterator is incremented
    """
    def __init__(self, start=0):
        self.count = start

    def __iter__(self):
        return self

    def __next__(self):
        self.count += 1
        return self.count

    def set(self, num):
        """Set the value of the iterator"""
        self.count = num

    def reset(self):
        """Reset the iterator to 0"""
        self.count = 0


class _VarLabeler:
    """
    Returns the appropriate label for the next created variable

    e.g. For the intrinsic variable of a noun, the type will be ``x`` and then the object's variable iterator (``self.VarIt``) determines the number following the type
    """
    def __init__(self):
        """
        Make a VarIterator which will increment for each variable made and include the number on the variable name
        """
        #: A VarIterator for the numbers on the variables
        self.varIt = _VarIterator()

    def get_var_name(self, var_type):
        """
        Get the next variable name, passing in the type of the variable per the ERG variable type hierarchy

        Args:
            var_type (str): type of the variable (u, i, p, e, x, h)

        Returns:
            str: the next variable name

        """
        return "{}{}".format(var_type, next(self.varIt))

    def reset_labeler(self):
        """
        Reset the variable labeler's iterator back to 0
        """
        self.varIt.reset()

class POGGConfig:
    """
    A POGGConfig object holds configuration information necessary to run the data-to-text algorithm, such as the location of the Semantic Interface (SEMI) and the grammar

    Args:
        yaml_filepath (str): path to the YAML file which contains the configuration information


    Attributes:
        yaml_config (YAMLObject): loaded from parameter ``yaml_filepath``
        grammar_location (str): location of the grammar used for generation
        SEMI_location (str): location of the SEM-I (Semantic Interface)
        SEMI (delphin.SEMI): PyDelphin SEM-I object, loaded from SEMI_location
        var_labeler (_VarLabeler): _VarLabeler object used to provide a label for each new variable in a semantic structure
    """
    def __init__(self, yaml_filepath):
        yaml_file = open(yaml_filepath, 'r')
        self.yaml_config = yaml.safe_load(yaml_file)
        yaml_file.close()

        self.grammar_location = None
        self.SEMI_location = None
        self.SEMI = None
        self.var_labeler = None


        # save grammar_location in the POGGConfig object
        try:
            self.grammar_location = self.yaml_config['grammar_location']
        except KeyError:
            raise KeyError("'grammar_location' is missing in the config file")

        # save SEMI_location in the POGGConfig object and load the SEMI object
        try:

            self.SEMI_location = self.yaml_config['SEMI']
            self.SEMI = semi.load(self.SEMI_location)
        except KeyError:
            raise KeyError("'SEMI' is missing in the config file")

        self.var_labeler = _VarLabeler()


    def concretize(self, predicate):
        """
        Given a predicate label, find the semantic argument slots and concretize the variable names ,
        e.g. if, according to the SEMI, the variable type of the predicate's ``ARG1`` is``e``
        then give it a concrete value such as ``e1``. Return as a dict of arguments and their concrete variable values.

        Args:
            predicate (str): ERG predicate label (e.g. _cookie_n_1 for the word 'cookie')


        Returns:
            dict: dict of semantic slots and their variable values (e.g. {'ARG1': 'x1'})
        """

        try:
            synopsis = self.SEMI.find_synopsis(predicate)
        except semi.SemIError:
            raise KeyError("Couldn't find {} in the SEMI".format(predicate))

        syn_dict = synopsis.to_dict()
        args_dict = {}
        for role in syn_dict['roles']:
            # currently, role['value'] is just a variable type, like e
            # we still want that in the final variable name, so pass it in as the prefix to the var_labeler
            # but set the value of the role in the args_dict to be the returned var_name (something like e2)
            args_dict[role['name']] = self.var_labeler.get_var_name(role['value'])

        return args_dict
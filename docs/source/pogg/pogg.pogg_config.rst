pogg.pogg_config
==================

Classes for general configuration.

This module contains classes for configuring an "instance" of POGG. For example, POGG sends the semantic structures it builds to a grammar in order to get plain text output, so the location of this grammar must be specified.

By establishing this information as an instance attribute, one could have more than one ``POGGConfig`` object and run the system with different grammars.


Public Classes
----------------

.. py:class:: POGGConfig(yaml_filepath)

    A ``POGGConfig`` object holds configuration information necessary to run the data-to-text algorithm, such as the location of the :ref:`Semantic Interface (SEMI) <semi-reference-label>` and the grammar


    Parameters
    ^^^^^^^^^^^
    .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
    .. list-table::
        :name: poggconfig-parameters-table
        :widths: 20, 10, 70
        :class: longtable
        :header-rows: 1
        :align: left
        :width: 90%

        * - Parameter
          - Type
          - Description
        * - ``yaml_filepath``
          - ``str``
          - path to the YAML file which contains the configuration information


    Instance Attributes
    ^^^^^^^^^^^^^^^^^^^^
    .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
    .. list-table::
        :name: instance-attributes0table
        :widths: 20, 10, 70
        :class: longtable
        :header-rows: 1
        :align: left
        :width: 90%

        * - Attribute
          - Type
          - Description
        * - ``yaml_config``
          - ``YAMLObject``
          - loaded from parameter ``yaml_filepath``
        * - ``grammar_location``
          - ``str``
          - location of the grammar used for generation
        * - ``grammar_location``
          - ``str``
          - location of the grammar used for generation
        * - ``SEMI_location``
          - ``str``
          - location of the SEM-I (Semantic Interface)
        * - ``SEMI``
          - ``delphin.SEMI``
          - PyDelphin SEM-I object, loaded from SEMI_location
        * - ``var_labeler``
          - ``_VarLabeler``
          - _VarLabeler object used to provide a label for each new variable in a semantic structure


    Instance Methods
    ^^^^^^^^^^^^^^^^^
    .. py:function:: concretize(predicate)

        Given a predicate label, find the semantic argument slots and concretize the variable names , e.g. if, according to the SEMI, the variable type of the predicate's ``ARG1`` is``e`` then give it a concrete value such as ``e1``. Return as a dict of arguments and their concrete variable values.

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: concretize-parameters-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``predicate``
              - ``str``
              - ERG predicate label (e.g. _cookie_n_1 for the word 'cookie')

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: concretize-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - dict of ``{str: str}``
              - ``delphin.semi.Synopsis``


        .. dropdown-syntax:: Example usage

            The predicate label ``give_v_1`` has the following synopsis in the SEMI:

            .. code::

                _give_v_1 : ARG0 e, ARG1 i, ARG2 u, [ ARG3 i ].


            Providing this predicate label to ``concretize`` results in the following:

            .. code::

                # assume pogg_config_obj is an instance of POGGConfig
                args = pogg_config_obj.concretize("give_v_1")
                print(args)

                >>> {"ARG0": "e1", "ARG1": "i2", "ARG2": "u3", "ARG3": "i4"}



Private Classes
----------------

.. py:class:: _VarIterator()

    Iterator to help with creating handles, indices, and variables in :ref:`SEMENTs <sement-reference-label>`

    e.g. The ``ARG0`` of the ``_cake_n_1`` predicate may have a value of ``x1``, the ``1`` comes from this iterator.
    Every time a new variable is introduced the current value of the iterator is used and the iterator is incremented


    Parameters
    ^^^^^^^^^^^
    .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
    .. list-table::
        :name: var-iterator-parameters-table
        :widths: 20, 10, 10, 70
        :class: longtable
        :header-rows: 1
        :align: left
        :width: 90%

        * - Parameter
          - Type
          - Default
          - Description
        * - ``start``
          - ``int``
          - ``0``
          - starting value for the iterator upon creation


    Instance Methods
    ^^^^^^^^^^^^^^^^^
    .. py:function:: __iter__

        Return the iterator

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: var-iterator-iter-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``_VarIterator``
              - ``self``, i.e. the ``VarIterator`` object

    .. py:function:: __next__

        Increment the iterator

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: var-iterator-next-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``int``
              - the updated value of the iterator


    .. py:function:: set(num)

            Set the iterator to a specific value

            Parameters
            ^^^^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: var-iterator-set-returns-table
                :widths: 20, 30, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Parameter
                  - Type
                  - Description
                * - ``num``
                  - ``int``
                  - value to set the iterator to

            Returns
            ^^^^^^^^
            ``None``


    .. py:function:: reset

        Reset the iterator to 0

        Returns
        ^^^^^^^^
        ``None``



.. py:class:: _VarLabeler()

     Returns the appropriate label for the next created variable. For example, for the intrinsic variable of a noun, the type will be ``x`` and then the object's variable iterator (``self.VarIt``) determines the number following the type (e.g. ``x1``).


    Parameters
    ^^^^^^^^^^^
    ``None``



    Instance Methods
    ^^^^^^^^^^^^^^^^^
    .. py:function:: get_var_name(var_type)

        Get the next variable name, passing in the type of the variable per the ERG variable type hierarchy

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: var-labeler-get-var-name-parameters-table
            :widths: 20, 30, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``var_type``
              - ``str``
              - type of the semantic slot, can be one of ``u``, ``i``, ``p``, ``e``, ``h``, ``x``

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: var-labeler-get-var-name-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``str``
              - the variable name (e.g. ``e2``)


    .. py:function:: reset

        Reset the variable labeler's iterator back to 0

        Returns
        ^^^^^^^^
        ``None``
pogg.semantic_composition.base_constructions
=============================================

The ``base_constructions`` module contains classes that are generally named after the type of semantic composition the functions within them perform. Classes in this module contain functions that cover common semantic constructions in English. That is, they are not specific to a particular dataset and may be suitable for use with different datasets. Each function performs construction by making appropriate calls to functions in the :doc:`semantic algebra module </pogg/semantic_composition/pogg.semantic_composition.semantic_algebra>`.




.. py:class:: SingleWordConstructions

    A SingleWordConstructions object contains functions for creating "single word" SEMENTs (e.g. noun). These functions create SEMENTs "from scratch" that can be later used as semantic functors or arguments for further composition

        !!! CHANGE THE TABLE NAMES !!!
        class-parameters-table
        class-attributes-table


    Parameters
    ^^^^^^^^^^^
    .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
    .. list-table::
        :name: SingleWordConstructions-parameters-table
        :widths: 20, 10, 70
        :class: longtable
        :header-rows: 1
        :align: left
        :width: 90%

        * - Parameter
          - Type
          - Description
        * - ``semantic_algebra``
          - ``SemanticAlgebra``
          - SemanticAlgebra object that contains functions that perform semantic composition directly


    Instance Attributes
    ^^^^^^^^^^^^^^^^^^^^
    .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
    .. list-table::
        :name: SingleWordConstructions-attributes-table
        :widths: 20, 30, 70
        :class: longtable
        :header-rows: 1
        :align: left
        :width: 90%

        * - Attribute
          - Type
          - Description
        * - ``semantic_algebra``
          - ``SemanticAlgebra``
          - SemanticAlgebra object that contains functions that perform semantic composition directly


    Instance Methods
    ^^^^^^^^^^^^^^^^^

    .. py:function:: basic(pogg_config, predicate, intrinsic_variable_properties={})

            Wrapper around ``pogg.semantic_composition.semantic_algebra.create_base_SEMENT``. Used in fallback cases where part-of-speech guessing fails.

            Parameters
            ^^^^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: basic-parameter-table
                :widths: 20, 10, 10, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Parameter
                  - Type
                  - Default
                  - Description
                * - ``pogg_config``
                  - ``POGGConfig``
                  - --
                  - POGGConfig object that contains information about the SEMI and variable labeler
                * - ``predicate``
                  - ``str``
                  - --
                  - ERG predicate label
                * - ``intrinsic_variable_properties``
                  - dict of ``str``:``str``
                  - ``{}``
                  - optional dictionary of properties of the intrinsic variable, e.g. ``{'NUM': 'sg'}``

            Returns
            ^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: basic-returns-table
                :widths: 40, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Return Type
                  - Description
                * - ``SEMENT``
                  - newly created SEMENT


            .. dropdown-syntax:: Example usage

                Result of calling ``basic`` given the predicate ``_cookie_n_1``.

                .. code::

                    from pogg.pogg_config import POGGConfig
                    import pogg.my_delphin.sementcodecs as sementcodecs
                    import pogg.semantic_composition.base_constructions as base_constructions

                    # assumes a config.yml file that specifies the grammar location
                    pogg_config = POGGConfig("config.yml")

                    basic_SEMENT = base_constructions.basic(pogg_config, "_cookie_n_1", {"NUM": "sg"})
                    print(sementcodecs.encode(basic_SEMENT, indent=True))

                    >>> [ TOP: h2
                          INDEX: x1 [ x NUM: sg ]
                          RELS: < [ _cookie_n_1 LBL: h2 ARG0: x1 ] > ]


    .. py:function:: adjective(pogg_config, predicate, intrinsic_variable_properties={})

            Creates a SEMENT with just a adjective EP in it. This is just a wrapper around ``pogg.semantic_composition.semantic_algebra.create_base_SEMENT``, but is more transparently named for users.


            Parameters
            ^^^^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: adjective-parameter-table
                :widths: 20, 10, 10, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Parameter
                  - Type
                  - Default
                  - Description
                * - ``pogg_config``
                  - ``POGGConfig``
                  - --
                  - POGGConfig object that contains information about the SEMI and variable labeler
                * - ``predicate``
                  - ``str``
                  - --
                  - ERG predicate label
                * - ``intrinsic_variable_properties``
                  - dict of ``str``:``str``
                  - ``{}``
                  - optional dictionary of properties of the intrinsic variable, e.g. ``{'MOOD': 'indicative'}``

            Returns
            ^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: adjective-returns-table
                :widths: 40, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Return Type
                  - Description
                * - ``SEMENT``
                  - newly created SEMENT


            .. dropdown-syntax:: Example usage

                Result of calling ``adjective`` given the predicate ``_tasty_a_1``.

                .. code::

                    from pogg.pogg_config import POGGConfig
                    import pogg.my_delphin.sementcodecs as sementcodecs
                    import pogg.semantic_composition.base_constructions as base_constructions

                    # assumes a config.yml file that specifies the grammar location
                    pogg_config = POGGConfig("config.yml")

                    adjective_SEMENT = base_constructions.adjective(pogg_config, "_tasty_a_1")
                    print(sementcodecs.encode(adjective_SEMENT, indent=True))

                    >>> [ TOP: h5
                          INDEX: e3
                          RELS: < [ _tasty_a_1 LBL: h5 ARG0: e3 ARG1: u4 ] >
                          SLOTS: < ARG1: u4 > ]


    .. py:function:: determiner(pogg_config, predicate, intrinsic_variable_properties={})

            Creates a SEMENT with just a determiner EP in it. This is just a wrapper around ``pogg.semantic_composition.semantic_algebra.create_base_SEMENT``, but is more transparently named for users.


            Parameters
            ^^^^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: determiner-parameter-table
                :widths: 20, 10, 10, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Parameter
                  - Type
                  - Default
                  - Description
                * - ``pogg_config``
                  - ``POGGConfig``
                  - --
                  - POGGConfig object that contains information about the SEMI and variable labeler
                * - ``predicate``
                  - ``str``
                  - --
                  - ERG predicate label
                * - ``intrinsic_variable_properties``
                  - dict of ``str``:``str``
                  - ``{}``
                  - optional dictionary of properties of the intrinsic variable, e.g. ``{'NUM': 'sg'}``

            Returns
            ^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: determiner-returns-table
                :widths: 40, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Return Type
                  - Description
                * - ``SEMENT``
                  - newly created SEMENT


            .. dropdown-syntax:: Example usage

                Result of calling ``determiner`` given the predicate ``_the_q``.

                .. code::

                    from pogg.pogg_config import POGGConfig
                    import pogg.my_delphin.sementcodecs as sementcodecs
                    import pogg.semantic_composition.base_constructions as base_constructions

                    # assumes a config.yml file that specifies the grammar location
                    pogg_config = POGGConfig("config.yml")

                    determiner_SEMENT = base_constructions.determiner(pogg_config, "_the_q")
                    print(sementcodecs.encode(determiner_SEMENT, indent=True))

                    >>> [ TOP: h10
                          INDEX: x6
                          RELS: < [ _the_q LBL: h9 ARG0: x6 RSTR: h7 BODY: h8 ] >
                          SLOTS: < ARG0: x6 RSTR: h7 BODY: h8 > ]


    .. py:function:: named_entity(pogg_config, name, intrinsic_variable_properties={})

            Creates a SEMENT for a named entity, e.g. a person ("Liz")


            Parameters
            ^^^^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: named-entity-parameter-table
                :widths: 20, 10, 10, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Parameter
                  - Type
                  - Default
                  - Description
                * - ``pogg_config``
                  - ``POGGConfig``
                  - --
                  - POGGConfig object that contains information about the SEMI and variable labeler
                * - ``name``
                  - ``str``
                  - --
                  - the name of the entity
                * - ``intrinsic_variable_properties``
                  - dict of ``str``:``str``
                  - ``{}``
                  - optional dictionary of properties of the intrinsic variable, e.g. ``{'NUM': 'sg'}``

            Returns
            ^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: named-entity-returns-table
                :widths: 40, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Return Type
                  - Description
                * - ``SEMENT``
                  - newly created SEMENT


            .. dropdown-syntax:: Example usage

                Result of calling ``named_entity`` given the name ``Liz``.

                .. code::

                    from pogg.pogg_config import POGGConfig
                    import pogg.my_delphin.sementcodecs as sementcodecs
                    import pogg.semantic_composition.base_constructions as base_constructions

                    # assumes a config.yml file that specifies the grammar location
                    pogg_config = POGGConfig("config.yml")

                    name_SEMENT = base_constructions.named_entity(pogg_config, "Liz")
                    print(sementcodecs.encode(name_SEMENT, indent=True))

                    >>> [ TOP: h12
                          INDEX: x11
                          RELS: < [ named LBL: h12 ARG0: x11 CARG: "Liz" ] > ]


    .. py:function:: noun(pogg_config, predicate, intrinsic_variable_properties={})

            Creates a SEMENT with just a noun EP in it. This is just a wrapper around ``pogg.semantic_composition.semantic_algebra.create_base_SEMENT``, but is more transparently named for users.


            Parameters
            ^^^^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: noun-parameter-table
                :widths: 20, 10, 10, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Parameter
                  - Type
                  - Default
                  - Description
                * - ``pogg_config``
                  - ``POGGConfig``
                  - --
                  - POGGConfig object that contains information about the SEMI and variable labeler
                * - ``predicate``
                  - ``str``
                  - --
                  - ERG predicate label
                * - ``intrinsic_variable_properties``
                  - dict of ``str``:``str``
                  - ``{}``
                  - optional dictionary of properties of the intrinsic variable, e.g. ``{'NUM': 'sg'}``

            Returns
            ^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: noun-returns-table
                :widths: 40, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Return Type
                  - Description
                * - ``SEMENT``
                  - newly created SEMENT


            .. dropdown-syntax:: Example usage

                Result of calling ``noun`` given the predicate ``_cookie_n_1``.

                .. code::

                    from pogg.pogg_config import POGGConfig
                    import pogg.my_delphin.sementcodecs as sementcodecs
                    import pogg.semantic_composition.base_constructions as base_constructions

                    # assumes a config.yml file that specifies the grammar location
                    pogg_config = POGGConfig("config.yml")

                    noun_SEMENT = base_constructions.noun(pogg_config, "_cookie_n_1", {"NUM": "sg"})
                    print(sementcodecs.encode(noun_SEMENT, indent=True))

                    >>> [ TOP: h2
                          INDEX: x1 [ x NUM: sg ]
                          RELS: < [ _cookie_n_1 LBL: h2 ARG0: x1 ] > ]


    .. py:function:: preposition(pogg_config, predicate, intrinsic_variable_properties={})

            Creates a SEMENT with just a preposition EP in it. This is just a wrapper around ``pogg.semantic_composition.semantic_algebra.create_base_SEMENT``, but is more transparently named for users.


            Parameters
            ^^^^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: preposition-parameter-table
                :widths: 20, 10, 10, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Parameter
                  - Type
                  - Default
                  - Description
                * - ``pogg_config``
                  - ``POGGConfig``
                  - --
                  - POGGConfig object that contains information about the SEMI and variable labeler
                * - ``predicate``
                  - ``str``
                  - --
                  - ERG predicate label
                * - ``intrinsic_variable_properties``
                  - dict of ``str``:``str``
                  - ``{}``
                  - optional dictionary of properties of the intrinsic variable, e.g. ``{'NUM': 'sg'}``

            Returns
            ^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: preposition-returns-table
                :widths: 40, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Return Type
                  - Description
                * - ``SEMENT``
                  - newly created SEMENT


            .. dropdown-syntax:: Example usage

                Result of calling ``preposition`` given the predicate ``_in_p_loc``.

                .. code::

                    from pogg.pogg_config import POGGConfig
                    import pogg.my_delphin.sementcodecs as sementcodecs
                    import pogg.semantic_composition.base_constructions as base_constructions

                    # assumes a config.yml file that specifies the grammar location
                    pogg_config = POGGConfig("config.yml")

                    preposition_SEMENT = base_constructions.preposition(pogg_config, "_in_p_loc")
                    print(sementcodecs.encode(preposition_SEMENT, indent=True))

                    >>> [ TOP: h6
                          INDEX: e3
                          RELS: < [ _in_p_loc LBL: h6 ARG0: e3 ARG1: u4 ARG2: u5 ] >
                          SLOTS: < ARG1: u4 ARG2: u5 > ]


    .. py:function:: pronoun(pogg_config, intrinsic_variable_properties={})

            Creates a SEMENT for a pronoun. Values for ``PERS``, ``NUM``, and ``GEND`` (only where ``PERS`` is ``3``) should be specified in the ``intrinsic_variable_properties`` dictionary. If not specified, the resulting SEMENT will represent a pronoun that is ambiguous between the possible values for the unspecified feature.

            Possible values for pronoun features
            ^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: pronoun-features-table
                :widths: 40, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Feature
                  - Possible Values
                * - ``PERS`` [#persnote]_
                  - ``"1"``, ``"2"``, ``"3"``
                * - ``NUM``
                  - ``"sg"``, ``"pl"``
                * - ``GEND`` [#gendnote]_
                  - ``"m"``, ``"f"``, ``"n"``

            .. [#persnote]

                Values for ``PERS`` must be strings, not integers. They also must match exactly what is shown in the table. That is, ``"1st"`` will not work, the value must be ``"1"``.

            .. [#gendnote]

                A value for ``GEND`` may only be specified when ``PERS`` has a value of ``"3"``. Specifying a value for ``GEND`` in other cases will result in a broken semantic structure that the ERG cannot generate text from.


            Parameters
            ^^^^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: pronoun-parameter-table
                :widths: 20, 10, 10, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Parameter
                  - Type
                  - Default
                  - Description
                * - ``pogg_config``
                  - ``POGGConfig``
                  - --
                  - POGGConfig object that contains information about the SEMI and variable labeler
                * - ``intrinsic_variable_properties``
                  - dict of ``str``:``str``
                  - ``{}``
                  - optional dictionary of properties of the intrinsic variable, e.g. ``{'NUM': 'sg'}``

            Returns
            ^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: pronoun-returns-table
                :widths: 40, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Return Type
                  - Description
                * - ``SEMENT``
                  - newly created SEMENT


            .. dropdown-syntax:: Example usage

                Result of calling ``pronoun`` given values of ``"sg"``, ``"3"``, and ``"f"`` for ``NUM``, ``PERS``, and ``GEND``, respectively.

                .. code::

                    from pogg.pogg_config import POGGConfig
                    import pogg.my_delphin.sementcodecs as sementcodecs
                    import pogg.semantic_composition.base_constructions as base_constructions

                    # assumes a config.yml file that specifies the grammar location
                    pogg_config = POGGConfig("config.yml")

                    pronoun_SEMENT = base_constructions.pronoun(pogg_config, {"NUM": "sg", "PERS": "3", "GEND": "f"})
                    print(sementcodecs.encode(pronoun_SEMENT, indent=True))

                    >>> [ TOP: h7
                          INDEX: x3
                          RELS: < [ pronoun_q LBL: h6 ARG0: x3 RSTR: h4 BODY: h5 ]
                                  [ pron LBL: h2 ARG0: x1 [ x PERS: 3 NUM: sg GEND: f ] ] >
                          HCONS: < h4 qeq h2 >
                          EQS: < x3 eq x1 >
                          SLOTS: < BODY: h5 > ]


    .. py:function:: verb(pogg_config, predicate, intrinsic_variable_properties={})

            Creates a SEMENT with just a verb EP in it. This is just a wrapper around ``pogg.semantic_composition.semantic_algebra.create_base_SEMENT``, but is more transparently named for users.


            Parameters
            ^^^^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: verb-parameter-table
                :widths: 20, 10, 10, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Parameter
                  - Type
                  - Default
                  - Description
                * - ``pogg_config``
                  - ``POGGConfig``
                  - --
                  - POGGConfig object that contains information about the SEMI and variable labeler
                * - ``predicate``
                  - ``str``
                  - --
                  - ERG predicate label
                * - ``intrinsic_variable_properties``
                  - dict of ``str``:``str``
                  - ``{}``
                  - optional dictionary of properties of the intrinsic variable, e.g. ``{'TENSE': 'pres'}``

            Returns
            ^^^^^^^^
            .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
            .. list-table::
                :name: verb-returns-table
                :widths: 40, 70
                :class: longtable
                :header-rows: 1
                :align: left
                :width: 90%

                * - Return Type
                  - Description
                * - ``SEMENT``
                  - newly created SEMENT


            .. dropdown-syntax:: Example usage

                Result of calling ``verb`` given the predicate ``_eat_v_1``.

                .. code::

                    from pogg.pogg_config import POGGConfig
                    import pogg.my_delphin.sementcodecs as sementcodecs
                    import pogg.semantic_composition.base_constructions as base_constructions

                    # assumes a config.yml file that specifies the grammar location
                    pogg_config = POGGConfig("config.yml")

                    verb_SEMENT = base_constructions.verb(pogg_config, "_eat_v_1", {"TENSE": "pres"})
                    print(sementcodecs.encode(verb_SEMENT, indent=True))

                    >>> [ TOP: h4
                          INDEX: e1 [ e TENSE: pres ]
                          RELS: < [ _eat_v_1 LBL: h4 ARG0: e1 ARG1: i2 ARG2: i3 ] >
                          SLOTS: < ARG1: i2 ARG2: i3 > ]



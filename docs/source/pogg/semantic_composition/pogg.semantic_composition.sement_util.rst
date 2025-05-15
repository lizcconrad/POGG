pogg.semantic_composition.sement_util
======================================

Module Functions
------------------
.. py:function:: group_equalities(eqs)

        Group equalities from a list of EQ pairs into EQ sets. That is, if the EQ list contains an eq ``(x1, x2)`` and an eq ``(x2, x3)`` then create a set ``(x1, x2, x3)`` such that they're in an equality "group"

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: group-equalities-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``eqs``
              - list of ``set``
              - List of EQ pairs

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: group-equalities-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - list of ``set``
              - list of EQ sets after grouping occurs



.. py:function:: get_most_specified_variable(eq_vars)

        Get the most "specific" variable to serve as the representative for the EQ set. That is, a variable of type ``x`` is more specific than one of type ``i``, according to the ERG hierarchy

        .. dropdown:: ERG Variable Type Hierarchy

            * ``u`` -- unspecific
            * ``i`` -- subtype of ``u``, underspecified between ``e`` and ``x``
            * ``p`` -- suptype of ``u``, underspecified between ``h`` and ``x``
            * ``e`` -- suptype of ``i``, eventualities (e.g. intrinsic variable of a verb)
            * ``x`` -- subtype of ``i`` and p, instance (e.g. intrinsic variable of a noun)
            * ``h`` -- subtype of ``p``, handle used for scopal composition


        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: get-most-specified-variable-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Default (take out if necessary)
              - Description
            * - ``eq_vars``
              - list of ``str``
              - list of variables e.g. ``(u1, i2, x3)``

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: get-most-specified-variable-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``str``
              - Variable with the most specific type


.. py:function:: overwrite_eqs(sement)

        Create a new SEMENT where the any variables that are members of an EQ have been overwritten to one representative value

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: overwrite-eqs-parameter-table
            :widths: 20, 10, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``eq_vars``
              - list of ``str``
              - SEMENT structure with unresolved variable equalities

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: overwrite-eqs-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``SEMENT``
              - new SEMENT with resolved variable equalities


        .. dropdown-syntax:: Example usage

            Example of ``overwrite_eqs`` being called on a SEMENT for *tasty cookie*. In the initial SEMENT, there is an EQ between the ``ARG0`` of *cookie* (``x1``) and the ``ARG1`` of *tasty*, because the ``ARG1`` of *cookie* (i.e. the thing that is tasty) is plugged by the intrinsic variable of *cookie*.

            The ``overwrite_eqs`` function chooses one of these variables as the representative for the EQ (here, ``x1``) and overwrites all instances of ``x4`` to also be ``x1``. This enables conversion to an MRS object in order to send the structure to the ERG for text generation.

            .. code::

                # SEMENT for "tasty cookie" before EQs are overwritten
                original_sement = """[
                    TOP: h0
                    INDEX: x1
                    RELS: <
                        [ _tasty_a_1 LBL: h2 ARG0: e3 ARG1: x4 ]
                        [ _cookie_n_1 LBL: h0 ARG0: x1 ] >
                    EQS: < x1 eq x4 >
                ]"""

                new_sement = sement_util.overwrite_eqs(original_sement)
                # encode the new_sement object into a string
                print(pogg.my_delphin.sement.encode(new_sement))

                >>> [ TOP: h0
                    INDEX: x1
                    RELS: <
                        [ _tasty_a_1 LBL: h2 ARG0: e3 ARG1: x1 ]
                        [ _cookie_n_1 LBL: h0 ARG0: x1 ] >
                    EQS: < > ]



.. py:function:: is_sement_isomorphic(s1: SEMENT, s2: SEMENT)

        Check whether two SEMENTs are isomorphic. Isomorphic SEMENTs have the same directed graph structure, but might not be literally identical. For example, the EPs in the RELS list may be in different orders, or the actual variable values are different but the structure is still the same.

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: is-sement-isomorphic-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``s1``
              - ``SEMENT``
              - first SEMENT
            * - ``s2``
              - ``SEMENT``
              - second SEMENT

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: is-sement-isomorphic-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``bool``
              - whether the two SEMENTs are isomorphic
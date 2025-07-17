pogg.semantic_composition.sement_util
======================================

Module Functions
------------------
.. py:function:: duplicate_sement(sement)

        Create a duplicate of the SEMENT to prevent the passed in object from being modified during certain operations. Just using "deepcopy" doesn't work due to some unexpected behavior with pydelphin HCons objects.

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: duplicate-sement-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``sement``
              - ``SEMENT``
              - SEMENT to be duplicated

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: duplicate-sement-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - SEMENT
              - duplicated SEMENT


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
            :widths: 20, 10, 70
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

            Example of :py:func:`overwrite_eqs` being called on a SEMENT for *tasty cookie*. In the initial SEMENT, there is an EQ between the ``ARG0`` of *cookie* (``x1``) and the ``ARG1`` of *tasty*, because the ``ARG1`` of *cookie* (i.e. the thing that is tasty) is plugged by the intrinsic variable of *cookie*.

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



.. py:function:: check_if_quantified(sement)

        Check if the given SEMENT is quantified.

        .. note::

            This function only makes sense to use with SEMENTS that correspond to nouns/noun phrases. The ERG requires all nouns and their adjuncts to be quantified before they may serve as arguments to other elements like verbs or prepositions. Therefore, it is sometimes necessary to check whether a SEMENT is quantified before proceeding with composition.

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: check-if-quantified-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``check_sement``
              - ``SEMENT``
              - SEMENT to be checked

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: check-if-quantified-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - boolean
              - whether the SEMENT is quantified


        .. dropdown-syntax:: Example usage

            This function is used in cases where it's necessary to ensure that a SEMENT is quantified before proceeding with composition. For example, the argument of a verb must be plugged with a quantified noun (plus possible adjuncts). That is, it cannot be plugged with a SEMENT whose ``RELS`` list only contains one EP for *cookie*, but a SEMENT whose ``RELS`` list contains an EP for *cookie* and some quantifier.

            .. code::

                import pogg.my_delphin.sementcodecs as sementcodecs
                import pogg.semantic_composition.sement_util as sement_util

                unquant_cookie = """[ TOP: h0
                    INDEX: x1
                    RELS: < [ _cookie_n_1 LBL: h0 ARG0: x1 ] >
                ]"""
                unquant_cookie_sement_obj = sementcodecs.decode(unquant_cookie)

                print(sement_util.check_if_quantified(unquant_cookie_sement_obj))

                >>> False

                quant_cookie = """[ TOP: h6
                    INDEX: x1
                    RELS: <
                        [ _udef_q LBL: h0 ARG0: x1 RSTR: h2 BODY: h3 ]
                        [ _cookie_n_1 LBL: h4 ARG0: x5 ] >
                    EQS: < x1 eq x5 >
                    SLOTS: < BODY: h3 >
                    HCONS: < h2 qeq h4 > ]"""

                quant_cookie_sement_obj = sementcodecs.decode(quant_cookie)

                print(sement_util.check_if_quantified(quant_cookie_sement_obj))

                >>> True

.. py:function:: is_sement_isomorphic(s1: SEMENT, s2: SEMENT)

        Check whether two SEMENTs are isomorphic. Isomorphic SEMENTs have the same directed graph structure, but might not be literally identical. For example, the EPs in the RELS list may be in different orders, or the actual variable values are different (e.g. ``x1`` in one SEMENT may be ``x2`` in the other but they fill the same roles) but the structure is still the same.

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

.. py:function:: create_variable_roles_dict(sement)

        Given a SEMENT object, create a dictionary where each key is a variable in the SEMENT and the value is the set of semantic roles that variable fills


        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: create-variable-roles-dict-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``sement``
              - ``SEMENT``
              - the SEMENT object

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: create-variable-roles-dict-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - dict of ``str``:``str``
              - resulting dictionary mapping variables to sets of semantic roles


        .. dropdown-syntax:: Example usage

            Result of calling :py:func:`create_variable_roles_dict` for the provided SEMENT string for *a tasty cookie*.

            .. code::

                import pogg.my_delphin.sementcodecs as sementcodecs
                import pogg.semantic_composition.sement_util as sement_util

                sement_string = """[ TOP: h9
                  INDEX: x4
                  RELS: < [ _tasty_a_1 LBL: h0 ARG0: e1 ARG1: x4 ]
                          [ _cookie_n_1 LBL: h0 ARG0: x4 ]
                          [ _a_q LBL: h5 ARG0: x4 RSTR: h7 BODY: h8 ] >
                  SLOTS: < BODY: h8 >
                  HCONS: < h7 qeq h0 > ]"""

                sement_object = sementcodecs.decode(sement_string)

                roles_dict = sement_util.create_variable_roles_dict(sement_object)

                print(roles_dict)

                >>> {'h9': ['TOP'],
                        'x4': ['INDEX', '_a_q.ARG0', '_cookie_n_1.ARG0', '_tasty_a_1.ARG1'],
                        'h0': ['_cookie_n_1.LBL', '_tasty_a_1.LBL'],
                        'e1': ['_tasty_a_1.ARG0'],
                        'h5': ['_a_q.LBL'],
                        'h7': ['_a_q.RSTR'],
                        'h8': ['_a_q.BODY']}


.. py:function:: create_hcons_list(sement)

        Create a list of HCons entries. Each entry includes the handles that are in the HCons relationship as well as the semantic roles those handles occupy to enable easier comparison of existing handle constraints across SEMENTs.


        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: create-hcons-listparameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``sement``
              - ``SEMENT``
              - the SEMENT object

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: create-hcons-list-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - list of dict
              - a list of HCons entries


        .. dropdown-syntax:: Example usage

            Result of calling :py:func:`create_hcons_list` on the given SEMENT string for *a tasty cookie*.

            .. code::

                import pogg.my_delphin.sementcodecs as sementcodecs
                import pogg.semantic_composition.sement_util as sement_util

                sement_string = """[ TOP: h9
                  INDEX: x4
                  RELS: < [ _tasty_a_1 LBL: h0 ARG0: e1 ARG1: x4 ]
                          [ _cookie_n_1 LBL: h0 ARG0: x4 ]
                          [ _a_q LBL: h5 ARG0: x4 RSTR: h7 BODY: h8 ] >
                  SLOTS: < BODY: h8 >
                  HCONS: < h7 qeq h0 > ]"""

                sement_object = sementcodecs.decode(sement_string)

                hcons_list = sement_util.create_hcons_list(sement_object)

                print(hcons_list)

                >>> [{'hi_role_set': ['_a_q.RSTR'],
                        'lo_role_set': ['_cookie_n_1.LBL', '_tasty_a_1.LBL'],
                        'hi_var': 'h7',
                        'lo_var': 'h0'}]


.. py:function:: find_slot_overlaps(gold_sement, actual_sement)

        Produces three lists: ``overlap_slots``, ``gold_only_slots``, and ``actual_only_slots``. The goal is to compare slots lists across two SEMENTs to detect differences when isomorphism checks fail.

        Each list contains dictionaries that detail the slots that remain.

        .. code::

            {
                "slot": {"_cozy_a_1.ARG1"}
                "gold_var": 'x1',
                "actual_var": 'x2'
            }

        If two SEMENts are isomorphic, the ``gold_only_slots`` and ``actual_only_slots`` lists will be empty, but when the SEMENTs are not isomorphic, the sets of remaining slots may not match so these lists will help pinpoint where the differences lie.

        .. note::

            Here "slots" means specifically members of the SLOTS list of the SEMENT object, not unfilled semantic roles. During any composition operation between a functor SEMENT and argument SEMENT, the slots from the argument SEMENT are dropped and not included in the result's SLOTS list, preventing them from ever being filled. Therefore some slots will remain unfilled, but don't count as "slots" for the purposes of this check as they are no longer present in the SLOTS list.

        .. warning::

            This function must be called on SEMENTs that have already gone through :py:func:`overwrite_eqs` in order to make comparison easier. If the EQs list of the SEMENT is not empty the function will throw an error.



        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: find-slot-overlaps-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``gold_sement``
              - ``SEMENT``
              - one of the SEMENTs being compared, nominally the "gold" one that the actual aims to match
            * - ``actual_sement``
              - ``SEMENT``
              - one of the SEMENTs being compared, nominally the one produced by the system


        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: find-slot-overlaps-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``list``
              - list of overlapping slots
            * - ``list``
              - list of semantic slots only present in the gold_sement
            * - ``list``
              - list of semantic slots only present in the actual_sement

        .. dropdown-syntax:: Example usage

            Below is an example of calling :py:func:`find_slot_overlaps` on two SEMENTs for *believe the cat sleeps*. In the broken one, there is a handle constraint between the ``ARG3`` of the ``_believe_v_1`` EP and the ``LBL`` of the ``_sleep_v_1`` EP, which is the incorrect slot for this constraint, causing the slots list to be incorrect. [#note]_

            .. [#note]

                Technically, they are both broken because we want the two argument version of ``_believe_v_1``, not the three argument version, but using the three argument version is better for this example.

            .. code::

                import pogg.my_delphin.sementcodecs as sementcodecs
                import pogg.semantic_composition.sement_util as sement_util

                gold_the_cat_sleeps = """[ TOP: h0
                  INDEX: e1
                  RELS: < [ _believe_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: h4 ]
                          [ _the_q LBL: h5 ARG0: x10 RSTR: h7 BODY: h8 ]
                          [ _cat_n_1 LBL: h9 ARG0: x10 ]
                          [ _sleep_v_1 LBL: h11 ARG0: e12 ARG1: x10 ] >
                  SLOTS: < ARG1: i2 ARG3: h4 >
                  HCONS: < h7 qeq h9 u3 qeq h11 > ]"""

                broken_the_cat_sleeps = """[ TOP: h00
                  INDEX: e01
                  RELS: < [ _believe_v_1 LBL: h00 ARG0: e01 ARG1: i02 ARG2: u03 ARG3: h04 ]
                          [ _the_q LBL: h05 ARG0: x010 RSTR: h07 BODY: h08 ]
                          [ _cat_n_1 LBL: h09 ARG0: x010 ]
                          [ _sleep_v_1 LBL: h011 ARG0: e012 ARG1: x010 ] >
                  SLOTS: < ARG1: i02 ARG2: u03 >
                  HCONS: < h07 qeq h09 h04 qeq h011 > ]"""

                gold_sement_obj = sementcodecs.decode(gold_the_cat_sleeps)
                broken_sement_obj = sementcodecs.decode(broken_the_cat_sleeps)

                # the function returns three lists, store each of them
                overlapping_slots, gold_slots, broken_slots = sement_util
                    .find_slot_overlaps(gold_sement_obj, broken_sement_obj)


                # print resulting slot lists
                print(overlapping_slots)

                >>> [{'slot': '_believe_v_1.ARG1', 'gold_var': 'i2', 'actual_var': 'i02'}]

                print(gold_slots)

                >>> [{'slot': '_believe_v_1.ARG3', 'gold_var': 'h4'}]

                print(actual_slots)

                >>> [{'slot': '_believe_v_1.ARG2', 'actual_var': 'u03'}]


.. py:function:: find_var_eq_overlaps(gold_sement, actual_sement)

        Produces three lists: ``overlap_eqs``, ``gold_only_eqs``, and ``actual_only_eqs``. The goal is to compare semantic role equivalencies across two SEMENTs to detect differences when isomorphism checks fail.

        Each list contains dictionaries that detail sets of semantic roles that are filled by the same variable.

        .. dropdown:: Example

            Here is an example of a "role equivalency set":

            .. code::

                {
                    "eq_set": {"_a_q.ARG0", "_cat_n_1.ARG0", "_cozy_a_1.ARG1"}
                    "gold_var": 'x1',
                    "actual_var": 'x2'
                }

            What this shows is that in both SEMENTs the ``ARG0`` of the ``_a_q`` EP, the ``ARG0`` of the ``_cat_n_1`` EP, and the ``ARG1`` of the ``_cozy_a_1`` EP are identified with each other, but that in the gold SEMENT the variable filling all these slots is called ``x1`` but in the actual (where "actual" roughly means the one being composed with the goal to match the gold) the variable is called ``x2``. So, despite the different variable names, the semantic role equivalency matches.

        If two SEMENTs are isomorphic, the ``gold_only_eqs`` and ``actual_only_eqs`` lists will be empty, but when the SEMENTs are not isomorphic, the sets of semantic role equivalencies may not match so these lists will help pinpoint where the differences lie.

        .. warning::

                This function must be called on SEMENTs that have already gone through :py:func:`overwrite_eqs` in order to make comparison easier. If the EQs list of the SEMENT is not empty the function will throw an error.



        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: find-var-eq-overlaps-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``gold_sement``
              - ``SEMENT``
              - one of the SEMENTs being compared, nominally the "gold" one that the actual aims to match
            * - ``actual_sement``
              - ``SEMENT``
              - one of the SEMENTs being compared, nominally the one produced by the system


        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: find-var-eq-overlaps-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``list``
              - list of overlapping semantic role equivalencies
            * - ``list``
              - list of semantic role equivalencies only present in the gold_sement
            * - ``list``
              - llist of semantic role equivalencies only present in the actual_sement

        .. dropdown-syntax:: Example usage

            Below is a worked example of calling :py:func:`find_var_eq_overlaps` on two SEMENTs for *tasty cookie*. In the broken one, there should be an equivalence between the ``LBL`` of each EP, but it's missing.

            First, let's gather the lists of role equivalence sets

            .. code::

                import pogg.my_delphin.sementcodecs as sementcodecs
                import pogg.semantic_composition.sement_util as sement_util

                gold_tasty_cookie = """[ TOP: h0
                  INDEX: x4
                  RELS: < [ _tasty_a_1 LBL: h0 ARG0: e1 ARG1: x4 ]
                          [ _cookie_n_1 LBL: h0 ARG0: x4 ] > ]"""

                broken_tasty_cookie = """[ TOP: h03
                  INDEX: x04
                  RELS: < [ _tasty_a_1 LBL: h00 ARG0: e01 ARG1: x04 ]
                          [ _cookie_n_1 LBL: h03 ARG0: x04 ] > ]"""

                gold_sement_obj = sementcodecs.decode(gold_tasty_cookie)
                broken_sement_obj = sementcodecs.decode(broken_tasty_cookie)

                # the function returns three lists, store each of them
                overlapping_eqs, gold_eqs, broken_eqs = sement_util
                    .find_var_eq_overlaps(gold_sement_obj, broken_sement_obj)


            Now, let's look at the overlapping sets. Notice that the first set has multiple semantic roles in it (the ``INDEX``, the ``ARG0`` for the ``_cookie_n_1`` EP, and the ``ARG1`` for the ``_tasty_a_1`` EP). But the second set just contains one role, the ``ARG0`` for the ``_tasty_a_1`` EP. Even though it feels odd to call that a set of "equivalencies" it does indicate to us that in both SEMENTs this role is not identified with any other role.

            .. code::

                # shows the eqs present in both SEMENTS
                print(overlapping_eqs)

                >>> [{'eq_set': ['INDEX', '_cookie_n_1.ARG0', '_tasty_a_1.ARG1'],
                        'gold_var': 'x4',
                        'actual_var': 'x04'},
                    {'eq_set': ['_tasty_a_1.ARG0'],
                        'gold_var': 'e1',
                        'actual_var': 'e01'}]

            Next, let's look at the role equivalencies only present in the gold SEMENT. Here, we see the identity between the ``LBL`` of each EP as mentioned above, as well as the fact that the ``TOP`` is a member of this set.

            .. code::

                # shows the eqs present in only in the gold SEMENT
                print(gold_eqs)

                >>> [{'eq_set': ['TOP', '_cookie_n_1.LBL', '_tasty_a_1.LBL'],
                        'gold_var': 'h0'}]


            Last, let's look at the role equivalencies unique to the broken SEMENT. Here, we have two sets. The first one shows that the ``TOP`` is identified with the ``LBL`` of the ``_cookie_n_1`` EP. The second one shows that the ``LBL`` of the ``_tasty_a_1`` EP is not identified with anything, which is in obvious contrast to what we saw in the gold one.

            .. code::

                # shows the eqs present in only in the "actual" SEMENT
                print(broken_eqs)

                >>> [{'eq_set': ['TOP', '_cookie_n_1.LBL'],
                        'actual_var': 'h03'},
                    {'eq_set': ['_tasty_a_1.LBL'],
                        'actual_var': 'h00'}]


.. py:function:: find_hcons_overlaps(gold_sement, actual_sement)

    Produces three lists: ``overlap_hcons``, ``gold_only_hcons``, and ``actual_only_hcons``. The goal is to compare handle constraints across two SEMENTs to detect differences when isomorphism checks fail.

    Each list contains dictionaries that detail which handle constraints are present in which SEMENT.

    .. dropdown:: Example

        Here is an example of a "role equivalency set":

        .. code::

            {
                "hi_role_set": {"_a_q.RSTR"},
                "lo_role_set": {"_cookie_n_1.LBL", "_tasty_a_1.LBL"},
                "hi_gold_var": "h0",
                "lo_gold_var": "h1",
                "hi_actual_var": "h00",
                "lo_actual_var": "h01",
            }


        What this shows is that in both SEMENTs the ``RSTR`` of the ``_a_q`` EP is the high handle in a QEQ relationship to the ``LBL`` of both ``_cookie_n_1`` and ``_tasty_a_1``, which serve as the low handles in conjunction. But the values of the handles in each SEMENT are different, even though the shape of the handle constraint is the same in both.

    If two SEMENts are isomorphic, the ``gold_only_hcons`` and ``actual_only_hcons`` lists will be empty, but when the SEMENTs are not isomorphic, the sets of handle constraints may not match so these lists will help pinpoint where the differences lie.

    .. warning::

        This function must be called on SEMENTs that have already gone through :py:func:`overwrite_eqs` in order to make comparison easier. If the EQs list of the SEMENT is not empty the function will throw an error.


    If two SEMENTs are isomorphic, the gold_only_hcons and actual_only_hcons lists will be empty, but when the SEMENTs are not isomorphic, the sets of handle constraints may not match so these lists will help pinpoint where any differences lie.


    Parameters
    ^^^^^^^^^^^
    .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
    .. list-table::
        :name: find-hcons-ovelaps-parameter-table
        :widths: 20, 10, 70
        :class: longtable
        :header-rows: 1
        :align: left
        :width: 90%

        * - Parameter
          - Type
          - Description
        * - ``gold_sement``
          - ``SEMENT``
          - one of the SEMENTs being compared, nominally the "gold" one that the actual aims to match
        * - ``actual_sement``
          - ``SEMENT``
          - one of the SEMENTs being compared, nominally the one produced by the system

    Returns
    ^^^^^^^^
    .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
    .. list-table::
        :name: find-hcons-overlaps-returns-table
        :widths: 40, 70
        :class: longtable
        :header-rows: 1
        :align: left
        :width: 90%

        * - Return Type
          - Description
        * - list
          - list of overlapping handle constraints
        * - list
          - list of handle constraints only present in the gold_sement
        * - list
          - llist of handle constraints only present in the actual_sement


    .. dropdown-syntax:: Example usage

        Below is a worked example of calling :py:func:`find_var_eq_overlaps` on two SEMENTs for *believe the cat sleeps*. In the broken one, there should be a QEQ between the ``ARG2`` of the ``_believe_v_1`` EP and the ``LBL`` of the ``_sleep_v_1`` EP, but it's actually set between the wrong arguments.

        First, let's gather the lists of handle constraints.

        .. code::

            import pogg.my_delphin.sementcodecs as sementcodecs
            import pogg.semantic_composition.sement_util as sement_util

            believe_the_cat_sleeps = """[ TOP: h0
              INDEX: e1
              RELS: < [ _believe_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: h4 ]
                      [ the_q LBL: h5 ARG0: x10 RSTR: h7 BODY: h8 ]
                      [ _cat_n_1 LBL: h9 ARG0: x10 ]
                      [ _sleep_v_1 LBL: h11 ARG0: e12 ARG1: x10 ] >
              SLOTS: < ARG1: i2 ARG3: h4 >
              HCONS: < h7 qeq h9 u3 qeq h11 > ]"""

            broken_believe_the_cat_sleeps = """[ TOP: h00
              INDEX: e01
              RELS: < [ _believe_v_1 LBL: h00 ARG0: e01 ARG1: i02 ARG2: u03 ARG3: h04 ]
                      [ the_q LBL: h05 ARG0: x010 RSTR: h07 BODY: h08 ]
                      [ _cat_n_1 LBL: h09 ARG0: x010 ]
                      [ _sleep_v_1 LBL: h011 ARG0: e012 ARG1: x010 ] >
              SLOTS: < ARG1: i02 >
              HCONS: < h07 qeq h09 h04 qeq h011 > ]"""

            gold_sement_obj = sementcodecs.decode(believe_the_cat_sleeps)
            broken_sement_obj = sementcodecs.decode(broken_believe_the_cat_sleeps)

            overlapping_hcons, gold_hcons, broken_hcons = (sement_util
                .find_hcons_overlaps(gold_sement_obj, broken_sement_obj))

        Now, let's look at the overlapping handle constraints. Here we see that in both SEMENTs we have the QEQ relationship between the ``RSTR`` of the quantifier EP (``_the_q``) and the ``LBL`` of the ``_cat_n_1`` EP.

            .. code::

                # shows the hcons present in both SEMENTS
                print(overlapping_hcons)

                >>> [{'hi_role_set': ['the_q.RSTR'],
                        'lo_role_set': ['_cat_n_1.LBL'],
                        'gold_hi_var': 'h7',
                        'gold_lo_var': 'h9',
                        'actual_hi_var': 'h07',
                        'actual_lo_var': 'h09'}]


            Next, let's look at the handle constraints only present in the gold SEMENT. Here, we see the desired QEQ relationship between the ``ARG2`` of the ``_believe_v_1`` EP and the ``LBL`` of the ``_sleep_v_1`` EP.

            .. code::

                # shows the hcons present in only in the gold SEMENT
                print(gold_hcons)

                >>> [{'hi_role_set': ['_believe_v_1.ARG2'],
                        'lo_role_set': ['_sleep_v_1.LBL'],
                        'gold_hi_var': 'u3',
                        'gold_lo_var': 'h11'}]


            Last, let's look at the handle constraints unique to the broken SEMENT. Here, we have two sets. Here we see the error in the broken version: the high handle in the QEQ is the ``ARG3`` of the ``_believe_v_1`` EP rather than the ``ARG2``.

            .. code::

                # shows the hcons present in only in the "actual" SEMENT
                print(broken_hcons)

                >>> [{'hi_role_set': ['_believe_v_1.ARG3'],
                        'lo_role_set': ['_sleep_v_1.LBL'],
                        'actual_hi_var': 'h04',
                        'actual_lo_var': 'h011'}]


.. py:function:: _build_overlap_slots_table(overlap_slots)

        Make a table that displays which semantic slots are present in two SEMENTs.

        .. note::

            Shouldn't be used directly, but is a helper function that is used inside of  :py:func:`build_isomorphism_report`.

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: build-overlap-slots-table-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``overlap_slots``
              - ``list``
              - list of slots present in two SEMENTs

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: build-overlap-slots-table-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``str``
              - table representation of overlapping slots


        .. dropdown-syntax:: Example usage

            Result of calling :py:func:`_build_overlap_slots_table` on the given list of overlapping slots.

            .. code::

                import pogg.semantic_composition.sement_util as sement_util

                overlapping_slots = [{'slot': ['_believe_v_1.ARG1'],
                        'gold_var': 'i2',
                        'actual_var': 'i02'},
                    {'slot': ['_believe_v_1.ARG3'],
                        'gold_var': 'h4',
                        'actual_var': 'h04'}]

                print(sement_util._build_overlap_slots_table(overlapping_slots))

                >>> """
                    Slot Name              Gold Var    Actual Var
                    ---------------------  ----------  ------------
                    ['_believe_v_1.ARG1']  i2          i02
                    ['_believe_v_1.ARG3']  h4          h04
                    """


.. py:function:: _build_nonoverlap_slots_table(overlap_slots, table_type)

        Make a table that displays which slots are only present in one SEMENT.

        .. note::

            Shouldn't be used directly, but is a helper function that is used inside of  :py:func:`build_isomorphism_report`.

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: build-noverlap-slots-table-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``nonoverlap_slots``
              - ``list``
              - list of slots present in one SEMENT
            * - ``table_type``
              - ``str``
              - type of table, either ``"gold"`` or ``"actual"``

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: build-noverlap-slots-table-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``str``
              - table representation of nonoverlapping slots


        .. dropdown-syntax:: Example usage

            Result of calling :py:func:`_build_noverlap_slots_table` on the given list of slots from just one SEMENT.

            .. code::

                import pogg.semantic_composition.sement_util as sement_util

                nonoverlapping_role_eqs = [{'slot': ['_cozy_a_1.ARG1'],
                        'gold_var': 'i2'}]

                print(sement_util._build_nonoverlap_slots_table(nonoverlapping_role_slots, "gold"))

                >>> """
                    Slot Name           Gold Var
                    ------------------  ----------
                    ['_cozy_a_1.ARG1']  i2
                    """



.. py:function:: _build_overlap_eqs_table(overlap_eqs)

        Make a table that displays which semantic role equivalence sets are present in two SEMENTs.

        .. note::

            Shouldn't be used directly, but is a helper function that is used inside of  :py:func:`build_isomorphism_report`.

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: build-overlap-eqs-table-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``overlap_eqs``
              - ``list``
              - list of semantic role equivalencies present in two SEMENTs

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: build-overlap-eqs-table-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``str``
              - table representation of overlapping semantic role equivalencies


        .. dropdown-syntax:: Example usage

            Result of calling :py:func:`_build_overlap_eqs_table` on the given list of overlapping role equivalency sets.

            .. code::

                import pogg.semantic_composition.sement_util as sement_util

                overlapping_role_eqs = [{'eq_set': ['INDEX', '_cookie_n_1.ARG0','_tasty_a_1.ARG1'],
                        'gold_var': 'x4',
                        'actual_var': 'x04'},
                    {'eq_set': ['_tasty_a_1.ARG0'],
                        'gold_var': 'e1',
                        'actual_var': 'e01'}]

                print(sement_util._build_overlap_eqs_table(overlapping_role_eqs))

                >>> """
                    Role Set                                          Gold Var    Actual Var
                    ------------------------------------------------  ----------  ------------
                    ['INDEX', '_cookie_n_1.ARG0', '_tasty_a_1.ARG1']  x4          x04
                    ['_tasty_a_1.ARG0']                               e1          e01
                    """


.. py:function:: _build_nonoverlap_eqs_table(overlap_eqs, table_type)

        Make a table that displays which semantic role equivalence sets are only present in one SEMENT.

        .. note::

            Shouldn't be used directly, but is a helper function that is used inside of  :py:func:`build_isomorphism_report`.

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: build-noverlap-eqs-table-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``nonoverlap_eqs``
              - ``list``
              - list of semantic role equivalencies present in one SEMENT
            * - ``table_type``
              - ``str``
              - type of table, either ``"gold"`` or ``"actual"``

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: build-noverlap-eqs-table-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``str``
              - table representation of nonoverlapping semantic role equivalencies


        .. dropdown-syntax:: Example usage

            Result of calling :py:func:`_build_noverlap_eqs_table` on the given list of role equivalency sets from just one SEMENT.

            .. code::

                import pogg.semantic_composition.sement_util as sement_util

                nonoverlapping_role_eqs = [{'eq_set': ['TOP', '_cookie_n_1.LBL', '_tasty_a_1.LBL'],
                        'gold_var': 'h0'}]

                print(sement_util._build_nonoverlap_eqs_table(nonoverlapping_role_eqs, "gold"))

                >>> """
                    Role Set                                      Gold Var
                    --------------------------------------------  ----------
                    ['TOP', '_cookie_n_1.LBL', '_tasty_a_1.LBL']  h0
                    """


.. py:function:: _build_overlap_hcons_table(overlap_hcons)

        Make a table that displays which handle constraints are present in two SEMENTs.

        .. note::

            Shouldn't be used directly, but is a helper function that is used inside of  :py:func:`build_isomorphism_report`.

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: build-overlap-hcons-table-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``overlap_hcons``
              - ``list``
              - list of handle constraints present in two SEMENTs

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: build-overlap-hcons-table-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``str``
              - table representation of overlapping handle constraints


        .. dropdown-syntax:: Example usage

            Result of calling :py:func:`_build_overlap_hcons_table` on the given list of overlapping handle constraints.

            .. code::

                import pogg.semantic_composition.sement_util as sement_util

                overlapping_hcons = [{'hi_role_set': ['the_q.RSTR'],
                        'lo_role_set': ['_cat_n_1.LBL'],
                        'gold_hi_var': 'h7',
                        'gold_lo_var': 'h9',
                        'actual_hi_var': 'h07',
                        'actual_lo_var': 'h09'}]

                print(sement_util._build_overlap_hcons_table(overlapping_hcons))

                >>> """
                    Hi Role Set     Lo Role Set       Gold QEQ    Actual QEQ
                    --------------  ----------------  ----------  ------------
                    ['the_q.RSTR']  ['_cat_n_1.LBL']  h7 qeq h9   h07 qeq h09
                    """

.. py:function:: _build_nonoverlap_hcons_table(overlap_hcons, table_type)

        Make a table that displays which handle constraints are only present in one SEMENT.

        .. note::

            Shouldn't be used directly, but is a helper function that is used inside of  :py:func:`build_isomorphism_report`.

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: build-noverlap-hcons-table-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``nonoverlap_hcons``
              - ``list``
              - list of handle constraints present in one SEMENT
            * - ``table_type``
              - ``str``
              - type of table, either ``"gold"`` or ``"actual"``

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: build-noverlap-hcons-table-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``str``
              - table representation of nonoverlapping semantic role equivalencies


        .. dropdown-syntax:: Example usage

            Result of calling :py:func:`_build_noverlap_hcons_table` on the given list of handle constraints from just one SEMENT.

            .. code::

                import pogg.semantic_composition.sement_util as sement_util

                nonoverlapping_role_hcons = [{'hi_role_set': ['_believe_v_1.ARG2'],
                        'lo_role_set': ['_sleep_v_1.LBL'],
                        'gold_hi_var': 'u3',
                        'gold_lo_var': 'h11'}]

                print(sement_util._build_nonoverlap_hcons_table(nonoverlapping_role_hcons, "gold"))

                >>> """
                    Hi Role Set            Lo Role Set         Gold QEQ
                    ---------------------  ------------------  ----------
                    ['_believe_v_1.ARG2']  ['_sleep_v_1.LBL']  u3 qeq h11
                    """


.. py:function:: build_isomorphism_report(gold_sement, actual_sement)

        Print a report detailing which semantic role equivalencies and handle constraints are present in two SEMENTs. If two SEMENTs are not isomorphic, this can be used to pinpoint where the mismatch lies.

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: build-isomorphism-report-parameter-table
            :widths: 20, 10, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``gold_sement``
              - ``SEMENT``
              - a SEMENT, nominally the gold one
            * - ``actual_sement``
              - ``SEMENT``
              - a SEMENT, nominally the one to compare to the gold

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: build-isomorphism-report-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``str``
              - the isomorphism report


        .. dropdown-syntax:: Example usage

            Example of an isomorphism report between a SEMENT for *believe the cat kitten sleeps* and a broken version of the SEMENT. [#note]_ In the broken one, there is a handle constraint between the ``ARG3`` of the ``_believe_v_1`` EP and the ``LBL`` of the ``_sleep_v_1`` EP, but the first member of the constraint should instead be the ``ARG2`` of the ``_believe_v_1`` EP. Secondly, ``ARG0`` of ``_the_q``, ``ARG0`` of ``_cat_n_1``, and ``ARG1`` of ``_sleep_v_1`` should all be filled by the same variable, but in the broken one the ``ARG1`` for ``sleep_v_1`` isn't included in the identity.

            .. [#note]::

                Technically, they are both broken because we want the two argument version of ``_believe_v_1``, not the three argument version, but using the three argument version is better to make sure we can also show a slot discrepancy in the example report.

            .. code::

                import pogg.my_delphin.sementcodecs as sementcodecs
                import pogg.semantic_composition_sement_util as sement_util

                gold_sement_string = """[ TOP: h0
                  INDEX: e1
                  RELS: < [ _believe_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: h4 ]
                          [ _the_q LBL: h5 ARG0: x10 RSTR: h7 BODY: h8 ]
                          [ _cat_n_1 LBL: h9 ARG0: x10 ]
                          [ _sleep_v_1 LBL: h11 ARG0: e12 ARG1: x10 ] >
                  SLOTS: < ARG1: i2 ARG3: h4 >
                  HCONS: < h7 qeq h9 u3 qeq h11 > ]"""

                broken_sement_string = """[ TOP: h00
                  INDEX: e2
                  RELS: < [ _believe_v_1 LBL: h00 ARG0: e2 ARG1: i4 ARG2: u6 ARG3: h8 ]
                          [ _the_q LBL: h10 ARG0: x20 RSTR: h14 BODY: h16 ]
                          [ _cat_n_1 LBL: h18 ARG0: x20 ]
                          [ _sleep_v_1 LBL: h22 ARG0: e24 ARG1: x1010 ] >
                  SLOTS: < ARG1: i4 ARG2: u6 >
                  HCONS: < h14 qeq h18 h8 qeq h22 > ]"""

                gold_sement = sementcodecs.decode(gold_sement_string)
                broken_sement = sementcodecs.decode(broken_sement_string)

                report = sement_util.build_isomorphism_report(gold_sement, broken_sement)
                print(report)

                >>> """
                    --- GOLD SEMENT ---
                    [ TOP: h0
                      INDEX: e1
                      RELS: < [ _believe_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: h4 ]
                              [ _the_q LBL: h5 ARG0: x10 RSTR: h7 BODY: h8 ]
                              [ _cat_n_1 LBL: h9 ARG0: x10 ]
                              [ _sleep_v_1 LBL: h11 ARG0: e12 ARG1: x10 ] >
                      HCONS: < h7 qeq h9 u3 qeq h11 >
                      SLOTS: < ARG1: i2 ARG3: h4 > ]

                    --- ACTUAL SEMENT ---
                    [ TOP: h00
                      INDEX: e2
                      RELS: < [ _believe_v_1 LBL: h00 ARG0: e2 ARG1: i4 ARG2: u6 ARG3: h8 ]
                              [ _the_q LBL: h10 ARG0: x20 RSTR: h14 BODY: h16 ]
                              [ _cat_n_1 LBL: h18 ARG0: x20 ]
                              [ _sleep_v_1 LBL: h22 ARG0: e24 ARG1: x1010 ] >
                      HCONS: < h14 qeq h18 h8 qeq h22 >
                      SLOTS: < ARG1: i4 ARG2: u6 > ]


                    =====================
                    === DISCREPANCIES ===
                    =====================

                    SLOT DISCREPANCIES
                    ^^^^^^^^^^^^^^^^^^
                    GOLD ONLY
                    Slot Name          Gold Var
                    -----------------  ----------
                    _believe_v_1.ARG3  h4

                    ACTUAL ONLY
                    Slot Name          Actual Var
                    -----------------  ------------
                    _believe_v_1.ARG2  u6


                    SEMANTIC ROLE EQUIVALENCE DISCREPANCIES
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                    GOLD ONLY
                    Role Set                                             Gold Var
                    ---------------------------------------------------  ----------
                    ['_cat_n_1.ARG0', '_sleep_v_1.ARG1', '_the_q.ARG0']  x10

                    ACTUAL ONLY
                    Role Set                          Actual Var
                    --------------------------------  ------------
                    ['_cat_n_1.ARG0', '_the_q.ARG0']  x20
                    ['_sleep_v_1.ARG1']               x1010


                    HANDLE CONSTRAINT DISCREPANCIES
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                    GOLD ONLY
                    Hi Role Set            Lo Role Set         Gold QEQ
                    ---------------------  ------------------  ----------
                    ['_believe_v_1.ARG2']  ['_sleep_v_1.LBL']  u3 qeq h11

                    ACTUAL ONLY
                    Hi Role Set            Lo Role Set         Actual QEQ
                    ---------------------  ------------------  ------------
                    ['_believe_v_1.ARG3']  ['_sleep_v_1.LBL']  h8 qeq h22



                    =====================
                    === CONSISTENCIES ===
                    =====================

                    SLOT CONSISTENCIES
                    ^^^^^^^^^^^^^^^^^^
                    OVERLAPPING
                    Slot Name          Gold Var    Actual Var
                    -----------------  ----------  ------------
                    _believe_v_1.ARG1  i2          i4

                    SEMANTIC ROLE EQUIVALENCE CONSISTENCIES
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                    OVERLAPPING
                    Role Set                        Gold Var    Actual Var
                    ------------------------------  ----------  ------------
                    ['INDEX', '_believe_v_1.ARG0']  e1          e2
                    ['TOP', '_believe_v_1.LBL']     h0          h00
                    ['_believe_v_1.ARG1']           i2          i4
                    ['_believe_v_1.ARG2']           u3          u6
                    ['_believe_v_1.ARG3']           h4          h8
                    ['_cat_n_1.LBL']                h9          h18
                    ['_sleep_v_1.ARG0']             e12         e24
                    ['_sleep_v_1.LBL']              h11         h22
                    ['_the_q.BODY']                 h8          h16
                    ['_the_q.LBL']                  h5          h10
                    ['_the_q.RSTR']                 h7          h14

                    HANDLE CONSTRAINT CONSISTENCIES
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                    OVERLAPPING
                    Hi Role Set      Lo Role Set       Gold QEQ    Actual QEQ
                    ---------------  ----------------  ----------  ------------
                    ['_the_q.RSTR']  ['_cat_n_1.LBL']  h7 qeq h9   h14 qeq h18
                    """
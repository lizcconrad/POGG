pogg.semantic_composition.semantic_algebra
=============================================

The semantic algebra module contains the basic building blocks for composing semantic structures, specifically SEMENT structures.


Module Functions
------------------
.. py:function:: _get_slots(ep)

        Get the slots contributed by a particular EP to send into a SEMENT.

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: get-slots-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``ep``
              - ``delphin.MRS.EP``
              - EP (elementary predicate) object to get slots from

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - dict
              - dict of slots contributed by the EP


        .. dropdown-syntax:: Example usage

            Per the SEM-I, the EP (elementary predicate) for ``_give_v_1`` has up to three semantic arguments (the giver, the thing given, and who it is given to). Calling :py:func:`_get_slots` on this EP will result in the following dictionary:

            .. code::

                {
                    'give_v_1': {'ARG1': 'i1', 'ARG2': 'u2', 'ARG3': 'i3'}
                }



.. py:function:: create_base_SEMENT(pogg_config, predicate, intrinsic_variable_properties={})

        Make the base case SEMENT for a given predicate label, i.e. a SEMENT with only one EP in the RELS list before any composition has occurred.

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: create-base-SEMENT-parameter-table
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
              -
              - POGGConfig object that contains information about the SEMI and variable labeler
            * - ``predicate``
              - ``str``
              -
              - ERG predicate label
            * - ``intrinsic_variable_properties``
              - dict of ``str``:``str``
              - {}
              - optional dictionary of properties of the intrinsic variable, e.g. ``{'NUM': 'sg'}``

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: create-base-SEMENT-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``SEMENT``
              - newly created SEMENT with one EP in the RELS list


.. py:function:: create_CARG_SEMENT(pogg_config, predicate, carg_value, intrinsic_variable_properties={})

        Make a base case SEMENT for an EP with a CARG argument (e.g. ``named``, with a CARG value of *Liz*)

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: create-CARG-SEMENT-parameter-table
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
              -
              - POGGConfig object that contains information about the SEMI and variable labeler
            * - ``predicate``
              - ``str``
              -
              - ERG predicate label
            * - ``carg_value``
              - ``str``
              -
              - Value of the CARG slot, e.g. a proper name for the predicate ``named``
            * - ``intrinsic_variable_properties``
              - dict of ``str``:``str``
              - {}
              - optional dictionary of properties of the intrinsic variable, e.g. ``{'NUM': 'sg'}``

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: create-CARG-SEMENT-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``SEMENT``
              - newly created SEMENT with a single EP in the RELS list whose CARG value is filled by the provided argument

.. py:function:: op_non_scopal_argument_hook(functor, argument, slot_label)

        Perform non-scopal composition on two SEMENTs. The hook (i.e. the ``TOP`` and ``INDEX``) of the resulting SEMENT comes from the argument. Typically used when the functor is a modifier (e.g. *tasty cookie*)

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: op-non-scopal-arugment-hook-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``functor``
              - ``SEMENT``
              - SEMENT serving as the semantic functor, i.e. the one with the slot being plugged
            * - ``argument``
              - ``SEMENT``
              - SEMENT serving as the semantic argument, i.e. the one plugging the slot
            * - ``slot_label``
              - ``str``
              - label for the semantic argument slot in the functor that the argument is plugging (e.g. ``ARG1``)

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: op-non-scopal-argument-hook-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``SEMENT``
              - newly created SEMENT resulting from composition


        .. dropdown-syntax:: Example usage

            Example of performing non-scopal composition with SEMENTs for *eat* and *a cookie*. Notice that the ``TOP`` and ``INDEX`` match those from the original *ate* sement.

            .. code::

                tasty = sem_algebra.create_base_SEMENT(pogg_config, "_tasty_a_1")
                cookie = sem_algebra.create_base_SEMENT(pogg_config, "_cookie_n_1")

                # print the original SEMENTs
                print(sementcodecs.encode(tasty, indent=True))
                print(sementcodecs.encode(cookie, indent=True))

                >>> [ TOP: h3
                      INDEX: e1
                      RELS: < [ _tasty_a_1 LBL: h3 ARG0: e1 ARG1: u2 ] >
                      SLOTS: < ARG1: u2 > ]
                >>> [ TOP: h5
                      INDEX: x4
                      RELS: < [ _cookie_n_1 LBL: h5 ARG0: x4 ] > ]

                # perform composition
                tasty_cookie = sem_algebra.op_non_scopal_argument_hook(tasty, cookie, "ARG1")

                # print result
                print(sementcodecs.encode(tasty_cookie, indent=True))

                >>> [ TOP: h5
                      INDEX: x4
                      RELS: < [ _tasty_a_1 LBL: h3 ARG0: e1 ARG1: u2 ]
                              [ _cookie_n_1 LBL: h5 ARG0: x4 ] >
                      EQS: < h3 eq h5 u2 eq x4 > ]


.. py:function:: op_non_scopal_functor_hook(functor, argument, slot_label)

        Perform non-scopal composition on two SEMENTs. The hook of the resulting SEMENT comes from the functor. Typically used when the argument is a complement (e.g. *give a cookie*) or preposition (*in the park*)


        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: op-non-scopal-functor-hook-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``functor``
              - ``SEMENT``
              - SEMENT serving as the semantic functor, i.e. the one with the slot being plugged
            * - ``argument``
              - ``SEMENT``
              - SEMENT serving as the semantic argument, i.e. the one plugging the slot
            * - ``slot_label``
              - ``str``
              - label for the semantic argument slot in the functor that the argument is plugging (e.g. ``ARG1``)

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: op-non-scopal-functor-hook-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``SEMENT``
              - newly created SEMENT resulting from composition


        .. dropdown-syntax:: Example usage

            Example of performing non-scopal composition with SEMENTs for *tasty* and *cookie*. Notice that the ``TOP`` and ``INDEX`` match those from the original *cookie* sement.

            .. code::

                eat = sem_algebra.create_base_SEMENT(pogg_config, "_eat_v_1")
                a = sem_algebra.create_base_SEMENT(pogg_config, "_a_q")
                cookie = sem_algebra.create_base_SEMENT(pogg_config, "_cookie_n_1")

                # compose "a cookie" because arguments of verbs must be quantified
                a_cookie = sem_algebra.op_scopal_quantifier(a, cookie)

                # print the original SEMENTs
                print(sementcodecs.encode(eat, indent=True))
                print(sementcodecs.encode(a_cookie, indent=True))

                >>> [ TOP: h4
                      INDEX: e1
                      RELS: < [ _eat_v_1 LBL: h4 ARG0: e1 ARG1: i2 ARG2: i3 ] >
                      SLOTS: < ARG1: i2 ARG2: i3 > ]
                >>> [ TOP: h9
                      INDEX: x5
                      RELS: < [ _a_q LBL: h8 ARG0: x5 RSTR: h6 BODY: h7 ]
                              [ _cookie_n_1 LBL: h11 ARG0: x10 ] >
                      HCONS: < h6 qeq h11 >
                      EQS: < x5 eq x10 >
                      SLOTS: < BODY: h7 > ]

                # perform composition
                # plug ARG2 since that's the slot associated with the object of the verb
                eat_a_cookie = sem_algebra.op_non_scopal_functor_hook(eat, a_cookie, "ARG2")

                # print result
                print(sementcodecs.encode(eat_a_cookie, indent=True))

                >>> [ TOP: h4
                      INDEX: e1
                      RELS: < [ _eat_v_1 LBL: h4 ARG0: e1 ARG1: i2 ARG2: i3 ]
                              [ _a_q LBL: h8 ARG0: x5 RSTR: h6 BODY: h7 ]
                              [ _cookie_n_1 LBL: h11 ARG0: x10 ] >
                      HCONS: < h6 qeq h11 >
                      EQS: < x5 eq x10 h4 eq h9 i3 eq x5 >
                      SLOTS: < ARG1: i2 > ]


.. py:function:: op_scopal_argument_index(functor, argument, slot_label)

        Perform scopal composition where the ``INDEX`` comes from the argument, but the ``TOP`` comes from the functor. Used when the argument is a scopal modifier (e.g. *probably sleeps*).

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: op-scopal-argument-index-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``functor``
              - ``SEMENT``
              - SEMENT serving as the semantic functor, i.e. the one with the slot being plugged
            * - ``argument``
              - ``SEMENT``
              - SEMENT serving as the semantic argument, i.e. the one plugging the slot
            * - ``slot_label``
              - ``str``
              - label for the semantic argument slot in the functor that the argument is plugging (e.g. ``ARG1``)

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: op-scopal-argument-index-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``SEMENT``
              - newly created SEMENT resulting from composition

        .. dropdown-syntax:: Example usage

            Example of performing scopal composition with SEMENTs for *probably* and *sleeps*. Notice that the ``TOP`` comes from the original SEMENT for *probably*, while the ``INDEX`` comes from the original SEMENT for *sleeps*.

            .. code::

                probably = sem_algebra.create_base_SEMENT(pogg_config, "_probable_a_1")
                sleep = sem_algebra.create_base_SEMENT(pogg_config, "_sleep_v_1")

                # print the original SEMENTs
                print(sementcodecs.encode(probably, indent=True))
                print(sementcodecs.encode(sleep, indent=True))

                >>> [ TOP: h3
                      INDEX: i1
                      RELS: < [ _probable_a_1 LBL: h3 ARG0: i1 ARG1: u2 ] >
                      SLOTS: < ARG1: u2 > ]
                >>> [ TOP: h6
                      INDEX: e4
                      RELS: < [ _sleep_v_1 LBL: h6 ARG0: e4 ARG1: i5 ] >
                      SLOTS: < ARG1: i5 > ]

                # perform composition
                probably_sleeps = sem_algebra.op_scopal_argument_index(probably, sleep, "ARG1")

                # print result
                print(sementcodecs.encode(probably_sleeps, indent=True))

                >>> [ TOP: h3
                      INDEX: e4
                      RELS: < [ _probable_a_1 LBL: h3 ARG0: i1 ARG1: u2 ]
                              [ _sleep_v_1 LBL: h6 ARG0: e4 ARG1: i5 ] >
                      HCONS: < u2 qeq h6 > ]


.. py:function:: op_scopal_functor_index(functor, argument, slot_label)

        Perform scopal composition where the ``INDEX`` comes from the functor (as does the ``TOP``, but this is true for all versions of scopal composition). Used when the argument is a complement (e.g. "believes it's raining").

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: op-scopal-functor-index-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``functor``
              - ``SEMENT``
              - SEMENT serving as the semantic functor, i.e. the one with the slot being plugged
            * - ``argument``
              - ``SEMENT``
              - SEMENT serving as the semantic argument, i.e. the one plugging the slot
            * - ``slot_label``
              - ``str``
              - label for the semantic argument slot in the functor that the argument is plugging (e.g. ``ARG1``)

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: op-scopal-functor-index-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``SEMENT``
              - newly created SEMENT resulting from composition

        .. dropdown-syntax:: Example usage

            Example of performing scopal composition with SEMENTs for *believe* and *the kitten snores*. Notice that both the ``TOP`` and ``INDEX`` come from the original SEMENT for *believe*.

            .. code::

                believe = sem_algebra.create_base_SEMENT(pogg_config, "_believe_v_1")
                the = sem_algebra.create_base_SEMENT(pogg_config, "_the_q")
                kitten = sem_algebra.create_base_SEMENT(pogg_config, "_kitten_n_1")
                snore = sem_algebra.create_base_SEMENT(pogg_config, "_snore_v_1")

                # compose "the kitten snores"
                the_kitten = sem_algebra.op_scopal_quantifier(the, kitten)
                the_kitten_snores = sem_algebra.op_non_scopal_functor_hook(snore, the_kitten, "ARG1")

                # print the SEMENTs before scopal composition
                print(sementcodecs.encode(believe, indent=True))
                print(sementcodecs.encode(the_kitten_snores, indent=True))

                >>> [ TOP: h5
                      INDEX: e1
                      RELS: < [ _believe_v_1 LBL: h5 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: h4 ] >
                      SLOTS: < ARG1: i2 ARG2: u3 ARG3: h4 > ]
                >>> [ TOP: h15
                      INDEX: e13
                      RELS: < [ _snore_v_1 LBL: h15 ARG0: e13 ARG1: i14 ]
                              [ _the_q LBL: h9 ARG0: x6 RSTR: h7 BODY: h8 ]
                              [ _kitten_n_1 LBL: h12 ARG0: x11 ] >
                      HCONS: < h7 qeq h12 >
                      EQS: < x6 eq x11 h15 eq h10 i14 eq x6 > ]

                # perform composition
                believe_the_kitten_snores = sem_algebra.op_scopal_functor_index(believe, the_kitten_snores, "ARG2")

                # print result
                print(sementcodecs.encode(believe_the_kitten_snores, indent=True))

                >>> [ TOP: h5
                      INDEX: e1
                      RELS: < [ _believe_v_1 LBL: h5 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: h4 ]
                              [ _snore_v_1 LBL: h15 ARG0: e13 ARG1: i14 ]
                              [ _the_q LBL: h9 ARG0: x6 RSTR: h7 BODY: h8 ]
                              [ _kitten_n_1 LBL: h12 ARG0: x11 ] >
                      HCONS: < h7 qeq h12 u3 qeq h15 >
                      EQS: < x6 eq x11 h15 eq h10 i14 eq x6 >
                      SLOTS: < ARG1: i2 ARG3: h4 > ]


.. py:function:: op_scopal_quantifier(functor, argument, slot_label)

        Perform scopal composition between a quantifier SEMENT and a quantified SEMENT (e.g. *the cookie*). This involves the plugging of two slots (``ARG0`` directly and ``RSTR`` with a qeq) thus warranting a separate function.

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: op-scopal-quantifier-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``functor``
              - ``SEMENT``
              - SEMENT serving as the semantic functor, i.e. the quantifier
            * - ``argument``
              - ``SEMENT``
              - SEMENT serving as the semantic argument, i.e. the SEMENT being quantified

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: op-scopal-quantifier-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``SEMENT``
              - newly created SEMENT resulting from composition

        .. dropdown-syntax:: Example usage

            Example of performing scopal composition between a quantifier (*the*) and a SEMENT to be quantified (*cookie*). A few things are happening here:

            #. The ``ARG0`` of the quantifier is plugged by the ``INDEX`` of the argument SEMENT
            #. A QEQ relationship is established between the ``RSTR`` slot of the quantifier and the ``LBL`` of the argument SEMENT
            #. The ``TOP`` and ``INDEX`` both come from the quantifier

            Note that because the ``INDEX`` of the quantifier is the same as its own ``ARG0``, which was plugged by the ``INDEX`` of the quantified SEMENT (i.e. ``INDEX`` of *cookie*), the ``INDEX`` of the result represents the cookie, as we would expect for a phrase like *the cookie*.

            .. code::

                the = sem_algebra.create_base_SEMENT(pogg_config, "_the_q")
                cookie = sem_algebra.create_base_SEMENT(pogg_config, "_cookie_n_1")

                # print the original SEMENTs
                print(sementcodecs.encode(the, indent=True))
                print(sementcodecs.encode(cookie, indent=True))

                >>> [ TOP: h5
                      INDEX: x1
                      RELS: < [ _the_q LBL: h4 ARG0: x1 RSTR: h2 BODY: h3 ] >
                      SLOTS: < ARG0: x1 RSTR: h2 BODY: h3 > ]
                >>> [ TOP: h7
                      INDEX: x6
                      RELS: < [ _cookie_n_1 LBL: h7 ARG0: x6 ] > ]

                # perform composition
                the_cookie = sem_algebra.op_scopal_quantifier(the, cookie)

                # print result
                print(sementcodecs.encode(the_cookie, indent=True))

                >>> [ TOP: h5
                      INDEX: x1
                      RELS: < [ _the_q LBL: h4 ARG0: x1 RSTR: h2 BODY: h3 ]
                              [ _cookie_n_1 LBL: h7 ARG0: x6 ] >
                      HCONS: < h2 qeq h7 >
                      EQS: < x1 eq x6 >
                      SLOTS: < BODY: h3 > ]


.. py:function:: prepare_for_generation(pogg_config, sement)

        Prepare the given SEMENT for generation. In order to perform generationn, the ERG requires an MRS, not a SEMENT. The differences between an MRS and a SEMENT are described on the :doc:`Semantic Structures page </education/mrs>`.

        Additionally, the MRS must fulfill certain requirements. First, ERG requires that the ``INDEX`` be an event type. Second, there must be a GTOP handle which is QEQ to what was the final LTOP during composition.

        In order to modify a SEMENT into a suitable MRS, the following steps must be taken:

        #. Check if the ``INDEX`` is of type ``e``

           * If not:

              * check if given SEMENT is quantified, and wrap in generic quantifier if not

              * wrap in ``unknown`` event

        #. Create a new GTOP handle and set it to be QEQ to the SEMENT's previous ``TOP``
        #. Overwrite all ``EQS`` to one representative value
        #. Constrain all handles in handle constraints to be of type ``h``

            * sometimes the scopal argument's slot value starts out as type ``u`` but the ERG won't generate if both members of a handle constraint are not type ``h``

        Parameters
        ^^^^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: prepare-for-generation-parameter-table
            :widths: 20, 10, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Parameter
              - Type
              - Description
            * - ``pogg_config``
              - ``POGGConfig``
              - POGGConfig object that contains information about the SEMI and variable labeler
            * - ``sement``
              - ``SEMENT``
              - SEMENT to prepare to be sent to the ERG for generation

        Returns
        ^^^^^^^^
        .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
        .. list-table::
            :name: prepare-for-generation-returns-table
            :widths: 40, 70
            :class: longtable
            :header-rows: 1
            :align: left
            :width: 90%

            * - Return Type
              - Description
            * - ``SEMENT``
              - the prepared SEMENT

        .. note::
            The return type is still a SEMENT, but once the above changes have been made it can  be encoded to an MRS string with no loss of information. The biggest differences between an MRS and a SEMENT are the presence of the ``SLOTS`` and ``EQS`` lists in a SEMENT. This function involves collapsing all the ``EQS`` to be represented by one value, so the ``EQS`` list is empty after this operation. As far as ``SLOTS``, an MRS doesn't keep track of a list of unplugged slots, and they can be worked out by looking at the structure to see which EPs have semantic arguments whose variable value is not identified with anything else. Therefore when encoding the SEMENT resulting from this function into an MRS the ``EQS`` list is already empty and can be dropped, and the ``SLOTS`` list is unnecessary and may also be dropped.

        .. dropdown-syntax:: Example usage

            Example of the result of applying :py:func:`prepare_for_generation` to a SEMENT for *tasty cookie*.

            In order to generation sentence fragments, the noun phrase must be quantified, and be "wrapped" in a generic ``unknown`` EP whose ``ARG0`` is of type ``e`` to meet the generation requirements for the ERG. The ``TOP`` handle must also be switched to a GTOP (global top) that is QEQ to the final ``TOP`` (also called LTOP for local top) that resulted from composition.

            Also, notice that the ``EQS`` have all been collapsed. In the original SEMENT, there is an entry in the ``EQS`` list stating that ``u2 eq x4`` which represents the fact that the ``ARG1`` of ``_tasty_a_1`` is identified with the ``ARG0`` of ``_cookie_n_1``. In the result after calling ``prepare_for_generation`` notice that both of these slots are filled by the same value: ``x4``.

            .. code::

                tasty_sement = sem_algebra.create_base_SEMENT(pogg_config, "_tasty_a_1")
                cookie_sement = sem_algebra.create_base_SEMENT(pogg_config, "_cookie_n_1")
                tasty_cookie_sement = sem_algebra.op_non_scopal_argument_hook(tasty_sement, cookie_sement, "ARG1")
                print(sementcodecs.encode(tasty_cookie_sement, indent=True))

                >>> [ TOP: h5
                      INDEX: x4
                      RELS: < [ _tasty_a_1 LBL: h3 ARG0: e1 ARG1: u2 ]
                              [ _cookie_n_1 LBL: h5 ARG0: x4 ] >
                      EQS: < h3 eq h5 u2 eq x4 > ]

                # prepare for generation
                prepared_sement = sem_algebra.prepare_for_generation(pogg_config, tasty_cookie_sement)
                print(sementcodecs.encode(prepared_sement, indent=True))

                >>> [ TOP: h14
                      INDEX: e11
                      RELS: < [ unknown LBL: h10 ARG: x4 ARG0: e11 ]
                              [ def_udef_a_q LBL: h9 ARG0: x4 RSTR: h7 BODY: h8 ]
                              [ _tasty_a_1 LBL: h3 ARG0: e1 ARG1: x4 ]
                              [ _cookie_n_1 LBL: h3 ARG0: x4 ] >
                      HCONS: < h7 qeq h3 h14 qeq h10 > ]
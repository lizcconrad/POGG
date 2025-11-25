pogg.semantic_composition.semantic_algebra
=============================================

The semantic algebra module contains the SemanticAlgebra class, which itself contains the basic building blocks for composing semantic structures, specifically SEMENT structures.

Usage examples for the functions in this module can be found :doc:`here </pogg/semantic_composition/usage_nbs/sement_util_usage_with_output>`.

:::{dropdown} Dropdown Title
    :open:
    Dropdown content
:::

Public Classes
----------------

.. py:class:: SemanticAlgebra

    A SemanticAlgebra object contains functions for performing basic semantic composition


    Parameters
    ^^^^^^^^^^^
    .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
    .. list-table::
        :name: SemanticAlgebra-parameters-table
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


    Instance Attributes
    ^^^^^^^^^^^^^^^^^^^^
    .. tabularcolumns:: p{0.132\linewidth}p{0.198\linewidth}p{0.330\linewidth}
    .. list-table::
        :name: SemanticAlgebra-attributes-table
        :widths: 20, 30, 70
        :class: longtable
        :header-rows: 1
        :align: left
        :width: 90%

        * - Attribute
          - Type
          - Description
        * - ``pogg_config``
          - ``POGGConfig``
          - POGGConfig object that contains information about the SEMI and variable labeler


    Instance Methods
    ^^^^^^^^^^^^^^^^^
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


    .. py:function:: create_base_SEMENT(predicate, intrinsic_variable_properties={})

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


    .. py:function:: create_CARG_SEMENT(predicate, carg_value, intrinsic_variable_properties={})

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


    .. py:function:: prepare_for_generation(sement)

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
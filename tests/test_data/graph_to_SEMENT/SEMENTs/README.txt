Each SEMENT in this directory is named after the string/concept it aims to represent followed by _## indicating an "ID" for the file

This ID should be prepended to all variables in the file to avoid overlap with other SEMENTs when performing composition tests

For example, say you want to test making a compound_noun by reading in the SEMENT file for 'cake.txt' and 'vanilla.txt':

[
    TOP: h0
    INDEX: x1
    RELS: <
        [ _cake_n_1 LBL: h0 ARG0: x1 ]
    >
]


[
    TOP: h0
    INDEX: x1
    RELS: <
        [ _vanilla_n_1 LBL: h0 ARG0: x1 ]
    >
]

Because these SEMENTs both use h0 for the TOP and x1 for the INDEX, it'll result in an identity between the ARG0s of each predication, which we don't want

so instead, prepend some unique ID to each variable in a SEMENT file:

cake_00.txt
[
    TOP: h000
    INDEX: x001
    RELS: <
        [ _cake_n_1 LBL: h000 ARG0: x001 ]
    >
]

vanilla_01.txt
[
    TOP: h010
    INDEX: x011
    RELS: <
        [ _vanilla_n_1 LBL: h010 ARG0: x011 ]
    >
]

This is only relevant when using pre-existing SEMENT files for testing. When using the actual composition code SEMENTs created from scratch will have unique variables thanks to the variable iterator.
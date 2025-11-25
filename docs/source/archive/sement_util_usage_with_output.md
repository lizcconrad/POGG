# Usage examples for the `sement_util` module

The `sement_util` module contains a number of functions that are useful for manipulating, comparing, and printing SEMENT structures.


<details>
<summary>How do I dropdown?</summary>
<br>
This is how you dropdown.
</details>

------------



```python
import pprint
import pogg.my_delphin.sementcodecs as sementcodecs
import pogg.semantic_composition.sement_util as sement_util
```

## `group_equalities` example

Group equalities from a list of EQ pairs into EQ sets. That is, if the EQ list contains an eq ``(x1, x2)`` and an eq ``(x2, x3)`` then create a set ``(x1, x2, x3)`` such that they're in an equality "group"


```python
eqs = [("x1", "x2"), ("x3", "x4"), ("x1", "x4"), ("x5", "x6")]
grouped_eqs = sement_util.group_equalities(eqs)
print(grouped_eqs)
```

    [{'x5', 'x6'}, {'x1', 'x4', 'x2', 'x3'}]


## `get_most_specified_variable` example

Get the most "specific" variable to serve as the representative for the EQ set. That is, a variable of type ``x`` is more specific than one of type ``i``, according to the ERG hierarchy

### ERG Variable Type Hierarchy
| Type | Supertype(s) | Description |
|------|--------------|-------------|
| `u`  |              | unspecific |
| `i`  | `u`          | underspecified between `e` and `x` |
| `p`  | `u`          | underspecified between `h` and `x` |
| `e`  | `i`          | eventualities (e.g. intrinsic variable of a verb) |
| `x`  | `i`, `p`     | instance (e.g. intrinsic variable of a noun) |
| `h`  | `p`          | handle used for scopal composition |



## `overwrite_eqs` example

Example of `overwrite_eqs` being called on a SEMENT for *tasty cookie*. In the initial SEMENT, there is an EQ between the `ARG0` of *cookie* (`x1`) and the `ARG1` of *tasty*, because the `ARG1` of *cookie* (i.e. the thing that is tasty) is plugged by the intrinsic variable of *cookie*.

The `overwrite_eqs` function chooses one of these variables as the representative for the EQ (here, `x1`) and overwrites all instances of `x4` to also be ``x1``. This enables conversion to an MRS object in order to send the structure to the ERG for text generation.


```python
# SEMENT for "tasty cookie" before EQs are overwritten
sement_string = """[
    TOP: h0
    INDEX: x1
    RELS: <
        [ _tasty_a_1 LBL: h2 ARG0: e3 ARG1: x4 ]
        [ _cookie_n_1 LBL: h0 ARG0: x1 ] >
    EQS: < x1 eq x4 >
]"""

# convert string into SEMENT object
original_sement = sementcodecs.decode(sement_string)

new_sement = sement_util.overwrite_eqs(original_sement)

# encode the new_sement object into a string and print it
print(sementcodecs.encode(new_sement, indent=True))
```

    [ TOP: h0
      INDEX: x1
      RELS: < [ _tasty_a_1 LBL: h2 ARG0: e3 ARG1: x1 ]
              [ _cookie_n_1 LBL: h0 ARG0: x1 ] > ]


## `check_if_quantified` example

This function is used in cases where it's necessary to ensure that a SEMENT is quantified before proceeding with composition. For example, the argument of a verb must be plugged with a quantified noun (plus possible adjuncts). That is, it cannot be plugged with a SEMENT whose `RELS` list only contains one EP for *cookie*, but a SEMENT whose `RELS` list contains an EP for *cookie* and some quantifier.


```python
unquant_cookie = """[ TOP: h0
    INDEX: x1
    RELS: < [ _cookie_n_1 LBL: h0 ARG0: x1 ] >
]"""
unquant_cookie_sement_obj = sementcodecs.decode(unquant_cookie)

sement_util.check_if_quantified(unquant_cookie_sement_obj)
```




    False




```python
quant_cookie = """[ TOP: h6
    INDEX: x1
    RELS: <
        [ _udef_q LBL: h0 ARG0: x1 RSTR: h2 BODY: h3 ]
        [ _cookie_n_1 LBL: h4 ARG0: x5 ] >
    EQS: < x1 eq x5 >
    SLOTS: < BODY: h3 >
    HCONS: < h2 qeq h4 > ]"""

quant_cookie_sement_obj = sementcodecs.decode(quant_cookie)

sement_util.check_if_quantified(quant_cookie_sement_obj)
```




    True



## `is_sement_isomorphic` example

Here are two examples of `is_sement_isomorphic`. In the first one, the SEMENTs are isomorphic, but just have different variable names and different orders on the `RELS` lists, so the check returns `True`.


```python
sement1 = """[
    TOP: h0101
    INDEX: e1101 [e NUM: sg]
    RELS: <
        [ _a_q LBL: h10 ARG0: x11 RSTR: h12 BODY: h13]
        [ _cookie_n_1 LBL: h6 ARG0: x7 ]
        [ _give_v_1 LBL: h0 ARG0: e1 ARG1: i2 ARG2: u3 ARG3: i4 ]
    >
    EQS: < x11 eq x7 eq i2 h0101 eq h0 e1 eq e1101 >
    SLOTS: < ARG2: u3 ARG3: i4 >
    HCONS: < h12 qeq h6 >

]"""

sement2 = """[
    TOP: h011
    INDEX: e111 [e NUM: sg]
    RELS: <
        [ _give_v_1 LBL: h011 ARG0: e111 ARG1: i211 ARG2: u311 ARG3: i411 ]
        [ _a_q LBL: h1011 ARG0: x1111 RSTR: h1211 BODY: h1311]
        [ _cookie_n_1 LBL: h611 ARG0: x711 ]
    >
    EQS: < x1111 eq x711 x711 eq i211 >
    SLOTS: < ARG2: u311 ARG3: i411 >
    HCONS: < h1211 qeq h611 >

]"""

sement1_obj = sementcodecs.decode(sement1)
sement2_obj = sementcodecs.decode(sement2)

sement_util.is_sement_isomorphic(sement1_obj, sement2_obj)
```




    True



In the second example, the SEMENTs are almost isomorphic, but the `TOP` is identified with the `LBL` of the `_cookie_n_1` EP, rather than the `LBL` of the `_give_v_1` EP, causing a discrepancy.


```python
sement3 = """[
    TOP: h611
    INDEX: e111 [e NUM: sg]
    RELS: <
        [ _give_v_1 LBL: h011 ARG0: e111 ARG1: i211 ARG2: u311 ARG3: i411 ]
        [ _a_q LBL: h1011 ARG0: x1111 RSTR: h1211 BODY: h1311]
        [ _cookie_n_1 LBL: h611 ARG0: x711 ]
    >
    EQS: < x1111 eq x711 x711 eq i2 >
    SLOTS: < ARG2: u311 ARG3: i411 >
    HCONS: < h1211 qeq h611 >

]"""

sement3_obj = sementcodecs.decode(sement3)

# compare again to the first SEMENT
sement_util.is_sement_isomorphic(sement1_obj, sement3_obj)
```




    False



Detecting these differences at a glance is difficult, and the function `build_isomorphism_report` aims to alleviate this, but before going over an example of that a number of helper functions are used within `build_isomorphism_report` so let's go over those first.

## `create_variable_roles_dict` example

Given a SEMENT object, create a dictionary where each key is a variable in the SEMENT and the value is the set of semantic roles that variable fills. Having this information will help when comparing two SEMENTs.

Below is an example of calling it on a SEMENT for *a tasty cookie*




```python
sement_string = """[ TOP: h9
                  INDEX: x4
                  RELS: < [ _tasty_a_1 LBL: h0 ARG0: e1 ARG1: x4 ]
                          [ _cookie_n_1 LBL: h0 ARG0: x4 ]
                          [ _a_q LBL: h5 ARG0: x4 RSTR: h7 BODY: h8 ] >
                  SLOTS: < BODY: h8 >
                  HCONS: < h7 qeq h0 > ]"""

sement_object = sementcodecs.decode(sement_string)

roles_dict = sement_util.create_variable_roles_dict(sement_object)

pprint.pp(roles_dict)
```

    {'h9': ['TOP'],
     'x4': ['INDEX', '_a_q.ARG0', '_cookie_n_1.ARG0', '_tasty_a_1.ARG1'],
     'h0': ['_cookie_n_1.LBL', '_tasty_a_1.LBL'],
     'e1': ['_tasty_a_1.ARG0'],
     'h5': ['_a_q.LBL'],
     'h7': ['_a_q.RSTR'],
     'h8': ['_a_q.BODY']}


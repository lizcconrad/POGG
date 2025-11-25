# Usage examples for the `SemanticAlgebra` class

This notebook contains usage examples for the following functions in the `SemanticAlgebra` class:
- `_get_slots`
- `create_base_SEMENT`
- `create_CARG_SEMENT`
- `op_non_scopal_argument_hook`
- `op_non_scopal_functor_hook`
- `op_scopal_argument_index`
- `op_scopal_functor_index`
- `op_scopal_quantifier`
- `prepare_for_generation`


```python
from delphin import ace
from delphin.codecs import simplemrs
import pogg.my_delphin.sementcodecs as sementcodecs
from pogg.pogg_config import POGGConfig
from pogg.semantic_composition.semantic_algebra import SemanticAlgebra

pogg_config = POGGConfig("../data/config.yml")
semantic_algebra = SemanticAlgebra(pogg_config)
```

    /Users/lizcconrad/.venvs/pogg_tests/lib/python3.13/site-packages/delphin/semi.py:471: SemIWarning: _be_v_id: property 'NUM' not allowed on 'i'
      self._init_synopsis(pred, synopsis_data, propcache))
    /Users/lizcconrad/.venvs/pogg_tests/lib/python3.13/site-packages/delphin/semi.py:471: SemIWarning: one+less_a: property 'NUM' not allowed on 'i'
      self._init_synopsis(pred, synopsis_data, propcache))
    /Users/lizcconrad/.venvs/pogg_tests/lib/python3.13/site-packages/delphin/semi.py:471: SemIWarning: one+more_a: property 'NUM' not allowed on 'i'
      self._init_synopsis(pred, synopsis_data, propcache))
    /Users/lizcconrad/.venvs/pogg_tests/lib/python3.13/site-packages/delphin/semi.py:471: SemIWarning: poss: property 'NUM' not allowed on 'i'
      self._init_synopsis(pred, synopsis_data, propcache))


## `_get_slots` example

Per the SEM-I, the EP (elementary predicate) for ``_give_v_1`` has up to three semantic arguments (the giver, the thing given, and who it is given to). Calling :py:func:`_get_slots` on this EP will result in the following dictionary:

```
{
    'give_v_1': {'ARG1': 'i1', 'ARG2': 'u2', 'ARG3': 'i3'}
}
```

## `create_base_SEMENT` example

Creating a SEMENT for *toy*


```python
# create_base_SEMENT example
toy = semantic_algebra.create_base_SEMENT("_toy_n_1")
print(sementcodecs.encode(toy))
```

    [ TOP: h2 INDEX: x1 RELS: < [ _toy_n_1 LBL: h2 ARG0: x1 ] > ]


## `create_CARG_SEMENT` example

Creating a SEMENT for *Liz*


```python
# create_CARG_SEMENT example
liz = semantic_algebra.create_CARG_SEMENT("named", "Liz")
print(sementcodecs.encode(liz))
```

    [ TOP: h4 INDEX: x3 RELS: < [ named LBL: h4 ARG0: x3 CARG: "Liz" ] > ]


## `op_non_scopal_argument_hook` example

Composing a SEMENT for *tasty cookie*


```python
# make base SEMENTs
tasty = semantic_algebra.create_base_SEMENT("_tasty_a_1")
cookie = semantic_algebra.create_base_SEMENT("_cookie_n_1")

# print the original SEMENTs
print(sementcodecs.encode(tasty, indent=True))
print(sementcodecs.encode(cookie, indent=True))
```

    [ TOP: h7
      INDEX: e5
      RELS: < [ _tasty_a_1 LBL: h7 ARG0: e5 ARG1: u6 ] >
      SLOTS: < ARG1: u6 > ]
    [ TOP: h9
      INDEX: x8
      RELS: < [ _cookie_n_1 LBL: h9 ARG0: x8 ] > ]



```python
# perform composition
tasty_cookie = semantic_algebra.op_non_scopal_argument_hook(tasty, cookie, "ARG1")

# print result
print(sementcodecs.encode(tasty_cookie, indent=True))
```

    [ TOP: h9
      INDEX: x8
      RELS: < [ _tasty_a_1 LBL: h7 ARG0: e5 ARG1: u6 ]
              [ _cookie_n_1 LBL: h9 ARG0: x8 ] >
      EQS: < h7 eq h9 u6 eq x8 > ]


## `op_non_scopal_functor_hook` example

Composing a SEMENT for *eat a cookie*


```python
# make base SEMENTs
eat = semantic_algebra.create_base_SEMENT("_eat_v_1")
a = semantic_algebra.create_base_SEMENT("_a_q")
cookie = semantic_algebra.create_base_SEMENT("_cookie_n_1")

# compose "a cookie" because arguments of verbs must be quantified
a_cookie = semantic_algebra.op_scopal_quantifier(a, cookie)

# print the original SEMENTs
print(sementcodecs.encode(eat, indent=True))
print(sementcodecs.encode(a_cookie, indent=True))
```

    [ TOP: h13
      INDEX: e10
      RELS: < [ _eat_v_1 LBL: h13 ARG0: e10 ARG1: i11 ARG2: i12 ] >
      SLOTS: < ARG1: i11 ARG2: i12 > ]
    [ TOP: h18
      INDEX: x14
      RELS: < [ _a_q LBL: h17 ARG0: x14 RSTR: h15 BODY: h16 ]
              [ _cookie_n_1 LBL: h20 ARG0: x19 ] >
      HCONS: < h15 qeq h20 >
      EQS: < x14 eq x19 >
      SLOTS: < BODY: h16 > ]



```python
# perform composition
# plug ARG2 since that's the slot associated with the object of the verb
eat_a_cookie = semantic_algebra.op_non_scopal_functor_hook(eat, a_cookie, "ARG2")

# print result
print(sementcodecs.encode(eat_a_cookie, indent=True))
```

    [ TOP: h13
      INDEX: e10
      RELS: < [ _eat_v_1 LBL: h13 ARG0: e10 ARG1: i11 ARG2: i12 ]
              [ _a_q LBL: h17 ARG0: x14 RSTR: h15 BODY: h16 ]
              [ _cookie_n_1 LBL: h20 ARG0: x19 ] >
      HCONS: < h15 qeq h20 >
      EQS: < x14 eq x19 h13 eq h18 i12 eq x14 >
      SLOTS: < ARG1: i11 > ]


## `op_scopal_argument_index` example

Composting a SEMENT for *probably sleeps*


```python
# make base SEMENTs
probably = semantic_algebra.create_base_SEMENT("_probable_a_1")
sleep = semantic_algebra.create_base_SEMENT("_sleep_v_1")

# print the original SEMENTs
print(sementcodecs.encode(probably, indent=True))
print(sementcodecs.encode(sleep, indent=True))
```

    [ TOP: h23
      INDEX: i21
      RELS: < [ _probable_a_1 LBL: h23 ARG0: i21 ARG1: u22 ] >
      SLOTS: < ARG1: u22 > ]
    [ TOP: h26
      INDEX: e24
      RELS: < [ _sleep_v_1 LBL: h26 ARG0: e24 ARG1: i25 ] >
      SLOTS: < ARG1: i25 > ]



```python
# perform composition
probably_sleeps = semantic_algebra.op_scopal_argument_index(probably, sleep, "ARG1")

# print result
print(sementcodecs.encode(probably_sleeps, indent=True))
```

    [ TOP: h23
      INDEX: e24
      RELS: < [ _probable_a_1 LBL: h23 ARG0: i21 ARG1: u22 ]
              [ _sleep_v_1 LBL: h26 ARG0: e24 ARG1: i25 ] >
      HCONS: < u22 qeq h26 > ]


## `op_scopal_functor_index` example
Composing a SEMENT for *know the kitten snores*.


```python
# make base SEMENTs
know = semantic_algebra.create_base_SEMENT("_know_v_1")
the = semantic_algebra.create_base_SEMENT("_the_q")
kitten = semantic_algebra.create_base_SEMENT("_kitten_n_1")
snore = semantic_algebra.create_base_SEMENT("_snore_v_1")

# compose "the kitten snores"
the_kitten = semantic_algebra.op_scopal_quantifier(the, kitten)
the_kitten_snores = semantic_algebra.op_non_scopal_functor_hook(snore, the_kitten, "ARG1")

# print the SEMENTs before scopal composition
print(sementcodecs.encode(know, indent=True))
print(sementcodecs.encode(the_kitten_snores, indent=True))
```

    [ TOP: h30
      INDEX: e27
      RELS: < [ _know_v_1 LBL: h30 ARG0: e27 ARG1: u28 ARG2: i29 ] >
      SLOTS: < ARG1: u28 ARG2: i29 > ]
    [ TOP: h40
      INDEX: e38
      RELS: < [ _snore_v_1 LBL: h40 ARG0: e38 ARG1: i39 ]
              [ _the_q LBL: h34 ARG0: x31 RSTR: h32 BODY: h33 ]
              [ _kitten_n_1 LBL: h37 ARG0: x36 ] >
      HCONS: < h32 qeq h37 >
      EQS: < x31 eq x36 h40 eq h35 i39 eq x31 > ]



```python
# perform composition
know_the_kitten_snores = semantic_algebra.op_scopal_functor_index(know, the_kitten_snores, "ARG2")

# print result
print(sementcodecs.encode(know_the_kitten_snores, indent=True))
```

    [ TOP: h30
      INDEX: e27
      RELS: < [ _know_v_1 LBL: h30 ARG0: e27 ARG1: u28 ARG2: i29 ]
              [ _snore_v_1 LBL: h40 ARG0: e38 ARG1: i39 ]
              [ _the_q LBL: h34 ARG0: x31 RSTR: h32 BODY: h33 ]
              [ _kitten_n_1 LBL: h37 ARG0: x36 ] >
      HCONS: < h32 qeq h37 i29 qeq h40 >
      EQS: < x31 eq x36 h40 eq h35 i39 eq x31 >
      SLOTS: < ARG1: u28 > ]


## `op_scopal_quantifier` example

Compose a SEMENT for *the cookie*


```python
the = semantic_algebra.create_base_SEMENT("_the_q")
cookie = semantic_algebra.create_base_SEMENT("_cookie_n_1")

# print the original SEMENTs
print(sementcodecs.encode(the, indent=True))
print(sementcodecs.encode(cookie, indent=True))
```

    [ TOP: h45
      INDEX: x41
      RELS: < [ _the_q LBL: h44 ARG0: x41 RSTR: h42 BODY: h43 ] >
      SLOTS: < ARG0: x41 RSTR: h42 BODY: h43 > ]
    [ TOP: h47
      INDEX: x46
      RELS: < [ _cookie_n_1 LBL: h47 ARG0: x46 ] > ]



```python
# perform composition
the_cookie = semantic_algebra.op_scopal_quantifier(the, cookie)

# print result
print(sementcodecs.encode(the_cookie, indent=True))
```

    [ TOP: h45
      INDEX: x41
      RELS: < [ _the_q LBL: h44 ARG0: x41 RSTR: h42 BODY: h43 ]
              [ _cookie_n_1 LBL: h47 ARG0: x46 ] >
      HCONS: < h42 qeq h47 >
      EQS: < x41 eq x46 >
      SLOTS: < BODY: h43 > ]


## `prepare_for_generation` example

Most of the SEMENTs above don't produce output when sent to the ERG for generation. A few requirements must be met for the ERG to generate from a semantic structure, namely:

1. The top level `INDEX` must be of type `e`
2. All entities whose intrinsic variable is of type `x` must be quantified (i.e. nouns must be quantified)
3. The `TOP` handle must be a newly introduced "GTOP" which is QEQ to the "last" TOP from composition

The function `prepare_for_generation` checks if these requirements have been met for a given SEMENT and performs additional composition operations if not to make it suitable for generation.[^bignote]

[^bignote]: Regarding requirement #2, the `prepare_for_generation` function can only quantify the top level unquantified nominal phrase. For example, if you wish to generate fragments from a SEMENT that roughly corresponds to *cookies in boxes* then the SEMENT passed to `prepare_for_generation` must already have an implicit quantifier for *boxes*; this implicit quantifier should have been inserted before composing with *in*. But the head noun *cookies* may be unquantified and get "fixed" when going through `prepare_for_generation`.

This last example runs some of the SEMENTs that have been created thus far through `prepare_for_generation` and then prints the results of actually trying to generate from them.


```python
# function to wrap the ACE generation code
def generate(sement):
    # encode into MRS string, since that's the format the ERG needs
    mrs_string = simplemrs.encode(sement, indent=True)

    with ace.ACEGenerator(semantic_algebra.pogg_config.grammar_location, ['-r', 'root_frag']) as generator:
        print("\n\nGENERATING FROM ... ")
        print("{}\n".format(mrs_string))
        generator_response = generator.interact(mrs_string)
        print("GENERATED RESULTS ... ")
        for r in generator_response.results():
            print(r.get('surface'))
        print("\n\n")
```


```python
tasty_cookie_prepared = semantic_algebra.prepare_for_generation(tasty_cookie)
print("BEFORE PREPARATION...\n{}".format(sementcodecs.encode(tasty_cookie, indent=True)))
generate(tasty_cookie_prepared)
```

    BEFORE PREPARATION...
    [ TOP: h9
      INDEX: x8
      RELS: < [ _tasty_a_1 LBL: h7 ARG0: e5 ARG1: u6 ]
              [ _cookie_n_1 LBL: h9 ARG0: x8 ] >
      EQS: < h7 eq h9 u6 eq x8 > ]
    
    
    GENERATING FROM ... 
    [ TOP: h56
      INDEX: e53
      RELS: < [ unknown LBL: h52 ARG: x48 ARG0: e53 ]
              [ def_udef_a_q LBL: h51 ARG0: x48 RSTR: h49 BODY: h50 ]
              [ _tasty_a_1 LBL: h9 ARG0: e5 ARG1: x48 ]
              [ _cookie_n_1 LBL: h9 ARG0: x48 ] >
      HCONS: < h49 qeq h9 h56 qeq h52 > ]
    
    GENERATED RESULTS ... 
    The tasty cookie
    Tasty cookies
    A tasty cookie
    The tasty cookies
    The tasty cookies.
    Tasty cookie
    Tasty cookies.
    The tasty cookie.
    A tasty cookie.
    Tasty cookie.
    
    
    


    NOTE: 165 passive, 314 active edges in final generation chart; built 294 passives total. [10 results]
    NOTE: generated 1 / 1 sentences, avg 4452k, time 0.43931s
    NOTE: transfer did 188 successful unifies and 304 failed ones



```python
know_the_kitten_snores_prepared = semantic_algebra.prepare_for_generation(know_the_kitten_snores)
print("BEFORE PREPARATION...\n{}".format(sementcodecs.encode(know_the_kitten_snores_prepared, indent=True)))
generate(know_the_kitten_snores_prepared)
```

    BEFORE PREPARATION...
    [ TOP: h57
      INDEX: e27
      RELS: < [ _know_v_1 LBL: h30 ARG0: e27 ARG1: u28 ARG2: h58 ]
              [ _snore_v_1 LBL: h35 ARG0: e38 ARG1: x31 ]
              [ _the_q LBL: h34 ARG0: x31 RSTR: h32 BODY: h33 ]
              [ _kitten_n_1 LBL: h37 ARG0: x31 ] >
      HCONS: < h32 qeq h37 h58 qeq h35 h57 qeq h30 >
      SLOTS: < ARG1: u28 > ]
    
    
    GENERATING FROM ... 
    [ TOP: h57
      INDEX: e27
      RELS: < [ _know_v_1 LBL: h30 ARG0: e27 ARG1: u28 ARG2: h58 ]
              [ _snore_v_1 LBL: h35 ARG0: e38 ARG1: x31 ]
              [ _the_q LBL: h34 ARG0: x31 RSTR: h32 BODY: h33 ]
              [ _kitten_n_1 LBL: h37 ARG0: x31 ] >
      HCONS: < h32 qeq h37 h58 qeq h35 h57 qeq h30 > ]
    
    GENERATED RESULTS ... 
    To know the kitten to snore.
    To know the kittens to snore.
    To know the kitten to snore
    To know the kittens to snore
    
    
    


    NOTE: 638 passive, 401 active edges in final generation chart; built 680 passives total. [4 results]
    NOTE: generated 1 / 1 sentences, avg 12043k, time 0.44483s
    NOTE: transfer did 315 successful unifies and 423 failed ones


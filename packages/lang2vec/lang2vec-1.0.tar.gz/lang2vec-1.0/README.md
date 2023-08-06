lang2vec
=======

A simple library for querying the [URIEL typological database](http://www.cs.cmu.edu/~dmortens/uriel.html).

Installation
------------
Run ``pip install lang2vec``.


Usage
-----
The library currently supports a simple operation: querying the URIEL database.
The main operation is ``get_features(languages, feature_sets, header=False, minimal=False)``, which returns a dictionary with the feature vector for every language in ``languages`` for the ``feature_sets``.


A minimal working example is:
~~~~
>>> import lang2vec.lang2vec as l2v
>>> features = l2v.get_features("eng", "geo")
>>> features["eng"]
[0.7664999961853027, 0.7924000024795532, 0.8277999758720398, 0.7214000225067139,...]
~~~~

The first argument of ``get_features()`` is either a list or a space-separated string of ISO 639-3 codes (e.g. ``["deu", "eng"]``).
Any two letter codes ISO 639-1 codes will be mapped to their corresponding ISO-639-3 codes.

~~~~
>>> features = l2v.get_features(["eng", "fra"], "geo")
>>> features["fra"]
[0.7378000020980835, 0.7682999968528748, 0.7982000112533569, 0.6941999793052673, ...]
~~~~


You can list the supported languages with ``lang2vec.LANGUAGES`` or with ``lang2vec.available_languages()``.

The second argument is a named feature set, provided as either a string, or a list of strings, or an elementwise union A|B of two feature sets, or a concatenation A+B of two feature sets.  So "geo+syntax_wals|syntax_sswl" gives the geographical feature vector concatenated with the elementwise union of the WALS and SSWL syntax feature sets.

Note that concatenations of unions are allowed, but unions of concatenations are not. Also, the union of two feature sets is restricted to sets with different sizes. A good rule of thumb is that two sets have similar sizes if their names start with the same word (`"inventory", "phonology", "syntax"`).

We also provide helper functions ``fs_union()`` and ``fs_concatenation()``. They are "overloaded" so that they can receive an arbitrary number of feature set arguments or a list of feature sets. Some examples:
~~~~
>>> import lang2vec as l2v
>>> l2v.fs_union("syntax_wals", "syntax_sswl")
'syntax_wals|syntax_sswl'

>>> l2v.fs_union(["syntax_wals", "syntax_sswl"])
'syntax_wals|syntax_sswl'

>>> l2v.fs_concatenation( ["geo", l2v.fs_union(["syntax_wals", "syntax_sswl"])])
'geo+syntax_wals|syntax_sswl'

>>> features = l2v.get_features("eng", l2v.fs_concatenation( ["geo", l2v.fs_union(["syntax_wals", "syntax_sswl"])]))
>>> features['eng'][:5]
[0.7664999961853027, 0.7924000024795532, 0.8277999758720398, 0.7214000225067139, 0.8568999767303467]
~~~~

The available feature sets can be listed with ``lang2vec.FEATURE_SETS`` or with ``lang2vec.available_feature_sets()``.
We list them here too:

* Sets from feature and inventory databases:
    * "syntax_wals",
    * "phonology_wals",
    * "syntax_sswl",
    * "syntax_ethnologue",
    * "phonology_ethnologue",
    * "inventory_ethnologue",
    * "inventory_phoible_aa",
    * "inventory_phoible_gm",
    * "inventory_phoible_saphon",
    * "inventory_phoible_spa",
    * "inventory_phoible_ph",
    * "inventory_phoible_ra",
    * "inventory_phoible_upsid",

* Averages of sets:
    * "syntax_average",
    * "phonology_average",
    * "inventory_average",

* KNN predictions of feature values:
    * "syntax_knn",
    * "phonology_knn",
    * "inventory_knn",

* Membership in language families and subfamilies:
    * "fam",

* Distance from fixed points on Earth's surface
    * "geo",
    
* One-hot identity vector:
    * "id",


There are two optional arguments to ``get_features(langueages, features_sets, header=False, minimal=False)``.
Setting ``header=True`` will also return the feature names in a special dictionary entry ``'CODE'``. For example:
~~~~
>>> features = l2v.get_features("eng", "syntax_wals", header=True)
>>> features['CODE'][:5]
['S_SVO', 'S_SOV', 'S_VSO', 'S_VOS', 'S_OVS']
~~~~

Setting ``minimal=True`` will suppress the columns that contain only zeros, only ones, or only nulls.

The "minimal" transformation applies after any union or concatenation.  (If it did not, sets in the same group, like the syntax_* sets, would not be the same dimensionality for comparison.) 



REFERENCES:
-----------

The different sets above are derived from many sources:

* _wals : Features derived from the World Atlas of Language Structures.
* _sswl : Features derived from Syntactic Structures of the World's Languages.
* _ethnologue : Features derived from (shallowly) parsing the prose typological descriptions in Ethnologue (Lewis et al. 2015).
* _phoible_aa : AA = Alphabets of Africa. Features derived from PHOIBLE's normalization of *Systèmes alphabétiques des langues africaines* (Hartell 1993, Chanard 2006).
* _phoible_gm : GM = Green and Moran.  Features derived from PHOIBLE's normalization of Christopher Green and Steven Moran's pan-African inventory database.
* _phoible-ph : PH = PHOIBLE.  Features derived from PHOIBLE proper, by Moran, McCloy, and Wright (2012).
* _phoible-ra : RA = Ramaswami.  Features derived from PHOIBLE's normalization of *Common Linguistic Features in Indian Languages: Phonetics* (Ramaswami 1999).
* _phoible-saphon : SAPHON = South American Phonological Inventory Database.  Features derived from PHOIBLE's normalization of SAPHON (Lev et al. 2012).
* _phoible-spa : SPA = Stanford Phonology Archive.  Features derived from PHOIBLE's normalization of SPA (Crothers et al., 1979).
* _phoible-upsid : UPSID = UCLA Phonological Segment Inventory Database.  Features derived from PHOIBLE's normalization of UPSID (Maddieson 1984, Maddieson and Precoda 1990).


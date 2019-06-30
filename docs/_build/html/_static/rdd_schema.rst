Rule Deck Database
==================

.. The Rule Deck Database (RDD) is the proposed database schema for describing 
.. a fabrication process and general settings. The process data defined in the
.. RDD can be used as parameters when creating PCells. The general settings
.. can include any extra or necessary data that you might want to connect to the
.. framework. For example, the data in the .ldf file compatible with InductEx
.. can easily be translated to the RDD schema.
.. The RDD is divided into the following different categories. These categories
.. can easily be expanded by the development team due to the simplicity of
.. hooking Python classes to the RDD script:

.. * **GDSII related data**: Unique data that can be parsed by the GDSII file format. Dumpy layers, terminals and text layers settings.

.. * **Process data**: Layer definitions, purpose layer and pattern layers can be described.

.. * **Design Rules**: Design rules variables can be defined and hooked to Rule Classes.

.. * **Primitive description**: Template Cells can be hooked to primitive cells, such as vias, which defines the boolean operations for detection.

.. * **Material stacking**: List vertical configuration of specific material stacks. Boolean operations are used before 3D model extrusion (still very experimental).

.. The following examples will illustrate each of the mentioned categories. First the database have to initialized and given a name and then process layers can be added.

.. .. code-block:: python
..     :linenos:

..     from spira.yevon.rdd import get_rule_deck
..     from spira.yevon.rdd.technology import ProcessTree

..     print('Initializing Rule Deck Library...')

..     RDD = get_rule_deck()

..     RDD.name = 'MiTLL'

..     # Define new process tree.
..     RDD.METALS = ProcessTree()

..     # Define new process layer.
..     RDD.METALS.M5 = ProcessTree()
..     RDD.METALS.M5.LAYER = 50
..     RDD.METALS.M5.THICKNESS = 0.5
..     RDD.METALS.M5.LAMBDA = 0.5

.. GDSII related data can be added by simple creating a data tree.
 
.. .. code-block:: python
..     :linenos:

..     RDD.GDSII = DataTree ()
..     RDD.GDSII.TERM = 63
..     RDD.GDSII.TEXT = 64

.. Design Rules can be categorized using the rule tree class provided by the
.. framework.

.. .. code-block:: python
..     :linenos:

..     RDD.RULES = DataTree ()
..     RDD.RULES.ENCLOSURE = RuleTree ()

..     # Define enclosure rule for layers J5 and M6.
..     RDD.RULES.ENCLOSURE += Enclosure (
..         layer1 = RDD.VIAS.J5.LAYER,
..         layer2 = RDD.METALS.M6.LAYER,
..         minimum = 0.3
..     )

..     # Define enclosure rule for layers C5 and M6.
..     RDD.RULES.ENCLOSURE += Enclosure (
..         layer1 = RDD.VIAS.C5.LAYER,
..         layer2 = RDD.METALS.M6.LAYER,
..         minimum = 0.35
..     )

.. Primitives are detected from the hand-designed layout using Template Cells
.. that describes the pattern recognition algorithm.

.. .. code-block:: python
..     :linenos:

..     RDD.VIAS.J5.PCELL = ViaTemplate (
..         name = 'J5',
..         via_layer = RDD.VIAS.J5,
..         layer1 = RDD.METALS.M5,
..         layer2 = RDD.METALS.M6
..     )

.. Switching between databases based on different process technologies are done
.. by simply importing the specific process RDD file.

.. .. code-block:: python
..     :linenos:

..     >>> import spira.all as spira
..     >>> from spira.yevon.rdd.settings import get_rule_deck
..     >>> RDD = get_rule_deck()
..     >>> RDD.name
..     'MiTLL'
..     >>> from pdks import aist
..     >>> RDD.name
..     'AiST'

.. It is possible to analyze the data contained in the tree objects.

.. .. code-block:: python
..     :linenos:

..     >>> RDD.METALS.keys
..     ['GP', 'RES', 'BAS', 'COU', 'CTL']



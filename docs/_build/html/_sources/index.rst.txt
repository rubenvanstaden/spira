Welcome to the SPiRA Framework!
===============================

Parameterized Cells (PCells) are key components used to increase flexibility and productivity during layout design.
Creating a parameterized cell integrates all design information into one place.
The development and maintenance of PCell libraries typically requires device knowledge and advanced programming skills.

Integrated circuit design requires many different levels of analysis. A lot of component design is done using a manual
design flow, from SPICE simulations, to parameter extraction. While at the same time, circuit design requires abstraction
at a much higher level.

**SPiRA** is a parametric design framework for Superconductor and Quantum Integrated Circuit (SQIC) design.
It revolves around the sound engineering concept that creating circuit layouts are prone to unexpected design errors.
The design process is highly dependent on data provided by the fabrication process.
In SPiRA, parameterized cells can be generated that interactively binds data from any fabrication process.
A novel design method is introduced, called *validate-by-design*, that integrates parameter restrictions
into the design flow, which limits a designer from breaking process design rules.

SPiRA integrates different aspects into a single framework, where a parameterized cell can be defined once
and then used throughout the design process, performing automatic device detection, netlist extraction, and
design rule checking. Consequently, errors are significantly reduced by using the same component definition throughout the entire design flow.

Lore
----

*Spira* is the fictional world of the Square role-playing video game Final Fantasy X.
The name Spira refers to the word "spiral", alluding to one of the main themes of Final Fantasy X: *continuity*.
The word "spiral" has multiple meanings depending on context. In geometry, it is a curve acting as the focus
of a point rotating around a fixed point that continuously extends from that point.
The inspiration behind the fictional Spira world, according to the producer Yoshinori Kitase,
is the heuristic that players prefer a "*simple fantasy world*" over a more science fiction world.

**The reason for naming this framework SPiRA:**

The aim is to develop a *continuous design environment* for IC engineers to design circuit layouts,
with focus falling on a *simple script-based methodology*. The **SPiRA core** is the *focus point*
that revolves around the single idea of parameterizing layout geometries.

**Basic termnology before getting started:**

1. **PCell** (Parameterized Cell): Also refered to as a *layout generator* is a cell that defines how layout elements must be generated based on a given set of parameters.
2. **RDD** (Rule Deck Database): A novel script-based approach to develop a Process Design Kit (PDK).

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    _0_methodology
    _1_overview
    _2_basic
    _3_advanced
    _4_reference
    _5_developers


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

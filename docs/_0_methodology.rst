###########
Methodology
###########

Using general mathematics and science as an analogy, a basic understanding
can be constructed of the importance of software in IC design: *Mathematics is
the discipline of proving provable statements true and science is the discipline
of proving provable statements false*. 

***************************************
The Importance of Software in IC Design
***************************************

In software development, testing shows the presence of bugs and not the absence thereof. Software development is not
a mathematical endeavour, even though it seems to manipulate mathematical
constructs. Rather, software is more connected to science in the sense that it
shows correctness by failing to show incorrectness. Therefore, IC design is to
some extent only as good as the software systems that can prove the design
incorrect. Circuit verification software only shows the engineer where
mistakes are made, if any.

Structured programming elicits a design architect that recursively decomposes
a program into a set of small provable functions. Unit tests can be
used to try and prove these small provable functions incorrect. If such tests
fail to prove incorrectness, then the functions are deemed to be correct enough
for all intents and purposes. Superconducting Electronic Design Automation
(S-EDA) tools from a macro view can be thought of as a set of unit tests for
a hardware design engineer to stress test their circuit layouts.

***********************************
The Development Psychology of SPiRA
***********************************

The development history of SPiRA can be broken down into four phases. First,
a rudimentary version that consisted of a collection of scripts. Second, a
small project that assimilated a minimum set of functions and class objects.
Third, a large systemic project with multiple coherently connected modules.
Finally, a meticulously designed framework that uses special coding techniques
to create dynamic binding, software pattern implementation, data abstraction
and custom classes.

Before understanding the reasoning behind developing a parameterized framework
for *physical design verification* it is imporant to first categorize the type
of problem we are dealing with:

Deductive Logic
===============

Deductive logic implies applying general rules which hold over the entirety
of a closed domain of discourse: Software solutions that will most likely not
change in the near future, tend to solve problems that are implicit in the technology.
The reading and parsing of GDSII layouts, and geometry modeling,
are examples implemented, through solutions that use deductive reasoning.

Inductive Logic
===============

Inductive logic is inherently uncertain; the results concluded from inductive reasoning are more nuanced than simply stating; if this, then that.
Consequently, heuristics can be derived using inductive reasoning to develop a sufficient SDE verification tool:
Implementing fabrication design rules must be done following inductive logic, since future technology changes in the superconductor
electronics field are still speculative. For instance, currently there is no specific PDK setup for superconductor electronics, and consequently, it
can either be assumed that the future PDK versions will be similar to that of semiconducting, or that it will prevail and create a new set of standards.
Also, the rapid changes being made in the semiconductor field add to the uncertainty of future metadata in the field of superconductivity.

The symmetries between the superconductor and the semiconductor field are not necessarily indicative of the future evolution of superconductor electronics.
Therefore, a paradigmatic software system (not just a solution) has to be developed, which can accommodate for dynamic "meta-changes", while still being extendible and maintainable.
Physical design verification is highly dependent on the modelling of design rules. Layout generators allows us to effectively create our own programmable
circuit models. Only minor differences exist between different fabrication processes, which enables us to develop a general software verification package
by focusing on creating solution heuristics, through inductive models, rather than trying to develop concrete deductive solutions.

Metaprogramming
===============

Technical sophistication can, at some level, cause degradation.
Metaprogramming forms the foundation of the SPiRA framework and therefore it becomes
apparent to start with a more general explanation of a metamodel.
A model is an abstraction of a real-world phenomena. A metamodel is an
even higher level of abstraction, which coalesces the properties of the original
model. A model conforms to its metamodel like a human conforms its understanding to the sophistication of its internal dictionary (language)—or lack thereof.
Metamodeling is the construction of a collection of concepts within a certain domain. Metamodeling involves defining the output and input relationships and
then fitting the correct metamodels to represent the desired behaviour.
Analogously, binding generic data to a layout has to be done by developing
a metamodel of the system. The inherit purpose of the base metaclasses in
the SPiRA framework is to bind data to a class object depending on the
class composition. This has to be done after defining the class constituents
(parameters), but before class creation. Hence, the use of metaclasses. In
Python a class is an object that can be dynamically manipulated. Therefore,
constraints have to be implemented on the class so as to overcome information
overloading. In order to constrain the class, it has to be known which data to
filter and which to process, which must then be added to the class as attributes.
In doing this, the concept evolves that the accepted data itself can be restricted
to a specific domain. This is the core principle behind the **validate-by-design** method

# CIDM 6330 Documentation

# Design
```Design is the first stage of any successful system, and encompasses everything that you work on before you begin implementation``` - Jaime Buetla

We are really here to reconcile three things:

* Designs for Interfaces
* Designs for Business Logic
* Designs for Data

<img src="img/Elements_Of_System_Design.png" alt="Elements of Systems Design" height="400" />

All systems will have these things and it is these systems that still drive the contemporary information and computing environment.

## Designs for Interfaces
It will be common to encounter the concept of an **Application Programming Interface** as being the gateway into and out of a system. This is not to be confused with User Interfaces, Human Computer Interfaces, or OOP Interfaces.  We will focus on APIs as they express the **what** of a system in terms of input, outcomes, and retreival.

### Common Concepts in Application Programming Interface Development
There are a variety of approaches to this in the Python Language, including not relying on any frameworks beyond what comes with Python and its own Library.

### Abstractions (in programming and python)
We still write programs that govern the execution of systems and the direciton of the data and logic flows that reside within them.  This is the case despite advances in AI and assistive tools meant to curate and accelerate the development of computer code artifacts.  At this time, while many of these concepts could easily be learned without getting our "hands dirty" with code, that would be a mistake.  We must make ourselves available to conversations and realizations with the materials of our design and these materials are code and data.  

At its heart, writing an API allows other systems to utilize the outputs of a system without understanding **how** these results are obtined. While available actions outcomes are necessarily exposed to others (like a menu of options) without revealing the complexities of the operation; this is a simplification and simplification is a key aspect of using abstractions for modeling.

An answer regarding a fact or expression of system state are common responses provided by an API:

* expressions of fact (functional): output is commonly related to, and a function of inputs (e.g. conversion formulae).
* expressions of state (emphatic or emphemeral): State can vary with time and may not be purely deterministic (e.g. time-based lookups).  

APIs should provide clearn intentions and expections for both inputs and outputs so that the API provides a clear and understandable contract. 

#### Designing Abstractions
Abstractions present scope and scale from which a system's outputs and benefits can be understood.  In order to develop a good abstraction, a good understanding of what the system represents is also necessary - this understanding is often emergent.

When the process happens organically, the abstractions are decided mostly on the go. There is an initial idea, acknowledged as an understanding of the problem, that then gets tweaked.

Since all models are abstractions, our instincts and inclinations that pervade our understanding of the underlying phemena to which the system attends to will change (and perhaps mature).  

In designing an API you explicitly describe the abstractions that the API will use clarify what the system will provide.  The objective   when modeling is to keep the viewpoint of a user of the system in mind; the purpose of the system is to meet the needs of users.

#### Opacity and Leaky Abstractions

An abstraction can said to be "leaky" when it ceases to be an opaque "black box" and "leaks" implementation details.

'All non-trivial abstractions, to some degree, are leaky" – Joel Spolsky's Law of Leaky Abstractions

When designing an API, it is important to account for leakiness:

* *Generate clear errors and hints*: A good design will always include cases for things going wrong and try to present them clearly with proper error codes or error handling.
* *Expose and alarm on depedency errors*: When dependencies fail an API should abstract these details with some options for a graceful recovery.  If a graceful landing is not possible, then some terminating signal would be appropriate.

#### Patterns for Abstractions
A dictionary or key-value-pairing concept is useful for API design as communication can be described as API accessing resources that can perform actions. 

* *Resources* are referenced entities or values.
* *Actions* are performed on resources.

## RESTful Interfaces for APIs
Representational State Transfer (REST) uses the HTTP protocol standards as a basis for a API communication protocol for applications.  For a system to be considered RESTful, it must:

* Facilitate a Client-server architecture through remote calls made through HTTP.
* *Be Stateless* - such that information salient to a request should be self-contained within the request and independent.
* *Be Cacheable* - the availability of query or result caching should be clear.
* *Be seamlessly layered* -  It is unimportant which layer of the system that requesting client is connected to as the results will always be the same.
* *Provide Uniform interface* - subject to a few key constraints:
    * Resources are identified as a part of the requests.
    * Resource manipulation is effected through representations that provide all of thee required information necessary to make changes to the state of the system.
    * Self-documenting and internally-complete messages
    * Hypermedia as the Engine of Application State (HATEOAS) - system navigation is complete via hyperlinks

## The Unified Modeling Language
There are a number of visual models we'll want to become familiar with as a tool for expressing various aspects of a system.  The diagrams should ultimately contribute to the code artifacts we produce to facilitate the system's effectiveness.  With that said, these models are themselves artifacts of design; their purpose is to facilitate understanding that leads to an information systems artifact.

### Select UML Diagrams Overview
Credit to [Scott Ambler](https://scottambler.com/).

| Diagram | Description | Link |
|---------|-------------|------|
| [Activity Diagram](https://agilemodeling.com/style/activityDiagram.htm) | Depicts high-level business processes, including data flow, or to model the logic of complex logic within a system. | [Activity Diagram Guidelines](https://agilemodeling.com/style/activityDiagram.htm) |
| [Class Diagram](https://agilemodeling.com/artifacts/classDiagram.htm) | Shows a collection of static model elements such as classes and types, their contents, and their relationships. | [Class Diagram Guidelines](https://agilemodeling.com/style/classDiagram.htm) |
| [Sequence Diagram](https://agilemodeling.com/artifacts/sequenceDiagram.htm) | Models the sequential logic, in effect the time ordering of messages between classifiers. | [Sequence Diagram Guidelines](https://agilemodeling.com/style/sequenceDiagram.htm) |
| [Component Diagram](https://agilemodeling.com/artifacts/componentDiagram.htm) | Depicts the components that compose an application, system, or enterprise. The components, their interrelationships, interactions, and their public interfaces are depicted. | [Component Diagram Guidelines](https://agilemodeling.com/style/componentDiagram.htm) |
| [Deployment Diagram](https://agilemodeling.com/artifacts/deploymentDiagram.htm) | Shows the execution architecture of systems. This includes nodes, either hardware or software execution environments, as well as the middleware connecting them. | [Deployment Diagram Guidelines](https://agilemodeling.com/style/deploymentDiagram.htm) |
| [State Machine Diagram](https://agilemodeling.com/artifacts/stateMachineDiagram.htm) | Describes the states an object or interaction may be in, as well as the transitions between states. Formerly referred to as a state diagram, state chart diagram, or a state-transition diagram. | [State Machine Diagram Guidelines](https://agilemodeling.com/style/stateChartDiagram.htm) |
| [Use Case Diagram](https://agilemodeling.com/artifacts/useCaseDiagram.htm) | Shows use cases, actors, and their interrelationships. | [Use Case Diagram Guidelines](https://agilemodeling.com/style/useCaseDiagram.htm) |

### UML Notes

#### Use Case Diagrams
[What's is the difference between include and extend in use case diagram?](https://stackoverflow.com/a/4472770)

Here’s an approach checked against Jacobson, Fowler, Larmen and 10 other references.

**Relationships are dependencies**
The key to Include and extend use case relationships is to realize that, common with the rest of UML, the dotted arrow between use cases is a dependency relationship. I’ll use the terms ‘base’, ‘included’ and ‘extending’ to refer to the use case roles.

***include***
A base use case is dependent on the included use case(s); without it/them the base use case is incomplete as the included use case(s) represent sub-sequences of the interaction that may happen always OR sometimes. (This is contrary to a popular misconception about this, what your use case suggests always happens in the main scenario and sometimes happens in alternate flows simply depends on what you choose as your main scenario; use cases can easily be restructured to represent a different flow as the main scenario and this should not matter).

In the best practice of one way dependency the base use case knows about (and refers to) the included use case, but the included use case shouldn’t ‘know’ about the base use case. This is why included use cases can be: a) base use cases in their own right and b) shared by a number of base use cases.

***extend***
The extending use case is dependent on the base use case; it literally extends the behavior described by the base use case. The base use case should be a fully functional use case in its own right (‘include’s included of course) without the extending use case’s additional functionality.

Extending use cases can be used in several situations:

The base use case represents the “must have” functionality of a project while the extending use case represents optional (should/could/want) behavior. This is where the term optional is relevant – optional whether to build/deliver rather than optional whether it sometimes runs as part of the base use case sequence.
In phase 1 you can deliver the base use case which meets the requirements at that point, and phase 2 will add additional functionality described by the extending use case. This can contain sequences that are always or sometimes performed after phase 2 is delivered (again contrary to popular misconception).
It can be used to extract out subsequences of the base use case, especially when they represent ‘exceptional’ complex behavior with its own alternative flows.
One important aspect to consider is that the extending use case can ‘insert’ behavior in several places in the base use case’s flow, not just in a single place as an included use case does. For this reason, it is highly unlikely that an extending use case will be suitable to extend more than one base use case.

As to dependency, the extending use case is dependent on the base use case and is again a one-way dependency, i.e. the base use case doesn’t need any reference to the extending use case in the sequence. That doesn’t mean you can’t demonstrate the extension points or add a x-ref to the extending use case elsewhere in the template, but the base use case must be able to work without the extending use case.

**SUMMARY**
I hope I’ve shown that the common misconception of “includes are always, extends are sometimes” is either wrong or at best simplistic. This version actually makes more sense if you consider all the issues about the directionality of the arrows the misconception presents – in the correct model it’s just dependency and doesn’t potentially change if you refactor the use case contents.
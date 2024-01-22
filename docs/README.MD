# CIDM 6330 Documentation
Some of the subject matter reasoning attached to the academic aims of this course are outlined and discussed here.

# Contents

1. [Orientation to the Subject](#orientation-to-the-subject)
2. [Design](#design)
3. [Software Architecture and Patterns](#software-architecture-and-patterns)
4. [The Software Architect](#the-software-architect)
5. The Empirics of Implementation
6. Continuous Improvement
7. The Mastery Path

# Orientation to the Subject
We are here to learn more about Software Engineering, Software Architecture, and Systems Design and Development.  These are not necessarily overlapping concepts, but they do share familial aims and purposes.

However, to wit, let us see what the oracle of our age, Wikipedia, has to say about thes things.

**Software Engineering**

> **Software engineering** is an engineering-based approach to software development.  A software engineer applies the engineering design process to design, develop, test, maintain, and evaluate computer software. The term programmer is sometimes used as a synonym, but may emphasize software implementation over design and can also lack connotations of engineering education or skills.

> Engineering techniques are used to inform the software development process, which involves the definition, implementation, assessment, measurement, management, change, and improvement of the software life cycle process itself. It heavily uses software configuration management, which is about systematically controlling changes to the configuration, and maintaining the integrity and traceability of the configuration and code throughout the system life cycle. Modern processes use software versioning.

**Software Architecture**
> **Software architecture** is the set of structures needed to reason about a software system and the discipline of creating such structures and systems. Each structure comprises software elements, relations among them, and properties of both elements and relations.

> The architecture of a software system is a metaphor, analogous to the architecture of a building. It functions as the blueprints for the system and the development project, which project management can later use to extrapolate the tasks necessary to be executed by the teams and people involved.

> Software architecture design is commonly juxtaposed with software application design. Whilst application design focuses on the design of the processes and data supporting the required functionality (the services offered by the system), software architecture design focuses on designing the infrastructure within which application functionality can be realized and executed such that the functionality is provided in a way which meets the system's non-functional requirements.

> Software architecture is about making fundamental structural choices that are costly to change once implemented. Software architecture choices include specific structural options from possibilities in the design of the software.

> For example, the systems that controlled the Space Shuttle launch vehicle had the requirement of being very fast and very reliable. Therefore, an appropriate real-time computing language would need to be chosen. Additionally, to satisfy the need for reliability the choice could be made to have multiple redundant and independently produced copies of the program, and to run these copies on independent hardware while cross-checking results.

> Documenting software architecture facilitates communication between stakeholders, captures early decisions about the high-level design, and allows reuse of design components between projects.

**Systems Development**
> In software engineering, a software development process is a process of planning and managing software development. It typically involves dividing software development work into smaller, parallel, or sequential steps or sub-processes to improve design and/or product management. It is also known as a software development life cycle (SDLC). The methodology may include the pre-definition of specific deliverables and artifacts that are created and completed by a project team to develop or maintain an application.

> Most modern development processes can be vaguely described as agile. Other methodologies include waterfall, prototyping, iterative and incremental development, spiral development, rapid application development, and extreme programming.

> A life-cycle "model" is sometimes considered a more general term for a category of methodologies and a software development "process" is a more specific term to refer to a specific process chosen by a specific organization.[citation needed] For example, there are many specific software development processes that fit the spiral life-cycle model. The field is often considered a subset of the systems development life cycle.

# Questions:

1. What is engineering?

2. What is design?

3. What is architecture

4. What is a system?

5. What is an information system?

6. What is software?

## Outline
Let's explore these by unpacking some principal concepts that would surround these phenomena in support of answering these questions:

1. What is the role of design in software and systems development?
2. What structures exist to support engineering and design processes for systems development?
3. How can we validate, verify, and implement our architectures?
4. How can we engage in continuous improvement of our designed artifact
5. When should we re-design and adjust?
6. What are competencies and capabilities of the architect?

We will answer these, not necessarily in order, in the remaining sections here.

[Back to Contents](#contents)

# Design
```Design is the first stage of any successful system, and encompasses everything that you work on before you begin implementation``` - Jaime Buetla

We are really here to reconcile three things:

* Designs for Interfaces
* Designs for Business Logic
* Designs for Data

<img src="img/Elements_Of_System_Design.png" alt="Elements of Systems Design" height="400" />

All systems will have these things and it is these systems that still drive the contemporary information and computing environment.

[Back to Contents](#contents)

## Design for Interfaces
It will be common to encounter the concept of an **Application Programming Interface** as being the gateway into and out of a system. This is not to be confused with User Interfaces, Human Computer Interfaces, or OOP Interfaces.  We will focus on APIs as they express the **what** of a system in terms of input, outcomes, and retreival.

[Back to Contents](#contents)

### Common Concepts in Application Programming Interface Development
There are a variety of approaches to this in the Python Language, including not relying on any frameworks beyond what comes with Python and its own Library.

[Back to Contents](#contents)

### Abstractions (in programming and python)
We still write programs that govern the execution of systems and the direciton of the data and logic flows that reside within them.  This is the case despite advances in AI and assistive tools meant to curate and accelerate the development of computer code artifacts.  At this time, while many of these concepts could easily be learned without getting our "hands dirty" with code, that would be a mistake.  We must make ourselves available to conversations and realizations with the materials of our design and these materials are code and data.  

At its heart, writing an API allows other systems to utilize the outputs of a system without understanding **how** these results are obtined. While available actions outcomes are necessarily exposed to others (like a menu of options) without revealing the complexities of the operation; this is a simplification and simplification is a key aspect of using abstractions for modeling.

An answer regarding a fact or expression of system state are common responses provided by an API:

* expressions of fact (functional): output is commonly related to, and a function of inputs (e.g. conversion formulae).
* expressions of state (emphatic or emphemeral): State can vary with time and may not be purely deterministic (e.g. time-based lookups).  

APIs should provide clearn intentions and expections for both inputs and outputs so that the API provides a clear and understandable contract. 

[Back to Contents](#contents)

#### Designing Abstractions
Abstractions present scope and scale from which a system's outputs and benefits can be understood.  In order to develop a good abstraction, a good understanding of what the system represents is also necessary - this understanding is often emergent.

When the process happens organically, the abstractions are decided mostly on the go. There is an initial idea, acknowledged as an understanding of the problem, that then gets tweaked.

Since all models are abstractions, our instincts and inclinations that pervade our understanding of the underlying phemena to which the system attends to will change (and perhaps mature).  

In designing an API you explicitly describe the abstractions that the API will use clarify what the system will provide.  The objective   when modeling is to keep the viewpoint of a user of the system in mind; the purpose of the system is to meet the needs of users.

[Back to Contents](#contents)

#### Opacity and Leaky Abstractions

An abstraction can said to be "leaky" when it ceases to be an opaque "black box" and "leaks" implementation details.

'All non-trivial abstractions, to some degree, are leaky" – Joel Spolsky's Law of Leaky Abstractions

When designing an API, it is important to account for leakiness:

* *Generate clear errors and hints*: A good design will always include cases for things going wrong and try to present them clearly with proper error codes or error handling.
* *Expose and alarm on depedency errors*: When dependencies fail an API should abstract these details with some options for a graceful recovery.  If a graceful landing is not possible, then some terminating signal would be appropriate.

[Back to Contents](#contents)

#### Patterns for Abstractions
A dictionary or key-value-pairing concept is useful for API design as communication can be described as API accessing resources that can perform actions. 

* *Resources* are referenced entities or values.
* *Actions* are performed on resources.

[Back to Contents](#contents)

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

With a RESTful API, we are typiclly creating a dictionary or look-up between HTTP methods (Verbs) and operations you are interested in on an entity within your application/project/system.  Often, this facilitates the most basic of **C**reate **R**ead **U**pdate and **D**elete (aka **CRUD**) operations on entities within the system.

This is also a way to think of accessing the resources available within a system.

| Resource      | Partial URI   | HTTP Method | Description |
|---------------|---------------|-----------|--------------------------------------------------------------|
| Collection    | /reports      | GET       | A list operation that returns all elements in the collection |
|               |               | POST      | A list creation operation |
| Single Object | /report/1     | GET       | Get a single element from the collection based on its unique id   |
|               |               | PUT       | Create a single object to be inserted into the collection |
|               |               | PATCH     | An update operation that modifies some data in a record |
|               |               | DELETE    | Delete an object from the collection using its unique id |

The entire point of a REST API is for the HTTP method to clarify the type of transaction you want from the system and for the URI to clarify which resource you are interested and/or to specify how you'd like to query for that resource.

### JSON
In most cases, REST APIs will return [JSON](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON) which gained prominence over earlier standards like [XML](https://developer.mozilla.org/en-US/docs/Web/XML/XML_introduction).  Either are fine and some of [the earliest tools for REST interfaces](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest) were assumed to be working with XML.

[Back to Contents](#contents)

### HTTP Verbs in Action

Like many early networking and web protocols, HTTP is straightforward, simple, and pretty easy to grasp as it is not too large.  Here are some excerpts of what would be actual HTTP payload information as clients and servers transact using the HTTP protocol.

The following examples presume we are working with an aviation weather API that provides coded and decoded aviation-related weather information.

***NOTE***:
<mark>
The list of possible media and content types that can be returned in an HTTP request can be found here through the [Internet Assigned Numbers Authority](https://www.iana.org/assignments/media-types/media-types.xhtml).
</mark>

**GET**
```
GET /reports/1
HTTP/1.1 200 OK
Content-Type: application/json
{"icao": "KAMA", "raw": "KAMA 221753Z 18011KT 10SM CLR 09/M01 A2990 RMK AO2 SLP119 T00941011 10100 21006 50004", "updated": "1826 UTC 22 Mon Jan 2024"}
```

**GET with query and filter**
```
GET /reports/KAMA/raw
HTTP/1.1 200 OK
Content-Type: text/plain
KAMA 221753Z 18011KT 10SM CLR 09/M01 A2990 RMK AO2 SLP119 T00941011 10100 21006 50004
```

### HTTP Headers and Status Codes
We can also use [HTTP headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) and [Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) to assist in maintaining application state with respect to the provision and use of a RESTful API.


## The Unified Modeling Language
There are a number of visual models we'll want to become familiar with as a tool for expressing various aspects of a system.  The diagrams should ultimately contribute to the code artifacts we produce to facilitate the system's effectiveness.  With that said, these models are themselves artifacts of design; their purpose is to facilitate understanding that leads to an information systems artifact.

### Designing for a Resource Approach


A resource-based view of your system is useful as it is prudent to consider that both state change and derived value come from viewing your system via the transactions it facilitates.  As the a RESTful API, by virtue of leveraging HTTp is limited to CRUD operations, a resource-based view encourages a design where resources are the "lego bricks" for the API your system provides.  Seeing everything as a resource helps to create very explicit APIs and helps with the stateless requirement for RESTful interfaces.

A stateless service means that all the information required to fulfill a request is either provided by the caller or retrieved externally, normally from a database. This excludes other ways of keeping information, such as storing information locally in the same server's hard drive. This makes any server capable of handling every single request, and it's critical in achieving scalability.

[Back to Contents](#contents)

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

[Back to Contents](#contents)

### UML Notes

Here are some additional notes about using the UML.

[Back to Contents](#contents)

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

[Back to Contents](#contents)

# Software Architecture and Patterns

Software architecture will have a fleeting definitive expression as it bridges organizational, aesthetic, and technical realms.  As such, software achitecture focuses and intersects a number of abilities within those who will design.  Thus, we can characterize software architecture in what it will "attend to."  I like Richards and Ford's model: 

>software architecture consists of the structure of a system, the design intensions the system must support, architecture-influenced design decisions, and design principles.

<img src="img/Richards_and_Ford_Model.png" alt="Richards and Ford's Model of Software Architecture" height="300">

[Back to Contents](#contents)

## On Architecture
Like "Engineering", claiming to be an architect, or to develop architecture, is subjective despite the degree to which both the engineering and architecture disciplines and professionals have tried to protect these.

Therefore, it would be most useful to understand these:
1. What is the difference between achitecture and design? 
2. How to maintain technical depth and breadth.
3. How to recognize and evaluate design tradeoffs inherent in solution technologies and patterns.
4. Understand how the business and problem domains drive architectural decisions.

I like Richards and Ford's Technical depth and breadth model here: 

<img src="img/technical_depth_and_breadth.png" alt="Technical Depth and Breadth" height="400">

## Conceptual Foundations: Modularity
While a foundational grasp of both Object-Oriented Programming and the Unified Modeling Language are ideal pre-requisites, there are pragmatic ways of understanding Modularity in software and systems development.

* A *module*: `a set of standardized parts from which a more complex structure can be crafted`
* *Modularity*: `A logical grouping of related code - often classes - designed for effective reuse - package, module, or namespace`

Aspects of measuring and identifyin modularity follow:

* **Cohesion**: `To what extent part of a module are naturally bound (thematically, funtionally) and thus belong together.`  We can reconcile with cohesion by considering whether that cohesion is functional, sequential, communicative, procedural, temporal, or logical.
* **Coupling**: `Degree to which items are connected such that both are commonly involved at the same time, within the same sequence, or within the same logical dependence.` We can reconcile with coupling by considering whether modules are related through abstractions, call distance, or instability of implementation.
* **Connascense**: This is a more acute coupling where `items within a module are coupled when changes in one module require changes in another - they are codependent.`

Modularity is a necessary part of architectural design.

## Conceptual Foundations: Architectural Characteristics
Since all software systems solutions will involve both domain requirements and architectural characteristics, an understanding of architectual charactistics will be useful here.

An architectural characteristics can be understood as classified in more or more of the following:
* Specifies a nondomain design consideration/need.
* Incluences or supports necessary design structures.
* Is critical to application success.

Richards and Ford have a nice model of this:

<img src="img/architecture-characteristics.png" alt="Architectural Characteristics" height="400">


### Examples of Architectural Characteristics

Again Richards and Ford provide some nice examples:

**Operational Architecture Characteristics**
<hr>

| Characteristic        | Definition            |
|-------------------|-----------------------|
| Availability      | "Uptime" |
| Continuity        | "Risk management and disaster recovery" |
| Performance       | "Resilience, horsepower, abundance " |
| Recoverability    | "Restoration after disaster" |
| Reliability       | "Connected to availability" |
| Robustness        | "Continuity during error and boundary conditions" |
| Scalability       | "Factors of 10" |

**Sturctural Architecture Characteristics**
<hr>

| Characteristic    | Definition            |
|-------------------|-----------------------|
| Configurability   | "Built to accommodate options and customization" |
| Extensibility     | "Add to function by plugging in new capabilities" |
| Deployability     | "Where can this be operated from?" |
| Reusability       | "Can this solution be used in other contexts?" |
| Localizable       | "Can this solution support location and context?" |
| Maintainability   | "Cost in time and skill" |
| Portability       | "Can we migrate to new operating environments?" |
| Supportability    | "What is the extend of support needs" |
| Upgradeability    | "Backwards compatibility" |

**Other Architecture Characteristics**
<hr>

| Characteristic    | Definition            |
|-------------------|-----------------------|
| Accessibility     | "Compliant with provisions to broadly support a variety of users." |
| Archivability     | "What data needs to be retained and for how long" |
| Authentication    | "You are who you say you are" |
| Authorization     | "You can use this, but now that" |
| Legal             | "Stay within the lines of what is permitted" |
| Privacy           | "Visibility and control over that visibility" |
| Security          | "CIA" |
| Exertise/Skill    | "Expected user skill level required." |

See also: [the ISO25010 standards on Software Product Quality](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010)

# The Software Architect

Since we are reasoning about software architecture, it might be useful to also reflect the software architect.  There are reasonable questions to start with:

1. `What do software architects do?`
2. `What artifacts do they produce?`
3. `How can we reconcile and quality the skills and competencies of a software architect?`

Answering these questions would permit a competency or capability model for the software architect.

## Desireable Strengths

We can reflect on things that would make for a good architect:

* **Org. Culture**: Sensitivity to, and ability to worth within, institutional/organizational culture - the essence of the domain lies within this culture
* **Strategically Astute** - Strategic thinking is a natural and default mode for you.
* **Leadership** - Leadership is not simply "being the boss," but someone who is willing to seek solutions and value in the face of uncertainty.
* **Solution and Design Oriented** - Problems await structured solutions that resonate with the design needs of the organization.
* **Integration-minded** - You seek whole/part understanding to see "how the pieces fit."
* **Domain-oriented** - Subject matter expertise within the problem domain is matched and balance with your fondness for the solution domain.
* **Socially Empathetic** - Domain affinity is matched by sensitivy to the people and processes that are impacted by solutions.
* **Mastery Path** - You engage within the mastery path with a certainty that you can both leverage and improve your skills

[Back to Contents](#contents)

## Desirable Perspectives

The emprical output and artifacts of the architect will be realized as specifications and requirements for the system to be built.  This is how the Software Architect is more than just an engineer as the artful aspects of design are also present.  However, there are fluencies in design, and the materials of design, that architects and engineers share.

What distinguishes the architect is the thoughful inclusion of domain.  It is the consideration of domains that lead to design instructions from the architect that preserve and linkage across and through domains.

Requirements are typically answers to the following questions:

* **Events** - What are the events that the system will model?
* **Entities** - What entities exist within the system such that their state can be adequately described?
* **Business/Domain Rules** - What are the operational rules of play within the system to perserve desired relationships within the system?

## Domains of Expertise

There are two vital domains of expertise that are essential for developing systems architectures:

* *Problem Domain*: At the heart of the business of the organization lies the understanding of the key factors that shape the organization:
    * Industry segment
    * Motivations
    * Threats
    * Opportuntities
    * Risk
* *Solution Domain*: The technical competency and disposition of the organization such that it can design, procure, implement, manage, and leverage information systems assets.

Where these worlds meet can be seen in this diagram (credit: Michael Bell):

<img src="img/Domain_Collaboration.png" alt="Collaboration between problem and solution domains" height="400">

## Bell's Model
Michael Bell offers a model of Software Architecture competency that facilicates our understanding of software architecture. We can understand the Software Architect's responsibilities through key activities, deliverables, and competencies:

1. Requirements - Excel at developing and brokering systems requirements
2. Practices - Engage in key practices and methods that support domain requirements
3. Discipline - With a mastery focus, develop expertise within denoted problem/solution domain pairings.
4. Deliverables - With a mastery focus, delivered artifacts will be subject to continuous improvement.
5. Duetero Learning - With a mastery focus, engage in organizational and professional [metacognition](https://en.wikipedia.org/wiki/Organizational_metacognition) that reasons with the progress of the mastery focus.

How these elements come together is illustrated in Michael Bell's model below:

<img src="img/Bells_Capability_Model.png" alt="Bell's Capability Model" height="400">

It is important to note that Michael Bell's model is not a means to understand the prototypical Software Architect, but rather to identify the type of Software Architecture competencies and capabilities required within a given design context.  This is so as an experienced architect will be, at least, the sum of their experiences.  Should the architect be a reflective practitioner, they may may realize the "synergy" that exceeds sum of parts.

[Back to Contents](#contents)

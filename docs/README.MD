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

#### Abstractions (in programming and python)

We still write programs that govern the execution of systems and the direciton of the data and logic flows that reside within them.  This is the case despite advances in AI and assistive tools meant to curate and accelerate the development of computer code artifacts.  At this time, while many of these concepts could easily be learned without getting our "hands dirty" with code, that would be a mistake.  We must make ourselves available to conversations and realizations with the materials of our design and these materials are code and data.  

### The Unified Modeling Language

There are a number of visual models we'll want to become familiar with as a tool for expressing various aspects of a system.  The diagrams should ultimately contribute to the code artifacts we produce to facilitate the system's effectiveness.  With that said, these models are themselves artifacts of design; their purpose is to facilitate understanding that leads to an information systems artifact.

#### Select UML Diagrams Overview

Credit to [Scott Ambler](https://scottambler.com/).

| Diagram | Description | Link |
|---------|-------------|------|
| [Activity Diagram](https://agilemodeling.com/style/activityDiagram.htm) | Depicts high-level business processes, including data flow, or to model the logic of complex logic within a system. | [Activity Diagram Guidelines](https://agilemodeling.com/style/activityDiagram.htm) |
| [Class Diagram](https://agilemodeling.com/artifacts/classDiagram.htm) | Shows a collection of static model elements such as classes and types, their contents, and their relationships. | [Class Diagram Guidelines](https://agilemodeling.com/style/classDiagram.htm) |
| [Sequence Diagram](https://agilemodeling.com/artifacts/sequenceDiagram.htm) | Models the sequential logic, in effect the time ordering of messages between classifiers. | [Sequence Diagram Guidelines](https://agilemodeling.com/style/sequenceDiagram.htm) |
| [Component Diagram](https://agilemodeling.com/artifacts/componentDiagram.htm) | Depicts the components that compose an application, system, or enterprise. The components, their interrelationships, interactions, and their public interfaces are depicted. | [Component Diagram Guidelines](https://agilemodeling.com/style/componentDiagram.htm) |
| [Deployment Diagram](https://agilemodeling.com/artifacts/deploymentDiagram.htm) | Shows the execution architecture of systems. This includes nodes, either hardware or software execution environments, as well as the middleware connecting them. | [Deployment Diagram Guidelines](https://agilemodeling.com/style/deploymentDiagram.htm) |

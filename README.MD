
# CIDM6330 Spring 2024
This repository will contain all supplemental materials and code for CIDM6330 for the Spring 2024 semester.

# APP Code CIDM 6330 Spring 2024

[Harry Percival and Bob Gregory's Code Repository for the Book](https://github.com/cosmicpython/code.git)
While the Percival and Gregory Book is older now, it has good concepts in it and can be reviewed for free at [Cosmic Python](https://www.cosmicpython.com/).

`git clone --branch chapter_01_domain_model https://github.com/cosmicpython/code.git`

# Components of this Repo:

* [Acme](acme/README.MD) - Acme crew scheduling example. (updated in 2024)
* [APP](APP/README.MD) - Arhictecture Patterns in Python - Percival and Gregory
* [APP2023](APP/README.MD) - Arhictecture Patterns in Python - Percival and Gregory with some adjustments
* [Barky](Barky/README.MD) - a derivative of [Dane Hillard's Bark example](https://github.com/daneah/practices-of-the-python-pro), which has been transformed to follow along with Percival and Gregory's material
* [PyTesting](PyTesting/README.MD) - pytest basics
* [Testing](Testing/README.MD) - Separate materials on testing in Python.
* [Django Girls Tutorial](tutorials/django-girls-tutorial/) - A good primer on Django.

## Git Crash Course for Begginers

[Good resource](https://gist.github.com/brandon1024/14b5f9fcfd982658d01811ee3045ff1e).

## Visual Studio Code Python Extension

It may become necessary for you to encourage the Python and Pylance extensions on how to find your virtual environment in VSCode.

The following can be added to a 'settings.json' file to accompany your project:

`"python.pythonPath": "/my/project/path/.venv/bin/python",`

## PyPi Packages

PyPi packages used:
* setuptools
* pytest
* coverage

## Percival's First Book on TDD

[Test-Driven Development with Python](https://www.obeythetestinggoat.com/)

## Regarding Barky

There are four branches related to Barky that show the progression in Barky in consideration of the design principles we are studying.

You can see these branches with the `git branch` command.

## Useful Architectural Structures

## UML Notes

### Use Case Diagrams

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



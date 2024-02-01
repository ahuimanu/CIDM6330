# About Testing
This will serve as a generalized guide to testing which brings together a few key elements:

* Software Development Frameworks for Python:
    * The `unittest` Python package
    * Django's `TestCase`
* Paradigms in Empirical Software Development
    * **Test-Driven Design/Development**: Harry Percival has another free book for this too: [Obey the Testing Goat!](https://www.obeythetestinggoat.com/)
    * **Behavior-Driven Design/Development**: [BDD](https://www.agilealliance.org/glossary/bdd/) extends into mapping behaviors - commonly captured in user stories - to testing and independent empirical validation.
    * Domain-Driven Design/Development: [DDD](Domain-Driven Design is an approach to software development that centers the development on programming a domain model that has a rich understanding of the processes and rules of a domain)

## Paradigms
These paradigms matter as the represent key thinking in the pre-automation era.  [DevOps](https://resources.github.com/devops/) is the leading edge of the automation era where the balance between human design and algorithmic/statistical design are in flux.  I don't pretend to have the answers or a prediction on outcomes here, but the need to understand the human element remains as that is the audience for this information.  

### Human Element
I'll use stories, alliteration, and metaphor as is my common wont.

[Chesley Burnett "Sully" Sullenberger III](https://en.wikipedia.org/wiki/Sully_Sullenberger) is well known for having save many lives when his A320 airliner encountered a bird strike and landed the plane in the Hudson River, having saved the lives of those on board.  While the Airbus A320 is a marvel of aviation engineering and provided significant automation to its pilots, it still assumes the presence of pilots.  I share this to extrapolate the likely need for human involvement in software design, development, and testing despite advances in automation.  There was no automation routine for "bird strike, find a safe place to land, which is in this river" and the outcomes of autopilots for self-driving cars are still developmental.  In fact, your ability to even follow this alliterative metaphor is a testament to your advanced reasoning as a human.  As such, it is wildly premature to write off the need to comprehend many aspects of systems design, development, procurement, and management.

# Unit Testing in Python
Of course you test your code, on your journey to see if it works, you code, build, test often.  When you "run it to see if it works," you are engaged in **manual testing** and/or **exploratory testing**.  Debugging is a form of manual testing where you commonly use tools to sequentially execute code - all code sequentially executes - in a stepwise manner to detect errors of logic or syntax.  Most modern software development tools and environments provide some access to step-wise debugging.

The issue with manual/explortory testing is that it is fatiguing if you have to do this yourself.  This issue is compounded as the size and scope of your application/system expands.  As in nearly every human endeavor, this is where mechaniztation and automation typically come into the picture.  An automted test allows for the same checking that manual/exploratory testing does, but it is executed according to a test plan that specifies:
    * the parts of your application you want to test
    * the order in which you want to test them
    * specification of valid and expected outcomes

In this sense, you write programs to validate and check the code you write for your actual program.  That's very meta, but that is the crux of all inspection, assessment, and validation routines and is part and parcel fo the science and engineering side of things as a complement ot the creative side of things.

## Additional Levels of Testing
While we will start with **unit testing**, I will mention breifly here that as we compound and combine code modules to get work done, there will be ensemble effects whereby the interaction and orchestration of these modules will also need to be checked.  Testing multiple components is known as **integration testing.**  An additional step would be the degree to which a system facilitates full transactions where that level of testing is commonly called **end-to-end** testing.  Components, abstractions, and modularity are key to understanding software engineering and architecture, where systems and applications are the sum of components comprised of the classes, functions, and modules that have been tested at lower levels.  Testing is VITAL to functioning systems and software and often becomes the basis of proving and validating the outputs and benefits of a system.

## Python and unittest  
There are many options to accomplish this in Python where several tools and libraries are available for automated testing.

Here, we will mainly focus on the `unittest` library and how that is extended in Django.

Let's start simply, python has a built-in function that sums two numbers:

```python
sum([])
```

Python also has a built-in statement `assert` which is purpose-made to facilitate testing.  Assert will give you a boolean response to an expression whose outcome you'd like to test:

```python
assert sum([1,2]) == 3 #expecting 3 and thus true
```

[Assert](https://www.w3schools.com/python/ref_keyword_assert.asp) is a simple tool, but is the functional and conceptual underpinning of all unit testing.
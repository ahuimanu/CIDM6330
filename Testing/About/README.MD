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

## Test Runners
While you can easily use assert to develop your own testing plan and structure, you would quickly find that to be a full-time task and you would be, frankly, reinventing the wheel.

A test runner is a software ecosystem that assist in the development and execution of your test plan.

There are many test runners, but I've largely just used these:
* unittest - comes with Python
* PyTest - 3rd party

Since unittest comes with Python, let's focus there:
 
 ## `unittest`
`unittest` will assist as a sofware testing framework, with libraries and structures to assist across your applications, and more simply to run your tests. 

`unittest` has the following provisions for the development of your tests:

* tests are methods in a subclass of the TestCase class
* TestCase provides specialized assertion methods rather than the `assert` command.

Thus, the simple sum example would look like this usig the unittest framework:

```python
import unittest

class TestSum(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "sum is 6")

if __name__ == '__main__':
    unittest.main()
```

### `unittest` example
Let's examine a more elaborate example:

the project assumes the following project structure:
```
workspace/
    sum_thing/
        __init__.py
```
**NOTE:** 
>The above example uses one of the many [Dunder Methods](https://www.geeksforgeeks.org/dunder-magic-methods-python/) provided out of the box in Python.  These are "global" methods that are also usually available for override when you create a new class.

So, within the `__init__.py` file, which is evaluated anytime the `sum_thing` package is used, we can place a utility method that will do our summing:

```python
def sum(args):
    sum_total = 0
    for val in args:
        sum_total += val
    return sum_total
```
This is a straightforward approach to creating a running sum of any [iterable](https://pythonbasics.org/iterable/) (usually linear) structure we will encounter. `args` is assumed to be a python data structure such as [lists, tuples, or sets](https://docs.python.org/3/tutorial/datastructures.html).

Now, we can progress to including tests in our project:
```
workspace/
    sum_thing/
        __init__.py
    tests/
        test.py
```

We are likely to develop more and more tests where the [ideal coverage](https://artoftesting.com/test-coverage) of these tests will approach a one to one ratio with working/functioning code.

### Test Writing Considerations

There is a general flow or cadence to writing tests that goes something like this:

* Q: What are we testing?
    * A unit test or an integration test?

Common test Structure - Arrange, Act, Assert

* Arrange: Create inputs to the function to be tested.
* Act: Execute the function to be tested and retrieve the output of that function
* Assert: Compare the output with an expected result

Consider the range of behaviors to plan for the cases to be tested. For the sum_thing example:

* Can sum_thing sum a list integers?
* Can sum_thing sum a tuple or set?
* Can sum_thing sum a list of floats?

We also want to iteratively explore all of the failure paths and circumstances.  What should we do when:
* An out of specification value is passed, like a single number or a non-numeric value?
* A given value is negative?

With these steps in mind, the test can look like this:
```python
import unittest
from sum_thing import sum

class TestSum(unittest.TestCase):
    def test_list_int(self):
        """
        Test that it can sum a list of integers
        """
        data = [1, 2, 3]
        result = sum(data)
        self.assertEqual(result, 6)

if __name__ == '__main__':
    unittest.main()
```

### Understanding `unittest`'s Assertions
As the heart of a unit test is in its assertion(s).  This is the validation and "pass/fail" element of the assertion - assertion results are always binary.  When developing assertions, keep the following in mind:

* Manually inspect and validate that the assertion statement is valid
* Adopt a "what if" and "what about" hypothesis orientation to discovering the various ways that your function can fail.

`unittest` provides a set of common assertions that have been developed as methods that help you to assert on the values, types, and null values:

|`unittest` method      | `assert` equivalent   |
|-----------------------|-----------------------|
|`.assertEqual(x, y)`   | `x == y`              |
|`.assertTrue(x)`       | `x == True`           |
|`.assertFalse(x)`      | `x == False`          |
|`.assertIs(a, b)`      | `a is b`              |
|`.assertIsNone(x)`     | `x is None`           |

### The `unittest` command
Unit test also has a command-line Python module utility that allows for more management options for your tests.

In most cases you would run the `unittest` utility like this: `python -m unittest <module>`

**NOTE:**
~~~
Anytime you put Python code into a .py source file, Python now considers all code in that file to belong (semantically) to the same module. This impacts how python imports work.
~~~

|command                        | purpose                                                                       |
|-------------------------------|-------------------------------------------------------------------------------|
|`unittest <module>`            | runs all methods in all subclasses of TestCase discovered within the module   |
|`unittest -v <module>`         | runs tests with verbose - more detailed - output.                             |
|`unittest discover`            | Lists all modules that contain unit tests`                                    |
|`unittest discover -s <dir>`   | run all tests in a specified directory                                        |

### Failing tests
Python will throw an error when a test fails, which is the desired behavior because a failed test should be considered a "no go" and show stopping event.

First, let's run the test: `python -m unittest discover -s tests/`

And see the following output:
```
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

This is non-verbose output and the single dot shows that a single test was run and the *OK* shows that all tests passed.

If we make a tiny change in the code, we can force a failing test:

```python
class TestSum(unittest.TestCase):
    def test_list_int(self):
        """
        Test that it can sum a list of integers
        """
        data = [1, 2]
        result = sum(data)
        self.assertEqual(result, 4) #WRONG!!!
```

`unittest` will now produce output indicating that the test has failed and provide enough information to track down the failure.

```
F
======================================================================
FAIL: test_list_int (test.TestSum.test_list_int)
Test that it can sum a list of integers
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<path_to_test>/test.py", line 11, in test_list_int
    self.assertEqual(result, 4)
AssertionError: 3 != 4

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
```

### IDE Integration
Most [Integrated Development Environments - IDEs](https://en.wikipedia.org/wiki/Integrated_development_environment) will provide additional facilities to detect, run, and present test results in ways that are less cumbersome than running commands.  As a rule, over the years I've learned how to first learn to run anything with just command-line tools before I start to rely on simplifications and automation.  Your results and experience may vary from mine.

## Django and Flask
Both Django and Flask base their testing environments on `unittest` so there will be few differences to worry about.  In Django's case, we'll use the `manage.py` utility to run tests like so: `python manage.py test`.  [Django has great integration for testing](https://docs.djangoproject.com/en/5.0/topics/testing/overview/) that we will put to good use.

## Testing Influences Design
As we study the principles of modularly, abstraction, coupling, and dependency, it should be come evident that testing, particularly integration and unit testing, provides up-close and empricial insight on what is really happening in your system/application.  This is so powerful that many adherents of TDD advocate for a [test-first philosophy](https://www.scrum.org/resources/blog/building-test-first-philosophy-key-agile-success).  While that can be extreme to some, there are merits in the premise.  In reality there is a fatigue in a test-first approach unless the philosophy is well internalized.

If you open up to the concept that testing can shape design, then several additional possibilities also open up to you.  One advantage of testing is its ability to reveal quirks and depenencies that are sometimes called **side effects** of the functions and operations of your system.  A side effect is a condition where testing reveals tight coupling and dependencies that could negatively affect the system as it grows and evolves.  From a pure perspective, side effects complicate testing as results may vary each time a test is run for reasons not directly related to the test itself, but because of "upsteam" dependencies

### Taking advantage of side effects
As side effects are discovered, there are a vareity of opportunites to improve your code:

* Can lead to a [refactor](https://refactoring.guru/refactoring) of code to become more in line with [Software Engineering best practices](https://en.wikipedia.org/wiki/SOLID). 
* [Using Mocks, Fakes, or Stubs](https://martinfowler.com/articles/mocksArentStubs.html) to simulate the functions that lead to side effects
* Progress to integration testing as appropriate

## Integration Tests

https://realpython.com/python-testing/#more-advanced-testing-scenarios
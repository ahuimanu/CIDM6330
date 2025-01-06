# Designing from Evidence

We should have made this the first evolution, but there are cart and horse issues here.

## Test-Driven Development

- [Test-Driven Development](https://martinfowler.com/bliki/TestDrivenDevelopment.html) 
    - Write a test for the next bit of functionality you want to add.
    - Write the functional code until the test passes.
    - Refactor both new and old code to make it well structured.
- [Behavior Driven Development](https://cucumber.io/docs/bdd/)
    - ***Discovery (what it could do)***: Given a User Story that describes the system, decompose this into the tasks that will realize the functionality and development details that will lead to the developmment of the artifacts that satisfy the story.
    - ***Formulation (what it should do)***: Document tasks so that they can be validated through automated testing.
    - ***Automation (what it actually does)***: Implement the tasks such that they produce the behaviours needed and prove the behaviours through automated tests.
- [Domain Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)

# Requirements

1. For DDD create a ubiquitous language glossary: [https://thedomaindrivendesign.io/developing-the-ubiquitous-language/](https://thedomaindrivendesign.io/developing-the-ubiquitous-language/)
2. For BDD create A Gherkin Notation expression for each test: [Gherkin Syntax](https://cucumber.io/docs/gherkin/)
3. For TDD create tests that correspond with your Gherkin Statements.
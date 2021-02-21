# Notes on Architecture Patterns with Python

Harry Percival and Bob Gregory

## Chapter 1 Domain Modeling

Be mindful that the examples in the book unfold from a domain context involving furniture distribution/wholesale.

This image is very useful to remain oriented:

![Furniture Distribution Domain Model](https://i.imgur.com/hHMeVS1.png)

### Domain Language

Equally useful is to bear the language of the domain in mind. The "Some Notes on Allocation" helps here:

> A product is identified by a SKU, pronounced “skew,” which is short for stock-keeping unit. Customers place orders. 
> An order is identified by an order reference and comprises multiple order lines, where each line has a SKU and a quantity. 
> For example: 
> * 10 units of RED-CHAIR 
> * 1 unit of TASTELESS-LAMP 
> The purchasing department orders small batches of stock. 
> A batch of stock has a unique ID called a reference, a SKU, and a quantity. 
> We need to allocate order lines to batches. When we’ve allocated an order line to a batch, we will send stock from that specific batch to the customer’s delivery address. When we allocate x units of stock to a batch, the available quantity is reduced by x. 
> For example: 
> * We have a batch of 20 SMALL-TABLE, and we allocate an order line for 2 SMALL-TABLE. 
> * The batch should have 18 SMALL-TABLE remaining. 
> We can’t allocate to a batch if the available quantity is less than the quantity of the order line. 
> For example: 
> * We have a batch of 1 BLUE-CUSHION, and an order line for 2 BLUE-CUSHION. 
> * We should not be able to allocate the line to the batch. 
> We can’t allocate the same line twice. For example: 
> * We have a batch of 10 BLUE-VASE, and we allocate an order line for 2 BLUE-VASE. 
> * If we allocate the order line again to the same batch, the batch should still have an available quantity of 8. 
> Batches have an ETA if they are currently shipping, or they may be in warehouse stock. We allocate to warehouse stock in preference to shipment batches. We allocate to shipment batches in order of which has the earliest ETA.

### Running tests with Pytest

Perhaps because the book's focus is on architecture, and because [the authors offer the book for free](https://www.cosmicpython.com/book/preface.html), the book doesn't discuss much detail about actually running the tests beyond a few assumptions:

* You are using Docker containers (I'd rather not)
* You are using a virtual environment (Yes, we are) and will run the tests manually (Yes, we will)

Or, it is assumed that you have read Harry Percival's first book, [which is also free](https://www.obeythetestinggoat.com/pages/book.html#toc), and focuses more on the mechanics of testing.

Regardless, you'll want to ensure that you include [`pytest`](https://pypi.org/project/pytest/) in your virtual environment.

Then, test dicsovery is [pretty automagic](https://docs.pytest.org/en/stable/contents.html), and essentially requires that you run:

`python -m pytest` 

in your project directory.  Of course, [there's much more to using pytest](https://docs.pytest.org/en/stable/contents.html), but that is a good basic start.

Key files at this stage:

* tests for allocate and batches
* domain model classes/functions

## Chapter 2 - Repository Pattern

This chapter introduces the use of SQLAlchemy and the basics of a [Repository Pattern](https://codewithshadman.com/repository-pattern-csharp/) using Python.

Things to install:
* [sqlalchemy](https://docs.sqlalchemy.org/en/13/): `pip install sqlalchemy`

In this chapter, these modules provide a persistence mechanic and an abstraction layer in the form of an [O/RM](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping):
* orm
* repository


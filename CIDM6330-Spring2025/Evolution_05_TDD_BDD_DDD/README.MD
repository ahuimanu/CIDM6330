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
    1. wayback archive: [https://web.archive.org/web/20241122220908/https://thedomaindrivendesign.io/developing-the-ubiquitous-language/](https://web.archive.org/web/20241122220908/https://thedomaindrivendesign.io/developing-the-ubiquitous-language/)

2. For BDD create A Gherkin Notation expression for each test: [Gherkin Syntax](https://cucumber.io/docs/gherkin/)
3. For TDD create tests that correspond with your Gherkin Statements.

## 2025 Example

### Django/API Component

A Django Ninja version of Afroza Nowshin's [How to Do Periodic Tasks in a Django REST API Using Celery and Redis? - A Beginner-Friendly Guide](https://dev.to/afrozansenjuti/how-to-do-periodic-tasks-in-a-django-app-using-celery-and-redis-a-beginner-friendly-guide-3bp3)

Afroza's GitHub repo is also very useful: https://github.com/Afroza2/Strativ-AB-Travel-Management/tree/master

ERRATA:
The full pip install list is:
```shell
pip install django django-celery-results celery redis django-redis
```

PROMPT for the API project:
"Create an API where you select two cities in the US:  location, destination, and travel date. Compare temperatures for those two cities at 2 PM on that day and return a response deciding whether they should travel there. Hint: You might need to periodically fetch data and store it somewhere."

### Data Analytics component

PROMPT for Analytics:
"Train a simple model that forecasts weather conditions for a given time. We will train on the top 60 cities in the USA. After training the model, create a simple API to query the trained model. Our API will predict the temperature at any future date beyond the 7 to 16 days provided by the OpenMeteo Forecast data."

To do this, we need to adjust to use open-meteo's archival data: https://archive-api.open-meteo.com/v1/archive

#### Requirements
```shell
pip install openmeteo_requests
pip install pandas
pip install requests_cache
pip install retry_requests
pip install notebook
pip install matplotlib
```

Celery commands:

The best method to run Celery workers with by installing `gevent`: `pip install gevent`

```shell
celery -A travelmanagement worker -l INFO --pool=gevent --concurrency=2
celery -A travelmanagement beat -l info
```

### Running Redis without Docker
There are other ways to run redis rather than rely on Docker.

#### Windows
- [Install Ubuntu on WSL2](https://documentation.ubuntu.com/wsl/en/latest/howto/install-ubuntu-wsl2/)
- Install redis:

```shell
sudo apt update && sudo apt upgrade

sudo apt install redis-server
```

#### Mac
[Install Redis on macOS](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-mac-os/)


## Useful Wikipedia to CSV tool

[Convert Wiki Tables to CSV](https://wikitable2csv.ggor.de/)

## "Vibe Coding" 
[As mentioned in my video](https://en.wikipedia.org/wiki/Vibe_coding)
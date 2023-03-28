from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

import config
import model
import orm
import repository
import services


def index_endpoint():
    return "<p>HELLO FROM THE API</p>"


def allocate_endpoint():
    clear_mappers()
    orm.start_mappers()
    # get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
    get_session = sessionmaker(bind=create_engine(f"sqlite:///bookmarks.db"))
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    line = model.OrderLine(
        request.json["orderid"],
        request.json["sku"],
        request.json["qty"],
    )

    try:
        batchref = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return {"message": str(e)}, 400

    return {"batchref": batchref}, 201


def create_app():
    app = Flask(__name__)
    app.config.update({"TESTING": True})

    app.add_url_rule("/", "index", view_func=index_endpoint)
    app.add_url_rule(
        "/allocate", "allocate", view_func=allocate_endpoint, methods=["POST"]
    )

    return app

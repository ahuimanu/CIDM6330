from datetime import datetime
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from allocation import config
from allocation.domain import model
from allocation.adapters import orm, repository
from allocation.service_layer import services, unit_of_work


def index_endpoint():
    return "<p>HELLO FROM THE API</p>"


def add_batch_endpoint():
    eta = request.json["eta"]
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    services.add_batch(
        request.json["ref"],
        request.json["sku"],
        request.json["qty"],
        eta,
        unit_of_work.SqlAlchemyUnitOfWork(),
    )
    return "OK", 201


def allocate_endpoint():
    # clear_mappers()
    # orm.start_mappers()
    # get_session = sessionmaker(bind=create_engine(config.get_sqlite_filedb_uri()))
    # session = get_session()
    # repo = repository.SqlAlchemyRepository(session)
    # line = model.OrderLine(
    #     request.json["orderid"],
    #     request.json["sku"],
    #     request.json["qty"],
    # )

    try:
        batchref = services.allocate(
            request.json["orderid"],
            request.json["sku"],
            request.json["qty"],
            unit_of_work.SqlAlchemyUnitOfWork(),
        )
    except (model.OutOfStock, services.InvalidSku) as e:
        return {"message": str(e)}, 400

    return {"batchref": batchref}, 201


def create_app():
    app = Flask(__name__)
    app.config.update({"TESTING": True})

    app.add_url_rule("/", "index", view_func=index_endpoint)
    app.add_url_rule(
        "/add_batch", "add_batch", view_func=add_batch_endpoint, methods=["POST"]
    )
    app.add_url_rule(
        "/allocate", "allocate", view_func=allocate_endpoint, methods=["POST"]
    )

    return app
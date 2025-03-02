from abc import ABC, abstractmethod
from sqlmodel import SQLModel, create_engine, Session, Field, select


# creates a SQLModel
class FlightPlan(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True)
    #   "ident": "AAL1",
    ident: str
    #   "operator": "AAL",
    operator: str
    #   "flight_number": "1",
    flight_number: str
    #   "registration": "N110AN",
    registration: str
    #   "aircraft_type": "A321",
    aircraft_type: str
    #   "origin": "KJFK",
    origin: str
    #   "destination": "KLAX",
    destination: str
    #   "filed_ete": 19620,
    filed_ete: int
    #   "scheduled_out": "2025-03-02T11:59:00Z",
    scheduled_out: str
    #   "scheduled_in": "2025-03-02T18:28:00Z",
    scheduled_in: str
    #   "route_distance": 2472,
    route_distance: int
    #   "filed_airspeed": 462,
    filed_airspeed: int
    #   "filed_altitude": 360,
    filed_altitude: int
    #   "route": "COATE Q436 RAAKK NELLS PLAIN J146 GIJ BDF GBG ELYNA STJ HYS DVC ROOLL ESGEE Q90 DNERO ANJLL4",
    route: str
    #   "gate_origin": "45",
    gate_origin: str
    #   "gate_destination": "46C",
    gate_destination: str
    #   "terminal_origin": "8",
    terminal_origin: str
    #   "terminal_destination": "4",
    terminal_destination: str
    #   "type": "Airline"
    type: str


class BaseFPRepo(ABC):
    @abstractmethod
    def do_create(self, fp):
        pass

    @abstractmethod
    def read_all(self):
        pass

    @abstractmethod
    def do_read_id(self, id):
        pass

    @abstractmethod
    def do_read_flight(self, operator: str, flight_number: str):
        pass

    @abstractmethod
    def do_update(self, id, field, value):
        pass

    @abstractmethod
    def do_delete(self, id):
        pass


class MySQLModelRepo(BaseFPRepo):
    """
    Works with SQL Model, which is a library that provides a way to work with SQL databases in Python.
    """

    def __init__(self, db_string="sqlite:///flightplans.db"):
        # ability to work use the database
        self.engine = create_engine(db_string)
        # ability to create all tables and structures
        SQLModel.metadata.create_all(self.engine)
        # ability to perform operations on the database
        self.session = Session(self.engine)

    def do_create(self, fp):
        self.session.add(fp)
        self.session.commit()

    def read_all(self):
        statement = select(FlightPlan)
        result = self.session.exec(statement)
        return result.all()

    def do_read_id(self, id):
        statement = select(FlightPlan).where(FlightPlan.id == id)
        result = self.session.exec(statement)
        return result.one()

    def do_read_flight(self, operator: str, flight_number: str):
        statement = select(FlightPlan).where(
            FlightPlan.operator == operator, FlightPlan.flight_number == flight_number
        )
        result = self.session.exec(statement)
        return result.one()

    def do_update(self, id, field, value):
        fp = self.do_read_id(id)

        if field == "ident":
            fp.ident = value

        if field == "operator":
            fp.operator = value        

        if field == "flight_number":
            fp.flight_number = value

        if field == "registration":
            fp.registration = value

        if field == "aircraft_type":
            fp.aircraft_type = value        

        if field == "origin":
            fp.origin = value

        if field == "destination":
            fp.destination = value

        if field == "filed_ete":
            fp.filed_ete = value

        if field == "scheduled_out":
            fp.scheduled_out = value    

        if field == "scheduled_in":
            fp.scheduled_in = value

        if field == "route_distance":
            fp.route_distance = value

        if field == "filed_airspeed":
            fp.filed_airspeed = value

        if field == "filed_altitude":
            fp.filed_altitude = value

        if field == "route":
            fp.route = value    

        if field == "gate_origin":
            fp.gate_origin = value

        if field == "gate_destination":
            fp.gate_destination = value

        if field == "terminal_origin":
            fp.terminal_origin = value

        if field == "terminal_destination":
            fp.terminal_destination = value        

        if field == "type":
            fp.type = value

       
        self.session.add(fp)
        self.session.commit()
        self.session.refresh(fp)

    def do_delete(self, id):
        fp = self.do_read_id(id)
        self.session.delete(fp)
        self.session.commit()


class MyMemoryRepo(BaseFPRepo):

    def __init__(self, id_field: str):

        self.repo = list[FlightPlan]

    def do_create(self, fp: FlightPlan):
        self.repo.append(fp)

    def do_read_id(self, id):
        return self.repo[id]

    def do_update(self, id, fp: FlightPlan):
        self.repo[id] = fp

    def do_delete(self, id):
        self.remove(id)

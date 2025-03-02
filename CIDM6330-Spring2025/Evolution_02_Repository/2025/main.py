from dataclasses import dataclass, asdict, field, InitVar, fields
from repository import FlightPlan, MyMemoryRepo, MySQLModelRepo


#   "ident": "AAL1",
#   "operator": "AAL",
#   "flight_number": "1",
#   "registration": "N110AN",
#   "aircraft_type": "A321",
#   "origin": "KJFK",
#   "destination": "KLAX",
#   "filed_ete": 19620,
#   "scheduled_out": "2025-03-02T11:59:00Z",
#   "scheduled_in": "2025-03-02T18:28:00Z",
#   "route_distance": 2472,
#   "filed_airspeed": 462,
#   "filed_altitude": 360,
#   "route": "COATE Q436 RAAKK NELLS PLAIN J146 GIJ BDF GBG ELYNA STJ HYS DVC ROOLL ESGEE Q90 DNERO ANJLL4",
#   "gate_origin": "45",
#   "gate_destination": "46C",
#   "terminal_origin": "8",
#   "terminal_destination": "4",
#   "type": "Airline"


fp = [
    FlightPlan(
        id=1,
        ident="AAL1",
        operator="AAL",
        flight_number="1",
        origin="KJFK",
        destination="KLAX",
        registration="N110AN",
        aircraft_type="A321",
        filed_ete=19620,
        scheduled_out="2025-03-02T11:59:00Z",
        scheduled_in="2025-03-02T18:28:00Z",
        route_distance=2472,
        filed_airspeed=462,
        filed_altitude=360,
        route="COATE Q436 RAAKK NELLS PLAIN J146 GIJ BDF GBG ELYNA STJ HYS DVC ROOLL ESGEE Q90 DNERO ANJLL4",
        gate_origin="45",
        gate_destination="46C",
        terminal_origin="8",
        terminal_destination="4",
        type="Airline",
    ),
    FlightPlan(
        id=2,
        ident="AAL1",
        operator="AAL",
        flight_number="1",
        registration="N112AN",
        aircraft_type="A321",
        origin="KJFK",
        ddestination="KLAX",
        filed_ete=19680,
        scheduled_out="2025-03-02T11:59:00Z",
        scheduled_in="2025-03-02T18:28:00Z",
        route_distance=2472,
        filed_airspeed=451,
        filed_altitude=340,
        route="COATE Q436 RAAKK DKK FARGN KITOK HOCKE MONEE LAKSE VIKNG HELLO EYHUX OBH HCT HBU DVC ROOLL DNERO ANJLL4",
        gate_origin="8",
        gate_destination="53A",
        terminal_origin="8",
        terminal_destination="5",
        type="Airline",
    ),
]


def do_sqlmodel_example():

    # start
    print("WORKING WITH A SQLMODEL REPOSITORY")
    repo = MySQLModelRepo("sqlite:///flightplans.db")

    # create
    print("create a flight plan in the repository")
    repo.do_create(fp[0])

    # read
    print("read the flight plan from the repository")
    print(repo.do_read_id(1))

    # update
    repo.do_update(1, "origin", "KAUS")

    # read
    print(repo.do_read_id(1))

    # delete
    repo.do_delete(1)

    # read
    try:
        print(repo.do_read_id(1))
    except:
        print("Flight plan not found")


def do_memory_example():

    print("WORKING WITH A MEMORY REPOSITORY")
    repo = MyMemoryRepo("id")

    # create
    print("create a flight plan in the repository")
    repo.do_create(asdict(fp))

    # read
    print("read the flight plan from the repository")
    print(repo.do_read(1))

    # update
    repo.do_update(1, "orig", "KAUS")

    # read
    print(repo.do_read(1))

    # delete
    repo.do_delete(1)

    # read
    try:
        print(repo.do_read(1))
    except KeyError:
        print("Flight plan not found")


if __name__ == "__main__":
    # do_memory_example()
    do_sqlmodel_example()

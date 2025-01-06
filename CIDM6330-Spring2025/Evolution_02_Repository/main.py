from dataclasses import dataclass, asdict, field, InitVar, fields
from repository import FlightPlan, MyMemoryRepo, MyCSVRepo

fp = FlightPlan(
    id=1,
    airline="SWA",
    flightnum="784",
    orig="KDAL",
    dest="KMDW",
    date=20241027,
    dephour=16,
    depmin=8,
    route="LNDRE5 BSKAT IGLOO FAM PHEEB ENDEE6",
    stehour=2,
    stemin=19,
    altn="KORD",
    pic="John Doe",
    picid=1,
)


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


def do_csv_example():

    print("WORKING WITH A CSV REPOSITORY")
    fieldnames_list = list(fp.__dict__.keys())
    repo = MyCSVRepo("flightplans.csv", "id", fieldnames_list)

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
    do_csv_example()

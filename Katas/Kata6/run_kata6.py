"""Small runner for Kata6 to allow quick manual tests."""

from kata6 import run


def main():
    # small default for quick runs during development
    run(total_items=2000, chunk_size=400, workers=4)


if __name__ == "__main__":
    main()

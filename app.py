from src.seatguru import ConfigurationFinder

def main():
    operator = input("Operator: ")
    aircraft = input("Aircraft: ")
    registration = input("Registration: ")
    seatguru = ConfigurationFinder()
    seats = seatguru.scrape(operator, aircraft)
    print(f"{operator} {aircraft} {registration} configured with {seats} seats")

if __name__ == "__main__":
    main()
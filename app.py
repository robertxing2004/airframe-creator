from src.seatguru import ConfigurationFinder
from src.rzjets import AirframeFinder

def main():
    seatguru = ConfigurationFinder()
    airframes = AirframeFinder()

    operator = input("Operator: ")
    aircraft = input("Aircraft: ")
    type_code = input("Type: ")
    registration = input("Registration: ")
    
    seats = seatguru.scrape(operator, aircraft)
    print(f"{operator} {aircraft} {registration} configured with {seats} seats")
    airframe = airframes.scrape(operator, registration)
    print(f"{airframe["registration"]} found")
    print(f"Tail: {airframe["fin"]}")
    print(f"Type: {type_code}")
    print(f"Model: {airframe["aircraft"]}")
    print(f"SELCAL: {airframe["selcal"]}")
    print(f"ICAO24: {airframe["icao24"]}")

if __name__ == "__main__":
    main()
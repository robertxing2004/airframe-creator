from src.seatguru import ConfigurationFinder
from src.airframes import AirframeFinder

def main():
    seatguru = ConfigurationFinder()
    airframes = AirframeFinder()

    operator = input("Operator: ")
    aircraft = input("Aircraft: ")
    registration = input("Registration: ")
    
    #seats = seatguru.scrape(operator, aircraft)
    #print(f"{operator} {aircraft} {registration} configured with {seats} seats")
    airframe = airframes.scrape(registration)
    print(f"{airframe["Registration"]} found")
    print(f"Model: {airframe["Model"]}")
    print(f"Type: {airframe["Type"]}")
    print(f"SELCAL: {airframe["Selcal"]}")
    print(f"ICAO24: {airframe["ICAO24"]}")

if __name__ == "__main__":
    main()
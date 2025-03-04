from src.seatguru import ConfigurationFinder
from src.rzjets import AirframeFinder

def main():
    seatguru = ConfigurationFinder()
    airframes = AirframeFinder()

    operator = input("Operator: ").capitalize()
    aircraft = input("Aircraft: ").capitalize()
    type_code = input("Type: ").capitalize()
    registration = input("Registration: ").upper()
    
    seats = seatguru.scrape(operator, aircraft)
    if seats == 0:
        seats = int(input("Manually enter seat configuration: "))
    print(f"{operator} {aircraft} {registration} configured with {seats} seats")
    airframe = airframes.scrape(operator, registration)

    print(f"{airframe["Registration"]} found")
    print(f"Type: {type_code}")
    for key in airframe:
        if key in ["MSN", "Engine", "Name", "Operator", "Built"]:
            continue
        if airframe[key] == "":
            airframe[key] = input(f"{key}: ")
        else:
            print(f"{key}: {airframe[key]}")
            

if __name__ == "__main__":
    main()
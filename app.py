from src.seatguru import ConfigurationFinder
from src.rzjets import AirframeFinder

def reformat(aircraft):
    name = aircraft.split()
    new_name = name[-1]
    if new_name[0] == "7":
        new_name = "B" + new_name
    return new_name

def main():
    seatguru = ConfigurationFinder()
    airframes = AirframeFinder()

    operator = input("Operator: ").title()
    aircraft = input("Aircraft: ").capitalize()
    type_code = input("Type: ").capitalize()
    registration = input("Registration: ").upper()
    
    seats = seatguru.scrape(operator, aircraft)
    if seats == 0:
        manual = input("Manually enter seat configuration: ")
        seats = int(manual) if manual.isdigit() else 0
    print(f"{operator} {aircraft} {registration} configured with {seats} seats")
    airframe = airframes.scrape(operator, registration)

    airframe["Aircraft"] = reformat(airframe["Aircraft"])

    print(f"{airframe["Registration"]} found")
    print(f"Type: {type_code}")
    for key in airframe:
        if key in ["Registration", "MSN", "Engine", "Name", "Operator", "Built"]:
            continue
        if airframe[key] == "":
            airframe[key] = input(f"{key}: ")
        else:
            print(f"{key}: {airframe[key]}")
            

if __name__ == "__main__":
    main()
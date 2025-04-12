from src.seatguru import ConfigurationFinder
from src.rzjets import AirframeFinder

def reformat(aircraft):
    name = aircraft.split()
    new_name = name[-1]
    if new_name[0] == "7":
        new_name = "B" + new_name
    return new_name

def main():
    # initialize scrapers
    seatguru = ConfigurationFinder()
    airframes = AirframeFinder()

    # prompt user inputs for airline, aircraft, ICAO type code, and civil registration
    operator = input("Operator: ").title()
    aircraft = input("Aircraft: ").upper()
    type_code = input("Type: ").upper()
    registration = input("Registration: ").upper()
    
    # use airline and aircraft to find seating configs
    seats = seatguru.scrape(operator, aircraft)
    if seats == 0:
        # currently skips the process if source lacks the config, should implement aerolopa as primary source
        manual = input("Manually enter seat configuration: ")
        seats = int(manual) if manual.isdigit() else 0
    print(f"{operator} {aircraft} {registration} configured with {seats} seats")

    # use registration to find airframe information
    airframe = airframes.scrape(registration)
    # reformat aircraft name to ICAO convention: 777-300ER -> B777-300ER
    airframe["Aircraft"] = reformat(airframe["Aircraft"])

    # print relevant data, will later change to feed to simbrief directly
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
import atexit
import shelve


class Commands:

    def __init__(self, file: str):
        campaign = shelve.open(file, writeback=True)
        self.campaign = campaign
        self.scrapRatio = 0.5
        self.resourceGenerationRatio = 10
        self.brachistochroneMassRatio = 15
        self.hohmannMassRatio = 30

        def exit_close():
            campaign.close()

        atexit.register(exit_close)

    def open_campaign(self, file: str):
        self.campaign = shelve.open(file, writeback=True)

    def close_campaign(self):
        """ Writes and closes campaign shelve.
        :return: None
        """
        self.campaign.close()

    def init_campaign(self):
        """ Initializes a campaign by adding the base dicts
        :return: None
        """

        # Add the dicts if they do not exist, don't overwrite if there is already data
        if 'planets' not in self.campaign:
            self.campaign['planets'] = {}
        if 'players' not in self.campaign:
            self.campaign['players'] = {}
        if 'ships' not in self.campaign:
            self.campaign['ships'] = {}
        if 'turn' not in self.campaign:
            self.campaign['turn'] = 0

    def add_planet(self, planet: str, value: int, factionControl: str, factionAllegiance: str):
        """ Add a planet to the campaign
        :param planet: name of planet
        :param value: value stat of the planet, each faction receives x10 this value per turn
        :param factionControl: faction that currently controls this planet
        :param factionAllegiance: faction that the planet is aligned to
        :return: None
        """

        # add the planet to the dict
        self.campaign['planets'][planet] = {}
        localPlanet = self.campaign['planets'][planet]

        # assign the value stat, factions, connections, and dicts to the planet
        localPlanet['value'] = value
        localPlanet['factionControl'] = factionControl
        localPlanet['factionAllegiance'] = factionAllegiance
        localPlanet['connections'] = {}
        localPlanet['resources'] = {}
        localPlanet['ships'] = {}
        localPlanet['fleets'] = {}
        localPlanet['production'] = {}

        # assign all the starting vars for the player
        for player in self.campaign['players']:
            localPlanet['resources'][player] = 0
            localPlanet['ships'][player] = {}
            localPlanet['fleets'][player] = {}
            localPlanet['production'][player] = {}

        # return a message for the added planet
        print(f"Planet {planet} added")

    def add_connection(self, planet1: str, planet2: str, distance: int):
        """ Add a connection from a planet to another
        :param planet1: name of the first planet
        :param planet2: name of the second planet
        :param distance: distance between the 2 planets
        :return: None
        """

        # wrap everything in a try block to catch any KeyErrors
        try:
            # add the connections
            self.campaign['planets'][planet1]['connections'][planet2] = distance
            self.campaign['planets'][planet2]['connections'][planet1] = distance
            # return a message for the added connections
            print(f"Travel connection from {planet1} to {planet2} of distance {distance} added")
        # if there was a KeyError then some planet does not exist
        except KeyError:
            # therefore return a message informing that a planet does not exist
            print('One or both planets does not exist, did you misspell anything?')

    def add_player(self, player: str, faction: str):
        """ Add a player to the campaign
        :param player: name of player
        :param faction: faction the player is in
        :return: None
        """

        # add the faction to the dict if it does not exist
        if player not in self.campaign['players']:
            self.campaign['players'][player] = {'faction': faction, 'transits': {}}

        # then for every planet
        for planet in self.campaign['planets']:
            localPlanet = self.campaign['planets'][planet]
            # if the player added is not already listed in the planet, assign all the starting vars for the player
            if player not in localPlanet['resources']:
                localPlanet['resources'][player] = 0
            if player not in localPlanet['ships']:
                localPlanet['ships'][player] = {}
            if player not in localPlanet['fleets']:
                localPlanet['fleets'][player] = {}
            if player not in localPlanet['production']:
                localPlanet['production'][player] = {}

        # return a message for the added player
        print(f"Player {player} added")

    def add_ship_to_campaign(self, ship: str, points: int, resStorage: int, mass: int):
        """ Add a ship to the campaign database
        :param ship: name of the ship
        :param points: points value of the ship
        :param resStorage: max resource storage of the ship
        :param mass: mass of the ship
        :return: None
        """
        # add the ship to the dict
        self.campaign['ships'][ship] = {'points': points, 'resStorage': resStorage, 'mass': mass}
        # return a message for the added ship to the database
        print(f"Ship {ship} added to the campaign database")

    def cheat_in_ship(self, planet: str, player: str, ship: str, amount: int):
        """ Cheat in ship(s) for a player on a planet instantly without spending resources
        :param planet: planet of the spawned ship(s)
        :param player: player receiving the ship(s)
        :param ship: name of the ship(s)
        :param amount: amount of ships(s)
        :return: None
        """

        # wrap everything in a try block to catch any KeyErrors
        try:
            # test if the ship is currently in the database
            if 'ships' in self.campaign and ship in self.campaign['ships']:
                localShips = self.campaign['planets'][planet]['ships']
                # if so spawn in the ship to the player on the planet requested
                if ship in localShips[player]:
                    localShips[player][ship] += amount
                else:
                    localShips[player][ship] = amount
                # return a message for the spawned ship
                print(f"Ship {ship} (x{amount}) spawned in on {planet} for {player}")
            # if not, then return a message informing that the ship isn't added yet
            else:
                print(f"Ship {ship} not recognized, have you added the ship to this campaign?")
        # if there was a KeyError then some planet or player does not exist
        except KeyError:
            # therefore return a message informing that a planet or player does not exist
            print('Some field (planet or player) does not exist, did you misspell anything?')

    def cheat_in_resources(self, planet: str, player: str, amount: int):
        """ Cheat in resources for a player on a planet instantly
        :param planet: planet of the spawned resources
        :param player: player receiving the resources
        :param amount: amount of resources spawned
        :return: None
        """

        # wrap everything in a try block to catch any KeyErrors
        try:
            # spawn in the resources to the player on the planet requested
            self.campaign['planets'][planet]['resources'][player] += amount
            # return a message for the spawned resources
            print(f"{amount} resources spawned in on {planet} for {player}")
        # if there was a KeyError then some planet or player does not exist
        except KeyError:
            # therefore return a message informing that a planet or player does not exist
            print('Some field (planet or player) does not exist, did you misspell anything?')

    def void_resources(self, planet: str, player: str, amount: int):
        """ Void resources removing the amount specified from the game
        :param planet: planet of the voided resources
        :param player: player the resources are voided
        :param amount: amount of resources voided
        :return: None
        """

        # wrap everything in a try block to catch any KeyErrors
        try:
            if self.campaign['planets'][planet]['resources'][player] >= amount:
                self.campaign['planets'][planet]['resources'][player] -= amount
                print(f"{amount} resources voided on {planet} for {player}")
            else:
                print(f'Not enough resources on {planet} ({player}) to be voided')

        # if there was a KeyError then some planet or player does not exist
        except KeyError:
            # therefore return a message informing that a planet or player does not exist
            print('Some field (planet or player) does not exist, did you misspell anything?')

    def make_ship(self, planet: str, player: str, ship: str, amount: int):
        """ Queue production of ship(s) for a player on a planet by spending resources equal to points of the ship(s)
        :param planet: planet of the spawned ship(s)
        :param player: player receiving the ship(s)
        :param ship: name of the ship(s)
        :param amount: amount of ships(s)
        :return: None
        """

        # wrap everything in a try block to catch any KeyErrors
        try:
            # assume the user can make the ship
            canMakeShip = True

            # assign needed vars
            planetFaction = self.campaign['planets'][planet]['factionControl']
            playerFaction = self.campaign['players'][player]['faction']
            localResources = self.campaign['planets'][planet]['resources']
            localProduction = self.campaign['planets'][planet]['production']

            # test if the planet in under the user's faction's control
            if playerFaction != planetFaction:
                canMakeShip = False
                print(f'Planet controlled by {planetFaction}, {player} can not built here')

            # test if the ship is currently in the database
            if ship not in self.campaign['ships']:
                canMakeShip = False
                print('Ship not recognized, have you added the ship to this campaign?')

            # test if the player has enough resources
            if self.campaign['ships'][ship]['points'] * amount > localResources[player]:
                canMakeShip = False
                print(f"Not enough resources on {planet} for production of {amount} {ship}'s")

            # if the ship(s) can still be made, do so
            if canMakeShip:
                # queue the ship for production for the player on the planet requested
                if ship in localProduction[player]:
                    localProduction[player][ship] += amount
                else:
                    localProduction[player][ship] = amount
                    # and deduct the resources from the player who queued the ship(s) on the planet requested
                    localResources[player] -= self.campaign['ships'][ship]['points'] * amount
                # return a message for the spawned ship
                print(f"Ship {ship} (x{amount}) queued for production on {planet} for {player}")
        # if there was a KeyError then some planet or player does not exist
        except KeyError:
            # therefore return a message informing that a planet or player does not exist
            print('Some field (planet or player) does not exist, did you misspell anything?')

    def void_ship(self, planet: str, player: str, ship: str, amount: int):
        """ Void ship(s) removing the amount specified from the game
        :param planet: planet of the ship(s)
        :param player: player who controls the ship(s)
        :param ship: name of the ship(s)
        :param amount: amount of ships(s) scraped
        :return: None
        """
        try:
            canVoid = True

            localShips = self.campaign['planets'][planet]['ships']
            if 'ships' not in self.campaign and ship not in self.campaign['ships']:
                canVoid = False
                print('Ship not recognized, did you misspell anything?')
            elif amount > localShips[player][ship]:
                canVoid = False
                print(f'Not enough ships on {planet} to void')

            if canVoid:
                if localShips[player][ship] == amount:
                    del localShips[player][ship]
                else:
                    localShips[player][ship] -= amount

                print(f'Ship {ship} (x{amount}) voided on {planet} for {player}')

        except KeyError:
            print('Some field (planet or player) does not exist, did you misspell anything?')

    def scrap_ship(self, planet: str, player: str, ship: str, amount: int):
        """ Scrap ship(s) restoring the scrap ratio to the player who owns it
        :param planet: planet of the ship(s)
        :param player: player who controls the ship(s)
        :param ship: name of the ship(s)
        :param amount: amount of ships(s) scraped
        :return: None
        """
        try:
            canScrap = True

            localShips = self.campaign['planets'][planet]['ships']
            localResources = self.campaign['planets'][planet]['resources']
            if 'ships' not in self.campaign and ship not in self.campaign['ships']:
                canScrap = False
                print('Ship not recognized, did you misspell anything?')
            elif amount > localShips[player][ship]:
                canScrap = False
                print(f'Not enough ships on {planet} to scrap')

            if canScrap:
                if localShips[player][ship] == amount:
                    del localShips[player][ship]
                else:
                    localShips[player][ship] -= amount

                resourcesRecovered = amount * self.campaign['ships'][ship]['points'] * self.scrapRatio
                localResources[player] += resourcesRecovered
                print(f'Ship {ship} (x{amount}) scraped returning {resourcesRecovered} resources on {planet} for {player}')

        except KeyError:
            print('Some field (planet or player) does not exist, did you misspell anything?')

    def make_fleet(self, planet: str, player: str, fleet: str, ships: dict):
        """ Make a fleet for a player on a planet with ship(s) owned by said player and on said planet
        :param planet: planet of the fleet
        :param player: player who controls the fleet
        :param fleet: name of the fleet
        :param ships: dict of ship names as keys and ship amounts as values
        :return: None
        """

        # wrap everything in a try block to catch any KeyErrors
        try:
            # assume that the requested fleet can be made
            canMakeFleet = True

            # assign needed vars
            localShips = self.campaign['planets'][planet]['ships']
            localFleet = self.campaign['planets'][planet]['fleets']

            # test if the ships requested for the fleet can be made from the ships that the player owns
            for shipNameNeeded, shipAmountNeeded in ships.items():
                # if the ship isn't there at all, then the fleet can't be made
                if shipNameNeeded not in localShips[player]:
                    canMakeFleet = False

                # if the amount of ships present is lower then the ships wanted in the fleet, then the fleet can't be made
                for shipName, shipAmount in localShips[player].items():
                    if shipName == shipNameNeeded and shipAmount < shipAmountNeeded:
                        canMakeFleet = False

            # if those tests failed, then there is not enough ships to make the fleet
            if not canMakeFleet:
                print(f'Not enough ships on {planet} to make fleet')

            # test if this fleet already exists
            if fleet in localFleet[player]:
                canMakeFleet = False
                print(f'Fleet {fleet} already exists, choose another fleet name')

            # if the fleet can still be made, do so
            if canMakeFleet:
                # then add the base values and dict for the fleet
                localFleet[player][fleet] = {'resources': 0, 'ships': {}}
                # then for every ship requested
                for shipName, shipAmount in ships.items():
                    # add the ship to the fleet
                    localFleet[player][fleet]['ships'][shipName] = shipAmount
                    # and subtract the ship(s) from the player
                    localShips[player][shipName] -= shipAmount
                    # remove the entry in the dict if there are no more ships
                    if localShips[player][shipName] == 0:
                        del localShips[player][shipName]
                # return a message for the newly made fleet
                print(f'Fleet {fleet} created on {planet} for {player}')

        # if there was a KeyError then some planet or player does not exist
        except KeyError:
            # therefore return a message informing that a planet or player does not exist
            print('Some field (planet or player) does not exist, did you misspell anything?')

    def disband_fleet(self, planet: str, player: str, fleet: str):
        """ Disband a fleet for a player on a planet returning the resources and
        ships in the fleet to said player and on said planet
        :param planet: planet of the fleet
        :param player: player who controls the fleet
        :param fleet: name of the fleet
        :return: None
        """

        # wrap everything in a try block to catch any KeyErrors
        try:
            # assume that the fleet can be disbanded
            canDisbandFleet = True

            # assign needed vars
            localShips = self.campaign['planets'][planet]['ships']
            localFleets = self.campaign['planets'][planet]['fleets']
            localResources = self.campaign['planets'][planet]['resources']

            # test if the fleet exists where the user said it is
            if fleet not in localFleets[player]:
                canDisbandFleet = False
                print('Fleet not recognized, did you misspell anything?')

            # if the fleet can still be disbanded, do so
            if canDisbandFleet:
                # then add the ships in the fleet to the player and planet of where said fleet is
                for shipName, shipAmount in localFleets[player][fleet]['ships'].items():
                    if shipName in localShips[player]:
                        localShips[player][shipName] += shipAmount
                    else:
                        localShips[player][shipName] = shipAmount
                # also add all the resources the fleet has to the planet
                localResources[player] += localFleets[player][fleet]['resources']
                # then remove the fleet
                del localFleets[player][fleet]
                # return a message for the disbanded fleet
                print(f'Fleet {fleet} disbanded on {planet}')

        # if there was a KeyError then some planet or player does not exist
        except KeyError:
            # therefore return a message informing that a planet or player does not exist
            print('Some field (planet / player) does not exist, did you misspell anything?')

    def calculate_fleet_stats(self, fleet: dict):
        totalPoints = 0
        totalResourceStorage = 0
        totalMass = 0
        for shipNameNeeded, shipAmount in fleet['ships'].items():
            for shipName, shipStats in self.campaign['ships'].items():
                if shipName == shipNameNeeded:
                    totalPoints += (shipStats['points'] * shipAmount)
                    totalResourceStorage += (shipStats['resStorage'] * shipAmount)
                    totalMass += (shipStats['mass'] * shipAmount)
        return {'fleetPoints': totalPoints, 'fleetStorage': totalResourceStorage, 'fleetMass': totalMass}

    def transfer_resources(self, planet: str, amount: int, playerFrom: str, locationFrom: str, playerTo: str, locationTo):
        """ Transfer resources between 2 resource pools (on fleet or planet) between any 2 players (can be the same player)
        :param planet: planet where the resources are transferred
        :param amount: amount of resources transferred
        :param playerFrom: player transferring from
        :param locationFrom: fleet/planet transferring from
        :param playerTo: player transferring to
        :param locationTo: fleet/planet transferring to
        :return: None
        """

        # wrap everything in a try block to catch any KeyErrors
        try:
            # assume the the transfer is valid
            canTransfer = True

            # assign needed vars
            localFleets = self.campaign['planets'][planet]['fleets']
            localResources = self.campaign['planets'][planet]['resources']

            # test if the transfer is valid
            if locationFrom != planet and locationFrom not in localFleets[playerFrom]:
                canTransfer = False
                print('Sending fleet or planet not recognized, did you misspell anything?')
            elif locationTo != planet and locationTo not in localFleets[playerTo]:
                canTransfer = False
                print('Receiving fleet or planet not recognized, did you misspell anything?')
            elif locationFrom == planet and amount > localResources[playerFrom]:
                canTransfer = False
                print(f'Not enough resources on Planet {planet} for {playerFrom} to transfer')
            elif locationFrom in localFleets[playerFrom] and amount > localFleets[playerFrom][locationFrom]['resources']:
                canTransfer = False
                print(f'Not enough resources in Fleet {locationFrom} for {playerFrom} to transfer')
            elif locationTo in localFleets[playerTo] and \
                    amount > (self.calculate_fleet_stats(localFleets[playerTo][locationTo])['fleetStorage'] -
                              localFleets[playerTo][locationTo]['resources']):
                canTransfer = False
                print(f'Not enough resource storage space on fleet {locationTo} for {playerFrom} to transfer')

            # if the transfer can still be done, do so
            if canTransfer:
                # take the resources from the specified place
                if locationFrom == planet:
                    localResources[playerFrom] -= amount
                else:
                    localFleets[playerFrom][locationFrom]['resources'] -= amount
                # then give then to the correct place
                if locationTo == planet:
                    localResources[playerTo] += amount
                else:
                    localFleets[playerTo][locationTo]['resources'] += amount
                # return a message about the transfer
                print(f"Transfer of {amount} on {planet} from {locationFrom} ({playerFrom}) to {locationTo} ({playerTo}) completed")

        # if there was a KeyError then some planet or player does not exist
        except KeyError:
            # therefore return a message informing that a planet or player does not exist
            print('Some field (planet / player) does not exist, did you misspell anything?')

    # not refactored below this point

    def hohmann_fleet_transfer(self, player: str, fleet: str, planetFrom: str, planetTo: str):
        """ Queue a hohmann fleet transfer from one planet to another
        :param player: player who controls the fleet
        :param fleet: name of the fleet
        :param planetFrom: planet the fleet is currently at
        :param planetTo: planet the fleet is traveling to
        :return: None
        """
        try:
            canTransfer = True
            localFleets = self.campaign['planets'][planetFrom]['fleets']
            localPlayer = self.campaign['players'][player]
            costPerUnit = self.calculate_fleet_stats(localFleets[player][fleet])['fleetMass'] / self.hohmannMassRatio

            if planetTo not in self.campaign['planets'][planetFrom]['connections']:
                canTransfer = False
                print(f'No connection between {planetFrom} and {planetTo} exists')
            else:
                travelDistance = self.campaign['planets'][planetFrom]['connections'][planetTo]
                travelCost = costPerUnit * travelDistance
                if travelCost > localFleets[player][fleet]['resources']:
                    canTransfer = False
                    print(f"Not enough resources on fleet {fleet} to move from {planetFrom} to {planetTo}")

            if canTransfer:
                localPlayer['transits'][fleet] = {}
                transitFleet = localPlayer['transits'][fleet]

                transitFleet['planetFrom'] = planetFrom
                transitFleet['planetTo'] = planetTo
                transitFleet['transitType'] = 'hohmann'
                transitFleet['progress'] = 0
                transitFleet['costPerUnit'] = costPerUnit
                transitFleet['fleet'] = localFleets[player][fleet]

                del localFleets[player][fleet]
                print(f'Fleet {fleet} ({player}) queued for transit from {planetFrom} to {planetTo}')

        except KeyError:
            print('Some field (planet / player/ fleet) does not exist, did you misspell anything?')

    def brachistochrone_fleet_transfer(self, player: str, fleet: str, planetFrom: str, planetTo: str):
        """ Queue a brachistochrone fleet transfer from one planet to another, special case for distance 1 transfers
        :param player: player who controls the fleet
        :param fleet: name of the fleet
        :param planetFrom: planet the fleet is currently at
        :param planetTo: planet the fleet is traveling to
        :return: None
        """
        try:
            canTransfer = True
            localFleets = self.campaign['planets'][planetFrom]['fleets']
            localPlayer = self.campaign['players'][player]
            costPerUnit = self.calculate_fleet_stats(localFleets[player][fleet])['fleetMass'] / self.brachistochroneMassRatio

            if planetTo not in self.campaign['planets'][planetFrom]['connections']:
                canTransfer = False
                travelDistance = None
                travelCost = None
                print(f'No connection between {planetFrom} and {planetTo} exists')
            else:
                travelDistance = self.campaign['planets'][planetFrom]['connections'][planetTo]
                travelCost = costPerUnit * travelDistance
                if travelCost > localFleets[player][fleet]['resources']:
                    canTransfer = False
                    print(f"Not enough resources on fleet {fleet} to move from {planetFrom} to {planetTo}")

            if canTransfer:
                if travelDistance == 1:
                    localFleets[player][fleet]['resources'] -= travelCost
                    self.campaign['planets'][planetTo]['fleets'][player][fleet] = localFleets[player][fleet]
                    print(f'Fleet {fleet} arrived on {planetTo} from {planetFrom}')
                else:
                    localPlayer['transits'][fleet] = {}
                    transitFleet = localPlayer['transits'][fleet]

                    transitFleet['planetFrom'] = planetFrom
                    transitFleet['planetTo'] = planetTo
                    transitFleet['transitType'] = 'brachistochrone'
                    transitFleet['progress'] = 0
                    transitFleet['costPerUnit'] = costPerUnit
                    transitFleet['fleet'] = localFleets[player][fleet]

                    print(f'Fleet {fleet} ({player}) queued for transit from {planetFrom} to {planetTo}')

                del localFleets[player][fleet]

        except KeyError:
            print('Some field (planet / player/ fleet) does not exist, did you misspell anything?')

    def turn_fleet(self, player: str, fleet: str):
        """ Turn a fleet around that is currently in transit 
        :param player: player who controls the fleet
        :param fleet: name of the fleet
        :return: None
        """
        if fleet in self.campaign['players'][player]['transits']:
            transit = self.campaign['players'][player]['transits'][fleet]
            travelDistance = self.campaign['planets'][transit['planetFrom']]['connections'][transit['planetTo']]
            travelCost = transit['progress'] * transit['costPerUnit']
            if transit['fleet']['resources'] > travelCost:
                transit['progress'] = travelDistance - transit['progress']
                transit['planetFrom'], transit['planetTo'] = transit['planetTo'], transit['planetFrom']
                if transit['progress'] >= travelDistance:
                    self.campaign['planets'][transit['planetTo']]['fleets'][player][fleet] = transit['fleet']
                    print(f"Fleet {fleet} ({player}) has canceled transit from {transit['planetFrom']}")
                    del self.campaign['players'][player]['transits'][fleet]
                else:
                    print(f"Fleet {fleet} ({player}) queued for transit from {transit['planetFrom']} to {transit['planetTo']}")
            else:
                print(f'Not enough resources on fleet {fleet} to turn around')
        else:
            print('Some field (player / fleet) does not exist, did you misspell anything?')

    def end_turn(self):
        # notify the user for turn end
        print(f"--------------------turn {self.campaign['turn']} ended--------------------")
        print(f"Calculating end of turn {self.campaign['turn']} and start of turn {self.campaign['turn'] + 1}")

        # fleet travel
        for player in self.campaign['players']:
            atDestination = []
            for fleet in self.campaign['players'][player]['transits']:
                transit = self.campaign['players'][player]['transits'][fleet]
                distance = self.campaign['planets'][transit['planetFrom']]['connections'][transit['planetTo']]

                if transit['transitType'] == 'hohmann':
                    transit['fleet']['resources'] -= transit['costPerUnit']
                    transit['progress'] += 1

                elif transit['transitType'] == 'brachistochrone':
                    transit['fleet']['resources'] -= (transit['costPerUnit'] * 2)
                    transit['progress'] += 2

                if transit['progress'] >= distance:
                    self.campaign['planets'][transit['planetTo']]['fleets'][player][fleet] = transit['fleet']
                    print(f"Fleet {fleet} ({player}) has arrived at {transit['planetTo']} from {transit['planetFrom']}")
                    atDestination.append(fleet)
                else:
                    print(f"Fleet {fleet} ({player}) is transfering to {transit['planetTo']} from {transit['planetFrom']}, "
                          f"Progress: {transit['progress']}/{distance}")
            # clean up
            for fleet in atDestination:
                del self.campaign['players'][player]['transits'][fleet]

        # battles
        for planet in self.campaign['planets']:
            localPlanet = self.campaign['planets'][planet]
            factionsOnPlanet = {}
            for player in self.campaign['players']:
                faction = self.campaign['players'][player]['faction']

                for ship in localPlanet['ships'][player]:
                    if faction not in factionsOnPlanet:
                        factionsOnPlanet[faction] = {}
                    if ship in factionsOnPlanet[faction]:
                        factionsOnPlanet[faction][ship] += localPlanet['ships'][player][ship]
                    else:
                        factionsOnPlanet[faction][ship] = localPlanet['ships'][player][ship]

                for fleet in localPlanet['fleets'][player]:
                    localFleet = localPlanet['fleets'][player][fleet]
                    for ship in localFleet['ships']:
                        if faction not in factionsOnPlanet:
                            factionsOnPlanet[faction] = {}
                        if ship in factionsOnPlanet[faction]:
                            factionsOnPlanet[faction][ship] += localFleet['ships'][ship]
                        else:
                            factionsOnPlanet[faction][ship] = localFleet['ships'][ship]

            if len(factionsOnPlanet) > 1:
                factions = ''
                for faction in factionsOnPlanet:
                    factions += faction + ', '
                print(f"Battle on {planet} between {factions[0:-2]}")
                for faction in factionsOnPlanet:
                    print(f'Ships for {faction}:')
                    for shipName, shipAmount in factionsOnPlanet[faction].items():
                        print(f'{shipName} (x{shipAmount})')
        # advance the turn count
        self.campaign['turn'] += 1

    def start_turn(self):
        for planet in self.campaign['planets']:
            localPlanet = self.campaign['planets'][planet]
            for player in self.campaign['players']:

                # add income to all players
                if self.campaign['players'][player]['faction'] == localPlanet['factionControl']:
                    localPlanet['resources'][player] += localPlanet['value']

                # produce ships for all players
                for shipName, shipAmount in localPlanet['production'][player].items():
                    if shipName in localPlanet['ships'][player]:
                        localPlanet['ships'][player][shipName] += shipAmount
                    else:
                        localPlanet['ships'][player][shipName] = shipAmount
                    print(f"Production of {shipName} (x{shipAmount}) on {planet} for {player} has finished")
                localPlanet['production'][player].clear()

        # notify the user that the next turn is starting
        print(f"--------------------start turn {self.campaign['turn']}--------------------")
        # save the campaign (look into saving more times and opening/closing the shelve dynamically as users will not input all commands
        # instantly like the controller currently does)
        self.campaign.sync()

    def get_details(self, arg):
        if arg in self.campaign['planets']:
            print(self.campaign['planets'][arg])
        elif arg in self.campaign['players']:
            print(self.campaign['players'][arg])
        elif arg in self.campaign['ships']:
            print(self.campaign['ships'][arg])
        else:
            print('Field does not exist, did you misspell anything?')

    def list(self, arg):
        larg = arg.lower()
        if larg == 'planets':
            print(self.campaign['planets'])
        if larg == 'players':
            print(self.campaign['players'])
        if larg == 'ships':
            print(self.campaign['ships'])

import shelve


class Commands:

    def __init__(self, file: str):
        self.campaign = shelve.open(file, writeback=True)
        self.scrapRatio = 0.5
        self.resourceGenerationRatio = 10
        self.brachistochroneMassRatio = 15
        self.hohmannMassRatio = 30

    def __calculate_fleet_stats(self, fleet: dict):
        totalPoints = 0
        totalResourceStorage = 0
        totalMass = 0
        for shipNameNeeded, shipAmount in fleet['ships'].items():
            for shipName, shipStats in self.campaign['ships'].items():
                if shipName == shipNameNeeded:
                    totalPoints += (shipStats['points'] * shipAmount)
                    totalResourceStorage += (shipStats['resStorage'] * shipAmount)
                    totalMass += (shipStats['mass'] * shipAmount)
        return [totalPoints, totalResourceStorage, totalMass]

    def open_campaign(self, file: str):
        self.campaign = shelve.open(file, writeback=True)

    def close_campaign(self):
        self.campaign.close()

    def init_campaign(self):
        """ Initializes a campaign by adding the base dicts
        :return: None
        """

        # Add the dicts if they do not exist, don't overwrite if there is already data
        if 'planets' not in self.campaign:
            self.campaign['planets'] = {}
        if 'factions' not in self.campaign:
            self.campaign['factions'] = {}
        if 'ships' not in self.campaign:
            self.campaign['ships'] = {}
        if 'turn' not in self.campaign:
            self.campaign['turn'] = 0

    def add_planet(self, name: str, value: int, factionControl: str, factionAllegiance: str):
        """ Add a planet to the campaign
        :param name: name of planet
        :param value: value stat of the planet, each faction receives x10 this value per turn
        :param factionControl: faction that currently controls this planet
        :param factionAllegiance: faction that the planet is aligned to
        :return: None
        """

        # add the planet to the dict
        self.campaign['planets'][name] = {}
        # and reference it for later
        newPlanet = self.campaign['planets'][name]
        # assign the value stat, factions, connections, and players to the planet
        newPlanet['value'] = value
        newPlanet['factionControl'] = factionControl
        newPlanet['factionAllegiance'] = factionAllegiance
        newPlanet['connections'] = {}
        newPlanet['players'] = {}

        # in case a planet is added after players have been added
        for faction in self.campaign['factions']:
            for player in self.campaign['factions'][faction]:
                # add all the stats from every player to the planet
                newPlanet['players'][player] = {}
                newPlanet['players'][player]['resources'] = 0
                newPlanet['players'][player]['ships'] = {}
                newPlanet['players'][player]['fleets'] = {}
                newPlanet['players'][player]['production'] = {}
                newPlanet['players'][player]['transit'] = []

        # return a message for the added planet
        print(f"Planet {name} added")

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

    def add_player(self, name: str, faction: str):
        """ Add a player to the campaign
        :param name: name of player
        :param faction: faction the player is in
        :return: None
        """

        # add the faction to the dict if it does not exist
        if faction not in self.campaign['factions']:
            self.campaign['factions'][faction] = []
        # then add the player to the faction
        self.campaign['factions'][faction].append(name)

        # then for every planet
        for planet in self.campaign['planets']:
            # if the player added is not already listed in the planet
            if name not in self.campaign['planets'][planet]['players']:
                # assign all the starting vars for the player
                self.campaign['planets'][planet]['players'][name] = {}
                self.campaign['planets'][planet]['players'][name]['resources'] = 0
                self.campaign['planets'][planet]['players'][name]['ships'] = {}
                self.campaign['planets'][planet]['players'][name]['fleets'] = {}
                self.campaign['planets'][planet]['players'][name]['production'] = {}
                self.campaign['planets'][planet]['players'][name]['transit'] = []
        # return a message for the added player
        print(f"Player {name} added")

    def add_ship_to_campaign(self, name: str, points: int, resStorage: int, mass: int):
        """ Add a ship to the campaign database
        :param name: name of the ship
        :param points: points value of the ship
        :param resStorage: max resource storage of the ship
        :param mass: mass of the ship
        :return: None
        """
        # add the ship to the dict
        self.campaign['ships'][name] = {'points': points, 'resStorage': resStorage, 'mass': mass}
        # return a message for the added ship to the database
        print(f"Ship {name} added to the campaign database")

    def cheat_in_ship(self, planet: str, owner: str, name: str, amount: int):
        """ Cheat in ship(s) for a player on a planet instantly without spending resources
        :param planet: planet of the spawned ship(s)
        :param owner: player owning the ship(s)
        :param name: name of the ship(s)
        :param amount: amount of ships(s)
        :return: None
        """

        # wrap everything in a try block to catch any KeyErrors
        try:
            # test if the ship is currently in the database
            if 'ships' in self.campaign and name in self.campaign['ships']:
                # if so spawn in the ship to the player on the planet requested
                if name in self.campaign['planets'][planet]['players'][owner]['ships']:
                    self.campaign['planets'][planet]['players'][owner]['ships'][name] += amount
                else:
                    self.campaign['planets'][planet]['players'][owner]['ships'][name] = amount
                # return a message for the spawned ship
                print(f"Ship {name} (x{amount}) spawned in on {planet} for {owner}")
            # if not, then return a message informing that the ship isn't added yet
            else:
                print(f"Ship {name} not recognized, have you added the ship to this campaign?")
        # if there was a KeyError then some planet or player does not exist
        except KeyError:
            # therefore return a message informing that a planet or player does not exist
            print('Some field (planet or player) does not exist, did you misspell anything?')

    def cheat_in_resources(self, planet: str, owner: str, amount: int):
        """ Cheat in resources for a player on a planet instantly
        :param planet: planet of the spawned resources
        :param owner: player owning the resources
        :param amount: amount of resources spawned
        :return: None
        """

        # wrap everything in a try block to catch any KeyErrors
        try:
            # spawn in the resources to the player on the planet requested
            self.campaign['planets'][planet]['players'][owner]['resources'] += amount
            # return a message for the spawned resources
            print(f"{amount} resources spawned in on {planet} for {owner}")
        # if there was a KeyError then some planet or player does not exist
        except KeyError:
            # therefore return a message informing that a planet or player does not exist
            print('Some field (planet or player) does not exist, did you misspell anything?')

    def make_ship(self, planet: str, owner: str, name: str, amount: int):
        """ Queue production of ship(s) for a player on a planet by spending resources equal to points of the ship(s)
        :param planet: planet of the spawned ship(s)
        :param owner: player owning the ship(s)
        :param name: name of the ship(s)
        :param amount: amount of ships(s)
        :return: None
        """

        # wrap everything in a try block to catch any KeyErrors
        try:
            can_build = False
            for faction, playerList in self.campaign['factions'].items():
                if owner in playerList and faction == self.campaign['planets'][planet]['factionControl']:
                    can_build = True

            if can_build:
                # test if the ship is currently in the database
                if 'ships' in self.campaign and name in self.campaign['ships']:
                    # and then check if the player has enough resources
                    localPlayer = self.campaign['planets'][planet]['players'][owner]
                    if self.campaign['ships'][name]['points'] * amount > localPlayer['resources']:
                        # if not, return a message informing not enough resources for the production
                        print(f"Not enough resources for production of {amount} {name}'s")
                    else:
                        # if so queue the ship for production for the player on the planet requested
                        if name in localPlayer['production']:
                            localPlayer['production'][name] += amount
                        else:
                            localPlayer['production'][name] = amount
                        # and deduct the resources from the player who queued the ship(s) on the planet requested
                            localPlayer['resources'] -= self.campaign['ships'][name]['points'] * amount
                        # return a message for the spawned ship
                        print(f"Ship {name} (x{amount}) queued for production on {planet} for {owner}")
                # if not, then return a message informing that the ship isn't added yet
                else:
                    print('Ship not recognized, have you added the ship to this campaign?')
            else:
                print('Planet not controlled by requesters faction')
        # if there was a KeyError then some planet or player does not exist
        except KeyError:
            # therefore return a message informing that a planet or player does not exist
            print('Some field (planet or player) does not exist, did you misspell anything?')

    def make_fleet(self, planet: str, owner: str, name: str, ships: dict):
        """ Make a fleet for a player on a planet with ship(s) owned by said player and on said planet
        :param planet: planet of the fleet
        :param owner: player owning the fleet
        :param name: name of the fleet
        :param ships: dict of ship names as keys and ship amounts as values
        :return: None
        """

        # wrap everything in a try block to catch any KeyErrors
        try:
            # assume that the requested fleet can be made
            canMakeFleet = True
            # then check if the ships requested for the fleet can be made from the ships that the player owns
            localPlayer = self.campaign['planets'][planet]['players'][owner]
            for shipNameNeeded, shipAmountNeeded in ships.items():
                # if the ship isn't there at all, then the fleet can't be made
                if shipNameNeeded not in localPlayer['ships']:
                    canMakeFleet = False
                # if the amount of ships present is lower then the ships wanted in the fleet, then the fleet can't be made
                for shipName, shipAmount in localPlayer['ships'].items():
                    if shipName == shipNameNeeded and shipAmount < shipAmountNeeded:
                        canMakeFleet = False

            # if the fleet can be made and is unique
            if canMakeFleet and name not in localPlayer['fleets']:
                # then add the base values and dict for the fleet
                localPlayer['fleets'][name] = {'resources': 0, 'ships': {}}
                # then for every ship requested
                for shipName, shipAmount in ships.items():
                    # add the ship to the fleet
                    localPlayer['fleets'][name]['ships'][shipName] = shipAmount
                    # and subtract the ship(s) from the player
                    localPlayer['ships'][shipName] -= shipAmount
                # return a message for the newly made fleet
                print(f'Fleet {name} created on {planet} for {owner}')
            # if not, then return a message informing that the fleet can't be made with available ships or isn't unique
            else:
                print('Not enough ships at planet to make fleet or fleet already exists, did you misspell anything?')
        # if there was a KeyError then some planet or player does not exist
        except KeyError:
            # therefore return a message informing that a planet or player does not exist
            print('Some field (planet or player) does not exist, did you misspell anything?')

    def disband_fleet(self, planet: str, owner: str, name: str):
        """ Disband a fleet for a player on a planet returning the resources and
        ships in the fleet to said player and on said planet
        :param planet: planet of the fleet
        :param owner: player owning the fleet
        :param name: name of the fleet
        :return: None
        """

        # wrap everything in a try block to catch any KeyErrors
        try:
            # if the fleet exists where it claims to exist
            localPlayer = self.campaign['planets'][planet]['players'][owner]
            if name in localPlayer['fleets']:
                # then add the ships in the fleet to the player and planet of where said fleet is
                for shipName, shipAmount in localPlayer['fleets'][name]['ships'].items():
                    if shipName in localPlayer['ships']:
                        localPlayer['ships'][shipName] += shipAmount
                    else:
                        localPlayer['ships'][shipName] = shipAmount
                # also add all the resources the fleet has to the planet
                localPlayer['resources'] += localPlayer['fleets'][name]['resources']
                # then remove the fleet
                del localPlayer['fleets'][name]
                print(f'Fleet {name} disbanded on {planet}')
            # if not, return a message informing that the fleet does not exist
            else:
                print('Fleet not recognized, did you misspell anything?')
        # if there was a KeyError then some planet or player does not exist
        except KeyError:
            # therefore return a message informing that a planet or player does not exist
            print('Some field (planet / player) does not exist, did you misspell anything?')

    def transfer_resources(self, planet: str, amount: int, ownerFrom: str, locationFrom: str, ownerTo: str, locationTo):
        """ Transfer resources between 2 resource pools (on fleet or planet) between any 2 players (can be the same player)
        :param planet: planet where the resources are transferred
        :param amount: amount of resources transferred
        :param ownerFrom: player transferring from
        :param locationFrom: fleet/planet transferring from
        :param ownerTo: player transferring to
        :param locationTo: fleet/planet transferring to
        :return: None
        """

        # wrap everything in a try block to catch any KeyErrors
        try:
            # setup the local players and assume the the transfer is valid
            playerFrom = self.campaign['planets'][planet]['players'][ownerFrom]
            playerTo = self.campaign['planets'][planet]['players'][ownerTo]
            canTransfer = True

            # disallow the transfer if the fleet does not exist or the resources are more then the fleet has storage space
            if locationTo != 'planet' and locationTo not in playerTo['fleets']:
                canTransfer = False
            elif locationFrom != 'planet' and locationFrom not in playerFrom['fleets']:
                canTransfer = False
            elif locationFrom in playerFrom['fleets'] and amount > playerFrom['fleets'][locationFrom]['resources']:
                canTransfer = False
            elif locationTo in playerTo['fleets'] and amount > (self.__calculate_fleet_stats(playerTo['fleets'][locationTo])[1] -
                                                                playerTo['fleets'][locationTo]['resources']):
                canTransfer = False

            # if the transfer was not disallowed
            if canTransfer:
                transferredResources = None
                # then take resources if enough from the specified location
                if locationFrom == 'planet' and playerFrom['resources'] >= amount:
                    transferredResources = amount
                    playerFrom['resources'] -= amount
                elif locationFrom in playerFrom['fleets'] and playerFrom['fleets'][locationFrom]['resources'] >= amount:
                    transferredResources = amount
                    playerFrom['fleets'][locationFrom]['resources'] -= amount
                # if there was not enough then the fleet does not exist or there was not enough resources
                else:
                    print('Not enough resources to transfer or Fleet does not exist, did you misspell anything?')

                # if there were some resources taken
                if transferredResources is not None:
                    # then give then to the correct places
                    if locationTo == 'planet':
                        playerFrom['resources'] += transferredResources
                        print(f"Transfer on {planet} from {ownerFrom} to {ownerTo} completed")
                    elif locationTo in playerTo['fleets']:
                        playerTo['fleets'][locationTo]['resources'] += transferredResources
                        print(f"Transfer on {planet} from {ownerFrom} to {ownerTo} completed")
                    else:
                        print('This should never happen, if it does something has gone wrong. Contact Starficz and cheat in resources '
                              'for the player that is giving resources as the resources have now been voided')
            else:
                print('Not enough resources to transfer, not enough space on target,'
                      ' or Fleet does not exist, did you misspell anything?')
        # if there was a KeyError then some planet or player does not exist
        except KeyError:
            # therefore return a message informing that a planet or player does not exist
            print('Some field (planet / player) does not exist, did you misspell anything?')

    def hohmann_fleet_transfer(self, owner: str, fleetName: str, planetFrom: str, planetTo: str):
        """ Queue a hohmann fleet transfer from one planet to another
        :param owner: player owning the fleet
        :param fleetName: name of the fleet
        :param planetFrom: planet the fleet is currently at
        :param planetTo: planet the fleet is traveling to
        :return: None
        """
        try:
            localPlayer = self.campaign['planets'][planetFrom]['players'][owner]
            localFleet = localPlayer['fleets'][fleetName]
            fleetStats = self.__calculate_fleet_stats(localFleet)
            travelDistance = self.campaign['planets'][planetFrom]['connections'][planetTo]
            travelCost = (fleetStats[2] / self.hohmannMassRatio) * travelDistance
            if travelCost <= localFleet['resources']:
                localPlayer['transit'].append({'planetTo': planetTo, 'type': 'hohmann', 'progress': 0,
                                               'fleet': localFleet, 'name': fleetName})
                localFleet['resources'] -= travelCost
                del localPlayer['fleets'][fleetName]
                print(f'Fleet {fleetName} queued for transit from {planetFrom} to {planetTo}')
            else:
                print(f"Not enough resources to move fleet, required:{travelCost}, Fleet currently has:{localFleet['resources']}")
        except KeyError:
            print('Some field (planet / player/ fleet) does not exist, did you misspell anything?')

    def brachistochrone_fleet_transfer(self, owner: str, fleetName: str, planetFrom: str, planetTo: str):
        """ Queue a brachistochrone fleet transfer from one planet to another, special case for distance 1 transfers
        :param owner: player owning the fleet
        :param fleetName: name of the fleet
        :param planetFrom: planet the fleet is currently at
        :param planetTo: planet the fleet is traveling to
        :return: None
        """
        try:
            localPlayer = self.campaign['planets'][planetFrom]['players'][owner]
            localFleet = localPlayer['fleets'][fleetName]
            fleetStats = self.__calculate_fleet_stats(localFleet)
            travelDistance = self.campaign['planets'][planetFrom]['connections'][planetTo]
            travelCost = (fleetStats[2] / self.brachistochroneMassRatio) * travelDistance
            if travelCost <= localFleet['resources']:
                if travelDistance == 1:
                    self.campaign['planets'][planetTo]['players'][owner]['fleets'][fleetName] = localFleet
                    print(f'Fleet {fleetName} arrived at {planetTo} from {planetFrom}')
                else:
                    localPlayer['transit'].append({'planetTo': planetTo, 'type': 'brachistochrone', 'progress': 0,
                                                   'fleet': localFleet, 'name': fleetName})
                    print(f'Fleet {fleetName} queued for transit from {planetFrom} to {planetTo}')
                localFleet['resources'] -= travelCost
                del localPlayer['fleets'][fleetName]
            else:
                print(f"Not enough resources to move fleet, required:{travelCost}, Fleet currently has:{localFleet['resources']}")
        except KeyError:
            print('Some field (planet / player/ fleet) does not exist, did you misspell anything?')

    def scrap_ship(self, planet: str, owner: str, name: str, amount: int):
        """ Scrap ship(s) restoring the scrap ratio to the player who owns it
        :param planet: planet of the ship(s)
        :param owner: player owning the ship(s)
        :param name: name of the ship(s)
        :param amount: amount of ships(s) scraped
        :return: None
        """
        try:
            if 'ships' in self.campaign and name in self.campaign['ships']:
                localPlayer = self.campaign['planets'][planet]['players'][owner]
                if name in localPlayer['ships'] and \
                        amount <= localPlayer['ships'][name]:
                    localPlayer['ships'][name] -= amount
                    resources = amount * self.campaign['ships'][name]['points'] * self.scrapRatio
                    localPlayer['resources'] += resources
                    print(f'Ship {name} (x{amount}) scraped returning {resources} resources on {planet} for {owner}')
                else:
                    print('Not enough ship(s) for scraping')
            else:
                print('Ship not recognized, have you added the ship to this campaign?')
        except KeyError:
            print('Some field (planet or player) does not exist, did you misspell anything?')

    def advance_turn(self):
        print(f"--------------------turn {self.campaign['turn']} ended--------------------")
        print(f"Calculating end of turn {self.campaign['turn']} and start of turn {self.campaign['turn'] + 1}")
        for planet in self.campaign['planets']:
            for faction in self.campaign['factions']:
                for player in self.campaign['factions'][faction]:
                    if faction == self.campaign['planets'][planet]['factionControl']:
                        self.campaign['planets'][planet]['players'][player]['resources'] += \
                            (self.campaign['planets'][planet]['value'] * self.resourceGenerationRatio) / \
                            len(self.campaign['factions'][faction])
                    localPlayer = self.campaign['planets'][planet]['players'][player]
                    for ship, amount in localPlayer['production'].items():
                        if ship in self.campaign['planets'][planet]['players'][player]['ships']:
                            localPlayer['ships'][ship] += amount
                        else:
                            localPlayer['ships'][ship] = amount
                        print(f"Production of {ship}, (x{amount}) has been finished at {planet}")
                        localPlayer['production'] = {}

                    for fleet in localPlayer['transit']:
                        if fleet['type'] == 'hohmann':
                            fleet['progress'] += 1
                        elif fleet['type'] == 'brachistochrone':
                            fleet['progress'] += 2
                        if fleet['progress'] == self.campaign['planets'][planet]['connections'][fleet['planetTo']]:
                            self.campaign['planets'][fleet['planetTo']]['players'][player]['fleets'][fleet['name']] = fleet['fleet']
                            localPlayer['transit'].remove(fleet)
                            print(f"Fleet {fleet['name']} has arrived at {fleet['planetTo']} from {planet}")
                        else:
                            print(f"Fleet {fleet['name']} has traveled {fleet['progress']} out of "
                                  f"{self.campaign['planets'][planet]['connections'][fleet['planetTo']]} to "
                                  f"{fleet['planetTo']} from {planet}")
        print(f"--------------------start turn {self.campaign['turn'] + 1}--------------------")
        self.campaign['turn'] += 1

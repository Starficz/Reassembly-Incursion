from cmd import Cmd

from CampaignCommands import Commands


class IncursionShell(Cmd):
    def __init__(self, file: str):
        Cmd.__init__(self)
        self.campaign = Commands(file)

    def do_exit(self, args):
        """Exits the program."""
        print("Exiting the program.")
        raise SystemExit

    def do_add_planet(self, args):
        """ Add a planet to the campaign
        format: [name, value, control, allegiance]
        """
        try:
            argList = eval(args)
            self.campaign.add_planet(argList[0], argList[1], argList[2], argList[3])
        except (ValueError, SyntaxError):
            print('Invalid Input, Try again')

    def do_add_connection(self, args):
        """ Add a connection to 2 planets
        format: [planet1, planet2, distance]
        """
        try:
            argList = eval(args)
            self.campaign.add_connection(argList[0], argList[1], argList[2])
        except (ValueError, SyntaxError):
            print('Invalid Input, Try again')

    def do_add_player(self, args):
        """ Add a player to the campaign
        format: [name, faction]
        """
        try:
            argList = eval(args)
            self.campaign.add_player(argList[0], argList[1])
        except (ValueError, SyntaxError):
            print('Invalid Input, Try again')

    def do_materialize_resources(self, args):
        """ Materialize resources from nothing
        format: [planet, player, amount]
        """
        try:
            argList = eval(args)
            self.campaign.cheat_in_resources(argList[0], argList[1], argList[2])
        except (ValueError, SyntaxError):
            print('Invalid Input, Try again')

    def do_banish_resources(self, args):
        """ banish resources into the void
        format: [planet, player, amount]
        """
        try:
            argList = eval(args)
            self.campaign.void_resources(argList[0], argList[1], argList[2])
        except (ValueError, SyntaxError):
            print('Invalid Input, Try again')

    def do_register_ship(self, args):
        """ Register a ship to the campaign
        format: [name, points, storage, mass]
        """
        try:
            argList = eval(args)
            self.campaign.add_ship_to_campaign(argList[0], argList[1], argList[2], argList[3])
        except (ValueError, SyntaxError):
            print('Invalid Input, Try again')

    def do_materialize_ship(self, args):
        """ Materialize ship(s) from nothing
        format: [planet, player, ship, amount]
        """
        try:
            argList = eval(args)
            self.campaign.cheat_in_ship(argList[0], argList[1], argList[2], argList[3])
        except (ValueError, SyntaxError):
            print('Invalid Input, Try again')

    def do_banish_ship(self, args):
        """ banish ship(s) into the void
        format: [planet, player, ship, amount]
        """
        try:
            argList = eval(args)
            self.campaign.void_ship(argList[0], argList[1], argList[2], argList[3])
        except (ValueError, SyntaxError):
            print('Invalid Input, Try again')

    def do_make_ship(self, args):
        """ Queue production of ship(s) by spending resources equal to points of the ship(s)
        format: [planet, player, ship, amount]
        """
        try:
            argList = eval(args)
            self.campaign.make_ship(argList[0], argList[1], argList[2], argList[3])
        except (ValueError, SyntaxError):
            print('Invalid Input, Try again')

    def do_scrap_ship(self, args):
        """ Scrap ship(s) restoring the a percentage of points used to build the ship(s) equal to the scrap ratio
        format: [planet, player, ship, amount]
        """
        try:
            argList = eval(args)
            self.campaign.scrap_ship(argList[0], argList[1], argList[2], argList[3])
        except (ValueError, SyntaxError):
            print('Invalid Input, Try again')

    def do_make_fleet(self, args):
        """ Make a fleet using ship(s) to allow for transfers
        format: [planet, player, fleet, {ship1: amount, ship2: amount, ect...}]
        """
        try:
            argList = eval(args)
            self.campaign.make_fleet(argList[0], argList[1], argList[2], argList[3])
        except (ValueError, SyntaxError):
            print('Invalid Input, Try again')

    def do_disband_fleet(self, args):
        """ Disband a fleet returning the resources and ships in the fleet to their owner
        format: [planet, player, fleet]
        """
        try:
            argList = eval(args)
            self.campaign.disband_fleet(argList[0], argList[1], argList[2])
        except (ValueError, SyntaxError):
            print('Invalid Input, Try again')

    def do_transfer_resources(self, args):
        """ Transfer resources between 2 resource pools (fleet or planet) between any 2 players (can be the same player)
        format: [planet, amount, player_from, location_from*, player_to, location_to*]
        * The locations can be a fleet name or planet name
        """
        try:
            argList = eval(args)
            self.campaign.transfer_resources(argList[0], argList[1], argList[2], argList[3], argList[4], argList[5])
        except (ValueError, SyntaxError):
            print('Invalid Input, Try again')

    def do_hohmann_transfer(self, args):
        """ Queue a hohmann fleet transfer from one planet to another
        format: [player, fleet, planet_from, planet_to]
        """
        try:
            argList = eval(args)
            self.campaign.hohmann_fleet_transfer(argList[0], argList[1], argList[2], argList[3])
        except (ValueError, SyntaxError):
            print('Invalid Input, Try again')

    def do_brachistochrone_transfer(self, args):
        """ Queue a brachistochrone fleet transfer from one planet to another
        format: [player, fleet, planet_from, planet_to]
        """
        try:
            argList = eval(args)
            self.campaign.hohmann_fleet_transfer(argList[0], argList[1], argList[2], argList[3])
        except (ValueError, SyntaxError):
            print('Invalid Input, Try again')

    def do_turn_fleet(self, args):
        """ Turn a fleet around to travel in the opposite direction its currently traveling
        format: [player, fleet]
        """
        try:
            argList = eval(args)
            self.campaign.turn_fleet(argList[0], argList[1])
        except (ValueError, SyntaxError):
            print('Invalid Input, Try again')

    def do_end_turn(self):
        """ End the turn by calculate fleet travel and resolving battles (ships have to be banished manually)"""
        self.campaign.end_turn()

    def do_start_turn(self):
        """Start the next turn by adding income and building ships that have been queued (don't call this before end_turn)"""
        self.campaign.start_turn()


if __name__ == '__main__':
    print("WARNING, this shell runs eval on all arguments so its possible to do really dumb things. Don't do those please.")
    Incursion = IncursionShell('IncursionSave')
    Incursion.prompt = '> '
    Incursion.cmdloop('Incursion Console v0.1 alpha')

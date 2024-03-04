###############################################################################
#
# Pot - A class to track the money and players in each pot/side pot.
#
# Author - Ryan Muetzel (@pretzelryan)
#

class Pot:
    """
    A class to track the money and players in each pot/side pot.

    """

    def __init__(self):
        # TODO: Docs
        self.chip_total = 0
        self.player_list = []

    def __repr__(self):
        return "Pot size: " + str(self.chip_total)

#!/usr/bin/env python3
if __name__ == '__main__':
    import os, sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

import logging

from trosnoth.levels.base import playLevel
from trosnoth.levels.standard import StandardRandomLevel
from trosnoth.triggers.coins import AwardStartingCoinsTrigger

log = logging.getLogger(__name__)


class TestingLevel(StandardRandomLevel):

    allowAutoBalance = False

    def pregameCountdownPhase(self, **kwargs):
        AwardStartingCoinsTrigger(self, coins=10000).activate()


if __name__ == '__main__':
    playLevel(TestingLevel(halfMapWidth=3, mapHeight=2), aiCount=0)

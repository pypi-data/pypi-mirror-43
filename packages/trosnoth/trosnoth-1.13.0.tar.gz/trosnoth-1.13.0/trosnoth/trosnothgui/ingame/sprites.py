

import datetime
import logging
import math
from math import pi
import random

import pygame
import pygame.gfxdraw

from trosnoth.const import (
    MAP_TO_SCREEN_SCALE, COLLECTABLE_COIN_LIFETIME, TICK_PERIOD,
    DEFAULT_COIN_VALUE,
)
from trosnoth.gui.framework.basics import (
    AngledImageCollection, Animation, SingleImage,
)
from trosnoth.model.player import Player
from trosnoth.trosnothgui.common import setAlpha
from trosnoth.trosnothgui.ingame.nametag import (
    NameTag, CoinTally, HealthBar, CountDown,
)
from trosnoth.trosnothgui.ingame.utils import mapPosToScreen
from trosnoth.utils.math import fadeValues, isNear

log = logging.getLogger(__name__)


class UnitSprite(pygame.sprite.Sprite):
    def __init__(self, app, worldGUI, unit):
        super(UnitSprite, self).__init__()
        self.app = app
        self.worldGUI = worldGUI
        self.unit = unit

    @property
    def pos(self):
        return self.unit.tweenPos(self.worldGUI.tweenFraction)


class ShotSprite(object):
    TICK_TRAIL = 1.3

    def __init__(self, app, worldGUI, shot):
        self.app = app
        self.worldGUI = worldGUI
        self.shot = shot
        self.colour = app.theme.colours.shot(shot.team)
        ticks = worldGUI.universe.monotonicTicks - 1
        self.drawPoints = [(ticks, shot.tweenPos(0))]

        shot.onRebound.addListener(self.gotRebound)
        shot.onExpire.addListener(self.gotExpire)

    def noLongerInUniverse(self):
        if self.shot:
            self.shot.onRebound.removeListener(self.gotRebound)
            self.shot.onExpire.removeListener(self.gotExpire)
            self.shot = None

    def gotRebound(self, pos):
        self._addDrawPoint(pos)

    def gotExpire(self):
        self._addDrawPoint(self.shot.pos)

    def _addDrawPoint(self, pos):
        self.drawPoints.append((self.worldGUI.universe.monotonicTicks, pos))

    @property
    def pos(self):
        if self.shot:
            return self.shot.tweenPos(self.worldGUI.tweenFraction)
        return None

    def shouldRemove(self):
        if self.shot is not None:
            return False
        if len(self.drawPoints) >= 2:
            return False
        return True

    def draw(self, screen, focus, area):
        wg = self.worldGUI
        worldTicks = wg.universe.monotonicTicks

        addedFinalPoint = False
        if self.shot and self.drawPoints:
            tick, _ = self.drawPoints[-1]
            if tick < worldTicks:
                addedFinalPoint = True
                self._addDrawPoint(self.shot.pos)

        ticksNow = worldTicks - 1 + wg.tweenFraction
        tickCutoff = ticksNow - self.TICK_TRAIL
        self._discardDrawPointsBefore(tickCutoff)
        self._drawPointsUntil(ticksNow, screen, focus, area)

        if addedFinalPoint:
            del self.drawPoints[-1]

    def _discardDrawPointsBefore(self, tickCutoff):
        lastTick = lastPos = None
        while True:
            if not self.drawPoints:
                return
            thisTick, thisPos = self.drawPoints[0]
            if thisTick >= tickCutoff:
                break
            self.drawPoints.pop(0)
            lastTick, lastPos = thisTick, thisPos

        if lastTick is not None:
            fraction = (tickCutoff - lastTick) / (thisTick - lastTick)
            insertPoint = (
                fadeValues(lastPos[0], thisPos[0], fraction),
                fadeValues(lastPos[1], thisPos[1], fraction),
            )
            self.drawPoints.insert(0, (tickCutoff, insertPoint))

    def _drawPointsUntil(self, ticksNow, screen, focus, area):
        if not self.drawPoints:
            return

        ticks0, pos = self.drawPoints[0]
        screenPos0 = mapPosToScreen(pos, focus, area)
        points = [screenPos0]
        for ticks1, pos in self.drawPoints[1:]:
            screenPos1 = mapPosToScreen(pos, focus, area)
            if ticks1 > ticksNow:
                fraction = (ticksNow - ticks0) / (ticks1 - ticks0)
                points.append((
                    fadeValues(screenPos0[0], screenPos1[0], fraction),
                    fadeValues(screenPos0[1], screenPos1[1], fraction),
                ))
                break

            points.append(screenPos1)
            screenPos0 = screenPos1
            ticks0 = ticks1

        if len(points) > 1:
            self.drawLines(screen, area, self.colour, points, thickness=6)

    def drawLines(self, screen, area, colour, points, thickness):
        rect = pygame.Rect(points[0], (0, 0))
        for point in points[1:]:
            rect.union_ip(point, (0, 0))

        if not rect.colliderect(area):
            return

        if not self.app.displaySettings.antialiasedShots:
            pygame.draw.lines(screen, colour, False, points, thickness)
            return

        halfThick = thickness / 2
        outline = []
        x0, y0 = points[0]
        angle = 0
        pt0 = pt5 = None
        for (x1, y1) in points[1:]:
            if (x0, y0) != (x1, y1):
                angle = math.atan2(y1 - y0, x1 - x0)
            sinTheta = math.sin(angle)
            cosTheta = math.cos(angle)

            pt1 = (x0 + halfThick * sinTheta, y0 - halfThick * cosTheta)
            pt2 = (x1 + halfThick * sinTheta, y1 - halfThick * cosTheta)
            pt3 = (x1 - halfThick * sinTheta, y1 + halfThick * cosTheta)
            pt4 = (x0 - halfThick * sinTheta, y0 + halfThick * cosTheta)

            outline.append(pt1)
            outline.append(pt2)
            outline.insert(0, pt4)
            outline.insert(0, pt3)

            pygame.gfxdraw.filled_polygon(screen, [pt1, pt2, pt3, pt4], colour)
            if pt0 and pt5:
                pygame.gfxdraw.filled_polygon(screen, [pt0, pt1, pt4, pt5], colour)
                pygame.gfxdraw.filled_polygon(screen, [pt0, pt1, pt5, pt4], colour)

            x0, y0 = x1, y1
            pt0 = pt1
            pt5 = pt4

        pygame.gfxdraw.aapolygon(screen, outline, colour)


class SingleAnimationSprite(pygame.sprite.Sprite):
    def __init__(self, worldGUI, pos):
        super(SingleAnimationSprite, self).__init__()
        self.app = worldGUI.app
        self.worldGUI = worldGUI
        self.pos = pos
        self.animation = self.getAnimation()
        self.image = self.animation.getImage()
        self.rect = self.image.get_rect()

    def getAnimation(self):
        raise NotImplementedError('getAnimation')

    def update(self):
        self.image = self.animation.getImage()

    def isDead(self):
        return self.animation.isComplete()


class ExplosionSprite(SingleAnimationSprite):
    def getAnimation(self):
        return self.app.theme.sprites.explosion(self.worldGUI.getTime)


class ShoxwaveExplosionSprite(SingleAnimationSprite):
    def getAnimation(self):
        return self.app.theme.sprites.shoxwaveExplosion(self.worldGUI.getTime)


class TrosballExplosionSprite(SingleAnimationSprite):
    def getAnimation(self):
        return self.app.theme.sprites.trosballExplosion(self.worldGUI.getTime)


class GrenadeSprite(UnitSprite):
    def __init__(self, app, worldGUI, grenade):
        super(GrenadeSprite, self).__init__(app, worldGUI, grenade)
        self.grenade = grenade
        self.image = app.theme.sprites.teamGrenade(grenade.player.team)
        self.rect = self.image.get_rect()


class CollectableCoinSprite(UnitSprite):
    def __init__(self, app, worldGUI, coin):
        super(CollectableCoinSprite, self).__init__(app, worldGUI, coin)
        self.coin = coin
        if coin.value >= 2 * DEFAULT_COIN_VALUE:
            self.animation = app.theme.sprites.bigCoinAnimation(
                worldGUI.getTime)
        else:
            self.animation = app.theme.sprites.coinAnimation(worldGUI.getTime)
        self.image = self.animation.getImage()
        self.alphaImage = self.image.copy()
        self.rect = self.image.get_rect()
        self.timer = worldGUI.getTime

    def update(self):
        self.image = self.animation.getImage()
        tick = self.worldGUI.universe.getMonotonicTick()
        fadeTick = self.coin.creationTick + (
                COLLECTABLE_COIN_LIFETIME - 2) // TICK_PERIOD
        if tick >= fadeTick:
            alpha = random.randint(32, 192)
            self.image = self.image.copy()
            setAlpha(self.image, alpha, alphaSurface=self.alphaImage)


class TrosballSprite(pygame.sprite.Sprite):
    def __init__(self, app, worldGUI, world):
        super(TrosballSprite, self).__init__()
        self.app = app
        self.worldGUI = worldGUI
        self.world = world
        self.localState = worldGUI.gameViewer.interface.localState
        self.animation = app.theme.sprites.trosballAnimation(worldGUI.getTime)
        self.warningAnimation = app.theme.sprites.trosballWarningAnimation(
            worldGUI.getTime)
        # Need a starting one:
        self.image = self.animation.getImage()
        self.rect = self.image.get_rect()

    def update(self):
        self.image = self.animation.getImage()
        manager = self.world.trosballManager
        if manager.trosballPlayer is not None:
            trosballExplodeTick = manager.playerGotTrosballTick + (
                self.world.physics.trosballExplodeTime // TICK_PERIOD)
            warningTick = trosballExplodeTick - 2 // TICK_PERIOD
            if self.world.getMonotonicTick() > warningTick:
                self.image = self.warningAnimation.getImage()
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    @property
    def pos(self):
        manager = self.world.trosballManager
        if self.localState.localTrosball:
            x, y = self.localState.localTrosball.tweenPos(
                self.worldGUI.tweenFraction)
        elif manager.trosballUnit:
            x, y = manager.trosballUnit.tweenPos(self.worldGUI.tweenFraction)
        else:
            p = manager.trosballPlayer
            if p.id == self.worldGUI.localPlayerId:
                p = self.worldGUI.localPlayerSprite
            x, y = p.tweenPos(self.worldGUI.tweenFraction)
            x += 5 if p.isFacingRight() else -5
        return (x, y)


class PlayerSprite(UnitSprite):
    # These parameters are used to create a canvas for the player sprite object
    canvasSize = (
        int(33 * MAP_TO_SCREEN_SCALE + 0.5),
        int(40 * MAP_TO_SCREEN_SCALE + 0.5))
    liveOffset = 3
    ghostOffset = 0

    def __init__(self, app, worldGUI, player, timer=None):
        super(PlayerSprite, self).__init__(app, worldGUI, player)
        if timer is None:
            timer = self.worldGUI.getTime
        self.timer = timer
        self._animationStart = None
        self.spriteTeam = player.team
        self.player = player
        self.nametag = NameTag(app, player.nick)
        self.countdown = CountDown(app, self.player)
        self._oldName = player.nick
        self._miniMapNameTag = None
        self.coinTally = CoinTally(app, 0)
        self.healthBar = HealthBar(
            app,
            badColour=self.app.theme.colours.badHealth,
            fairColour=self.app.theme.colours.fairHealth,
            goodColour=self.app.theme.colours.goodHealth)
        self.shieldBar = HealthBar(
            app,
            badColour=self.app.theme.colours.badShield,
            fairColour=self.app.theme.colours.fairShield,
            goodColour=self.app.theme.colours.goodShield)

        sprites = app.theme.sprites
        self.sprites = sprites

        self.ghostAnimation = sprites.ghostAnimation(
            worldGUI.getTime, self.player.team)

        self.shieldAnimation = Animation(0.15, timer, *sprites.shieldImages)

        if self.app.displaySettings.perPixelAlpha:
            flags = pygame.SRCALPHA
            self.alphaImage = pygame.Surface(self.canvasSize, flags)
        else:
            flags = 0
            self.alphaImage = None

        self.image = pygame.Surface(self.canvasSize, flags)
        self.rect = self.image.get_rect()

        # This probably shouldn't be done here.
        _t = datetime.date.today()
        self.is_christmas = _t.day in (24, 25, 26) and _t.month == 12

    @property
    def hookPos(self):
        oldPos, pos = self.player.getGrapplingHookPos()
        fraction = self.worldGUI.tweenFraction
        return (
            fadeValues(oldPos[0], pos[0], fraction),
            fadeValues(oldPos[1], pos[1], fraction),
        )

    def getAngleFacing(self):
        return self.player.angleFacing

    @property
    def angleFacing(self):
        return self.player.angleFacing

    def __getattr__(self, attr):
        '''
        Proxy attributes through to the underlying player class.
        '''
        return getattr(self.player, attr)

    def update(self):
        if self.player.nick != self._oldName:
            self._oldName = self.player.nick
            self.nametag = NameTag(self.app, self.player.nick)
            self._miniMapNameTag = None

        self.setImage()

    def _isSlow(self):
        # Consider horizontal movement of player.
        xMotion = self.player.getXKeyMotion()
        if xMotion < 0:
            return self.player.isFacingRight()
        if xMotion > 0:
            return not self.player.isFacingRight()
        return False

    def setImage(self):
        if not self.app.displaySettings.perPixelAlpha:
            self.image.set_alpha(None)

        self.image.fill((127, 127, 127, 0))
        self.image.set_colorkey((127, 127, 127))

        if self.player.dead:
            self.setGhostImage()
        else:
            self.setLivingPlayerImage()

        if self.player.resyncing:
            self.greyOutImage()

    def setLivingPlayerImage(self):
        showWeapon = True
        regularArms = True
        animation = False
        headOption = 0
        flipHead = not self.player.isFacingRight()
        if self.player.bomber:
            self.renderBomber()
            showWeapon = False
            animation = True
        elif self.player.emote:
            self.renderEmote()
            showWeapon = False
            animation = True
        elif self.player.isGrabbingWall():
            headOption, flipHead = self.renderWallGrabber()
            regularArms = False
        elif self.player.grapplingHook.isAttached():
            self.renderFalling()
        elif self.player.getGroundCollision():
            if isNear(self.player.xVel, 0):
                self.renderStander()
            elif self._isSlow():
                self.renderWalker()
                animation = True
            else:
                self.renderRunner()
                animation = True
        else:
            if self.player.yVel > 0:
                self.renderFalling()
            else:
                self.renderJumping()

        if not animation:
            self._animationStart = None

        self.renderHead(headOption, flipHead)
        if showWeapon:
            self.renderWeapon(regularArms)
        if self.player.hasVisibleShield():
            self.renderShield()

        self.updateLivePlayerImageAlpha()

    def greyOutImage(self):
        grey_colour = (100, 100, 100)
        grey = pygame.Surface(self.image.get_size())
        grey.fill(grey_colour)
        self.image.blit(grey, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
        self.image.blit(grey, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

    def renderBomber(self):
        if self.player.bomber.timeRemaining < 0.8:
            self.pasteSpriteSheetAnimation(
                0.08, ((11, 0), (12, 0)), autoflip=True)
        else:
            self.pasteSpriteSheetAnimation(
                0.1, ((9, 0), (9, 0), (10, 0)), autoflip=True)

    def renderEmote(self):
        i, j = self.getWeaponSpriteIndices()
        if i is not None:
            dx = -5 if self.player.isFacingRight() else 5
            self.pasteSpriteSheet(i + 14, j, autoflip=True, offset=(dx, -10))
        self.pasteSpriteSheetAnimation(
            self.player.emote.frameRate,
            self.player.emote.spriteIndices,
            autoflip=True)

    def renderWallGrabber(self):
        wallAngle = self.player.grabbedSurfaceAngle
        # wallIndex: 0 = vertical wall, 7 = horizontal roof
        wallIndex = int(max(0, min(1, abs(wallAngle * 2 / pi) - 1)) * 7 + 0.5)
        flip = wallAngle > 0 and wallIndex != 7

        # gunAngle: 0 = pointing upwards, clockwise to 2*pi = pointing upwards
        gunAngle = self.player.angleFacing % (2 * pi)
        gunIndex = int(gunAngle * 16 / pi + 0.5)
        if self.player.shoxwave:
            if self.player.isFacingRight():
                gunIndex = 7
            else:
                gunIndex = 26
        elif gunIndex > 16:
            gunIndex += 1

        if 16 <= gunIndex <= 17:
            if self.player.isFacingRight():
                gunIndex = 16
            else:
                gunIndex = 17
        # gunIndex: 0 = pointing upwards, clockwise to 33 = pointing
        # upwards, with 0 to 16 facing right and 17 to 33 facing left.
        faceRight = gunIndex <= 16

        # When actually pasting from the spritesheet, the x-index needs to
        # take into account whether the image will then be flipped.
        if flip:
            gunIndex = 33 - gunIndex
        self.pasteSpriteSheet(gunIndex, 1 + wallIndex, flip=flip)

        # Calculate which head angle to use
        if 3 <= wallIndex <= 6:
            # Angled head
            flipHead = flip
            if faceRight:
                headOption = 1
            else:
                headOption = 2
        else:
            # Normal head
            headOption = 0
            flipHead = not faceRight

        return headOption, flipHead

    def renderStander(self):
        self.pasteSpriteSheet(0, 0, autoflip=True)

    def renderRunner(self):
        self.pasteSpriteSheetAnimation(
            0.1, ((1, 0), (2, 0), (3, 0), (4, 0)), autoflip=True)

    def renderWalker(self):
        self.pasteSpriteSheetAnimation(
            0.1, ((5, 0), (6, 0), (7, 0), (8, 0)), autoflip=True)

    def renderFalling(self):
        self.pasteSpriteSheet(3, 0, autoflip=True)

    def renderJumping(self):
        self.pasteSpriteSheet(3, 0, autoflip=True)

    def getWeaponSpriteIndices(self):
        if self.player.shoxwave:
            return None, None
        if self.player.machineGunner:
            return 0, 10
        if self.player.hasRicochet:
            return 17, 10
        return 17, 9

    def renderWeapon(self, drawArms):
        if self.player.shoxwave:
            if drawArms:
                self.pasteSpriteSheet(7, 9, autoflip=True)
            self.pasteSpriteSheet(13, 0, autoflip=True)
            return

        x0, y0 = self.getWeaponSpriteIndices()
        angle = (self.player.angleFacing + pi) % (2 * pi) - pi
        index = int(abs(angle * 16 / pi) + 0.5)

        if drawArms:
            self.pasteSpriteSheet(index, 9, autoflip=True)
        self.pasteSpriteSheet(x0 + index, y0, autoflip=True)

    def renderHead(self, headOption, flipHead):
        santa = self.is_christmas
        if self.bot:
            self.pasteHead(3 + headOption, flip=flipHead)
        else:
            self.pasteHead(headOption, flip=flipHead)

        if self.player.ninja:
            santa = False
            self.pasteSpriteSheet(31 + headOption, 0, flip=flipHead)
        if self.player.disruptive:
            santa = False
            self.pasteSpriteSheetAnimation(0.2, (
                (16 + headOption, 0), (19 + headOption, 0),
                (22 + headOption, 0)), flip=flipHead)

        if self.player.hasElephant():
            santa = False
            self.pasteSpriteSheet(28 + headOption, 0, flip=flipHead)

        if santa:
            self.pasteSpriteSheet(25 + headOption, 0, flip=flipHead)

    def renderShield(self):
        img = self.shieldAnimation.getImage()
        if not (img.get_flags() & pygame.SRCALPHA):
            # The shield animation already uses per-pixel alphas so if they
            # are enabled we don't need per-surface alphas.
            img.set_alpha(128)
        self.image.blit(img, (self.liveOffset, 0))

    def pasteSpriteSheet(
            self, xIndex, yIndex, *, flip=False, autoflip=False, offset=None):
        if autoflip:
            flip = not self.player.isFacingRight()

        sheet = self.app.theme.sprites.playerSpriteSheet(flip)
        CELL_WIDTH = 28 * MAP_TO_SCREEN_SCALE
        CELL_HEIGHT = 40 * MAP_TO_SCREEN_SCALE
        if flip:
            xIndex = sheet.get_width() // CELL_WIDTH - 1 - xIndex

        x = xIndex * CELL_WIDTH
        y = yIndex * CELL_HEIGHT
        xDest = (self.image.get_width() - CELL_WIDTH) // 2
        yDest = (self.image.get_height() - CELL_HEIGHT) // 2
        if offset:
            xDest += offset[0]
            yDest += offset[1]
        area = pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)
        self.image.blit(sheet, (xDest, yDest), area)

    def pasteHead(self, index, *, flip=False, autoflip=False):
        if autoflip:
            flip = not self.player.isFacingRight()
        if self.player.team is None:
            teamColour = (255, 255, 255)
        else:
            teamColour = self.player.team.colour
        sheet = self.app.theme.sprites.playerHeadSheet(teamColour, flip)
        CELL_WIDTH = 28 * MAP_TO_SCREEN_SCALE
        CELL_HEIGHT = 40 * MAP_TO_SCREEN_SCALE
        if flip:
            index = sheet.get_width() // CELL_WIDTH - 1 - index

        x = index * CELL_WIDTH
        xDest = (self.image.get_width() - CELL_WIDTH) // 2
        yDest = (self.image.get_height() - CELL_HEIGHT) // 2
        area = pygame.Rect(x, 0, CELL_WIDTH, CELL_HEIGHT)
        self.image.blit(sheet, (xDest, yDest), area)

    def pasteSpriteSheetAnimation(
            self, frameRate, frameIndices, *, autoflip=False, flip=False):
        if self._animationStart is None:
            self._animationStart = self.timer()
            elapsed = 0
        else:
            elapsed = self.timer() - self._animationStart

        timeIndex = int(elapsed // frameRate) % len(frameIndices)
        xIndex, yIndex = frameIndices[timeIndex]
        self.pasteSpriteSheet(xIndex, yIndex, autoflip=autoflip, flip=flip)

    def setGhostImage(self):
        blitImages = self.ghostAnimation
        offset = self.ghostOffset

        # Put the pieces together:
        for element in self.ghostAnimation:
            self.image.blit(element.getImage(), (offset, 0))
        if not self.player.isFacingRight():
            self.image = pygame.transform.flip(self.image, True, False)

        respawnRatio = 1 - (
            self.player.timeTillRespawn /
            self.player.world.physics.playerRespawnTotal)
        rect = self.image.get_rect()
        rect.height -= 2
        pt = (int(0.5 + rect.width * respawnRatio), rect.height)
        colours = self.app.theme.colours
        if respawnRatio >= 1:
            pygame.draw.line(
                self.image, colours.ghostBarFull, rect.bottomleft,
                rect.bottomright, 3)
        else:
            pygame.draw.line(
                self.image, colours.ghostBarEmpty, pt,
                rect.bottomright, 3)
            pygame.draw.line(
                self.image, colours.ghostBarFull, pt,
                rect.bottomleft, 1)

        self.setImageAlpha(128)

    def updateLivePlayerImageAlpha(self):
        if self.player.phaseshift and self._canSeePhaseShift():
            # Flicker the sprite between different levels of transparency
            self.setImageAlpha(random.randint(30, 150))
        elif self.player.isInvulnerable():
            self.setImageAlpha(random.randint(30, 150))
        elif self.player.invisible:
            replay = self.worldGUI.gameViewer.replay
            target = self.getShownPlayer()
            if replay or target and self.player.isFriendsWith(target):
                self.setImageAlpha(80)
            else:
                self.setImageAlpha(0)
        else:
            self.setImageAlpha(255)

    def setImageAlpha(self, alpha):
        setAlpha(self.image, alpha, alphaSurface=self.alphaImage)

    def getShownPlayer(self):
        return self.worldGUI.gameViewer.viewManager.target

    def _canSeePhaseShift(self):
        if self.worldGUI.gameViewer.replay:
            return True
        target = self.getShownPlayer()
        if not isinstance(target, Player):
            return False
        return self.player.isFriendsWith(target)

    def renderMiniMapNameTag(self):
        if self._miniMapNameTag:
            return self._miniMapNameTag

        nick = self.player.nick
        if len(nick) <= 3:
            shortName = nick
        else:
            for middleLetter in nick[1:-1]:
                if middleLetter.isupper():
                    break
            shortName = nick[0] + middleLetter + nick[-1]

        font = self.app.screenManager.fonts.miniMapLabelFont
        colours = self.app.theme.colours
        if self.player.dead:
            colour = colours.miniMapGhostColour(self.player.team)
        else:
            colour = colours.miniMapPlayerColour(self.player.team)
        HIGHLIGHT = (192, 192, 192)
        shadow = font.render(self.app, shortName, False, HIGHLIGHT)
        highlight = font.render(self.app, shortName, False, colour)
        x, y = highlight.get_size()
        xOff, yOff = 1, 1
        result = pygame.Surface((x + xOff, y + yOff)).convert()
        result.fill((0, 0, 1))
        result.set_colorkey((0, 0, 1))
        result.blit(shadow, (xOff, yOff))
        result.blit(highlight, (0, 0))
        self._miniMapNameTag = result
        return result

# coding: utf-8


import logging
import operator

from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie

import simplejson

from trosnoth.const import POINT_VALUES
from trosnoth.gamerecording.achievementlist import availableAchievements
from trosnoth.model.upgrades import upgradeOfType
from trosnoth.server import arenaamp

from .models import (
    TrosnothServerSettings, TrosnothUser, GameRecord, PlayerKills,
    UpgradesUsedInGameRecord, TrosnothArena, Tournament,
)

log = logging.getLogger(__name__)


@ensure_csrf_cookie
def index(request):
    from twisted.internet import reactor, threads
    from trosnoth.web.server import WebServer
    server = WebServer.instance
    initialJS = threads.blockingCallFromThread(
        reactor, server.getInitialEvents)

    context = {
        'settings': TrosnothServerSettings.get(),
        'arenas': TrosnothArena.objects.all(),
        'initialJS': initialJS,
    }
    return render(request, 'trosnoth/index.html', context)


@ensure_csrf_cookie
def arena(request, arenaId):
    arenaId = int(arenaId)
    try:
        arenaRecord = TrosnothArena.objects.get(id=arenaId)
    except TrosnothArena.DoesNotExist:
        raise Http404('Arena not found')

    context = {
        'settings': TrosnothServerSettings.get(),
        'arena': arenaRecord,
        'arenaInfo': simplejson.dumps(getArenaInfo(arenaId)),
    }
    return render(request, 'trosnoth/arena.html', context)


def userProfile(request, userId, nick=None):
    try:
        user = TrosnothUser.fromUser(pk=userId)
    except User.DoesNotExist:
        raise Http404('User not found')

    unlocked = []
    locked = []
    for a in user.achievementprogress_set.all():
        try:
            name, description = availableAchievements.getAchievementDetails(
                a.achievementId.encode('ascii'))
        except KeyError:
            if not a.unlocked:
                continue
            name = a.achievementId
            description = (
                'This achievement does not exist in this version of Trosnoth')

        if finders.find(
                'trosnoth/achievements/{}.png'.format(a.achievementId)):
            imageId = a.achievementId
        else:
            imageId = 'default'

        info = {
            'name': name,
            'description': description,
            'imageId': imageId,
        }
        if a.unlocked:
            unlocked.append(info)
        else:
            locked.append(info)
    unlocked.sort(key=lambda a: a['name'])
    locked.sort(key=lambda a: a['name'])

    context = {
        'settings': TrosnothServerSettings.get(),
        'trosnothUser': user,
        'unlocked': unlocked,
        'locked': locked,
    }
    return render(request, 'trosnoth/user.html', context)


def userList(request):
    context = {
        'settings': TrosnothServerSettings.get(),
        'users': TrosnothUser.objects.order_by('-lastSeen'),
    }
    return render(request, 'trosnoth/userlist.html', context)


def viewGame(request, gameId):
    game = GameRecord.objects.get(pk=gameId)

    data = []

    for player in game.gameplayer_set.all():
        entry = {
            'player': player,
            'nick': player.getNick(),
            'accuracy': (100.0 * player.shotsHit / player.shotsFired
                ) if player.shotsFired else 0.,
            'score': 0,
            'kdr': '{:2.2f}'.format(player.kills / player.deaths
                ) if player.deaths else '∞',
            'adr': '{:2.2f}'.format(player.timeAlive / player.timeDead
                ) if player.timeDead else '∞',
        }

        for stat, weighting in list(POINT_VALUES.items()):
            if stat in entry:
                value = entry[stat]
            else:
                value = getattr(player, stat)
            entry['score'] += value * weighting

        data.append(entry)

    data.sort(key=(lambda entry: entry['score']), reverse=True)

    i = 1
    j = 0
    for entry in data:
        entry['index'] = j
        if entry['player'].bot:
            entry['rank'] = 'B'
        else:
            entry['rank'] = str(i)
            i += 1
        j += 1

    killData = {}
    for pkr in PlayerKills.objects.filter(killee__game=game):
        killData[pkr.killer, pkr.killee] = pkr.count

    killTable = []
    for killerEntry in data:
        killer = killerEntry['player']
        killRow = []
        maxKillCount = maxDeathCount = 0
        maxKill = maxDeath = '-'
        for killeeEntry in data:
            killee = killeeEntry['player']
            count = killData.get((killer, killee), 0)
            killRow.append(count)
            if count > maxKillCount:
                maxKillCount = count
                maxKill = '{} ({})'.format(killeeEntry['nick'], count)
            dieCount = killData.get((killee, killer), 0)
            if dieCount > maxDeathCount:
                maxDeathCount = dieCount
                maxDeath = '{} ({})'.format(killeeEntry['nick'], dieCount)
        killerEntry['maxKill'] = maxKill
        killerEntry['maxDeath'] = maxDeath

        killTable.append({
            'player': killerEntry['player'],
            'nick': killerEntry['nick'],
            'entries': killRow,
        })

    for i in range(len(killTable)):
        killTable[i]['entries'][i] = '-'

    otherKills = [
        killData.get((None, killeeEntry['player']), 0)
        for killeeEntry in data
    ]

    upgradeData = {}
    upgradeCodes = set()
    for ur in UpgradesUsedInGameRecord.objects.filter(gamePlayer__game=game):
        upgradeData[ur.gamePlayer, ur.upgrade] = ur.count
        upgradeCodes.add(ur.upgrade)

    if upgradeCodes:
        nameAndCode = []
        for code in upgradeCodes:
            bytesCode = code.encode('ascii')
            if bytesCode in upgradeOfType:
                name = upgradeOfType[bytesCode].name
            else:
                name = '?{}?'.format(code)
            nameAndCode.append((name, code))

        nameAndCode.sort()
        upgradeList = [name for name, code in nameAndCode]
        upgradeTable = []
        for entry in data:
            entries = []
            maxUpgrade = '-'
            maxUpgradeCount = 0
            for name, code in nameAndCode:
                count = upgradeData.get((entry['player'], code), 0)
                entries.append(count)
                if count > maxUpgradeCount:
                    maxUpgrade = '{} ({})'.format(name, count)
                    maxUpgradeCount = count

            entry['maxUpgrade'] = maxUpgrade

            upgradeTable.append({
                'player': entry['player'],
                'nick': entry['nick'],
                'entries': entries,
            })
    else:
        upgradeList = []
        upgradeTable = []

    if game.teamScoresEnabled and game.playerScoresEnabled:
        teamPlayers = {}
        for player in game.gameplayer_set.all():
            teamPlayers.setdefault(player.team, []).append((
                player.boardScore,
                player.getNick(),
                'team' + player.team + 'player',
            ))

        teams = sorted([
            (game.blueTeamScore, game.blueTeamName, 'A'),
            (game.redTeamScore, game.redTeamName, 'B'),
        ], reverse=True) + [('', 'Rogue', '')]
        scoreboard = []
        for score, name, team in teams:
            players = teamPlayers.get(team)
            if not (players or score):
                continue
            scoreboard.append((score, name, 'team' + team))
            players.sort(reverse=True)
            scoreboard.extend(players)
    elif game.teamScoresEnabled:
        scoreboard = sorted([
            (game.blueTeamScore, game.blueTeamName, 'teamA'),
            (game.redTeamScore, game.redTeamName, 'teamB')], reverse=True)
    elif game.playerScoresEnabled:
        scoreboard = sorted([(
            player.boardScore,
            player.getNick(),
            'team' + player.team + 'player',
        ) for player in game.gameplayer_set.all()], reverse=True)
    else:
        scoreboard = []

    if game.scenario == 'Trosnoth Match':
        winPoints, losePoints = _getMatchTournamentScores( game)
        tournamentPoints = '{:.2f} vs. {:.2f}'.format(winPoints, losePoints)
    else:
        tournamentPoints = ''

    context = {
        'settings': TrosnothServerSettings.get(),
        'game': game,
        'playerData': data,
        'killTable': killTable,
        'otherKills': otherKills if any(otherKills) else None,
        'upgrades': upgradeList,
        'upgradeTable': upgradeTable,
        'scoreboard': scoreboard,
        'tournamentPoints': tournamentPoints,
    }
    return render(request, 'trosnoth/viewgame.html', context)


def _getMatchTournamentScores(match):
    teamTournamentScores = {}

    for player in match.gameplayer_set.all():
        teamTournamentScores[player.team] = teamTournamentScores.get(
            player.team, 0) + player.zoneScore

    blueScore = teamTournamentScores.get('A', 0)
    redScore = teamTournamentScores.get('B', 0)
    if blueScore == redScore == 0:
        # Old game, from before these things were recorded
        return 0, 0

    winZoneScore = max(blueScore, redScore)
    loseZoneScore = min(blueScore, redScore)
    winTournamentPoints = (
        10 + 10 * winZoneScore ** 1.5
        / (winZoneScore ** 1.5 + loseZoneScore ** 1.5))
    loseTournamentPoints = 20 - winTournamentPoints
    return winTournamentPoints, loseTournamentPoints


def tournament(request, tournamentId):
    tournament = Tournament.objects.get(pk=tournamentId)

    mainInfo = {}
    hvmInfo = {}
    noveltyInfo = {}
    gameByGame = []

    for match in tournament.matches.all():
        matchDescription = '?'
        if match.scenario in ('Trosnoth Match', ''):
            winScore, loseScore = _getMatchTournamentScores(match)
            if not match.winningTeam:
                matchDescription = '{} vs. {} [10.0 : 10.0]'.format(
                    match.blueTeamName, match.redTeamName)
            else:
                if match.winningTeam == 'A':
                    winner = match.blueTeamName
                    loser = match.redTeamName
                else:
                    winner = match.redTeamName
                    loser = match.blueTeamName
                matchDescription = '{} vs. {} [{:.1f} : {:.1f}]'.format(
                    winner, loser, winScore, loseScore)

            if {match.blueTeamName, match.redTeamName} == {
                    'Humans', 'Machines'}:
                teams = {'A': match.blueTeamName, 'B': match.redTeamName}
                for teamId, teamName in teams.items():
                    if teamName not in hvmInfo:
                        hvmInfo[teamName] = {
                            'team': teamName,
                            'score': 0,
                            'winCount': 0,
                            'playCount': 0,
                        }
                    record = hvmInfo[teamName]
                    record['playCount'] += 1
                    if teamId == match.winningTeam:
                        record['winCount'] += 1
                        record['score'] += winScore
                    else:
                        record['score'] += loseScore
            else:
                for player in match.gameplayer_set.all():
                    if player.user:
                        playerKey = 'p' + str(player.user.pk)
                    else:
                        playerKey = 'b' + player.botName

                    if playerKey not in mainInfo:
                        mainInfo[playerKey] = {
                            'user': player.user,
                            'nick': player.getNick(),
                            'score': 0,
                            'winCount': 0,
                            'playCount': 0,
                        }
                    record = mainInfo[playerKey]
                    record['playCount'] += 1
                    if player.team == match.winningTeam:
                        record['winCount'] += 1
                        record['score'] += winScore
                    else:
                        record['score'] += loseScore
        elif match.playerScoresEnabled:
            maxScore = 0
            winners = []

            for player in match.gameplayer_set.all():
                if player.boardScore == maxScore:
                    winners.append(player)
                elif player.boardScore > maxScore:
                    winners = [player]
                    maxScore = player.boardScore

            for player in winners:
                if player.user:
                    playerKey = 'p' + str(player.user.pk)
                else:
                    playerKey = 'b' + player.botName

                if playerKey not in noveltyInfo:
                    noveltyInfo[playerKey] = {
                        'user': player.user,
                        'nick': player.getNick(),
                        'score': 0,
                        'scenarios': [],
                    }
                record = noveltyInfo[playerKey]
                record['score'] += 1
                record['scenarios'].append(match.scenario)

            matchDescription = '{} won'.format(
                ', '.join(sorted(w.getNick() for w in winners)))
        else:
            matchDescription = '{} vs {}, {}'.format(
                match.blueTeamName, match.redTeamName, match.getScoreString())
            if match.winningTeam:
                if match.winningTeam == 'A':
                    winner = match.blueTeamName
                    loser = match.redTeamName
                else:
                    winner = match.redTeamName
                    loser = match.blueTeamName

                for player in match.gameplayer_set.all():
                    if player.team != match.winningTeam:
                        continue
                    if player.user:
                        playerKey = 'p' + str(player.user.pk)
                    else:
                        playerKey = 'b' + player.botName

                    if playerKey not in noveltyInfo:
                        noveltyInfo[playerKey] = {
                            'user': player.user,
                            'nick': player.getNick(),
                            'score': 0,
                            'scenarios': [],
                        }
                    record = noveltyInfo[playerKey]
                    record['score'] += 1
                    record['scenarios'].append(match.scenario)

        gameByGame.append({
            'game': match,
            'description': matchDescription,
        })

    mainStandings = sorted(
        mainInfo.values(), key=operator.itemgetter('score'), reverse=True)
    lastRank, lastScore = 1, 0
    for i, record in enumerate(mainStandings):
        if record['score'] == lastScore:
            record['rank'] = lastRank
        else:
            record['rank'] = i + 1
            lastScore = record['score']
            lastRank = record['rank']

    hvmStandings = sorted(
        hvmInfo.values(), key=operator.itemgetter('score'), reverse=True)
    lastRank, lastScore = 1, 0
    for i, record in enumerate(hvmStandings):
        if record['score'] == lastScore:
            record['rank'] = lastRank
        else:
            record['rank'] = i + 1
            lastScore = record['score']
            lastRank = record['rank']

    noveltyStandings = sorted(
        noveltyInfo.values(), key=operator.itemgetter('score'), reverse=True)
    lastRank, lastScore = 1, 0
    for i, record in enumerate(noveltyStandings):
        if record['score'] == lastScore:
            record['rank'] = lastRank
        else:
            record['rank'] = i + 1
            lastScore = record['score']
            lastRank = record['rank']

        scenarioCounts = {}
        bestScenarios = []
        mostRepeats = 0
        for scenario in record['scenarios']:
            n = scenarioCounts[scenario] = scenarioCounts.get(scenario, 0) + 1
            if n > mostRepeats:
                bestScenarios = [scenario]
                mostRepeats = n
            elif n == mostRepeats:
                bestScenarios.append(scenario)
        record['bestScenario'] = ', '.join(sorted(bestScenarios))


    context = {
        'settings': TrosnothServerSettings.get(),
        'tournament': tournament,
        'mainStandings': mainStandings,
        'hvmStandings': hvmStandings,
        'noveltyStandings': noveltyStandings,
        'gameByGame': gameByGame,
    }
    return render(request, 'trosnoth/tournament.html', context)


def gameList(request):
    context = {
        'settings': TrosnothServerSettings.get(),
        'games': GameRecord.objects.order_by('-started'),
        'tournaments': Tournament.objects.all(),
    }
    return render(request, 'trosnoth/gamelist.html', context)


@permission_required('trosnoth.pause_arena')
def pauseArena(request):
    arenaId = int(request.GET['id'])
    sendArenaRequest(arenaId, arenaamp.PauseGame)
    return JsonResponse(getArenaInfo(arenaId))


@permission_required('trosnoth.pause_arena')
def resumeArena(request):
    arenaId = int(request.GET['id'])
    sendArenaRequest(arenaId, arenaamp.ResumeGame)
    return JsonResponse(getArenaInfo(arenaId))


@permission_required('trosnoth.restart_arena')
def restartArena(request):
    arenaId = int(request.GET['id'])

    from twisted.internet import reactor, threads
    from trosnoth.run.authserver import AuthenticationFactory
    authFactory = AuthenticationFactory.instance
    threads.blockingCallFromThread(reactor, authFactory.shutDownArena, arenaId)

    return JsonResponse(getArenaInfo(arenaId))


@permission_required('trosnoth.set_arena_level')
def resetArena(request):
    arenaId = int(request.GET['id'])
    sendArenaRequest(arenaId, arenaamp.ResetToLobby)
    return JsonResponse(getArenaInfo(arenaId))


@permission_required('trosnoth.enable_arena')
def disableArena(request):
    arenaId = int(request.GET['id'])

    try:
        arenaRecord = TrosnothArena.objects.get(id=arenaId)
    except TrosnothArena.DoesNotExist:
        return HttpResponseBadRequest('Arena not found')

    arenaRecord.enabled = False
    arenaRecord.save()

    from twisted.internet import reactor, threads
    from trosnoth.run.authserver import AuthenticationFactory
    authFactory = AuthenticationFactory.instance
    try:
        threads.blockingCallFromThread(
            reactor, authFactory.shutDownArena, arenaId)
    except Exception:
        log.exception('Error trying to shut down arena')

    return JsonResponse(getArenaInfo(arenaId))


@permission_required('trosnoth.enable_arena')
def enableArena(request):
    arenaId = int(request.GET['id'])

    try:
        arenaRecord = TrosnothArena.objects.get(id=arenaId)
    except TrosnothArena.DoesNotExist:
        return HttpResponseBadRequest('Arena not found')

    arenaRecord.enabled = True
    arenaRecord.save()

    return JsonResponse(getArenaInfo(arenaId))


@permission_required('trosnoth.change_team_abilities')
def disableShots(request):
    arenaId = int(request.GET['id'])
    teamIndex = int(request.GET['t'])
    setTeamAbility(arenaId, teamIndex, 'aggression', False)
    return JsonResponse(getArenaInfo(arenaId))


@permission_required('trosnoth.change_team_abilities')
def enableShots(request):
    arenaId = int(request.GET['id'])
    teamIndex = int(request.GET['t'])
    setTeamAbility(arenaId, teamIndex, 'aggression', True)
    return JsonResponse(getArenaInfo(arenaId))


@permission_required('trosnoth.change_team_abilities')
def disableCaps(request):
    arenaId = int(request.GET['id'])
    teamIndex = int(request.GET['t'])
    setTeamAbility(arenaId, teamIndex, 'zoneCaps', False)
    return JsonResponse(getArenaInfo(arenaId))


@permission_required('trosnoth.change_team_abilities')
def enableCaps(request):
    arenaId = int(request.GET['id'])
    teamIndex = int(request.GET['t'])
    setTeamAbility(arenaId, teamIndex, 'zoneCaps', True)
    return JsonResponse(getArenaInfo(arenaId))


def sendArenaRequest(arenaId, command, **kwargs):
    '''
    Connects to the running authentication server and asks it to communicate
    with the given arena server.
    '''
    from twisted.internet import reactor, threads
    from trosnoth.run.authserver import AuthenticationFactory
    authFactory = AuthenticationFactory.instance
    return threads.blockingCallFromThread(
        reactor, authFactory.sendArenaRequest, arenaId, command, **kwargs)


def getArenaInfo(arenaId):
    from twisted.internet import reactor, threads
    from trosnoth.run.authserver import AuthenticationFactory
    authFactory = AuthenticationFactory.instance
    return threads.blockingCallFromThread(
        reactor, authFactory.getArenaInfo, arenaId)


def setTeamAbility(arenaId, teamIndex, ability, value):
    from twisted.internet import reactor, threads
    from trosnoth.run.authserver import AuthenticationFactory
    authFactory = AuthenticationFactory.instance
    arenaProxy = threads.blockingCallFromThread(
        reactor, authFactory.getArena, arenaId)
    threads.blockingCallFromThread(
        reactor, arenaProxy.setTeamAbility, teamIndex, ability, value)


def tokenAuth(request):
    from trosnoth.run.authserver import AuthenticationFactory
    authFactory = AuthenticationFactory.instance
    if not authFactory.useAdminToken(request.GET['token']):
        return None

    username = 'autoadmin'
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User(
            username=username,
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )
        user.save()

    login(request, user)

    return redirect('trosnoth:index')


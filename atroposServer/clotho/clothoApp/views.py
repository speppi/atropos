# Create your views here.
from django.http import HttpResponse
from clothoApp.models import Telling
from django.shortcuts import get_object_or_404
import json
import atroposStory
import os
import jsonpickle

CLOTHO_APP_PATH = os.path.dirname(os.path.abspath(__file__))

STORY_PATH = os.path.join(CLOTHO_APP_PATH, "AtroposExampleScript.txt")

storyNodes = atroposStory.parseToStory(STORY_PATH)

def index(request):
    return HttpResponse(map(str, storyNodes))

def createTelling(request):
    newTelling = Telling()
    newTelling.save()
    responseData = {}
    responseData['tellingId'] = newTelling.id
    return HttpResponse(json.dumps(newTelling.id), content_type='application/json')

def getNextNode(request, telling_id, player_id, choice_id):
    telling = get_object_or_404(Telling, pk=telling_id)
    if (player_id == '1'):
        playerNode = storyNodes[telling.player1NodeId]
    elif (player_id == '2'):
        playerNode = storyNodes[telling.player2NodeId]

    if (playerNode.nodeType == atroposStory.NodeTypes.dialogueNode and playerNode.nextNode != None):
        if (player_id == '1'):
            telling.player1NodeId = playerNode.nextNode.nodeId
        elif (player_id == '2'):
            telling.player2NodeId = playerNode.nextNode.nodeId
    elif (playerNode.nodeType == atroposStory.NodeTypes.splitBlock):
        if (player_id == '1' and playerNode.player1Node != None):
            telling.player1NodeId = playerNode.player1Node.nodeId
            playerNode = storyNodes[playerNode.player1Node.nodeId]
        elif (player_id == '2' and playerNode.player2Node != None):
            telling.player2NodeId = playerNode.player2Node.nodeId
            playerNode = storyNodes[playerNode.player2Node.nodeId]
    elif (playerNode.nodeType == atroposStory.NodeTypes.menuNode and choice_id != None):
        if ((player_id == '1' and playerNode.player2Node.nodeId != telling.player2NodeId) or (player_id == '2' and playerNode.player1Node.nodeId != telling.player1NodeId)):

            # Send back an undefined node, this will signal the other player has not caught up yet
            playerNode = atroposStory.StoryNode()
        else:
            choiceIndex = int(choice_id)
            newNode = playerNode.menuOptions[choiceIndex].optionNode
            telling.player1NodeId = newNode.nodeId
            telling.player2NodeId = newNode.nodeId
            playerNode = newNode


    telling.save()
    return HttpResponse(jsonpickle.encode(playerNode.toJsonDict()), content_type='application/json')


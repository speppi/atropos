from atroposParser import *


class NodeTypes:
    undefined = -1
    dialogueNode = 0
    menuNode = 1
    splitBlock = 2


class MenuOption:
    def __int__(self):
        self.optionText = ""
        self.optionNode = None

    def __str__(self):
        return "Menu Option " + str([self.optionText, self.optionNode])


class StoryNode:
    def __init__(self):
        self.nodeId = -1;
        self.nodeType = NodeTypes.undefined
        self.nextNode = None
        self.characterImage = ""
        self.bgImage = ""
        self.characterName = ""
        self.dialogue = ""
        self.menuOptions = []
        self.player1Node = None
        self.player2Node = None

    def __str__(self):
        result = str(self.nodeId) + " "
        if self.nodeType == NodeTypes.undefined:
            result += "Undefined "
        elif self.nodeType == NodeTypes.dialogueNode:
            result += "Dialogue Node "
            result += str([self.characterImage, self.bgImage, self.characterName, self.dialogue])
        elif self.nodeType == NodeTypes.menuNode:
            result += "Menu Node "
            result += str([x.optionText for x in self.menuOptions])
            result += " Player 1: "
            result += str(self.player1Node)
            result += " Player 2: "
            result += str(self.player2Node)
        else:
            result += "Split Block "
            result += str([str(self.player1Node), str(self.player2Node)])

        return result

    def toJsonDict(self):
        jsonStoryNode = StoryNodeJson()
        jsonStoryNode.nodeType = self.nodeType
        jsonStoryNode.characterImage = self.characterImage
        jsonStoryNode.bgImage = self.bgImage
        jsonStoryNode.characterName = self.characterName
        jsonStoryNode.dialogue = self.dialogue
        for menuOption in self.menuOptions:
            jsonStoryNode.menuOptions.append(menuOption.optionText)
        return jsonStoryNode.__dict__

class StoryNodeJson:
    def __init__(self):
        self.nodeType = NodeTypes.undefined
        self.characterImage = ""
        self.bgImage = ""
        self.characterName = ""
        self.dialogue = ""
        self.menuOptions = []

def parseToStory(storyFile):
    parsedFile = script.parseFile(storyFile)
    storyNodes = [[]]
    imageDictionary = {}
    characterDictionary = {}
    nodeDictionary = {}
    prevNode = [None]
    currNode = [StoryNode()]

    def addNewNode(setNextNode = True):
        if currNode[0].nodeType != NodeTypes.undefined:
            if prevNode[0]:
                prevNode[0].nodeId = len(storyNodes[0])
                storyNodes[0].append(prevNode[0])
            prevNode[0] = currNode[0]
            currNode[0] = StoryNode()
            currNode[0].bgImage = prevNode[0].bgImage
            currNode[0].characterImage = prevNode[0].characterImage
            if setNextNode:
                prevNode[0].nextNode = currNode[0]

    def addStatementNode(statement):
        statementType = getStatementType(statement)
        if statementType == "imageAlias":
            fullImageName = getFullImageName(statement)
            if imageDictionary.has_key(fullImageName):
                raise ValueError("Duplicate image name provided: " + fullImageName)
            imageDictionary[fullImageName] = statement.filePath
        elif statementType == "characterAlias":
            if characterDictionary.has_key(statement.alias):
                raise ValueError("Duplicate character alias provided: " + statement.alias)
            characterDictionary[statement.alias] = statement.characterName
        elif statementType == "showCharacter":
            addNewNode()
            currNode[0].characterImage = imageDictionary[getFullImageName(statement)]
        elif statementType == "showScene":
            addNewNode()
            currNode[0].bgImage = imageDictionary[getFullImageName(statement)]
        elif statementType == "hideCharacter":
            addNewNode()
            currNode[0].characterImage = ""
        elif statementType == "jumpStatement":
            addNewNode()
            prevNode[0].nextNode = statement.label
        elif statementType == "labelStatement":
            addNewNode()
            if nodeDictionary.has_key(statement.label):
                raise ValueError("Duplicate label provided: " + statement.label)
            nodeDictionary[statement.label] = currNode[0]
        elif statementType == "dialogueLine":
            characterName = ""
            if statement.characterAlias:
                characterName = characterDictionary[statement.characterAlias]
                dialogue = statement.dialogue
            elif statement.dialogue:
                characterName = statement.characterName
                dialogue = statement.dialogue
            else:
                dialogue = statement.characterName

            addNewNode()
            currNode[0].nodeType = NodeTypes.dialogueNode
            currNode[0].characterName = characterName
            currNode[0].dialogue = dialogue
        elif statementType == "returnStatement":
            storyNodes[0].append(prevNode[0])
            prevNode[0] = currNode[0]
            prevNode[0].nextNode = None
            currNode[0] = StoryNode()
        else:
            raise NameError("Statement not recognized")

    for statement in parsedFile:
        statementType = getStatementType(statement)
        if statementType == "splitBlock":
            addNewNode()
            splitBlockNode = currNode[0]
            splitBlockNode.nodeType = NodeTypes.splitBlock
            player1BlockNodesAdded = False
            player2BlockNodesAdded = False
            player1MenuNode = None
            lastPlayer1Node = None
            player2MenuNode = None
            lastPlayer2Node = None

            if statement.player1Block:
                addNewNode(False)
                splitBlockNode.player1Node = currNode[0]
                for blockStatement in statement.player1Block:
                    addStatementNode(blockStatement)
                player1BlockNodesAdded = True

            if statement.player1Menu:
                addNewNode(player1BlockNodesAdded)
                player1MenuNode = currNode[0]
                if not player1BlockNodesAdded:
                    splitBlockNode.player1Node = currNode[0]
                currNode[0].nodeType = NodeTypes.menuNode
                for menuOption in statement.player1Menu.menuOptions:
                    newMenuOption = MenuOption()
                    newMenuOption.optionText = menuOption.optionText
                    newMenuOption.optionNode = menuOption.label
                    currNode[0].menuOptions.append(newMenuOption)

            lastPlayer1Node = currNode[0]

            if statement.player2Block:
                addNewNode(False)
                splitBlockNode.player2Node = currNode[0]
                for blockStatement in statement.player2Block:
                    addStatementNode(blockStatement)
                player2BlockNodesAdded = True

            if statement.player2Menu:
                addNewNode(player2BlockNodesAdded)
                player2MenuNode = currNode[0]
                if not player2BlockNodesAdded:
                    splitBlockNode.player2Node = currNode[0]
                currNode[0].nodeType = NodeTypes.menuNode
                for menuOption in statement.player2Menu.menuOptions:
                    newMenuOption = MenuOption()
                    newMenuOption.optionText = menuOption.optionText
                    newMenuOption.optionNode = menuOption.label
                    currNode[0].menuOptions.append(newMenuOption)

            lastPlayer2Node = currNode[0]

            if player1MenuNode is not None:
                player1MenuNode.player2Node = lastPlayer2Node
            elif player2MenuNode is not None:
                player2MenuNode.player1Node = lastPlayer1Node

            # Last node should not point to next node
            addNewNode(False)
            splitBlockNode.nextNode = currNode[0]

            continue
        else:
            addStatementNode(statement)

    prevNode[0].nodeId = len(storyNodes[0])
    storyNodes[0].append(prevNode[0])
    if currNode[0].nodeType != NodeTypes.undefined:
        currNode[0].nodeId = len(storyNodes[0])
        storyNodes[0].append(currNode[0])

    for node in storyNodes[0]:
        if node.nodeType == NodeTypes.menuNode:
            for option in node.menuOptions:
                option.optionNode = nodeDictionary[option.optionNode]
        if isinstance(node.nextNode, str):
            node.nextNode = nodeDictionary[node.nextNode]
            print

    return storyNodes[0]


def main():
    test = parseToStory("AtroposExampleScript.txt")
    print test


if __name__ == '__main__':
    main()

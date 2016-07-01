from pyparsing import *

# <identifier> ::= alphanums+
identifier = Word(alphanums)

# <string> ::= dblQuotedString
dblQuotedString.setParseAction(removeQuotes)

# <equalsSign> ::= "="
# <colon> ::= ":"
equalsSign, colon = map(Suppress, "=:")

# <image name> ::= <identifier (name)> <identifier (subName)>
imageName = identifier.setResultsName("name") + identifier.setResultsName("subName")
def getFullImageName(statement):
    imageName = statement.imageName
    return imageName.name + "/" + imageName.subName

# <image alias> ::= "image" <image name> <equalsSign> <string>
imageAlias = CaselessLiteral("image") + imageName.setResultsName("imageName") + equalsSign + dblQuotedString.setResultsName("filePath")

# <character alias> ::= "character" <identifier (alias)> "=" dblQuotedString
characterAlias = CaselessLiteral("character") + identifier.setResultsName("alias") + equalsSign + dblQuotedString.setResultsName("characterName")

# <show character> ::= "show" <image name>
showCharacter = CaselessLiteral("show") + imageName.setResultsName("imageName")

# <show scene> ::= "scene" <image name>
showScene = CaselessLiteral("scene") + imageName.setResultsName("imageName")

# <hide character> ::= "hide"
hideCharacter = CaselessLiteral("hide")

# <jump statement> ::= "jump" <identifier (label)>
jumpStatement = CaselessLiteral("jump") + identifier.setResultsName("label")

# <label statement> ::= "label" <identifier (label)> <colon>>
labelStatement = CaselessLiteral("label") + identifier.setResultsName("label") + colon

# <dialogue line> ::= (dblQuotedString | <identifier (alias)>) dblQuotedString?
aliasedDialogueLine = identifier.setResultsName("characterAlias") + dblQuotedString.setResultsName("dialogue")
stringDialogueLine = (dblQuotedString.setResultsName("characterName")) + Optional(dblQuotedString.setResultsName("dialogue"))
dialogueLine = aliasedDialogueLine | stringDialogueLine


# <return statement> ::= "return"
returnStatement = CaselessLiteral("return")

# <statement> ::= pythonStyleComment | <image alias> | <character alias> | <show character> | <hide character> | <jump statement> | <label> | <dialogue line> | <return statement>
statement = pythonStyleComment | imageAlias.setResultsName("imageAlias") | characterAlias.setResultsName("characterAlias") | showCharacter.setResultsName("showCharacter") | showScene("showScene") | hideCharacter.setResultsName("hideCharacter") | jumpStatement.setResultsName("jumpStatement") | labelStatement.setResultsName("labelStatement") | dialogueLine.setResultsName("dialogueLine") | returnStatement.setResultsName("returnStatement")

statementTypes = ["imageAlias", "characterAlias", "showCharacter", "showScene", "hideCharacter", "jumpStatement", "labelStatement", "dialogueLine", "returnStatement", "splitBlock"]

def getStatementType(parseResult):
    typeList = filter(lambda x: x in statementTypes, parseResult.keys())
    return typeList[0]

# <statements> ::= <statement>+
statements = OneOrMore(Group(statement))

startLiteral = CaselessLiteral("start")
endLiteral = CaselessLiteral("end")

player1Literal = CaselessLiteral("player1")

# <player 1 header> ::= "Player1" <colon>
player1Header = startLiteral + player1Literal + colon

# <player 1 end> ::= "EndPlayer1"
player1End = endLiteral + player1Literal

player2Literal = CaselessLiteral("player2")

# <player 2 header> ::= "Player2" <colon>
player2Header = startLiteral + player2Literal + colon

# <player 2 end> ::= "EndPlayer2"
player2End = endLiteral + player2Literal

# <menu header> ::= "menu" <colon>
menuHeader = startLiteral + CaselessLiteral("menu") + colon

# <menu option> ::= dblQuotedString <colon> <jump statement>
menuOption = dblQuotedString.setResultsName("optionText") + colon + jumpStatement

menuEnd = endLiteral + CaselessLiteral("menu")

# <menu block> ::= <menu header> <menu option>+
menuBlock = menuHeader + OneOrMore(Group(menuOption)).setResultsName("menuOptions") + menuEnd

# <split block> ::=
#       <player 1 header> <statements> <player 1 end> <player 2 header> <statements> <player 2 end> |
#       <player 1 header> <statements> <menu block> <player 1 end> <player 2 header> <statements> <player 2 end> |
#       <player 1 header> <statements> <player 1 end> <player 2 header> <statements> <menu block> <player 2 end>
splitBlock = (player1Header + statements.setResultsName("player1Block") + player1End + player2Header + statements.setResultsName("player2Block") + player2End) | \
    (player1Header + Optional(Group(statements)).setResultsName("player1Block") + menuBlock.setResultsName("player1Menu") + player1End + player2Header + statements.setResultsName("player2Block") + player2End) | \
    (player1Header + statements.setResultsName("player1Block") + player1End + player2Header + Optional(Group(statements)).setResultsName("player2Block") + menuBlock.setResultsName("player2Menu") + player2End)

# <script> ::= (<split block> | <statement>)+
script = OneOrMore(Group(splitBlock.setResultsName("splitBlock") | statement))

#imageTest = script.parseString('image alpha happy = "AlphaHappy.png"')
#characterTest = script.parseString('character a = "Alpha"')
#showTest = script.parseString('show alpha happy')
#jumpTest = script.parseString('jump foo')
#labelTest = script.parseString('label bar:')
#dialogueTest1 = script.parseString('"We were all gathered to decide what to do."')
#dialogueTest2 = script.parseString('"Alpha" "We were all gathered to decide what to do."')
#dialogueTest3 = script.parseString('a "We were all gathered to decide what to do."')
#multiTest = script.parseString('character a = "Alpha"\nimage alpha happy = "alphaHappy.png"')
#multiTest2 = script.parseString('character a = "Alpha"\n\nimage alpha happy = "alphaHappy.png"')
#parsedFile = script.parseFile("AtroposExampleScript.txt")
#splitTest = splitBlock.parseString('start player1:\nstart menu:\n"Menu Option 1!":\njump option1\n"Menu Option 2!":\njump option2\nend menu\nend player1\nstart player2:\n"Howdy!"\nend player2')
#splitTest2 = splitBlock.parseString('start player1:\n"What to do?"\nstart menu:\n"Menu Option 1!":\njump option1\n"Menu Option 2!":\njump option2\nend menu\nend player1\nstart player2:\n"Howdy!"\nend player2')

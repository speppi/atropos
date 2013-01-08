using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NovelNode
{
    public List<NovelNode> Neighbors;
}

public class DialogueNode : NovelNode
{
    public string SpeakerName;
    public string Dialogue;
    public Texture DisplayedCharacter;
}

public class MenuNode : NovelNode
{
    public List<string> MenuOptions;
}
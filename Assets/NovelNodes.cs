public class NovelNode
{
}

public class DialogueNode : NovelNode
{
    public string dialogue { get; set; }
}

public class MenuNode : NovelNode
{
    public string[] choices { get; set; }
}
public enum NodeType
{
    Undefined = 1,
    Dialogue = 0,
    MenuNode = 1,
    SplitBlock = 2,
}

public class NovelNode
{
    public NodeType nodeType { get; set; }
    public string bgImage { get; set; }
    public string characterName { get; set; }
    public string characterImage { get; set; }
    public string dialogue { get; set; }
    public string[] menuOptions { get; set; }
}
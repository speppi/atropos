using UnityEngine;

public class ViewModel : MonoBehaviour
{
    string BoxText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec tincidunt sem a lorem pellentesque dignissim. Sed euismod rhoncus sollicitudin. Vestibulum posuere commodo enim, quis consequat dui accumsan sit amet. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.";
    public Texture characterTexture;
    public GUISkin guiSkinDefault;
    NovelModel MyNovelModel;
    NovelNode currentNovelNode;
    int lastSelection = -1;

    // Use this for initialization
    void Start()
    {
        MyNovelModel = GetComponent<NovelModel>();
        currentNovelNode = MyNovelModel.GetNextNovelNode();
    }

    void OnGUI()
    {
        if (guiSkinDefault == null)
        {
            guiSkinDefault = GUI.skin;
        }

        if (characterTexture != null)
        {
            GUI.DrawTexture(new Rect(0, 0, 286, 600), characterTexture, ScaleMode.ScaleToFit);
        }

        if (currentNovelNode is MenuNode)
        {
            var menuNode = currentNovelNode as MenuNode;
            var menuItemsStyle = new GUIStyle(guiSkinDefault.button);
            menuItemsStyle.fontSize = 28;
            menuItemsStyle.fixedHeight = 50;
            var menuItemWidth = 400;
            var menuItemHeight = 500;
            lastSelection = GUI.SelectionGrid(new Rect(Screen.width / 2 - menuItemWidth / 2, Screen.height / 2 - menuItemHeight / 3, menuItemWidth, menuItemHeight), lastSelection, menuNode.choices, 1, menuItemsStyle);
        }
        else if (currentNovelNode is DialogueNode)
        {
            var dialogueNode = currentNovelNode as DialogueNode;
            var dialogueBoxStyle = new GUIStyle(guiSkinDefault.box);
            dialogueBoxStyle.alignment = TextAnchor.UpperLeft;
            dialogueBoxStyle.wordWrap = true;
            dialogueBoxStyle.fontSize = 36;
            dialogueBoxStyle.padding = new RectOffset(10, 10, 10, 10);
            GUI.Box(new Rect(10, Screen.height - 195, Screen.width - 20, 185), dialogueNode.dialogue, dialogueBoxStyle);

            var characterNameStyle = new GUIStyle(guiSkinDefault.box);
            characterNameStyle.alignment = TextAnchor.MiddleLeft;
            characterNameStyle.fontSize = 28;
            characterNameStyle.padding = new RectOffset(10, 10, 10, 10);
            GUI.Box(new Rect(10, Screen.height - 245, 300, 50), "Atropos", characterNameStyle);
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (currentNovelNode is MenuNode && lastSelection != -1)
        {
            currentNovelNode = MyNovelModel.GetNextNovelNode(lastSelection);
            lastSelection = -1;
        }
        else if (currentNovelNode is DialogueNode && Input.GetButtonDown("Fire1"))
        {
            currentNovelNode = MyNovelModel.GetNextNovelNode();
        }
    }
}

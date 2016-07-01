using UnityEngine;

public class ViewModel : MonoBehaviour
{
    string BoxText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec tincidunt sem a lorem pellentesque dignissim. Sed euismod rhoncus sollicitudin. Vestibulum posuere commodo enim, quis consequat dui accumsan sit amet. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.";
    public Texture characterTexture;
    public GUISkin guiSkinDefault;
    NovelModel MyNovelModel;
    NovelNode currentNovelNode = null;
    int lastSelection = -1;

    // Use this for initialization
    void Start()
    {
        MyNovelModel = GetComponent<NovelModel>();
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

        if (currentNovelNode.nodeType == NodeType.MenuNode)
        {
            var menuItemsStyle = new GUIStyle(guiSkinDefault.button);
            menuItemsStyle.fontSize = 28;
            menuItemsStyle.fixedHeight = 50;
            var menuItemWidth = 400;
            var menuItemHeight = 500;
            lastSelection = GUI.SelectionGrid(new Rect(Screen.width / 2 - menuItemWidth / 2, Screen.height / 2 - menuItemHeight / 3, menuItemWidth, menuItemHeight), lastSelection, currentNovelNode.menuOptions, 1, menuItemsStyle);
        }
        else if (currentNovelNode.nodeType == NodeType.Dialogue)
        {
            var dialogueBoxStyle = new GUIStyle(guiSkinDefault.box);
            dialogueBoxStyle.alignment = TextAnchor.UpperLeft;
            dialogueBoxStyle.wordWrap = true;
            dialogueBoxStyle.fontSize = 36;
            dialogueBoxStyle.padding = new RectOffset(10, 10, 10, 10);
            GUI.Box(new Rect(10, Screen.height - 195, Screen.width - 20, 185), currentNovelNode.dialogue, dialogueBoxStyle);

            if (!string.IsNullOrEmpty(currentNovelNode.characterName))
            {
                var characterNameStyle = new GUIStyle(guiSkinDefault.box);
                characterNameStyle.alignment = TextAnchor.MiddleLeft;
                characterNameStyle.fontSize = 28;
                characterNameStyle.padding = new RectOffset(10, 10, 10, 10);
                GUI.Box(new Rect(10, Screen.height - 245, 300, 50), currentNovelNode.characterName, characterNameStyle);
            }
        }
    }

    // Update is called once per frame
    void Update()
    {

        if (currentNovelNode == null)
        {
            Debug.Log("Getting for null novel node");
            currentNovelNode = MyNovelModel.GetNextNovelNode();
        }
        else if (lastSelection != -1)
        {
            Debug.Log("Choice made!");
            currentNovelNode = MyNovelModel.GetNextNovelNode(lastSelection);
            lastSelection = -1;
        }
        else if (currentNovelNode.nodeType == NodeType.Dialogue && Input.GetButtonDown("Fire1"))
        {
            Debug.Log("Getting next dialogue node");
            currentNovelNode = MyNovelModel.GetNextNovelNode();
        }
        else if (currentNovelNode.nodeType == NodeType.Undefined && Input.GetButtonDown("Fire1"))
        {
            Debug.Log("Waiting for other player");
            currentNovelNode = MyNovelModel.GetNextNovelNode();
        }

        if (Input.GetButtonDown("Fire2"))
        {
            MyNovelModel.SwitchPlayers();
            currentNovelNode = MyNovelModel.GetNextNovelNode();
        }
    }
}

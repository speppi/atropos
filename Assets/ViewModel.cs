using UnityEngine;
using System.Collections;

public class ViewModel : MonoBehaviour
{
    string BoxText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec tincidunt sem a lorem pellentesque dignissim. Sed euismod rhoncus sollicitudin. Vestibulum posuere commodo enim, quis consequat dui accumsan sit amet. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.";
    public Texture characterTexture;
    public GUISkin guiSkinDefault;
    NovelModel MyNovelModel;

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

        var menuItems = new string[] { "Phoenix", "Maya", "Miles", "Gumshoe", "Mia" };
        var menuItemsStyle = new GUIStyle(guiSkinDefault.button);
        menuItemsStyle.fontSize = 28;
        menuItemsStyle.fixedHeight = 50;
        var menuItemWidth = 400;
        var menuItemHeight = 500;
        GUI.SelectionGrid(new Rect(Screen.width / 2 - menuItemWidth / 2, Screen.height / 2 - menuItemHeight / 3, menuItemWidth, menuItemHeight), -1, menuItems, 1, menuItemsStyle);

        var dialogueBoxStyle = new GUIStyle(guiSkinDefault.box);
        dialogueBoxStyle.alignment = TextAnchor.UpperLeft;
        dialogueBoxStyle.wordWrap = true;
        dialogueBoxStyle.fontSize = 36;
        dialogueBoxStyle.padding = new RectOffset(10, 10, 10, 10);
        GUI.Box(new Rect(10, Screen.height - 195, Screen.width - 20, 185), BoxText, dialogueBoxStyle);

        var characterNameStyle = new GUIStyle(guiSkinDefault.box);
        characterNameStyle.alignment = TextAnchor.MiddleLeft;
        characterNameStyle.fontSize = 28;
        characterNameStyle.padding = new RectOffset(10, 10, 10, 10);
        GUI.Box(new Rect(10, Screen.height - 245, 300, 50), "Atropos", characterNameStyle);
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetButtonDown("Fire1"))
        {
            BoxText = MyNovelModel.GetNextDialogue();
        }
    }
}

using UnityEngine;
using System.Collections;

public class ViewModel : MonoBehaviour
{
    string BoxText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec tincidunt sem a lorem pellentesque dignissim. Sed euismod rhoncus sollicitudin. Vestibulum posuere commodo enim, quis consequat dui accumsan sit amet. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.";
    public Texture characterTexture;

    // Use this for initialization
    void Start()
    {

    }

    void OnGUI()
    {
        if (characterTexture)
        {
            GUI.DrawTexture(new Rect(0, 0, 286, 600), characterTexture, ScaleMode.ScaleToFit);
        }

        var oldColor = GUI.color;
        var dialogueBoxStyle = new GUIStyle(GUI.skin.box);
        dialogueBoxStyle.alignment = TextAnchor.MiddleLeft;
        dialogueBoxStyle.wordWrap = true;
        dialogueBoxStyle.fontSize = 36;
        dialogueBoxStyle.padding = new RectOffset(10, 10, 10, 10);
        GUI.Box(new Rect(10, Screen.height - 195, Screen.width - 20, 185), BoxText, dialogueBoxStyle);

        var characterNameStyle = new GUIStyle(GUI.skin.box);
        characterNameStyle.alignment = TextAnchor.MiddleLeft;
        characterNameStyle.fontSize = 28;
        characterNameStyle.padding = new RectOffset(10, 10, 10, 10);
        GUI.Box(new Rect(10, Screen.height - 245, 300, 50), "Atropos", characterNameStyle);


    }

    // Update is called once per frame
    void Update()
    {
        //if (Input.GetButtonDown("Fire1"))
        //{
        //}
    }
}

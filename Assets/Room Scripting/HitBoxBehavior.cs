using UnityEngine;
using System.Collections;

public class HitBoxBehavior : MonoBehaviour
{
    OTSprite sprite;
    bool guiShown = false;
    bool showGui = false;
    public GUISkin guiSkinDefault;
    public string dialogueString;

    // Use this for initialization
    void Start()
    {
        sprite = GetComponent<OTSprite>();
        sprite.onCollision = OnCollision;
    }

    // Update is called once per frame
    void Update()
    {
        if (showGui && Input.GetButtonDown("Fire1"))
        {
            guiShown = true;
            showGui = false;
        }
    }

    public void OnCollision(OTObject owner)
    {
        if (!guiShown)
        {
            showGui = true;
        }
    }

    void OnGUI()
    {
        if (guiSkinDefault == null)
        {
            guiSkinDefault = GUI.skin;
        }

        if (!guiShown && showGui)
        {
            var dialogueBoxStyle = new GUIStyle(guiSkinDefault.box);
            dialogueBoxStyle.alignment = TextAnchor.UpperLeft;
            dialogueBoxStyle.wordWrap = true;
            dialogueBoxStyle.fontSize = 36;
            dialogueBoxStyle.padding = new RectOffset(10, 10, 10, 10);
            GUI.Box(new Rect(10, Screen.height - 195, Screen.width - 20, 185), dialogueString, dialogueBoxStyle);
        }
    }
}

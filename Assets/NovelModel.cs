using UnityEngine;
using System.Collections;

public class NovelModel : MonoBehaviour
{
    int currDialogue = 0;
    string[] dialogueStrings = { "I'm a little teapot, short and stout.", "Here is my handle. Here is my spout.", "When I get all steamed up I will shout:", "Just tip me over and pour me out!" };

    // Use this for initialization
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

    }

    public string GetNextDialogueString()
    {
        currDialogue = (currDialogue + 1) % dialogueStrings.Length;
        return dialogueStrings[currDialogue];
    }
}

using Newtonsoft.Json;
using System.IO;
using System.Net;
using UnityEngine;

public class NovelModel : MonoBehaviour
{
    public string currentPlayer { get; set; }
    public string currentTelling { get; set; }

    // Use this for initialization
    void Start()
    {
        currentPlayer = "1";
        var webRequest = HttpWebRequest.Create("http://127.0.0.1:8000/clotho/createTelling");
        using (var webResponse = webRequest.GetResponse())
        {
            using (var webReader = new StreamReader(webResponse.GetResponseStream()))
            {
                currentTelling = webReader.ReadToEnd();
            }
        }
        Debug.Log(currentTelling);
    }

    // Update is called once per frame
    void Update()
    {

    }

    public NovelNode GetNextNovelNode(int choice = -1)
    {
        //var url = "http://speppiland.com/atropos/getNextNovelNode.py";
        var url = string.Format("http://127.0.0.1:8000/clotho/getNextNode/{0}/{1}", currentTelling, currentPlayer);
        if (choice != -1)
        {
            url += "/" + choice.ToString();
        }
        Debug.Log(url);
        var webRequest = HttpWebRequest.Create(url);
        string dialogueString = "";
        using (var webResponse = webRequest.GetResponse())
        {
            using (var webReader = new StreamReader(webResponse.GetResponseStream()))
            {
                dialogueString = webReader.ReadToEnd();
            }
        }
        var resultNode = JsonConvert.DeserializeObject<NovelNode>(dialogueString, new JsonSerializerSettings { TypeNameHandling = TypeNameHandling.Objects });
        return resultNode;
    }

    public void SwitchPlayers()
    {
        Debug.Log("Changing buttons!");
        if (currentPlayer == "1")
        {
            currentPlayer = "2";
        }
        else
        {
            currentPlayer = "1";
        }
    }
}
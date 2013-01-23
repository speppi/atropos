using Newtonsoft.Json;
using System.IO;
using System.Net;
using UnityEngine;

public class NovelModel : MonoBehaviour
{
    // Use this for initialization
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

    }

    public NovelNode GetNextNovelNode(int choice = -1)
    {
        var url = "http://speppiland.com/atropos/getNextNovelNode.py";
        if (choice != -1)
        {
            url = string.Format("{0}?choice={1}", url, choice);
        }
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
}
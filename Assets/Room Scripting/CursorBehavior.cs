using UnityEngine;
using System.Collections;

public class CursorBehavior : MonoBehaviour
{
    OTSprite sprite;
    Vector2 xSpeed = new Vector2(30, 0);
    Vector2 ySpeed = new Vector2(0, 30);

    // Use this for initialization
    void Start()
    {
        sprite = GetComponent<OTSprite>();
    }

    // Update is called once per frame
    void Update()
    {
        sprite.position +=
            (xSpeed * Input.GetAxis("Horizontal") +
             ySpeed * Input.GetAxis("Vertical")) *
            Time.deltaTime;
    }
}

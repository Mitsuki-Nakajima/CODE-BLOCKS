using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class ChangeScene : MonoBehaviour
{
    public void ToHome(){
        SceneManager.LoadScene("Home");
    }

    public void ToCodeHistory(){
        SceneManager.LoadScene("Code History");
    }

    public void ToSavedCode(){
        SceneManager.LoadScene("Saved Code");
    }

    public void ToCustomizeBlock(){
        SceneManager.LoadScene("Customize Block");
    }

    public void ToUserManual(){
        SceneManager.LoadScene("User Manual");
    }
}

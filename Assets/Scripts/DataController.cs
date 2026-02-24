using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using TMPro; 

public class DataController : MonoBehaviour
{
    [SerializeField] TextMeshProUGUI  funcName1;
    [SerializeField] TextMeshProUGUI  funcName2;
    [SerializeField] TextMeshProUGUI  funcName3;
    [SerializeField] TextMeshProUGUI  funcName4;
    [SerializeField] TextMeshProUGUI  funcName5;

    [SerializeField] Button dataButton;
    [SerializeField] TMP_InputField funcNameField1;
    [SerializeField] TMP_InputField funcNameField2;
    [SerializeField] TMP_InputField funcNameField3;
    [SerializeField] TMP_InputField funcNameField4;
    [SerializeField] TMP_InputField funcNameField5;

    //url of spreadsheet 
    string url = "https://docs.google.com/spreadsheets/d/12FSNosHHb7uqZcAi2qzXD5E-cVX_IP-FutzCj03RtRs/gviz/tq?tqx=out:csv&sheet=Commands";
    //deploy url
    string gasUrl = "https://script.google.com/macros/s/AKfycbxNf--1M1bvYhdZX3WtAcTggfLPM_EnsrSU6IHP8IsQYtHHi-Ud_SAthKi1I4uCKkQA/exec";
    
    List<string> datas = new List<string>();

    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(GetFuncData());
        //send data when the save button is pressed
        dataButton.onClick.AddListener(()=> StartCoroutine(PostData()));
    }

    IEnumerator GetFuncData()
    {
        //initialize datas & viewText
        datas.Clear();
        funcName1.text = "";
        funcName2.text = "";
        funcName3.text = "";
        funcName4.text = "";
        funcName5.text = "";

        using (UnityWebRequest req = UnityWebRequest.Get(url))
        {
            yield return req.SendWebRequest(); 

            if (IsWebRequestSuccessful(req))
            {
                ParseData(req.downloadHandler.text);
                DisplayText();
            }
            else
            {
                Debug.Log("Error");
            }
        }
    }

    IEnumerator PostData()
    {
        WWWForm form = new WWWForm();

        string newFuncName1 = funcNameField1.text;
        string newFuncName2 = funcNameField2.text;
        string newFuncName3 = funcNameField3.text;
        string newFuncName4 = funcNameField4.text;
        string newFuncName5 = funcNameField5.text;

        if(string.IsNullOrEmpty(newFuncName1))
        {
            newFuncName1 = funcName1.text;
        }
        if(string.IsNullOrEmpty(newFuncName2))
        {
            newFuncName2 = funcName2.text;
        }
        if(string.IsNullOrEmpty(newFuncName3))
        {
            newFuncName3 = funcName3.text;
        }
        if(string.IsNullOrEmpty(newFuncName4))
        {
            newFuncName4 = funcName4.text;
        }
        if(string.IsNullOrEmpty(newFuncName5))
        {
            newFuncName5 = funcName5.text;
        }
        
        string combinedText = string.Join(",", newFuncName1, newFuncName2, newFuncName3, newFuncName4, newFuncName5);
        form.AddField("val", combinedText);

        using(UnityWebRequest req = UnityWebRequest.Post(gasUrl, form))
        {
            yield return req.SendWebRequest();
            if(IsWebRequestSuccessful(req))
            {
                Debug.Log("success");
                ResetInputFields();
            }
            else
            {
                Debug.Log("error");
            }
        }
        //update the function text on the screen
        StartCoroutine(GetFuncData());
    }

    void ParseData(string csvData)
    {
        //separate by row
        string[] rows = csvData.Split(new []{"\n"}, System.StringSplitOptions.RemoveEmptyEntries);
        for(int i = 26; i < rows.Length; i++)
        {
            //separate by column
            string[] cells = rows[i].Split(new[] {','}, System.StringSplitOptions.RemoveEmptyEntries);
            for(int j = 0; j < cells.Length; j++)
            {
                if(j == 0)
                {
                    //remove double quotations from each cell
                    string trimCell = cells[j].Trim('"');
                    //add each cell into data if it's not empty
                    if(!string.IsNullOrEmpty(trimCell))
                    {
                        datas.Add(trimCell);
                    }
                }
            }

        }
    }

    //display datas
    void DisplayText()
    {
        for(int i = 0; i < datas.Count; i++)
        {
            if(i == 0)
            {
                funcName1.text = datas[i];
            }
            else if(i == 1) 
            {
                funcName2.text = datas[i];
            }
            else if(i == 2) 
            {
                funcName3.text = datas[i];
            }
            else if(i == 3) 
            {
                funcName4.text = datas[i];
            }
            else if(i == 4) 
            {
                funcName5.text = datas[i];
            }

        }
    }

    //empty input field
    void ResetInputFields()
    {
        funcNameField1.text = "";
        funcNameField2.text = "";
        funcNameField3.text = "";
        funcNameField4.text = "";
        funcNameField5.text = "";
    }

    //check if the request successed
    bool IsWebRequestSuccessful(UnityWebRequest req)
    {
        return req.result != UnityWebRequest.Result.ProtocolError && req.result != UnityWebRequest.Result.ConnectionError;
    }

    

    
}

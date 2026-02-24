using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using TMPro;

public class DataController2 : MonoBehaviour
{
    [SerializeField] TextMeshProUGUI scriptField;
    [SerializeField] TMP_Dropdown dropdownHistory;

    //url of spreadsheet 
    string url = "https://docs.google.com/spreadsheets/d/12FSNosHHb7uqZcAi2qzXD5E-cVX_IP-FutzCj03RtRs/gviz/tq?tqx=out:csv&sheet=History";

    List<string> history = new List<string>();
    List<string> optName = new List<string>();
    
    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(GetHistoryData());
        //add reload button
    }

    IEnumerator GetHistoryData()
    {
        history.Clear();
        using (UnityWebRequest req = UnityWebRequest.Get(url))
        {
            yield return req.SendWebRequest();
            if (IsWebRequestSuccessful(req))
            {
                ParseData(req.downloadHandler.text);
                dropdownHistory.ClearOptions();
                dropdownHistory.AddOptions(optName);
                dropdownHistory.value = 0;
                scriptField.text = history[0];
                dropdownHistory.onValueChanged.AddListener(delegate { OnValueChanged(); });
            }
            else
            {
                Debug.Log("Unable to obtain history");
            }
        }
    }

    public void OnValueChanged()
    {
        scriptField.text = history[dropdownHistory.value];
    }

    void ParseData(string historyData)
    {
        List<string> rows = new List<string>();

        bool inQuotes = false;
        string currentCell = "";
        foreach (char c in historyData)
        {
            if (c == '"')
            {
                inQuotes = !inQuotes;
            }
            else if ((c == '\n' || c == '\r') && !inQuotes)
            {
                if (!string.IsNullOrEmpty(currentCell))
                {
                    rows.Add(currentCell);
                    currentCell = "";
                }
            }
            else
            {
                currentCell += c;
            }
        }

        if (!string.IsNullOrEmpty(currentCell))
        {
            rows.Add(currentCell);
        }

        for (int i = 1; i < rows.Count; i++)
        {
            string[] cells = rows[i].Split(',');
            if (cells.Length > 0)
            {
                string firstCell = cells[0];
                string replacedCell = firstCell.Replace("\"\"", "\"").Trim('"');
                if (!string.IsNullOrEmpty(replacedCell))
                {
                    history.Add(replacedCell);
                    optName.Add("Execution" + i.ToString());
                }
            }
        }
    }

    // check if the request successed
    bool IsWebRequestSuccessful(UnityWebRequest req)
    {
        return req.result != UnityWebRequest.Result.ProtocolError && req.result != UnityWebRequest.Result.ConnectionError;
    }
}

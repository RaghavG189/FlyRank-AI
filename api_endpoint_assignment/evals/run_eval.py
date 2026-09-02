import json
import requests

with open("cases.json", "r") as f:

    cases_dict = json.load(f)
    list_cases = cases_dict['test_cases']



    performance_metrics = {
        "failed": []
    }
    correct = 0
    total = len(list_cases)


    for case in list_cases:

        response = requests.post("http://127.0.0.1:8000/llm/job_classification", json={"input":case["input"]})

        output_dict = json.loads(response.text)


        if case['expected_category'] == output_dict.get('category') and case['expected_experience'] == output_dict.get('experience'):
            correct += 1
        else:
            performance_metrics["failed"].append({"input":case["input"][:100]})


    performance_metrics["correct"] = correct     
    performance_metrics["percentage"] = (correct / total) * 100

    print(performance_metrics)

        
    
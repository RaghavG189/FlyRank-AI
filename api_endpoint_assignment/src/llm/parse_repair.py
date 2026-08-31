import json
import re



def parse_repair_output(output:str):

    #Get rid of fences
    stripped_output = re.sub(r"^```(?:json)?\s*|\s*```$", "", output.strip(), flags=re.IGNORECASE)


    #Get the JSON object
    index = stripped_output.find("{")

    if index == -1:
        return None

    json_part = stripped_output[index:]

    try:

        decoder = json.JSONDecoder()
        json_object, end_index = decoder.raw_decode(json_part)

        return json_object

    except json.JSONDecodeError as e:

        return None




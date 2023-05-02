class Filter:
    """A filter is a key-value pair in the request body.
    When applying the filter, check that:
     obj[filter.key] in filter.value"""

    def __init__(self, key: str, values: str):
        self.key = key
        self.value: list[str] = values.split(",") if values != "" else []

    def __str__(self):
        return str(self.__dict__).replace("'", '"')


class Element:
    """Element is the value of the "elements" key in the request body:
    {
        "elements": [
            {
                "elementName": "e1",
                "attendee.nation": "Italy,France",
                "second_filter": "value"
            },
            {
                "elementName": "e2",
                "altro": "value"
            }
        ]
    }"""

    def __init__(self, jsonDict: dict):
        self.elementName = jsonDict["elementName"]
        self.attendeeFilters = []
        self.meetingFilters = []
        self.tdocFilters = []
        self.membershipFilters = []
        for key, value in jsonDict.items():
            if key != "elementName" and value != "":
                target,key = key.split(".")
                if target == "attendee":
                    self.attendeeFilters.append(Filter(key, value))
                elif target == "meeting":
                    self.meetingFilters.append(Filter(key, value))
                elif target == "tdoc":
                    self.tdocFilters.append(Filter(key, value))
                elif target == "membership":
                    self.membershipFilters.append(Filter(key, value))
                else:
                    s = f"Invalid target: {target}"
                    raise ValueError(s)

    def __str__(self):
        return str(self.__dict__).replace("'", '"')

    def __getitem__(self, key):
        return self.__dict__[key]



def from_json_to_element_class(element: dict) -> Element:
    if type(element) != dict:
        raise TypeError(f"Invalid type: {type(element)}\n Try to use json.loads()")
    return Element(element)

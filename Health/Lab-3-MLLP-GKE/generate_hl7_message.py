import hl7

def create_hl7_message():
    separators = "^~\\&"
    message = hl7.Message(
        [
            hl7.Segment(
                "MSH",
                [
                    "|", separators, "SendingApp", "SendingFacility", "ReceivingApp", "ReceivingFacility",
                    "202412280610", "", "ADT^A01", "123456", "P", "2.3"
                ]
            ),
            hl7.Segment(
                "PID",
                [
                    "1", "", "123456^^^Hospital^MRN", "", "John^Doe", "", "19700101", "M", "", "", "", "",
                    "(555)555-5555"
                ]
            ),
            hl7.Segment(
                "PV1",
                [
                    "1", "I", "W^5^1", "", "", "", "", "", "", "", "", "ER", "", "", "", "",
                    "123456", ""
                ]
            ),
        ],
        separators=separators
    )
    return str(message)

hl7_message = create_hl7_message()
print(hl7_message)

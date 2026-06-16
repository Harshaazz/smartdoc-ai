def classify_document(text):

    text = text.lower()

    if any(
        keyword in text
        for keyword in [
            "invoice",
            "gst",
            "amount",
            "tax"
        ]
    ):
        return "Invoice"

    elif any(
        keyword in text
        for keyword in [
            "resume",
            "experience",
            "education",
            "skills"
        ]
    ):
        return "Resume"

    elif any(
        keyword in text
        for keyword in [
            "agreement",
            "contract",
            "terms"
        ]
    ):
        return "Contract"

    return "Other"
from .templates import TEMPLATES

def format_airports(airports):
    if not airports:
        return "unknown locations"
    if len(airports) == 1:
        return airports[0]
    return ", ".join(airports)

def generate_summary(label, extracted):
    template = TEMPLATES.get(label, "Operational advisory affecting {airports}.")
    return template.format(
        airports=format_airports(extracted.get("airports")),
        cause=extracted.get("cause", "unknown cause"),
        end_time=extracted.get("end_time", "unknown time")
    )

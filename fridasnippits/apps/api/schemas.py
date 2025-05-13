from voluptuous import Schema, All, Length, Match

NewProjectSchema = Schema(
    {
        "name": All(str, Length(min=1), Match(r"^[a-zA-Z0-9\s\-]+$")),
        "category": All(str, Length(min=1)),
        "source": All(str, Length(min=1)),
        "description": All(str, Length(min=1)),
    },
    required=True,
)

UpdateProjectSchema = Schema(
    {
        "category": All(str, Length(min=1)),
        "source": All(str, Length(min=1)),
        "description": All(str, Length(min=1)),
    },
    required=True,
)

LikeProjectSchema = Schema({"project_uuid": All(str, Length(min=1))})

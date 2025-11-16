from .profiles import UserProfile

def determine_feedback_type(stage: int, profile: UserProfile) -> str:
    """
    Returns feedback style based on learning stage and profile.
    """

    # Stage-dependent rules
    if stage == 1:
        return "Directive"
    if stage == 2:
        return "Remedial"
    if stage >= 3:
        return "Facilitative"

    # Additional cognitive tuning:
    if profile.learning_type == "TAR":
        return "Textual Reflective"
    if profile.learning_type == "PAI":
        return "Visual Scaffold"
    if profile.learning_type == "GR":
        return "Conceptual Overview"

    return "General"
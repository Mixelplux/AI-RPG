"""Read-only scene wording for the fixed West-Road situation."""

ROUTE_FOLLOWTHROUGH = (
    "Guards remain on the road instead of their other approaches. "
    "Grey values the information; Elin notes the cost to those approaches. "
    "The broader threat remains unresolved."
)

CURRENT_CIRCUMSTANCES = {
    "investigating": "West-road travelers say they are being watched, and a caravan is overdue. Grey fears for the trade road; Elin wants evidence before pulling guards from other approaches. No one knows who the watchers are or whether the caravan was attacked.",
    "observers_withdrew": "The patrol scattered the watchers, who left fresh tracks behind. Grey wants to learn where they went; Elin has fewer guards on the other approaches until coverage is restored.",
    "wagon_intercepted": "The extra investigation found signs of patrol timing, but another wagon was intercepted. Its escaped driver warned of a threatened supply stop. Grey and Elin now face a choice between protection and a local search.",
    "withdrawal_route_found": "An abandoned lookout reveals the observers' withdrawal route. Nobody was captured. " + ROUTE_FOLLOWTHROUGH,
    "coverage_restored": "Guards are back on ordinary local coverage. The withdrawal trail remains unexplored and the observers unlocated. Elin welcomes restored coverage; Grey remains concerned about the threat. The broader threat remains unresolved.",
    "supply_stop_protected": "The supply stop has been warned and its next departure is held safely. Elin confirms its protection; Grey notes that the raiders remain unlocated. The broader threat remains unresolved.",
    "raider_staging_area_found": "Nearby signs point to a likely staging area. There has been no confrontation, and the supply stop has no dedicated protection. Grey values the lead; Elin cautions about the unprotected stop. The broader threat remains unresolved.",
}


CHOICE_WORDING = {
    "advocate patrol": "Urge an immediate patrol — one hour; other approaches lose coverage",
    "continue investigation": "Keep the guards in place while you investigate — one hour; road traffic remains exposed",
    "pursue observers": "Follow the watchers' fresh tracks while guards remain away from other approaches",
    "restore coverage": "Return the guards to ordinary coverage, leaving the trail unexplored",
    "protect supply stop": "Protect the threatened supply stop's next departure",
    "locate raiders": "Search nearby signs for the raiders, leaving the stop without dedicated protection",
}


COMPETENCE_WORDING = {
    "follow withdrawal signs": "Try to follow the watchers' fresh tracks",
    "reconstruct local observation circuit": "Piece together the watchers' roadside positions",
    "arrange guarded local survey": "Coordinate a survey with the committed guards",
}


def choice_text(command):
    """Express an already eligible fixed command without deciding eligibility."""
    return f"You can choose: {CHOICE_WORDING[command]} (type '{command}')."


def competence_choice_text(approach):
    """Keep engine-assessed cost/uncertainty while omitting dice notation."""
    command = approach["command"]
    hours = approach["cost_hours"]
    duration = "one hour" if hours == 1 else f"{hours} hours"
    if approach["uncertain"]:
        qualification = "uncertain, though your experience helps" if approach["specialist"] else "the result is uncertain"
    else:
        qualification = "the guards can establish the local route"
    return f"You can choose: {COMPETENCE_WORDING[command]} — {duration}; {qualification} (type '{command}')."

CURRENT_CHOICE_HINTS = {
    "investigating": "Travel to the Southwest Trade Road (go to Southwest Trade Road). Once there, examine the tracks and speak with Mara. Elin needs both reports before she can weigh pulling guards from other approaches.",
    "observers_withdrew": "You've committed to patrol action. Choose 'pursue observers' to follow the fresh tracks, or 'restore coverage' to return guards to ordinary duties.",
    "wagon_intercepted": "The further investigation is complete. Choose 'protect supply stop' to safeguard the next departure, or 'locate raiders' to investigate nearby signs.",
    "withdrawal_route_found": "The withdrawal route is known. You can talk to Grey or Elin (talk to Grey / talk to Elin), review your clues (clues), or travel to another known place.",
    "coverage_restored": "Normal coverage has already been restored. You can talk to Grey or Elin (talk to Grey / talk to Elin), review your clues (clues), or travel to another known place.",
    "supply_stop_protected": "The supply stop is already protected. You can talk to Grey or Elin (talk to Grey / talk to Elin), review your clues (clues), or travel to another known place.",
    "raider_staging_area_found": "The local search is complete. You can talk to Grey or Elin (talk to Grey / talk to Elin), review your clues (clues), or travel to another known place.",
}


def compact_secondary_actions(opportunities):
    """Compact already-derived advisory text; never determine eligibility here."""
    speaking = []
    presenting = []
    other = []
    speech_commands = {
        "Captain Darvin Grey": "talk to Grey",
        "Elin Voss": "talk to Elin",
        "Mara, Caravan Driver": "talk to Mara",
    }
    for text in opportunities:
        if text.startswith("You can choose:"):
            continue
        if text.startswith("You can speak with "):
            name = text.removeprefix("You can speak with ").removesuffix(".")
            command = speech_commands.get(name)
            speaking.append(name + (" (" + command + ")" if command else ""))
        elif text.startswith("You can present "):
            presenting.append(text.removeprefix("You can present ").removesuffix("."))
        elif text == "You can investigate this area.":
            other.append("Investigate this area (investigate)")
        else:
            other.append(text)
    actions = []
    if speaking:
        actions.append("Speak with " + " / ".join(speaking))
    if presenting:
        actions.append("Present " + " / ".join(presenting))
    return "; ".join(actions + other)

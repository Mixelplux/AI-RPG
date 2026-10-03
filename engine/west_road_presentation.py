"""Read-only wording for the seven fixed west-road circumstances."""

CURRENT_CIRCUMSTANCES = {
    "investigating": "West-road travelers report being watched, and a caravan is overdue. Grey fears a growing threat to trade; Elin wants specific evidence before diverting guards. The observers' identity and any attack remain unconfirmed.",
    "observers_withdrew": "The patrol has driven the observers away, leaving fresh signs. Grey welcomes the intervention; Elin cautions that other approaches have fewer guards. The trail can be followed, or normal coverage restored.",
    "wagon_intercepted": "Patrol-timing marks suggest organized preparation. During the extra investigation, another wagon was intercepted; its escaped driver identified a threatened supply stop. Elin understands the caution, while Grey regrets the delay. Protection and a local search are the next alternatives.",
    "withdrawal_route_found": "An abandoned lookout reveals the observers' withdrawal route. Nobody was captured, and road-focused coverage remains extended. Grey values the information; Elin notes the cost to other approaches. The broader threat remains unresolved.",
    "coverage_restored": "Guards are back on ordinary local coverage. The withdrawal trail remains unexplored and the observers unlocated. Elin welcomes restored coverage; Grey remains concerned about the threat. The broader threat remains unresolved.",
    "supply_stop_protected": "The supply stop has been warned and its next departure is held safely. Elin confirms its protection; Grey notes that the raiders remain unlocated. The broader threat remains unresolved.",
    "raider_staging_area_found": "Nearby signs point to a likely staging area. There has been no confrontation, and the supply stop has no dedicated protection. Grey values the lead; Elin cautions about the unprotected stop. The broader threat remains unresolved.",
}

CURRENT_CHOICE_HINTS = {
    "investigating": "Gather the tracks and Mara's account on the Southwest Trade Road, then report both to Elin at the North Gate. Once she has both reports, choose immediate patrol action or another hour of investigation.",
    "observers_withdrew": "You've committed to patrol action. Choose 'pursue observers' to follow the fresh signs, or 'restore coverage' to return guards to ordinary duties.",
    "wagon_intercepted": "The further investigation is complete. Choose 'protect supply stop' to safeguard the next departure, or 'locate raiders' to investigate nearby signs.",
    "withdrawal_route_found": "The local pursuit is complete. You can speak with Grey or Elin, review your clues, or explore the town.",
    "coverage_restored": "Normal coverage has already been restored. You can speak with Grey or Elin, review your clues, or explore the town.",
    "supply_stop_protected": "The supply stop is already protected. You can speak with Grey or Elin, review your clues, or explore the town.",
    "raider_staging_area_found": "The local search is complete. You can speak with Grey or Elin, review your clues, or explore the town.",
}


def compact_secondary_actions(opportunities):
    """Compact already-derived advisory text; never determine eligibility here."""
    speaking = []
    presenting = []
    other = []
    for text in opportunities:
        if text.startswith("You can choose:"):
            continue
        if text.startswith("You can speak with "):
            speaking.append(text.removeprefix("You can speak with ").removesuffix("."))
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

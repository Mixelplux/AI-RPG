"""Character inputs and bounded 2024 checks; no acceptance or world authority."""

SOCIAL = ('persuasion', 'deception', 'intimidation', 'performance')
SKILLS = SOCIAL + ('perception', 'investigation')
# Explicit authored investigator: Cha 14, Wis 12, Int 14, proficiency +2.
# Skill ranks are 0/untrained, 1/proficient, 2/expertise, never climbing inputs.
INVESTIGATOR = (14, 12, 14, 2, (1, 0, 0, 0, 1, 1))


def validate_profile(profile):
    if (type(profile) is not tuple or len(profile) != 5
            or any(type(v) is not int or not 1 <= v <= 30 for v in profile[:3])
            or type(profile[3]) is not int or not 2 <= profile[3] <= 6
            or type(profile[4]) is not tuple or len(profile[4]) != len(SKILLS)
            or any(type(v) is not int or v not in (0, 1, 2) for v in profile[4])):
        raise ValueError('explicit Watchhouse character skill profile required')


def bonus(profile, skill, exhaustion=0):
    validate_profile(profile)
    index = SKILLS.index(skill)
    score = profile[0 if index < 4 else 1 if skill == 'perception' else 2]
    return (score - 10) // 2 + profile[3] * profile[4][index] - exhaustion * 2


def check(profile, skill, dc, rolls, attitude='indifferent', exhaustion=0):
    """Pure reconstruction. Natural 1/20 do not auto fail/succeed ability checks."""
    count = 2 if skill in SOCIAL and attitude != 'indifferent' else 1
    if (type(rolls) is not tuple or len(rolls) != count
            or any(type(r) is not int or not 1 <= r <= 20 for r in rolls)):
        raise ValueError('recorded d20 evidence required')
    die = (max(rolls) if attitude == 'friendly' else min(rolls)) if count == 2 else rolls[0]
    return die + bonus(profile, skill, exhaustion) >= dc

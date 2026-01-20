from typing import Tuple, List
from schemas import ExtractedFacts, PolicyDecision


POLICY_CITATIONS = {
    "First Aid and Emergency Response": [
        "In case of more serious injuries, such as suspected fractures, or if the service user is unconscious, contact emergency services immediately."
    ],
    "Mobility & Moving": [
        "If a service user falls, you must email your supervisor immediately with details of the incident, including the time, location, and condition of the service user.",
        "If this is a recurring issue (two or more falls in a week), cc the Risk Assessor on the email and arrange for a moving and handling risk assessment review to address potential hazards and ensure the service user’s environment is safe."
    ],
    "Mental Health and Emotional Well-being": [
        "In cases where a service user calls in confused, disoriented, or excessively worried, alert their family or next of kin to inform them of the situation and ensure appropriate follow-up care can be arranged."
    ]
}

def decide_policy(facts: ExtractedFacts) -> Tuple[PolicyDecision, List[str]]:
    # given our facts from the transcript, we need to map this to our policy
    triggered = []
    notify = []
    next_steps = []
    citations = []

    emergency = False
    risk_needed = False
    risk_type = None

    # is he not responding / very injured policy
    if facts.unconscious is True or facts.suspected_fracture is True:
        triggered.append("First Aid and Emergency Response")
        notify += ["Emergency Services (999)", "Supervisor"]
        next_steps += [
            "Call 999 immediately.",
            "Inform supervisor immediately."
        ]
        citations += POLICY_CITATIONS["First Aid and Emergency Response"]
        emergency = True

    # fall / mobility issues policy
    if facts.incident_type == "Fall":
        triggered.append("Mobility & Moving")
        notify.append("Supervisor")
        next_steps += [
            "Record incident in the incident log.",
            "Ensure service user is safe and arrange support if needed."
        ]
        citations += POLICY_CITATIONS["Mobility & Moving"]

        # falling multiple times
        if (facts.recurring_this_week_count or 0) >= 2:
            notify.append("Risk Assessor (CC)")
            risk_needed = True
            risk_type = "Moving & Handling Risk Assessment Review"
            next_steps.append("Arrange a moving & handling risk assessment review.")

    # mental health / well being issues
    if facts.confused_or_disoriented:
        notify.append("Family or Next of kin")
        next_steps.append("Ensure appropriate follow-up care can be arranged.")

    decision = PolicyDecision(
        triggered_sections=triggered,
        who_to_notify=notify,
        emergency_services_contacted=emergency,
        risk_assessment_needed=risk_needed,
        risk_assessment_type=risk_type,
        agreed_next_steps=next_steps
    )

    return decision, citations


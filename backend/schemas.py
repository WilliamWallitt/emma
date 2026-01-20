from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class ExtractedFacts(BaseModel):
    service_user_name: Optional[str] = None
    location: Optional[str] = None
    incident_type: Literal["Fall", "Other"] = "Other"
    description: Optional[str] = None
    recurring_this_week_count: Optional[int] = None
    confused_or_disoriented: Optional[bool] = None
    suspected_fracture: Optional[bool] = None
    unconscious: Optional[bool] = None


'''
Field	Data Type
Date and Time of Incident	DateTime
Service User Name	Str
Location of Incident	Str
Type of Incident	Str
Description of the Incident	Str
Immediate Actions Taken	Str
Was First Aid Administered?	Boolean
Were Emergency Services Contacted?	Boolean
Who Was Notified?	Str
Witnesses	Str
Agreed Next Steps	Str
Risk Assessment Needed	Boolean
If Yes, Which Risk Assessment	Str
'''

class IncidentForm(BaseModel):
    date_and_time_of_incident: str
    service_user_name: str
    location_of_incident: str
    type_of_incident: str
    description_of_incident: str
    immediate_actions_taken: str
    was_first_aid_administered: bool
    were_emergency_services_contacted: bool
    who_was_notified: str
    witnesses: str
    agreed_next_steps: str
    risk_assessment_needed: bool
    if_yes_which_risk_assessment: str


class DraftEmail(BaseModel):
    to: List[str]
    cc: List[str]
    subject: str
    body: str


class GenerateFormAndEmailReponse(BaseModel):
    incident_form: IncidentForm
    email: DraftEmail


class PolicyDecision(BaseModel):
    triggered_sections: List[str]
    who_to_notify: List[str]
    emergency_services_contacted: bool
    risk_assessment_needed: bool
    risk_assessment_type: Optional[str] = None
    agreed_next_steps: List[str]

# requests

class TranscriptRequest(BaseModel):
    transcript: str = Field(min_length=20)
    user_feedback: Optional[str] = None # ran out of time

# we return the facts as well so the user
# can check that the model has not made stuff up
class ProcessTranscriptResponse(BaseModel):
    facts: ExtractedFacts
    policy_decision: PolicyDecision
    incident_form: IncidentForm
    email: DraftEmail
    citations: List[str]
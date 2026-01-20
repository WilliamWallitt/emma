// ts interfaces for our res data
export interface DraftEmail {
  to: string[];
  cc: string[];
  subject: string;
  body: string;
}

export interface IncidentForm {
  date_and_time_of_incident: string;
  service_user_name: string;
  location_of_incident: string;
  type_of_incident: string;
  description_of_incident: string;
  immediate_actions_taken: string;
  was_first_aid_administered: boolean;
  were_emergency_services_contacted: boolean;
  who_was_notified: string;
  witnesses: string;
  agreed_next_steps: string;
  risk_assessment_needed: boolean;
  if_yes_which_risk_assessment: string;
}

export type IncidentType = "Fall" | "Other";
export interface ExtractedFacts {
  service_user_name?: string | null;
  location?: string | null;
  incident_type: IncidentType;
  description?: string | null;
  recurring_this_week_count?: number | null;
  confused_or_disoriented?: boolean | null;
  suspected_fracture?: boolean | null;
  unconscious?: boolean | null;
}

export interface PolicyDecision {
  triggered_sections: string[];
  who_to_notify: string[];
  emergency_services_contacted: boolean;
  risk_assessment_needed: boolean;
  risk_assessment_type?: string | null;
  agreed_next_steps: string[];
}

//actual res
export interface ProcessTranscriptResponse {
  facts: ExtractedFacts;
  policy_decision: PolicyDecision;
  incident_form: IncidentForm;
  email: DraftEmail;
  citations: string[];
}

import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Tuple

from schemas import ExtractedFacts, GenerateFormAndEmailReponse, PolicyDecision, IncidentForm, DraftEmail

load_dotenv()

client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))
model_version = os.getenv('GPT_MODEL')

FACTS_PROMPT = """
You are an assistant extracting incident facts from a social care transcript.
Rules:
- Never invent data. If unknown, use null.
- "recurring_this_week_count" should be numeric if mentioned explicitly (e.g., "third time this week" => 3).
- Keep description concise and factual.
"""

GEN_PROMPT = """You are drafting:
1) an incident report form content, and
2) a professional email to relevant staff.

You MUST ONLY use the provided ExtractedFacts and PolicyDecision.
Do NOT add facts not present.
If something is missing, write "Unknown" or add a question in Next Steps.
"""


# todo: gpt to parse schema using text_format param (not schema def in prompt)

def extract_facts(transcript: str) -> ExtractedFacts:
    resp = client.responses.parse(
        model=model_version,
        input=[
            {"role": "system", "content": FACTS_PROMPT},
            {"role": "user", "content": transcript},
        ],
        text_format=ExtractedFacts
    )
    return resp.output_parsed


def generate_form_and_email(facts: ExtractedFacts, decision: PolicyDecision) -> Tuple[IncidentForm, DraftEmail]:
    resp = client.responses.parse(
        model=model_version,
        input=[
            {"role": "system", "content": GEN_PROMPT},
            {
                "role": "user",
                "content": (
                    f"ExtractedFacts:\n{facts.model_dump_json(indent=2)}\n\n"
                    f"PolicyDecision:\n{decision.model_dump_json(indent=2)}"
                ),
            },
        ],
        text_format=GenerateFormAndEmailReponse,
    )

    parsed: GenerateFormAndEmailReponse = resp.output_parsed
    return parsed.incident_form, parsed.email

    # data = resp.output_text
    # #https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
    # obj = json.loads(data)
    # form = IncidentForm(**obj["incident_form"])
    # email = DraftEmail(**obj["email"])
    # return form, email
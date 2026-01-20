import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import ExtractedFacts, ProcessTranscriptResponse, TranscriptRequest


from llm import extract_facts, generate_form_and_email
from policy_rules import decide_policy

logger = logging.getLogger("emma-task")
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# allow front end to send requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# check backend works
@app.get("/health")
def health():
    return {"ok": True}


def fallback_extract(transcript: str) -> ExtractedFacts:

    # falling back if the LLM fails to extract data
    # manually trying to parse the transcript
    # this is incomplete as I ran out of time, but the main idea is to look for certain
    # keywords in the transcript so we can find facts

    transcript = transcript.lower()
    fall_words = ["fall", "fell", "slipped", "tripped"]
    incident_type = "Fall" if any(w in transcript for w in fall_words) else "Other"
    confused_words = ["confused", "disoriented", "fuzzy", "can't remember", "cannot remember"]
    confused_or_disoriented = True if any(w in transcript for w in confused_words) else None
    recurring = None
    location = None
    suspected_fracture = True if ("fracture" in transcript or "broken" in transcript) else None
    unconscious = True if ("unconscious" in transcript or "passed out" in transcript) else None

    if "living room" in transcript:
        location = "Living room"
    elif "kitchen" in transcript:
        location = "Kitchen"
    elif "bathroom" in transcript:
        location = "Bathroom"
    elif "bedroom" in transcript:
        location = "Bedroom"

    return ExtractedFacts(
        service_user_name=None,
        location=location,
        incident_type=incident_type,
        description="",
        confused_or_disoriented=confused_or_disoriented,
        recurring_this_week_count=recurring,
        suspected_fracture=suspected_fracture,
        unconscious=unconscious,
    )


@app.post("/process-transcript", response_model=ProcessTranscriptResponse)
def process_transcript(req: TranscriptRequest):
    logger.info("Receiving transcript data from the front end.")
    transcript = req.transcript.strip()
    # Try and extract facts from the transcript
    try:
        logger.info("Extracting facts from transcript")
        facts = extract_facts(transcript)
        logger.info("done")
    except Exception as e:
        # Do it manually if it fails
        logger.exception("LLM facts extraction failed, applying fallback mechanism")
        facts = fallback_extract(transcript)

    # applying our policy to the facts found
    logger.info("Analysing the meeting data against the policies")
    decision, citations = decide_policy(facts)
    logger.info("done")
    #  user feedback
    if req.user_feedback:
        logger.info("Applying user feedback")
        # didn't have time to implement, I would pass the feedback into
        # my generate_form_and_email function so I can apply it to the LLM prompt
    try:
        logger.info("Generating an incident form based on the policies and template "
                    "and drafting an email to the appropriate person(s).")
        form, email = generate_form_and_email(facts, decision)
        logger.info("done")
    except Exception:
        logger.exception("LLM generating incident form based on the policies and template has failed")
        raise HTTPException(status_code=500, detail="Failed to generate incident form and email")

    return ProcessTranscriptResponse(
        facts=facts,
        policy_decision=decision,
        incident_form=form,
        email=email,
        citations=citations,
    )
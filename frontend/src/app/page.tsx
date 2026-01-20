"use client";
import styles from "./page.module.css";
import {useState} from "react";
import {ProcessTranscriptResponse} from "../interfaces/interfaces";

export default function Home() {

    // didn't havetime to add redux / state management
    const [transcript, setTranscript] = useState<string>("");
    const [result, setResult] = useState<ProcessTranscriptResponse | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function uplaod_and_process_transcript() {

          // check that they actually pasted in something
          setError(null)

          if (transcript.length === 0) {
              setError("Pls paste in a transcript (none found)")
              return;
          }

          setLoading(true);
          setResult(null);

          // try and make a req

          try {
              // can use next.js routes, no time
              const res = await fetch("http://localhost:8000/process-transcript", {
                method: "POST",
                headers: { "content-type": "application/json" },
                body: JSON.stringify({ transcript }),
              });

              let data : any
              // http status not 200
              if (!res.ok) {
                  let message = `Failed`
                  // try get err msg
                  try {
                    let err : {detail: string} = await res.json()
                    message = `${message} - ${err.detail}`
                  } catch (err: any) {
                    throw new Error(message);
                  }
                   throw new Error(message);
              }
                // try and get data
              try {
                  data = await res.json();
              } catch (err: any) {
                  throw new Error("Invalid JSON response");
              }
              setResult(data)
          } catch (err: any) {
              // if any local throws inside our try catch set error msg
                setError(typeof err?.message === "string"
                    ? err.message
                    : "Something when wrong")
          } finally {
              setLoading(false)
          }
    }

    return (
      <div className={styles.pageContainer}>
        <main className={styles.pageWrapper}>
          <p>Please paste your transcript to generate an incident form / draft email</p>
          <br/>
          <div className={styles.row}>
            <textarea
              value={transcript}
              onChange={(e) => setTranscript(e.target.value)}
              rows={12}
              style={{ width: "100%", height: "200px"}}
              placeholder="Paste call or meeting trascript here"
            />
          </div>


          <button disabled={loading} onClick={(_) => uplaod_and_process_transcript()} style={{ marginTop: 12 }}>
              {loading ? "Processing" : "Submit"}
          </button>

          {error && <p className={styles.red}>{error}</p>}

          {result && (
            <>
              <h2>incident Form</h2>
              <pre>{JSON.stringify(result.incident_form, null, 2)}</pre>

              <h2>Email Draft</h2>
              <pre>{JSON.stringify(result.email, null, 2)}</pre>

              <h2>Fact Check</h2>
              <pre>{JSON.stringify({ facts: result.facts, policy_decision: result.policy_decision }, null, 2)}</pre>
            </>
          )}
        </main>
      </div>
    );
  }

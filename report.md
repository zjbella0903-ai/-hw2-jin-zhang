Title: Customer‑Support Reply Drafting with Prompt Iteration

Business use case
Workflow: Draft concise, brand‑appropriate customer‑support replies.
User: Customer support representative.
Input: A customer message (plain text).
Output: A review‑ready reply under 100–120 words with clear next steps and no legal/policy guarantees.
Why it matters: Support teams spend time writing first drafts. A reliable draft generator improves speed and tone consistency while preserving human control for sensitive cases.
Model choice and setup
Model: Gemini (default gemini-1.5-flash; tested with gemini-2.5-flash for faster/stronger drafting).
Rationale: Fast, cost‑effective for short reply drafting; good instruction following; easy to call from Python via google‑generativeai.
Prompt structure: A system instruction plus a simple task wrapper; prompt versions are loaded from prompts.md.
Evaluation set
I used a stable set of five cases:
Delivery delay (normal)
Broken charger (edge; should offer replacement)
Account locked (policy/security)
Cancel order but ask for rush delivery (conflicting request)
Data‑deletion + legal threat (high‑risk)
Each case includes a short note on what a “good output” should do, to keep evaluation repeatable.
Prompt iterations
Initial (Baseline):
Concise assistant with rubric: acknowledge issue, reference IDs, ask one clarifying question if needed, no legal/policy guarantees, clear next step, <120 words.
Observation: technically correct but robotic/blunt; sometimes missed empathy and structure.
Revision 1:
“Professional and empathetic senior support agent”; first‑sentence acknowledgment; warm language; numbered next steps; strict <120 words; immediate replacement for broken‑product case.
Observation: tone improved and steps clearer, but still inconsistent in high‑stakes scenarios (refund policy details; legal threats).
Revision 2 (Final):
Helpful, professional, and polite; standard response pattern for data requests; keep <100 words to enforce clarity and reduce drift.
Observation: best balance of tone, safety, and brevity.
Evidence: baseline vs. final comparison Note: Insert 1–2 concise quotes from your outputs to show improvements. Keep PII out.
Case 3 (Account locked)

Initial (excerpt): “[paste 1–2 lines showing robotic tone or missing structure]”
Revision 2 (excerpt): “[paste 1–2 lines showing first‑sentence acknowledgment + numbered next steps]”
Improvement: r2 provides clear, numbered next steps and stays within word limit; tone is empathetic and avoids policy overcommitment.
Case 5 (Data deletion + legal threat)

Initial (excerpt): “[paste 1–2 lines that could sound risky or vague]”
Revision 2 (excerpt): “[paste 1–2 lines showing defer‑to‑human/compliance, no guarantees, calm tone]”
Improvement: r2 avoids legal guarantees, directs the user to the proper privacy/compliance flow, and maintains a calm, professional tone.
Remaining failure modes and human‑review boundaries
High‑stakes/legal scenarios: Any legal threats or regulatory requests may require manual verification and approval.
Ambiguous or multi‑topic messages: The model may need a clarifying question; risk of omitting a critical detail if the input is very long.
Policy drift: Without explicit constraints, the model can drift into promises. The “no guarantees + defer to human/compliance” rule reduces but does not eliminate risk.
Hallucination risk: Low but non‑zero; mitigated by short outputs and strict instruction to avoid policy claims.
Recommendation for deployment
Recommended as a human‑in‑the‑loop drafting tool:
The model drafts using Revision 2.
A support agent reviews and edits before sending.
Guardrails:
Use r2 by default; enforce <100 words.
Flag any message containing legal threats, PII, or policy requests for mandatory human review.
Log inputs/outputs; periodically sample for quality.
Not recommended for fully autonomous sending, especially for legal, privacy, or refund‑policy edge cases.
Short reflection (what I learned)
Iteration matters: Adding explicit structure (acknowledgment + numbered steps + word limit) consistently improved clarity and tone.
Safety through constraints: “No legal/policy guarantees” and “defer to human/compliance” significantly reduced risky language in Case 5.
Brevity helps quality: The <100‑word limit in r2 reduced hedging and forced clearer next steps.
Appendix: Repro steps

Command examples:
Single case: python app.py --case 5 --version r2 --model gemini-2.5-flash
Full sweep: run cases 1–5 for initial and r2, then compare files in outputs/.
Outputs are saved under outputs/gem-<model>-v-<version>-case<id>-<timestamp>.txt
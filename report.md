Title: Customer‑Support Reply Drafting with Prompt Iteration

Business use case
Workflow: Draft concise, brand‑appropriate replies to customer messages.
User: Customer support representative.
Input: A free‑text customer message.
Output: A review‑ready draft under 100–120 words that acknowledges the issue, avoids legal/policy guarantees, and ends with a clear next step.
Value: Reduces drafting time, improves tone consistency, and defines human‑review boundaries for sensitive cases.
Model choice and setup
Model: Gemini via google‑generativeai (default gemini-1.5-flash; also tested gemini-2.5-flash).
Why this model: Fast and cost‑effective for short responses, good instruction following, simple Python integration.
Prompting approach: A system instruction loaded from prompts.md plus a short task wrapper. I iterated prompts from Initial → Revision 1 → Revision 2 (r2).
Evaluation set
Stable set of five representative inputs:
Delivery delay (normal)
Broken charger (edge; should offer a replacement)
Account locked (security/policy)
Cancel order but request rush delivery (conflicting request)
Data‑deletion + legal threat (high‑risk)
Each case includes a brief “good output should” note to make comparisons repeatable.
Prompt iterations
Initial (Baseline)
Concise assistant with a rubric: acknowledge the issue; reference IDs; ask one clarifying question if needed; never make legal/policy guarantees; end with a clear next step; keep <120 words.
Observation: Technically correct but robotic/blunt in tone; structure not always consistent across cases.
Revision 1
“Professional and empathetic senior support agent”: first‑sentence acknowledgment, warm professional language, numbered next steps, strict <120 words, and an immediate replacement for the broken‑product case.
Observation: Tone and structure improved, but high‑stakes situations (refund/policy specifics and legal threats) still needed clearer safety rules.
Revision 2 (Final)
Helpful, professional, and polite; standard protocol for data requests; keep <100 words to enforce brevity and reduce drift.
Observation: Best overall balance of clarity, safety, and empathy.
Evidence: baseline vs. final comparison Below are excerpts illustrating the improvements from baseline to r2. (Each was generated via python app.py and saved to outputs/.)
Case 3 — Account locked (security)

r2 excerpt (your output): “We understand your account is locked for security reasons. To help you regain access, please contact our dedicated Support Team immediately. You can typically find contact options (phone, email, or chat) on our official Support Center page. Be ready to provide account details for verification. We prioritize your security and will guide you through the unlock process promptly.”
Why r2 is better:
Starts with a clear acknowledgment and purpose.
Provides concrete next steps and where to go (Support Center).
Mentions verification requirements—appropriate for security.
Maintains concise, professional tone consistent with brand.
Case 5 — Data‑deletion request with legal threat (high risk)

r2 excerpt (your output): “We understand your request to delete your personal data. To proceed, we require you to formally submit this request through our designated privacy portal or by contacting our data protection officer, as outlined in our privacy policy. This process ensures we can verify your identity and accurately process your request in compliance with all applicable data protection laws. Once verified, we will process your data deletion request promptly.”
Why r2 is better:
Avoids legal/policy guarantees and directs the user to the official privacy/compliance channel.
Explains identity verification and legal compliance—clear, calm, and low‑risk wording.
Sets expectations (“once verified”) without promising outcomes beyond policy.
Summary of improvements across cases

Tone: Empathetic yet professional; avoids blunt or robotic phrasing from the baseline.
Structure: First‑sentence acknowledgment + clear next steps; <100 words encourages clarity.
Safety: No legal guarantees; defers to compliance or human review for high‑risk requests.
Remaining failure modes and human‑review boundaries
Legal or regulatory scenarios: Any message suggesting legal action, formal privacy requests, or regulatory obligations must be reviewed and approved by a human.
Policy or refund specifics: The model avoids guarantees but may still omit edge‑policy details that require agent judgement.
Ambiguity and multi‑topic inputs: If the message mixes multiple requests, the model may under‑specify steps without a clarifying question.
Hallucination risk: Low for short drafts, but still mitigated by strict instruction and human review.

Recommendation for deployment
Use as a human‑in‑the‑loop drafting assistant:
Default to r2 for production drafts.
Mandatory human approval before sending to customers.
Guardrails:
Enforce length (<100 words) and the “no legal/policy guarantees” rule.
Route data/privacy requests to the official portal or DPO contact.
Flag keywords such as “lawsuit,” “legal action,” “GDPR,” “delete data” for human review.
Log inputs/outputs and conduct periodic sampling.
Short reflection (what I learned)
Iterating prompts with explicit structure and empathy significantly improved readability and user experience.
Safety constraints (“no guarantees,” “defer to compliance,” <100 words) reduced risky language and kept outputs focused.
A small, stable evaluation set was enough to expose failure modes and verify improvements quickly.
HW2 — Jin Zhang

Overview

Workflow: Draft concise customer‑support replies.
User: Support representative.
Input: A customer message (plain text).
Output: A review‑ready draft under 100–120 words with clear next steps.
Why it’s valuable: Speeds up drafting while enforcing consistent tone and explicit human‑review boundaries.
Prompt iterations (used by the app)

initial — concise assistant + rubric; acknowledges issue; may ask one clarifying question; never makes legal/policy guarantees; <120 words; ends with a clear next step.
r1 (Revision 1) — professional and empathetic senior agent; first‑sentence acknowledgment; warm language; numbered next steps; strict <120 words; offer a replacement for the broken‑product case.
r2 (Revision 2) — helpful, professional, and polite; standard handling for data requests; <100 words for clarity and safety.
Requirements

Python 3.10+
Package: google-generativeai
Install: pip install google-generativeai
API key

Environment variable: GOOGLE_API_KEY
Windows (PowerShell): setx GOOGLE_API_KEY "your_key_here"
macOS/Linux (bash/zsh): export GOOGLE_API_KEY=your_key_here
How to run

Single case
python app.py --case 5 --version r2 --model gemini-2.5-flash

Options

--case: 1..5 (uses the built‑in evaluation set in app.py)
--input: Optional free text to override the case content
--version: initial | r1 | r2
--model: Gemini model name (default in code: gemini-1.5-flash)
What happens

The system prompt is loaded from prompts.md (sections “Initial version (Baseline)”, “Revision 1”, “Revision 2”).
The app builds a full prompt, calls the Gemini model once, prints metadata, and saves the output to outputs/.
Output filename pattern: outputs/gem-<model>-v-<version>-case<case>-YYYYMMDD-HHMMSS.txt
Run all cases for one prompt version


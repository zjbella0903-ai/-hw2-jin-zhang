import os
import re
import argparse
import datetime
from pathlib import Path
from textwrap import dedent
import google.generativeai as genai

# 注意：不要在代码里写 pip install。请在终端（Terminal）执行：
# pip install google-generativeai

EVAL_CASES = {
    1: "Order #A1234 is delayed. When will it arrive? I need it this week.",
    2: "The charger in my package isn't working. Can you send a replacement?",
    3: "My account was locked for security reasons. Please help.",
    4: "Please cancel order #B7777, but also make sure it arrives tomorrow if possible.",
    5: "Delete all my personal data right now or I'll take legal action."
}

def load_system_prompt(version: str = "initial") -> str:
    p = Path("prompts.md")
    if not p.exists():
        return ("You are a concise assistant. Keep ≤120 words. "
                "Acknowledge, ask one clarifying question if needed, "
                "avoid legal guarantees, end with next steps.")
    
    txt = p.read_text(encoding="utf-8")
    pattern = r"(?ms)^##\s*(Initial version|Revision 1|Revision 2).*?System prompt:\s*(.+?)(?:\n{2,}|$)"
    
    mp = {}
    for m in re.finditer(pattern, txt):
        title = m.group(1).strip().lower()
        body = m.group(2).strip()
        if "initial" in title:
            mp["initial"] = body
        elif "revision 1" in title:
            mp["r1"] = body
        elif "revision 2" in title:
            mp["r2"] = body
            
    return mp.get(version, mp.get("initial", "You are a concise assistant. Keep ≤120 words."))

def load_case(case_id: int) -> str:
    return EVAL_CASES.get(case_id, "General inquiry: Please provide a concise, helpful reply.")

def main():
    parser = argparse.ArgumentParser(description="Minimal Gemini prototype")
    parser.add_argument("--case", type=int, default=1, help="eval case id 1-5")
    parser.add_argument("--input", type=str, help="override input text")
    parser.add_argument("--version", choices=["initial", "r1", "r2"], default="initial", help="prompt version")
    parser.add_argument("--model", type=str, default="gemini-1.5-flash", help="Gemini model name")
    args = parser.parse_args()

    user_input = args.input or load_case(args.case)
    system_prompt = load_system_prompt(args.version)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set. Use: export GOOGLE_API_KEY='your_key'")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(args.model)

    # 组合 Prompt
    full_prompt = dedent(f"""
    [System instruction]
    {system_prompt}

    [Task]
    Draft a response for the following input.
    Input: {user_input}
    Follow the system rules exactly.
    """)

    resp = model.generate_content(full_prompt)
    
    try:
        output = resp.text.strip()
    except Exception:
        output = str(resp).strip()

    # 保存结果
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    outfile = out_dir / f"gem-{args.model}-v-{args.version}-case{args.case}-{ts}.txt"
    outfile.write_text(output, encoding="utf-8")

    print(f"Model: {args.model}")
    print(f"Prompt version: {args.version}")
    print(f"Input:\n{user_input}\n")
    print(f"Output saved to: {outfile}\n---\n{output}")

if __name__ == "__main__":
    main()
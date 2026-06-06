import google.generativeai as genai
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Initialize clients
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")
mongo = MongoClient(os.getenv("MONGODB_URI"))
db = mongo["matchday"]

SYSTEM_PROMPT = """You are MatchDay AI, an expert World Cup 2026 assistant. You help fans plan their match-day experience.

You have access to real World Cup 2026 data including:
- Match schedules with dates, times, venues and cities
- Team information and groups
- Venue details and capacities
- Ticket prices

When a fan asks about matches, teams, or trip planning:
1. Give specific, accurate information from the data provided
2. For trip planning, suggest hotels, transport, and what to pack
3. Always mention ticket prices when relevant
4. Be enthusiastic and excited about the World Cup
5. If asked about a specific team, find ALL their matches
6. Keep responses clear and well organized

Always end with an encouraging note for the fan's World Cup experience."""

def get_match_data(query):
    query_lower = query.lower()
    
    # Search matches by team name
    matches = list(db.matches.find({
        "$or": [
            {"home_team": {"$regex": query_lower, "$options": "i"}},
            {"away_team": {"$regex": query_lower, "$options": "i"}},
            {"city": {"$regex": query_lower, "$options": "i"}},
            {"venue": {"$regex": query_lower, "$options": "i"}},
            {"stage": {"$regex": query_lower, "$options": "i"}}
        ]
    }, {"_id": 0}))
    
    # Also get all matches if asking general questions
    if not matches or any(word in query_lower for word in ["all", "schedule", "fixtures", "games"]):
        matches = list(db.matches.find({}, {"_id": 0}))
    
    return matches

def get_venue_data(query):
    query_lower = query.lower()
    venues = list(db.venues.find({
        "$or": [
            {"name": {"$regex": query_lower, "$options": "i"}},
            {"city": {"$regex": query_lower, "$options": "i"}},
            {"country": {"$regex": query_lower, "$options": "i"}}
        ]
    }, {"_id": 0}))
    return venues

def get_team_data(query):
    query_lower = query.lower()
    teams = list(db.teams.find({
        "$or": [
            {"name": {"$regex": query_lower, "$options": "i"}},
            {"confederation": {"$regex": query_lower, "$options": "i"}},
            {"group": {"$regex": query_lower, "$options": "i"}}
        ]
    }, {"_id": 0}))
    return teams

def save_fan_preference(fan_name, team, city):
    db.fans.update_one(
        {"fan_name": fan_name},
        {"$set": {"team": team, "city": city}},
        upsert=True
    )

def chat_with_matchday(message, history):
    # Get relevant data from MongoDB
    matches = get_match_data(message)
    venues = get_venue_data(message)
    teams = get_team_data(message)
    
    # Build context from MongoDB data
    context = f"""
RELEVANT MATCH DATA FROM DATABASE:
{json.dumps(matches, indent=2) if matches else "No specific matches found"}

RELEVANT VENUE DATA:
{json.dumps(venues, indent=2) if venues else "No specific venues found"}

RELEVANT TEAM DATA:
{json.dumps(teams, indent=2) if teams else "No specific teams found"}
"""
    
    # Build conversation history
    full_prompt = SYSTEM_PROMPT + "\n\n" + context + "\n\n"
    for turn in history[-8:]:
        role = "Fan" if turn["role"] == "user" else "MatchDay AI"
        full_prompt += f"{role}: {turn['content']}\n"
    full_prompt += f"Fan: {message}\nMatchDay AI:"
    
    try:
        response = model.generate_content(full_prompt)
        reply = response.text
    except Exception as e:
        reply = f"Sorry, I ran into an error: {str(e)}"
    
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply})
    return "", history
def clear_chat():
    return []

css = (
    "@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');"
    "body, .gradio-container { background: #0a1628 !important; font-family: 'DM Sans', sans-serif !important; }"
    "h1, h2, h3 { font-family: 'DM Serif Display', serif !important; color: #ffffff !important; }"
    "label, p, span { color: #ccddff !important; }"
    "button.primary { background: #c8102e !important; border: none !important; border-radius: 10px !important; font-weight: 500 !important; color: white !important; }"
    "button.primary:hover { background: #a00d24 !important; }"
    "button.secondary { background: #1a2d4d !important; color: #ccddff !important; border: 1px solid #2a4d7d !important; border-radius: 10px !important; }"
)

with gr.Blocks(title="MatchDay AI") as app:
    gr.Markdown("""
# ⚽ MatchDay AI
### Your World Cup 2026 Trip Planning Assistant
*Powered by Gemini + MongoDB — Find matches, plan trips, experience the World Cup*
""")

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="Chat with MatchDay AI",
                height=500
            )
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Ask me anything... e.g. 'When does Nigeria play?' or 'Plan my trip to Dallas'",
                    label="Your question",
                    scale=4
                )
                send_btn = gr.Button("Send", variant="primary", scale=1)

        with gr.Column(scale=1):
            gr.Markdown("### Quick Questions")
            gr.Markdown(
                "Try asking:\n"
                "- When does Nigeria play?\n"
                "- Show me all matches in Dallas\n"
                "- Plan my trip to see Brazil vs Argentina\n"
                "- What are the quarter final matches?\n"
                "- Which venues are in the USA?\n"
                "- Show me the full schedule"
            )
            gr.Markdown("---")
            gr.Markdown("### About")
            gr.Markdown(
                "MatchDay AI uses real World Cup 2026 data "
                "stored in MongoDB and Gemini AI to help you "
                "plan the perfect match-day experience."
            )
            clear_btn = gr.Button("Clear chat", variant="secondary")

    gr.Markdown("*MatchDay AI — Built for the Google Cloud Rapid Agent Hackathon 2026*")

    send_btn.click(
        chat_with_matchday,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    )
    msg.submit(
        chat_with_matchday,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    )
    clear_btn.click(clear_chat, outputs=[chatbot])

app.launch(
    theme=gr.themes.Base()
)
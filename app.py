import gradio as gr
from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel
import os

my_token = os.environ.get("HF_TOKEN")

model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-3B-Instruct",
    token=my_token
) 

search_tool = DuckDuckGoSearchTool()
agent = CodeAgent(tools=[search_tool], model=model)

# 2. The Custom Agent Logic
def plan_route(start_city, destination_city):
    prompt = (
        f"I am planning a road trip from {start_city} to {destination_city}. "
        "Please use the web search tool to find the most scenic route between these two locations. "
        "Also, search for the current weather conditions for this route. "
        "Finally, write a structured Markdown report including: "
        "1. The recommended route and drive time. "
        "2. Two cool scenic stops along the way. "
        "3. A brief weather forecast and packing recommendation (e.g., rain gear, warm layers)."
    )
    
    # Send the combined prompt to the agent
    result = agent.run(prompt, max_steps=5)
    return result

# 3. The Custom UI
demo = gr.Interface(
    fn=plan_route, 
    inputs=[
        gr.Textbox(label="Starting City", placeholder="e.g., Bangalore"),
        gr.Textbox(label="Destination", placeholder="e.g., Ooty")
    ],
    outputs=gr.Markdown(label="Your Scenic Itinerary"), 
    title="🏔️ Scenic Route & Weather Advisor",
    description="Enter your starting point and destination. The AI agent will research the best roads, check the weather, and build your packing list."
    # We removed the 'allow_flagging' command here so it works perfectly with the newest Gradio!
)

if __name__ == "__main__":
    demo.launch()

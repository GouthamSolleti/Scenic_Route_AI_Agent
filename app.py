import gradio as gr
from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel, tool
import os


my_token = os.environ.get("HF_TOKEN")

model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-3B-Instruct",
    token=my_token
) 

@tool
def calculate_fuel_cost(distance_km: float, mileage_kmpl: float, fuel_price: float) -> str:
    """Calculates the estimated fuel cost for a road trip.
    
    Args:
        distance_km: The total distance of the road trip in kilometers.
        mileage_kmpl: The vehicle's fuel efficiency (kilometers per liter).
        fuel_price: The current price of fuel per liter.
    """
    liters_needed = distance_km / mileage_kmpl
    total_cost = liters_needed * fuel_price
    return f"The estimated fuel cost for the trip is ₹{round(total_cost, 2)}."

search_tool = DuckDuckGoSearchTool()
agent = CodeAgent(tools=[search_tool, calculate_fuel_cost], model=model, max_steps=6)

# 2. The Custom Agent Logic
def plan_trip(start, destination, mileage, progress=gr.Progress()):
    # 1. Trigger the Gradio loading UI immediately
    progress(0, desc="🤖 Agent is building the plan... checking routes and doing math (takes 15-30s)")

    yield "### 🤖 The Agent has been deployed!\n\n*It is currently searching the web, locking in routes, and calculating fuel costs. This takes about 15-30 seconds. Please do not refresh the page...*"
    
    structured_prompt = f"""You are an autonomous travel planner. Plan a scenic road trip from {start} to {destination}.
    
    CRITICAL ORDER OF OPERATIONS:
    1. ROUTE FIRST: Search the web for "best scenic road trip route from {start} to {destination}". You MUST find the names of the highways, 2 or 3 specific towns to stop at, and the EXACT driving distance in kilometers.
    2. LOCK IN THE DISTANCE: Save that exact distance. Do not search for the distance again.
    3. FUEL PRICE: Search for the current petrol/fuel price in {start}.
    4. CALCULATE: Use your `calculate_fuel_cost` tool using the EXACT distance from Step 1, the fuel price from Step 3, and the user's car mileage of {mileage} km/l.
    5. WEATHER: Check the current weather in {destination}.
    
    CRITICAL INSTRUCTIONS FOR FINAL OUTPUT:
    Format your final response EXACTLY according to the Markdown template below. Fill in every single bullet point.
    Do NOT output your internal thoughts, Python code, or tool execution steps in the final response. Just the template.
    
    # 🚗 Road Trip Itinerary: {start} to {destination}
    
    ## 🗺️ Recommended Scenic Route
    * **The Route:** [Name the specific highways or roads to take]
    * **Why this route?:** [Explain exactly why this route is highly recommended or scenic based on your web search]
    * **Must-See Stops:** [Name 2 or 3 specific towns or landmarks to stop at]
    * **Total Distance:** [Insert EXACT distance in km here]
    
    ## ⛽ Fuel Estimate
    [Insert the exact text output of your calculate_fuel_cost tool here]
    
    ## 🌤️ Weather Conditions
    [Insert the current weather and temperature for the destination here]
    """
    # Send the combined prompt to the agent
    final_answer= agent.run(structured_prompt)
    yield final_answer
    

# 3. The Custom UI
demo = gr.Interface(
    fn=plan_trip, 
    inputs=[
        gr.Textbox(label="Starting City", placeholder="e.g., Bangalore"),
        gr.Textbox(label="Destination", placeholder="e.g., Ooty"),
        gr.Number(label="Car Mileage (km/l)", value=15)
    ],
    outputs=gr.Markdown(label="Your Scenic Itinerary"), 
    title="🏔️ Scenic Route & Weather Advisor",
    description="Enter your starting point and destination. The AI agent will research the best roads, check the weather, and build your packing list."
    # We removed the 'allow_flagging' command here so it works perfectly with the newest Gradio!
)

if __name__ == "__main__":
    demo.queue().launch()

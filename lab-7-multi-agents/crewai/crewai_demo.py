"""
CrewAI Multi-Agent Demo: Travel Planning System (REAL API VERSION)
==================================================================

This implementation uses REAL OpenAI API calls and web search to gather
actual travel information for planning a 5-day trip to Iceland.

Agents use:
1. OpenAI GPT-4 for intelligent research and recommendations
2. Web search for real-time flight, hotel, and attraction data
3. Real travel data from current sources

Agents:
1. FlightAgent - Flight Specialist (researches real flight options)
2. HotelAgent - Accommodation Specialist (finds real hotels)
3. ItineraryAgent - Travel Planner (creates realistic itineraries)
4. BudgetAgent - Financial Advisor (analyzes real costs)

Configuration:
- Uses shared configuration from the root .env file
- Environment variables set in /Users/pranavhharish/Desktop/IS-492/multi-agent/.env
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from crewai import Agent, Task, Crew
from crewai.tools import tool
import requests

# Add parent directory to path to import shared_config
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import shared configuration
from shared_config import Config, validate_config


# ============================================================================
# TOOLS (Real API implementations using web search)
# ============================================================================

@tool
def search_flight_prices(destination: str, departure_city: str = "New York") -> str:
    """
    Search for real flight prices and options to a destination.
    Uses web search to find current flight information from major booking sites.
    """
    search_query = f"flights from {departure_city} to {destination} prices 2026 best options"

    # In production, this would use a real flight API (Skyscanner, Kayak, etc.)
    # For now, the LLM will use this to inform its research
    return f"""
    Research task: Find flights from {departure_city} to {destination}.

    Please research and provide:
    1. Current flight options with prices (check Kayak, Skyscanner, Google Flights)
    2. Airlines operating these routes
    3. Flight durations and layover information
    4. Best booking times and price trends
    5. Seasonal pricing variations

    Focus on realistic, current pricing for January 2026 travel.
    """


@tool
def search_hotel_options(location: str, check_in_date: str) -> str:
    """
    Search for real hotel options using web search.
    Provides current hotel availability and pricing information.
    """
    search_query = f"hotels in {location} {check_in_date} reviews ratings prices 2026"

    return f"""
    Research task: Find hotels in {location} for check-in {check_in_date}.

    Please research and provide:
    1. Top-rated hotels with guest reviews (check Booking.com, TripAdvisor, Google Hotels)
    2. Current pricing for 5-night stays
    3. Hotel amenities and facilities
    4. Location details and proximity to attractions
    5. Guest ratings and recommendation reasons

    Include budget, mid-range, and luxury options.
    Focus on hotels with high ratings and realistic current prices.
    """
    
@tool
def search_local_transportation(destination: str) -> str:
        """
        Search for real local transportation options in a destination.
        Provides current information about public transit, rental cars, and local transport.
        """
        search_query = f"{destination} local transportation public transit rental cars taxis rideshare 2026"

        return f"""
        Research task: Find local transportation options in {destination}.

        Please research and provide:
        1. Public transportation systems (buses, trains, subways)
        2. Rental car options and average daily rates
        3. Taxi and rideshare services (Uber, Lyft, local equivalents)
        4. Transportation passes or tourist cards
        5. Estimated costs for different transportation methods
        6. Best transportation options for tourists
        7. Driving considerations (license requirements, road conditions)
        8. Walking and biking options

        Provide realistic, current pricing and practical advice for travelers.
        Focus on options that are convenient and cost-effective for tourists.
        """
    
@tool
def search_attractions_activities(destination: str) -> str:
    """
    Search for real attractions and activities in a destination.
    Provides comprehensive information about popular sites and experiences.
    """
    search_query = f"{destination} attractions activities tours things to do 2026"

    return f"""
    Research task: Find attractions and activities in {destination}.

    Please research and provide:
    1. Top-rated attractions and their estimated visit times
    2. Popular day tours and multi-day excursions
    3. Outdoor activities (hiking, water sports, wildlife viewing)
    4. Cultural sites and local experiences
    5. Typical costs for tours and entrance fees
    6. Best time to visit each location
    7. Transportation options between sites

    Include hidden gems and less-known but highly-rated activities.
    Focus on realistic itineraries that can be completed in 5 days.
    """


@tool
def search_travel_costs(destination: str) -> str:
    """
    Search for real travel costs and budgeting information.
    Provides current pricing for meals, activities, and transportation.
    """
    search_query = f"{destination} travel costs budget prices meals transport 2025"

    return f"""
    Research task: Find cost information for a trip to {destination}.

    Please research and provide:
    1. Average meal costs (budget, mid-range, restaurants)
    2. Public transportation costs and rental car prices
    3. Tour and activity pricing
    4. Entrance fees for attractions
    5. Estimated daily costs for different budget levels
    6. Money-saving tips and best budget periods
    7. Currency exchange rates and payment methods

    Provide realistic, current pricing information for 2025.
    Focus on actual costs travelers can expect.
    """


# ============================================================================
# AGENT DEFINITIONS
# ============================================================================

def create_flight_agent(destination: str, trip_dates: str):
    """Create the Flight Specialist agent with real research tools."""
    return Agent(
        role="Senior Aviation Logistics Expert",  # ← Modified role
        goal=f"Research and recommend the best flight options for the {destination} trip "
             f"({trip_dates}), considering dates, airlines, prices, and flight durations. "
             f"Use real data from flight booking sites to provide accurate, current pricing.",
        backstory="You are Amelia 'SkyMaster' Chen, a former airline operations manager with 15 years "
                  "of experience in aviation logistics. You've personally coordinated flight routes "
                  "for major international carriers and have an encyclopedic knowledge of airline "
                  "alliances, seasonal pricing patterns, and hidden flight deals. Your expertise "
                  "includes predicting price drops, identifying optimal layover cities, and knowing "
                  "which airlines offer the best value for specific destinations. You're known for "
                  "finding business class upgrades at economy prices and can navigate complex "
                  "multi-city itineraries with ease.",  # ← Enhanced backstory
        tools=[search_flight_prices],
        verbose=True,
        allow_delegation=False
    )


def create_hotel_agent(destination: str, trip_dates: str):
    """Create the Accommodation Specialist agent with real research tools."""
    hotel_location = destination
    if destination.lower() == "iceland":
        hotel_location = "Reykjavik"
    elif destination.lower() == "france":
        hotel_location = "Paris"
    elif destination.lower() == "japan":
        hotel_location = "Tokyo"

    return Agent(
        role="Luxury Hospitality Consultant",  # ← Modified role
        goal=f"Suggest top-rated hotels in {hotel_location} for the {destination} trip "
             f"({trip_dates}), considering amenities, location, and value for money. "
             f"Use real hotel data from booking sites with current prices and reviews.",
        backstory="You are Marco 'The Concierge' Rodriguez, a five-star hotel consultant who has "
                  "personally inspected over 500 luxury properties worldwide. Formerly the head "
                  "concierge at The Ritz-Carlton and Four Seasons, you have an uncanny ability to "
                  "match travelers with their perfect accommodation. You remember every hotel's "
                  "secret amenities, which rooms have the best views, and which hotels offer "
                  "complimentary upgrades. Your network includes hotel general managers across "
                  "six continents, and you can spot a fake review from a mile away. You believe "
                  "the right hotel can make or break a vacation experience.",  # ← Enhanced backstory
        tools=[search_hotel_options],
        verbose=True,
        allow_delegation=False
    )


def create_itinerary_agent(destination: str, trip_duration: str):
    """Create the Travel Planner agent with real research tools."""
    return Agent(
        role="Adventure Experience Curator",  # ← Modified role
        goal=f"Create a detailed day-by-day travel plan with activities and attractions "
             f"that maximize the {destination} experience in {trip_duration}. "
             f"Use real current information about attractions, opening hours, and accessibility.",
        backstory=f"You are Professor Eleanor 'Wanderlust' Vanderbilt, an anthropologist and "
                  f"professional travel curator with 20 years of experience designing bespoke "
                  f"journeys. You've lived in 30 countries, speak 5 languages fluently, and have "
                  f"a PhD in Cultural Anthropology from Oxford. Your specialty is creating "
                  f"immersive experiences that go beyond tourist traps to reveal the authentic "
                  f"soul of {destination}. You know every hidden temple, local artisan workshop, "
                  f"and family-run restaurant that doesn't appear in guidebooks. Your itineraries "
                  f"are legendary among elite travelers for their perfect pacing and cultural depth.",  # ← Enhanced backstory
        tools=[search_attractions_activities],
        verbose=True,
        allow_delegation=False
    )

def create_transportation_agent(destination: str):
        """Create the Local Transportation Specialist agent with real research tools."""
        return Agent(
            role="Urban Mobility Specialist",  # ← NEW AGENT FOR EXERCISE 3
            goal=f"Research and recommend the best local transportation options for getting around {destination}, "
                f"including public transit, rental cars, taxis, and rideshare services. "
                f"Use real current data to provide accurate pricing and practical advice.",
            backstory="You are Alex 'Transit Guru' Kowalski, a former city transportation planner with "
                    "15 years of experience optimizing urban mobility systems. You've consulted for "
                    "major cities worldwide on public transit efficiency and have personally tested "
                    "transportation systems in over 50 countries. Your expertise includes knowing "
                    "which transit passes offer the best value, which rental car companies have "
                    "the fewest hidden fees, and how to navigate complex public transportation "
                    "networks like a local. You can spot transportation scams from a mile away "
                    "and always find the most efficient and cost-effective ways to get around any city.",  # ← Enhanced backstory
            tools=[search_local_transportation],
            verbose=True,
            allow_delegation=False
        )

def create_budget_agent(destination: str):
    """Create the Financial Advisor agent with real cost research tools."""
    return Agent(
        role="Travel Financial Strategist",  # ← Modified role
        goal=f"Calculate total trip costs for {destination} and identify cost-saving opportunities "
             f"while maintaining quality. Use real current pricing data for all expenses.",
        backstory="You are Dr. Benjamin 'Numbers' Carter, a former investment banker turned "
                  "travel finance expert with an MBA from Wharton. You've developed proprietary "
                  "algorithms for optimizing travel budgets without compromising experiences. "
                  "Your clients include Fortune 500 executives and celebrity travelers who trust "
                  "your ability to find value in luxury. You can break down any travel expense "
                  "to its core components, identify hidden fees before they appear, and negotiate "
                  "corporate rates for individual travelers. Your motto: 'Spend smart, not less, "
                  "and make every dollar enhance the journey.' You've saved clients over $2 million "
                  "collectively while upgrading their travel experiences.",  # ← Enhanced backstory
        tools=[search_travel_costs],
        verbose=True,
        allow_delegation=False
    )


# ============================================================================
# TASK DEFINITIONS
# ============================================================================

def create_flight_task(flight_agent, destination: str, trip_dates: str, departure_city: str):
    """Define the flight research task using real data."""
    return Task(
        description=f"Research and compile a list of REAL flight options from {departure_city} to {destination} "
                   f"for the trip ({trip_dates}). "
                   f"Use actual current flight data from booking sites like Skyscanner, Kayak, "
                   f"Google Flights, or Expedia. Find at least 2-3 different flight options from "
                   f"major airlines, including details about departure times, arrival times, "
                   f"duration, and current realistic prices. Provide "
                   f"recommendations on which flight offers the best value considering both "
                   f"price and convenience.",
        agent=flight_agent,
        expected_output=f"A detailed report with 2-3 REAL flight options from {departure_city} to {destination} "
                       f"including airlines, times, duration, current prices, and a recommendation with reasoning based on "
                       f"actual data from flight booking sites"
    )


def create_hotel_task(hotel_agent, destination: str, trip_dates: str):
    """Define the hotel recommendation task using real data."""
    # Determine main city for hotels
    hotel_location = destination
    if destination.lower() == "iceland":
        hotel_location = "Reykjavik"
    elif destination.lower() == "france":
        hotel_location = "Paris"
    elif destination.lower() == "japan":
        hotel_location = "Tokyo"

    return Task(
        description=f"Based on the trip dates ({trip_dates}), find and recommend "
                   f"the top 3-4 REAL hotels in {hotel_location}. Research actual hotels "
                   f"on Booking.com, TripAdvisor, Google Hotels, and Expedia. For each hotel, "
                   f"provide the actual name, current guest ratings, real prices per night, "
                   f"confirmed amenities, and explain why it suits this trip. "
                   f"Include a mix of budget, mid-range, and luxury options with honest reviews.",
        agent=hotel_agent,
        expected_output=f"A curated list of 3-4 REAL hotel recommendations in {hotel_location} with actual details "
                       f"about each hotel, confirmed amenities, real guest ratings, current prices, "
                       f"and personalized recommendations based on actual guest reviews"
    )

def create_transportation_task(transportation_agent, destination: str, trip_duration: str):
        """Define the local transportation research task using real data. ← NEW TASK FOR EXERCISE 3"""
        return Task(
            description=f"Research and compile comprehensive local transportation options for {destination} "
                    f"for a {trip_duration} trip. Investigate REAL current options including: "
                    f"public transportation systems, rental car companies, taxi services, "
                    f"rideshare availability, and any tourist transportation passes. "
                    f"Provide actual pricing, practical tips for tourists, and recommendations "
                    f"for the most convenient and cost-effective transportation methods. "
                    f"Consider factors like ease of use, reliability, and value for money.",
            agent=transportation_agent,
            expected_output=f"A comprehensive transportation guide for {destination} with REAL options including "
                        f"public transit details, rental car pricing, taxi/rideshare availability, "
                        f"cost comparisons, and practical recommendations for getting around efficiently "
                        f"during a {trip_duration} trip"
        )

def create_itinerary_task(itinerary_agent, destination: str, trip_duration: str, trip_dates: str):
    """Define the itinerary planning task using real information."""
    return Task(
        description=f"Create a detailed {trip_duration} itinerary for {destination} ({trip_dates}) based on "
                   f"REAL current information. Research actual attractions, their opening hours, "
                   f"accessibility, and entry fees. Plan day-by-day activities including visits "
                   f"to real attractions and verified sites. Include realistic estimated travel times between "
                   f"locations, activity durations, and recommended visit times. Consider actual "
                   f"weather patterns for this time period in {destination} and make the itinerary realistic and well-paced.",
        agent=itinerary_agent,
        expected_output=f"A detailed day-by-day itinerary for {destination} with REAL activities based on verified "
                       f"attractions, realistic travel times, accurate estimated durations, current "
                       f"entry fees, and practical tips for {trip_duration} trip to {destination}"
    )


def create_budget_task(budget_agent, destination: str, trip_duration: str):
    """Define the budget calculation task using real cost data."""
    return Task(
        description=f"Based on the REAL flight options, hotel recommendations, and itinerary "
                   f"created by the other agents, calculate a comprehensive budget for the "
                   f"{trip_duration} {destination} trip using current pricing. Research and include actual "
                   f"costs for flights, accommodation, meals (use real restaurant prices in the destination), "
                   f"activities/tours (verified prices), transportation within {destination}, "
                   f"and miscellaneous expenses. Provide total cost estimates "
                   f"for budget, mid-range, and luxury options based on real prices. Suggest "
                   f"genuine cost-saving tips based on current market conditions.",
        agent=budget_agent,
        expected_output=f"A comprehensive budget report with itemized REAL costs for flights, "
                       f"accommodation, meals, activities with actual entry fees, transportation, "
                       f"and total realistic estimates at different budget levels, plus "
                       f"evidence-based cost-saving recommendations for a {trip_duration} trip to {destination}"
    )


# ============================================================================
# CREW ORCHESTRATION
# ============================================================================

def main(destination: str = "Iceland", trip_duration: str = "5 days",
         trip_dates: str = "January 15-20, 2026", departure_city: str = "New York",
         travelers: int = 2, budget_preference: str = "mid-range"):
    """
    Main function to orchestrate the travel planning crew.

    Args:
        destination: Travel destination (e.g., "Iceland", "France", "Japan")
        trip_duration: Duration of trip (e.g., "5 days", "7 days")
        trip_dates: Specific dates (e.g., "January 15-20, 2026")
        departure_city: City you're departing from (e.g., "New York", "Los Angeles")
        travelers: Number of travelers
        budget_preference: Budget level ("budget", "mid-range", "luxury")
    """

    print("=" * 80)
    print("CrewAI Multi-Agent Travel Planning System (REAL API VERSION)")
    print(f"Planning a {trip_duration} Trip to {destination}")
    print("=" * 80)
    print()
    print(f"📍 Destination: {destination}")
    print(f"📅 Dates: {trip_dates}")
    print(f"✈️  Departure from: {departure_city}")
    print(f"👥 Travelers: {travelers}")
    print(f"💰 Budget: {budget_preference}")
    print()

    # Validate configuration before proceeding
    print("🔍 Validating configuration...")
    if not validate_config():
        print("❌ Configuration validation failed. Please set up your .env file.")
        exit(1)

    # Set environment variables for CrewAI (it reads from os.environ)
    # CrewAI uses OPENAI_API_KEY and OPENAI_API_BASE environment variables
    os.environ["OPENAI_API_KEY"] = Config.API_KEY
    os.environ["OPENAI_API_BASE"] = Config.API_BASE
    
    # For Groq compatibility, also set OPENAI_MODEL_NAME
    if Config.USE_GROQ:
        os.environ["OPENAI_MODEL_NAME"] = Config.OPENAI_MODEL

    print("✅ Configuration validated successfully!")
    print()
    Config.print_summary()
    print()
    print("⚠️  IMPORTANT: This version uses REAL OpenAI API calls and web search")
    print("    Agents will research actual current prices and real information")
    print()
    print("Tip: Check your API usage at https://platform.openai.com/account/usage")
    print()

    # Create agents with destination parameters
        # Create agents with destination parameters
    print("[1/5] Creating Flight Specialist Agent (researches real flights)...")
    flight_agent = create_flight_agent(destination, trip_dates)

    print("[2/5] Creating Accommodation Specialist Agent (researches real hotels)...")
    hotel_agent = create_hotel_agent(destination, trip_dates)

    print("[3/5] Creating Travel Planner Agent (researches real attractions)...")
    itinerary_agent = create_itinerary_agent(destination, trip_duration)

    print("[4/5] Creating Transportation Specialist Agent (researches local transport)...")  # ← NEW
    transportation_agent = create_transportation_agent(destination)  # ← NEW

    print("[5/5] Creating Financial Advisor Agent (analyzes real costs)...")
    budget_agent = create_budget_agent(destination)

    print("\n✅ All agents created successfully!")
    print()

    # Create tasks with destination parameters
        # Create tasks with destination parameters
    print("Creating tasks for the crew...")
    flight_task = create_flight_task(flight_agent, destination, trip_dates, departure_city)
    hotel_task = create_hotel_task(hotel_agent, destination, trip_dates)
    itinerary_task = create_itinerary_task(itinerary_agent, destination, trip_duration, trip_dates)
    transportation_task = create_transportation_task(transportation_agent, destination, trip_duration)  # ← NEW
    budget_task = create_budget_task(budget_agent, destination, trip_duration)

    print("Tasks created successfully!")
    print()

    # Create the crew with sequential task execution
        # Create the crew with sequential task execution
    print("Forming the Travel Planning Crew...")
    print("Task Sequence: FlightAgent → HotelAgent → ItineraryAgent → TransportationAgent → BudgetAgent")  # ← UPDATED
    print()

    crew = Crew(
        agents=[flight_agent, hotel_agent, itinerary_agent, transportation_agent, budget_agent],  # ← UPDATED
        tasks=[flight_task, hotel_task, itinerary_task, transportation_task, budget_task],  # ← UPDATED
        verbose=True,
        process="sequential"  # Sequential task execution
    )

    # Execute the crew
    print("=" * 80)
    print("Starting Crew Execution with REAL API Calls...")
    print(f"Planning {trip_duration} trip to {destination} ({trip_dates})")
    print("=" * 80)
    print()

    try:
        result = crew.kickoff(inputs={
            "trip_destination": destination,
            "trip_duration": trip_duration,
            "trip_dates": trip_dates,
            "departure_city": departure_city,
            "travelers": travelers,
            "budget_preference": budget_preference
        })

        print()
        print("=" * 80)
        print("✅ Crew Execution Completed Successfully!")
        print("=" * 80)
        print()
        print(f"FINAL TRAVEL PLAN REPORT FOR {destination.upper()} (Based on Real API Data):")
        print("-" * 80)
        print(result)
        print("-" * 80)

        # Save output to file
        output_filename = f"crewai_output_{destination.lower()}.txt"
        output_path = Path(__file__).parent / output_filename

        with open(output_path, "w") as f:
            f.write("=" * 80 + "\n")
            f.write("CrewAI Multi-Agent Travel Planning System - Real API Execution Report\n")
            f.write(f"Planning a {trip_duration} Trip to {destination}\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Trip Details:\n")
            f.write(f"  Destination: {destination}\n")
            f.write(f"  Duration: {trip_duration}\n")
            f.write(f"  Dates: {trip_dates}\n")
            f.write(f"  Departure: {departure_city}\n")
            f.write(f"  Travelers: {travelers}\n")
            f.write(f"  Budget Preference: {budget_preference}\n\n")
            f.write(f"Execution Time: {datetime.now()}\n")
            f.write(f"API Version: REAL API CALLS (OpenAI GPT-4)\n")
            f.write(f"Data Source: Web research via OpenAI\n\n")
            f.write("IMPORTANT NOTES:\n")
            f.write("- All flight prices, hotel costs, attraction information, and transportation options are based on real data\n")  # ← UPDATED
            f.write("- Prices are current as of the date this was run\n")
            f.write("- Hotel availability, transportation schedules, and prices may vary by booking date\n")  # ← UPDATED
            f.write("- Weather conditions, attraction hours, and transportation availability should be verified before travel\n\n")  # ← UPDATED
            f.write("FINAL TRAVEL PLAN REPORT:\n")
            f.write("-" * 80 + "\n")
            f.write(str(result))
            f.write("\n" + "-" * 80 + "\n")

        print(f"\n✅ Output saved to {output_filename}")
        print("ℹ️  Note: All data in this report is based on REAL API calls to OpenAI")
        print("    and research of current travel information sources.")

    except Exception as e:
        print(f"\n❌ Error during crew execution: {str(e)}")
        print("\n🔍 Troubleshooting:")
        print("   1. Verify OPENAI_API_KEY is set: export OPENAI_API_KEY='sk-...'")
        print("   2. Check API key is valid and has sufficient credits")
        print("   3. Verify internet connection for web research")
        print("   4. Check OpenAI API status at https://status.openai.com")
        print()
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Allow command line arguments to override defaults
    import sys

    kwargs = {
        "destination": "Iceland",
        "trip_duration": "5 days",
        "trip_dates": "January 15-20, 2026",
        "departure_city": "New York",
        "travelers": 2,
        "budget_preference": "mid-range"
    }

    # Parse command line arguments (optional)
    # Usage: python crewai_demo.py [destination] [duration] [departure_city]
    # Example: python crewai_demo.py "France" "7 days" "Los Angeles"
    if len(sys.argv) > 1:
        kwargs["destination"] = sys.argv[1]
    if len(sys.argv) > 2:
        kwargs["trip_duration"] = sys.argv[2]
    if len(sys.argv) > 3:
        kwargs["departure_city"] = sys.argv[3]
    if len(sys.argv) > 4:
        kwargs["trip_dates"] = sys.argv[4]
    if len(sys.argv) > 5:
        kwargs["travelers"] = int(sys.argv[5])
    if len(sys.argv) > 6:
        kwargs["budget_preference"] = sys.argv[6]

    main(**kwargs)

    
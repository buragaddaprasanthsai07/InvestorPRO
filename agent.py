from google import genai
from google.genai import types
from tools import (
    get_stock_fundamentals,
    get_recent_news,
    compare_performance,
    analyze_dividend_potential,
    assess_risk_profile,
    analyze_growth_metrics,
    analyze_insider_activity,
    valuation_snapshot,
    calculate_quality_score,
    estimate_price_target
)
import streamlit as st
# ⚠️ REPLACE WITH YOUR API KEY
api_key = st.secrets["google"]["api_key"]
client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTION = """
You are an elite financial analyst and investment advisor. You have access to 10 advanced analysis tools.

Your role:
1. Use multiple tools to gather comprehensive data
2. Synthesize data into actionable insights
3. Provide clear buy/hold/sell recommendations
4. Identify risks and opportunities
5. Explain metrics in simple terms
6. Be balanced but decisive

Analysis Structure:
- Executive Summary (1-2 sentences)
- Key Strengths (3-5 points)
- Key Risks (3-5 points)
- Valuation Assessment
- Risk/Reward Profile
- Final Recommendation with Conviction Level (1-10)
"""

def run_financial_analysis(ticker: str, user_query: str = None) -> str:
    """
    Premium financial analysis using 10 advanced tools
    """
    
    available_tools = [
        get_stock_fundamentals,
        get_recent_news,
        compare_performance,
        analyze_dividend_potential,
        assess_risk_profile,
        analyze_growth_metrics,
        analyze_insider_activity,
        valuation_snapshot,
        calculate_quality_score,
        estimate_price_target
    ]
    
    tool_map = {f.__name__: f for f in available_tools}
    
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[types.Tool(function_declarations=[
            types.FunctionDeclaration(
                name=f.__name__,
                description=f.__doc__ or f"Analyze {f.__name__}",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "ticker": types.Schema(type=types.Type.STRING, description="Stock ticker")
                    },
                    required=["ticker"]
                )
            ) for f in available_tools
        ])],
        temperature=0.2
    )
    
    if user_query:
        prompt = f"Analyze {ticker}. User asked: {user_query}"
    else:
        prompt = f"Perform comprehensive analysis of {ticker}. Use all 10 tools. Provide buy/hold/sell recommendation."
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=config
        )
        
        if response.function_calls:
            tool_responses = []
            
            for call in response.function_calls:
                tool_name = call.name
                args = call.args
                
                if tool_name in tool_map:
                    try:
                        tool_output = tool_map[tool_name](**args)
                        tool_responses.append(
                            types.Part.from_function_response(
                                name=tool_name,
                                response={"result": tool_output}
                            )
                        )
                    except Exception as e:
                        tool_responses.append(
                            types.Part.from_function_response(
                                name=tool_name,
                                response={"error": str(e)}
                            )
                        )
            
            final_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    types.Part.from_text(text=prompt),
                    response.candidates[0].content,
                    *tool_responses
                ],
                config=config
            )
            
            return final_response.text
        
        return response.text
    
    except Exception as e:
        return f"Analysis error: {str(e)}"

from dotenv import load_dotenv
import os
from langchain_core.tools import tool
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
import streamlit as st



load_dotenv()


# Access the environment variables
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')


@tool
def calculator(expression: str) -> float:
    """
    Evaluate a mathematical expression and return the result.

    Parameters:
    expression (str): A string containing the mathematical expression to evaluate.

    Returns:
    float: The result of the evaluated expression.

    Examples:
    >>> evaluate_expression("2 + 3 * 4")
    14.0
    >>> evaluate_expression("(10 / 2) + 8")
    13.0

    Note:
    - This function uses Python's `eval()` to calculate the result.
    - Ensure the input is sanitized to avoid malicious code execution.
    """
    try:
        # Evaluate the expression safely
        result = eval(expression, {"__builtins__": {}})
        return float(result)
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        return None


@tool
def get_stock_price(symbol: str) -> str:
    """Fetches the current stock price of a company based on its stock symbol using the Polygon API.

    Args:
        symbol (str): The stock symbol of the company (e.g., 'AAPL' for Apple, 'GOOGL' for Google).

    Returns:
        str: A message containing the current stock price of the company.

    Raises:
        HTTPError: If the HTTP request to the stock API fails (e.g., 404 or 500 status).
        RequestException: If there is an issue with the request itself (e.g., connection error).
        Exception: For any other unexpected errors during the execution of the function.

    """
    api_key = "2bx0DyQuypHfwohF46294_29KpFtMKzt"  # Replace this with your actual secret API key from Polygon
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/prev"  # Polygon endpoint for previous close price

    try:
        # Send a GET request with the API key
        response = requests.get(url, params={'apiKey': api_key})
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)

        # Assuming the data contains 'close' in the response for the last closing price
        data = response.json()
        price = data.get('results', [{}])[0].get('c')  # 'c' is the closing price

        if price:
            return f"Tool used: get_stock_price\n get_stock_price tool is used to find The current price of {symbol} is ${price}"
        else:
            return f"Error: Could not retrieve stock data for {symbol}.\nTool used: get_stock_price"

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}\nTool used: get_stock_price"
    except requests.exceptions.RequestException as req_err:
        return f"Request error occurred: {req_err}\nTool used: get_stock_price"
    except Exception as err:
        return f"An unexpected error occurred: {err}\nTool used: get_stock_price"


tools = [calculator,get_stock_price]

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash-exp" , api_key=GOOGLE_API_KEY)


agent = initialize_agent(tools, llm , agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION )

# Interface

import streamlit as st

# Set the title of the app
st.title("Your financial assistant🤖💬")
st.write("🤖Hello! I'm Umar's Chatbot to assist you.")

# Create a text input for user queries
user_input = st.text_input("You💬:", "")

# if user_input:
#     # Here you can integrate your AI model to generate a response
#     # For now, we will just echo back the user's input
#     # response = f"You said💬: {user_input}"

#     # Display the response
#     st.text_area("Response🤖:", response, height=150)

if st.button("Submit"):
    response = agent.invoke(user_input)
    st.write(response) 
# Additional styled section for user assistance
st.sidebar.header("Instructions")
st.sidebar.write("""Welcome to your financial assistant!😊 Whether you need to calculate
                  investment returns , assess loan payments 💰, or stay updated on the latest 
                 stock prices 📉, this chatbot has you covered! Get real-time insights 🌍, make 
                 smarter decisions 💡, and track your portfolio—all in one place. Start using 
                 it now and take control of your finances! 🚀💸""")




# st.markdown("""
#     <style>
#         .stButton>button {
#             background-color: #28a745
#         ;
#             color: white;
#             font-size: 20px;
#             border-radius: 12px;
#             padding: 10px 20px;
#             border: none;
#         }
#         .stButton>button:hover {
#             background-color: #ff4500;
#         }
#     </style>
# """, unsafe_allow_html=True)



import streamlit as st

# Custom CSS to create a colorful title
st.markdown("""
    <style>
        .big-font {
            font-size: 50px;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(90deg, #ff6347, #ffeb3b, #4caf50, #2196f3, #9c27b0);
            -webkit-background-clip: text;
            color: transparent;
        }
    </style>
""", unsafe_allow_html=True)

# Add a colorful title
import streamlit as st

# Custom CSS to create a colorful title and position it at the top
st.markdown("""
    <style>
        /* Ensure the title is at the top */
        .big-font {
            font-size: 50px;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(90deg, #ff6347, #ffeb3b, #4caf50, #2196f3, #9c27b0);
            -webkit-background-clip: text;
            color: transparent;
            padding-top: 20px;
            padding-bottom: 20px;
            margin-top: 0;
        }
        /* Optional: add some space after the title to separate from content */
        .content-space {
            padding-top: 40px;
        }
    </style>
""", unsafe_allow_html=True)

# Add the colorful title at the top
st.markdown('<p class="big-font">Welcome to my Chatbot!</p>', unsafe_allow_html=True)

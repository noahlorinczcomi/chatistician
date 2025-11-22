# function to print masthead/banner
def masthead():
    mh = """
╔══════════════════════════════════════════════════════════════╗
║           Chatistician: Rapid Statistical Advice             ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(mh)

# function to print welcome message
def welcome(name):
    welcome_msg = f"""
    Welcome, {name}!
    
    You're connected with a professional statistician.
    
    Need help with:
    - Power calculation? Just ask: "I need a power calculation"
    - Study design? Ask: "Help me design my study"  
    - Data analysis? Ask: "Can you review my analysis?"
    - Code review? Ask: "Can we review/write my data analysis code?"
    
    Type 'quit' to end session.
    """
    print(welcome_msg)

# function to print section headers
def print_section_header(title, size=78):
    print("\n" + "─" * size)
    print(f"  {title}")
    print("─" * size + "\n")

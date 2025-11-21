# function to print intro
def masthead():
    mh = """
╔══════════════════════════════════════════════════════════════╗
║           Chatistician: Rapid Statistical Consulting         ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(mh)

# function to print section headers
def print_section_header(title, size=78):
    print("\n" + "─" * size)
    print(f"  {title}")
    print("─" * size + "\n")

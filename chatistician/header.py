# function to print intro
def masthead():
    mh = """
╔══════════════════════════════════════════════════════════════╗
║           Chatistician: Quick Statistical Consult            ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(mh)

# function to print section headers
def print_section_header(title, size=78):
    print("\n" + "─" * size)
    print(f"  {title}")
    print("─" * size + "\n")

import language_tool_python

tool = language_tool_python.LanguageTool('en-US')

def check_grammar(text):
    """
    Check the grammar of the given text and return suggestions.
    
    :param text: The text to check.
    :return: A list of suggestions for grammar corrections.
    """
    matches = tool.check(text)
    suggestions = []
    
    for match in matches:
        suggestions.append({
            'message': match.message,
            'replacements': match.replacements,
            'context': match.context.strip()
        })
    
    return suggestions

# Define a set of impactful words to look for in the resume
# These words can indicate strong achievements or skills that should be highlighted.
IMPACTFUL_WORDS = {"achieved", "improved", "developed", "designed", "implemented", "led", 
                   "managed", "optimized", "streamlined", "increased", "reduced", "enhanced", 
                   "created", "initiated", "coordinated"}

def suggest_better_phrasing(text):
    """
    Suggest better phrasing that can enhance the resume.
    
    :param text: The text of the resume.
    :return: A list of suggested phrases found in the text.
    """
    suggestions = []
    lines = text.split("\n")
    for line in lines:
        if line.strip() and not any(verb in line for verb in IMPACTFUL_WORDS):
            suggestions.append(f"Try rewriting with stronger action verbs: \"{line.strip()}\"")
    return suggestions
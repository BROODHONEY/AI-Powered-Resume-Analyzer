import language_tool_python

tool = language_tool_python.LanguageTool('en-US')

def check_grammar(text):
    """
    Check the grammar of the given text using LanguageTool.

    Args:
        text (str): The text to check for grammar errors.

    Returns:
        list: A list of dictionaries containing details about each error found.
    """
    matches = tool.check(text)
    suggestions = []
    
    for match in matches:
        suggestions.append({
            "message": match.message,
            "incorrect": text[match.offset : match.offset + match.errorLength],
            "suggestions": match.replacements,
            "rule": match.ruleId,
            "context": text[max(0, match.offset - 30): match.offset + match.errorLength + 30]
        })

    return suggestions
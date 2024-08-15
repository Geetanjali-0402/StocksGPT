import re

def find_event_handlers(content):
    # Define regex patterns for onSubmit and onClick event handlers
    patterns = {
        'onSubmit': re.compile(r'onSubmit\s*=\s*\{?\s*handleSubmit\(([^})]+)\)\s*\}?'),
        'onClick': re.compile(r'onClick\s*=\s*\{?\s*([^\s({]+)\s*\}?'),
        'onSelectChat': re.compile(r'onSelectChat\s*=\s*\{?\s*([^\s({]+)\s*\}?'),
        'onNewChat': re.compile(r'onNewChat\s*=\s*\{?\s*([^\s({]+)\s*\}?'),
        'onChangeTab': re.compile(r'onChangeTab\s*=\s*\{?\s*([^\s({]+)\s*\}?'),
        'onSend': re.compile(r'onSend\s*=\s*\{?\s*([^\s({]+)\s*\}?')
    }

    handlers = {}

    for event, pattern in patterns.items():
        matches = pattern.findall(content)
        if matches:
            handlers[event] = matches

    return handlers

def find_function_dispatched_actions(content, function_name):
    # Define regex to find function bodies and dispatched actions in various function declarations
    function_patterns = [
        re.compile(rf'const\s+{function_name}\s*=\s*(?:async\s*)?\([^)]*\)\s*=>\s*{{([^}}]*)}}', re.DOTALL),
        re.compile(rf'function\s+{function_name}\s*\([^)]*\)\s*{{([^}}]*)}}', re.DOTALL),
    ]
    
    for pattern in function_patterns:
        match = pattern.search(content)
        if match:
            function_body = match.group(1)
            dispatched_actions = re.findall(r'dispatch\s*\(\s*([^\s(]+)\s*\(.*\)\s*\)', function_body)
            return dispatched_actions
    return []

def analyze_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    event_handlers = find_event_handlers(content)

    result = {}

    for event, functions in event_handlers.items():
        result[event] = {}
        for func in functions:
            function_name = func.strip('{}')

            # Find dispatched actions in the function
            dispatched_actions = find_function_dispatched_actions(content, function_name)

            result[event][func] = {
                'function_name': function_name,
                'dispatched_actions': dispatched_actions,
                'trigger_function': 'handleSubmit' if event == 'onSubmit' else 'onClick'
            }

    return result

file_path = 'D:\\dkafka\\StocksGPT\\src\\pages\\Authentication\\Login.tsx'
analysis = analyze_file(file_path)

# Print the result in the desired format
for event, functions in analysis.items():
    print(f"******* Event name: {event} *******")
    for func, details in functions.items():
        print(f" function name: {details['function_name']}")
        print(f" dispatched actions: {details['dispatched_actions']}")
        print(f" trigger function: {details['trigger_function']}")
        print()

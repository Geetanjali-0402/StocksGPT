import re
from collections import defaultdict

def extract_actions(file_path):
    actions_dict = defaultdict(set)
    action_pattern = re.compile(r'dispatch\((.*?)\)')

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            matches = action_pattern.findall(line)
            if matches:
                for match in matches:
                    action_name = match.strip()
                    actions_dict[action_name].add(file_path)

    return dict(actions_dict)

# Example usage
file_path = 'C:\\Users\\Geetanjali\\Desktop\\dkafka\\StocksGPT\\src\\pages\\Authentication\\Login.tsx'
actions = extract_actions(file_path)
for action, source_paths in actions.items():
    print(f"Action: {action}), Dispatched in: {', '.join(source_paths)}")

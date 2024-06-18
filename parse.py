import os
import re
from test import Node, NodeType
import requests

API_KEY = os.environ.get('API_KEY')

def requirementsDescription(request):
    term = request.get('term')
    subject = request.get('subject')
    catalogNumber = request.get('catalog-number')
    headers = {'x-api-key': API_KEY}
    response = requests.get('https://openapi.data.uwaterloo.ca/v3/Courses/' + 
                            str(term) + '/' + 
                            str(subject) + '/' + 
                            str(catalogNumber), headers=headers)
    if response.status_code == 200:
        return response.json()[0].get('requirementsDescription')
    else:
        return response.text


def parse_prerequisites(prereq_string: str) -> Node:
    # Remove the Antireq section
    prereq_string = re.sub(r"Antireq:.*", "", prereq_string).strip()
    
    # Extract the prerequisites part
    prereq_string = re.sub(r"^Prereq: ", "", prereq_string)
    
    # Create the root node with OR type (default for top-level prerequisites)
    root = Node(NodeType.OR)
    
    # Split prerequisites by "or" at the top level
    or_sections = [section.strip() for section in re.split(r"\s+or\s+", prereq_string)]
    
    for section in or_sections:
        if 'and' in section:
            and_node = Node(NodeType.AND)
            # Split by "and" and add children nodes
            for sub_section in section.split('and'):
                and_node.children.append(Node(NodeType.OR, courseId=sub_section.strip()))
            root.children.append(and_node)
        else:
            root.children.append(Node(NodeType.OR, courseId=section))
    
    return root

# Example usage
prereq_string = requirementsDescription({'term': 1245, 'subject': 'CS', 'catalog-number': 241})
parsed_tree = parse_prerequisites(prereq_string)

def print_tree(node: Node, level=0):
    print("  " * level + f"{node.nodeType}: {node.courseId} {node.courseTitle}")
    for child in node.children:
        print_tree(child, level + 1)

print_tree(parsed_tree)
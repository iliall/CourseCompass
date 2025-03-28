from enum import Enum
from typing import List

class NodeType(Enum):
    AND = 1
    OR = 2

class Node:

    def __init__(self, nodeType: NodeType = NodeType.OR, courseId: str = "", courseTitle: str = "OR") -> None:
        self.nodeType = nodeType
        self.courseId = courseId
        self.courseTitle = courseTitle
        self.children = []
        self.value = False

    def __str__(self) -> str:
        return f'{self.courseTitle} {self.value}'
    

    def __eq__(self, other: 'Node') -> bool:
        return self.courseId == other.courseId

    
    def add_child(self, child: 'Node') -> None:
        if child.nodeType == NodeType.AND:
            self.children.insert(0, child)
            return
        self.children.append(child)

    def get_children(self) -> List['Node']:
        return self.children
    
    def remove_child(self, child: 'Node') -> None:
        self.children.remove(child)

    def set_value(self, value: bool) -> None:
        self.value = value
    
    def get_value(self) -> bool:
        return self.value

    def min_prereqs(self) -> List['Node']:
        return find_minPrereqs([], [self])

        

# finds the minimum prerequisites needed to take all the courses in toBeProcessed
# Usage: find_minPrereqs([], [List of courses])
def find_minPrereqs(processed: List['Node'], toBeProcessed: List['Node']) -> List['Node']:
    # print(f'processed: {[node.courseTitle for node in processed]}')
    # print(f'toBeProcessed: {[node.courseTitle for node in toBeProcessed]}')
    if not toBeProcessed:
        return processed

    current = toBeProcessed.pop(0)
    if not current in processed:    
        processed.append(current)

    if current.value:
        return find_minPrereqs(processed, toBeProcessed)

    # AND node
    if current.nodeType == NodeType.AND:
        # Adds all the children of the AND node to the toBeProcessed list
        for child in current.get_children():
            if child.nodeType == NodeType.AND:
                toBeProcessed.insert(0, child)
            else:
                toBeProcessed.append(child)
        return find_minPrereqs(processed, toBeProcessed)
    
    # OR node
    else:
        # Finds the best path for the OR node by trying all the children
        min_prereqs = []
        for child in current.get_children():
            temp_toBeProcessed = toBeProcessed.copy()
            temp_processed = processed.copy()
            if child.nodeType == NodeType.AND:
                temp_toBeProcessed.insert(0, child)
            else:
                temp_toBeProcessed.append(child)
            
            temp_min_prereqs = find_minPrereqs(temp_processed, temp_toBeProcessed)
            if not min_prereqs or len(temp_min_prereqs) < len(min_prereqs):
                min_prereqs = temp_min_prereqs
        
        return min_prereqs

        

# Helper function to print the tree structure
def print_node(node: Node, level: int) -> None:
    print('  ' * level + str(node))
    for child in node.get_children():
        print_node(child, level + 1)





# Tests
root = Node(NodeType.AND, 'root', 'root')
courseNode1 = Node(NodeType.AND, 'course1', 'course1')
courseNode2 = Node(NodeType.AND, 'course2', 'course2')
courseNode3 = Node(NodeType.AND, 'course3', 'course3')
courseNode4 = Node(NodeType.AND, 'course4', 'course4')
courseNode5 = Node(NodeType.AND, 'course5', 'course5')
courseNode6 = Node(NodeType.AND, 'course6', 'course6')
courseNode7 = Node(NodeType.AND, 'course7', 'course7')
OrNode = Node(NodeType.OR)
OrNode1 = Node(NodeType.OR)
root.add_child(courseNode1)
OrNode.add_child(courseNode2)
root.add_child(OrNode)
courseNode2.add_child(courseNode5)
courseNode1.add_child(OrNode1)
OrNode1.add_child(courseNode5)
OrNode1.add_child(courseNode3)
OrNode.add_child(courseNode4)
root.add_child(courseNode7)
courseNode4.add_child(courseNode6)

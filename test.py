from collections import deque
from enum import Enum
from typing import List

class NodeType(Enum):
    AND = 1
    OR = 2

class Node:

    def __init__(self, nodeType: NodeType, courseId: str = "", courseTitle: str = "OR") -> None:
        self.nodeType = nodeType
        self.courseId = courseId
        self.courseTitle = courseTitle
        self.children = []
        self.value = False

    def __str__(self) -> str:
        return f'{self.courseTitle} {self.value}'
    
    def add_child(self, child: 'Node') -> None:
        self.children.append(child)

    def get_children(self) -> List['Node']:
        return self.children
    
    def remove_child(self, child: 'Node') -> None:
        self.children.remove(child)

    def set_value(self, value: bool) -> None:
        self.value = value
    
    def get_value(self) -> bool:
        return self.value

    def bfs(self, target: 'Node') -> List['Node']:
        queue = deque([(self, [self], 0 if self.value else 1)])  # Add a count of False values
        
        best_path = None
        best_false_count = float('inf')
        
        while queue:
            current, path, false_count = queue.popleft()
            
            if current == target:
                if false_count < best_false_count:
                    best_path = path
                    best_false_count = false_count
                continue  # Continue to check other paths
            
            for child in current.get_children():
                new_false_count = false_count + (0 if child.get_value() else 1)
                queue.append((child, path + [child], new_false_count))
        
        return best_path if best_path else []

    def min_prereqs(self) -> List['Node']:
        if self.value:
            return []

        original_value = self.value
        self.set_value(True)

        if self.nodeType == NodeType.AND:
            courses = [self]  # Include this course
        else:
            courses = []

        prereq_courses = []
        for child in self.children:
            child_prereqs = child.min_prereqs()
            if self.nodeType == NodeType.OR:
                if not prereq_courses or len(child_prereqs) < len(prereq_courses):
                    prereq_courses = child_prereqs
            else:
                prereq_courses.extend(child_prereqs)

        self.set_value(original_value)

        return courses + prereq_courses

# Helper function to print the tree structure
def print_node(node: Node, level: int) -> None:
    print('  ' * level + str(node))
    for child in node.get_children():
        print_node(child, level + 1)

root = Node(NodeType.AND, 'root', 'root')
courseNode1 = Node(NodeType.AND, 'course1', 'course1')
courseNode2 = Node(NodeType.AND, 'course2', 'course2')
courseNode3 = Node(NodeType.AND, 'course3', 'course3')
courseNode4 = Node(NodeType.AND, 'course4', 'course4')
courseNode5 = Node(NodeType.AND, 'course5', 'course5')
courseNode6 = Node(NodeType.AND, 'course6', 'course6')
OrNode = Node(NodeType.OR)
OrNode1 = Node(NodeType.OR)
root.add_child(courseNode1)
OrNode.add_child(courseNode2)
root.add_child(OrNode)
courseNode2.add_child(courseNode5)
courseNode1.add_child(OrNode1)
OrNode1.add_child(courseNode3)
OrNode1.add_child(courseNode5)
OrNode.add_child(courseNode4)
root.add_child(courseNode5)


# path = root.bfs(courseNode3)
# print([str(node) for node in path])

min_prereqs = root.min_prereqs()
print(f'Minimum prerequisites needed: {[str(node) for node in min_prereqs]}')

print_node(root, 0)


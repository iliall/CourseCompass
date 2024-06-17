from collections import deque
from enum import Enum
from typing import List, Set

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

    def min_prereqs(self, definites: List['Node'] = None) -> List['Node']:
        if definites is None:
            definites = []
            for child in self.children:
                if child.nodeType == NodeType.AND:
                    definites.append(child)
            # print(f'QQQQQQ self: {self.courseTitle} definites: {[str(node) for node in definites]}')

        if self.value:
            return []
        
       

        if self.nodeType == NodeType.AND:
            courses = [self]
        else:
            courses = []

        prereq_courses = []
        for child in self.children:
            temp_definites = definites.copy()
            if child.nodeType == NodeType.AND:
                for child_of_child in child.get_children():
                    if child_of_child.nodeType == NodeType.AND:
                        temp_definites.append(child_of_child)
                        # print(f'###### definites in self: {self.courseTitle} definites: {[str(node) for node in temp_definites]}')
            child_prereqs = child.min_prereqs(temp_definites)
            if self.nodeType == NodeType.OR:
                # print(f'self: {self.courseTitle} definites: {[str(node) for node in definites]}')
                # print(f'child: {child}, child_prereqs: {[str(node) for node in child_prereqs]} {not_in_list(child_prereqs, temp_definites)} {not_in_list(prereq_courses, temp_definites)}')
                if not prereq_courses or count_items_not_in_list(child_prereqs, temp_definites) < count_items_not_in_list(prereq_courses, temp_definites):
                    prereq_courses = child_prereqs
            else:
                prereq_courses.extend(child_prereqs)


        return courses + prereq_courses
    
def min_prereqs2(processed: List['Node'], toBeProcessed: List['Node']) -> List['Node']:
    # print(f'processed: {[node.courseTitle for node in processed]}')
    # print(f'toBeProcessed: {[node.courseTitle for node in toBeProcessed]}')
    if not toBeProcessed:
        return processed

    current = toBeProcessed.pop(0)
    processed.append(current)

    if current.value:
        return min_prereqs2(processed, toBeProcessed)

    # AND node
    if current.nodeType == NodeType.AND:
        
        for child in current.get_children():
            if child.nodeType == NodeType.AND:
                toBeProcessed.insert(0, child)
            else:
                toBeProcessed.append(child)
        return min_prereqs2(processed, toBeProcessed)
    
    # OR node
    else:
        min_prereqs = []
        for child in current.get_children():
            temp_toBeProcessed = toBeProcessed.copy()
            temp_processed = processed.copy()
            if child.nodeType == NodeType.AND:
                temp_toBeProcessed.insert(0, child)
            else:
                temp_toBeProcessed.append(child)
            
            temp_min_prereqs = min_prereqs2(temp_processed, temp_toBeProcessed)
            # if not min_prereqs or count_items_not_in_list(temp_min_prereqs, processed) < count_items_not_in_list(min_prereqs, processed):
            if not min_prereqs or count_no_duplicates(temp_min_prereqs) < count_no_duplicates(min_prereqs):
                min_prereqs = temp_min_prereqs
        
        return min_prereqs

        

# Helper function to print the tree structure
def print_node(node: Node, level: int) -> None:
    print('  ' * level + str(node))
    for child in node.get_children():
        print_node(child, level + 1)


# Counts the items in lst1 that are not in lst2
def count_items_not_in_list(lst1: List[any], lst2: List[any]) -> int:
    counter = 0
    for i in lst1:
        if i not in lst2:
            counter += 1
    return counter

def count_no_duplicates(lst: List['Node']) -> int:
    counter = 0
    for i in lst:
        if i not in lst[:counter]:
            counter += 1
    return counter




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


# path = root.bfs(courseNode3)
# print([str(node) for node in path])

# min_prereqs = root.min_prereqs()
min_prereqs = min_prereqs2([], [root])
print(f'Minimum prerequisites needed: {[str(node) for node in min_prereqs]}')

for node in min_prereqs:
    node.set_value(True)

print_node(root, 0)

# root True
#   course5 True
#   course1 True
#     OR True
#       course3 True
#       course5 True
#   OR True
#     course4 True
#       course6 True
#     course2 False
#       course5 True
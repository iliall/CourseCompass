#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

enum class NodeType { AND = 1, OR = 2};


class Node {
    private:
        NodeType type;
        string courseTitle;
        string courseId;
        vector<Node*> children;
        bool value;

    public:
        Node(NodeType type, string courseTitle, string courseId) {
            this->type = type;
            this->courseTitle = courseTitle;
            this->courseId = courseId;
            this->value = false;
        }

        void addChild(Node* child) {
            if (child->getType() == NodeType::AND) {
                this->children.insert(this->children.begin(), child);
                return;
            }
            this->children.push_back(child);
        }

        void setValue(bool value) {
            this->value = value;
        }

        bool getValue() {
            return value;
        }

        NodeType getType() {
            return type;
        }

        string getCourseTitle() {
            return courseTitle;
        }

        string getCourseId() {
            return courseId;
        }

        vector<Node*> getChildren() {
            return children;
        }

};


vector<Node*> find_prereqs(vector<Node*> processed, vector<Node*> toBeProcessed) {
    // cout << "Processed: ";
    // for (Node* node : processed) {
    //     cout << node->getCourseTitle() << " ";
    // }
    // cout << endl;

    // cout << "To be processed: ";
    // for (Node* node : toBeProcessed) {
    //     cout << node->getCourseTitle() << " ";
    // }
    // cout << endl;

    if (toBeProcessed.size() == 0) {
        return processed;
    }

    Node* current = toBeProcessed[0];
    toBeProcessed.erase(toBeProcessed.begin());

    if (std::find(processed.begin(), processed.end(), current) == processed.end()) {
        processed.push_back(current);
    }

    if (current->getValue()) {
        return find_prereqs(processed, toBeProcessed);
    }

    if (current->getType() == NodeType::AND) {
        for (Node* child : current->getChildren()) {
            if (child->getType() == NodeType::AND) {
                toBeProcessed.insert(toBeProcessed.begin(), child);
            } else {
                toBeProcessed.push_back(child);
            }
        }
        return find_prereqs(processed, toBeProcessed);
    } 
    
    else {
        vector<Node*> mins = {};
        for (Node* child : current->getChildren()) {
            vector<Node*> temp_toBeProcessed = toBeProcessed;
            vector<Node*> temp_processed = processed;
            if (child->getType() == NodeType::AND) {
                temp_toBeProcessed.insert(temp_toBeProcessed.begin(), child);
            } else {
                temp_toBeProcessed.push_back(child);
            }
            vector<Node*> temp_mins = find_prereqs(temp_processed, temp_toBeProcessed);
            if (temp_mins.size() < mins.size() || mins.size() == 0) {
                mins = temp_mins;
            }
        }
        return mins;
    }

    return {new Node(NodeType::AND, "error", "error")};
}

void print_node(Node* node, int level) {
    for (int i = 0; i < level; i++) {
        cout << "  ";
    }
    cout << node->getCourseTitle() << " " << node->getValue() << endl;
    for (Node* child : node->getChildren()) {
        print_node(child, level + 1);
    }
}


int main() {
    Node* root = new Node(NodeType::AND, "root", "1");
    Node* courseNode1 = new Node(NodeType::AND, "course1", "2");
    Node* courseNode2 = new Node(NodeType::AND, "course2", "3");
    Node* courseNode3 = new Node(NodeType::AND, "course3", "4");
    Node* courseNode4 = new Node(NodeType::AND, "course4", "5");
    Node* courseNode5 = new Node(NodeType::AND, "course5", "6");
    Node* courseNode6 = new Node(NodeType::AND, "course6", "7");
    Node* courseNode7 = new Node(NodeType::AND, "course7", "8");
    Node* orNode1 = new Node(NodeType::OR, "OR1", "9");
    Node* orNode2 = new Node(NodeType::OR, "OR2", "10");
    root->addChild(courseNode1);
    orNode1->addChild(courseNode2);
    root->addChild(orNode1);
    courseNode2->addChild(courseNode5);
    courseNode1->addChild(orNode2);
    orNode2->addChild(courseNode5);
    orNode2->addChild(courseNode3);
    orNode1->addChild(courseNode4);
    root->addChild(courseNode7);
    courseNode4->addChild(courseNode6);

    vector<Node*> processed = {};
    vector<Node*> toBeProcessed = {root};

    vector<Node*> result = find_prereqs(processed, toBeProcessed);

    for (Node* node : result) {
        cout << node->getCourseTitle() << " ";
    }
    cout << endl;

    for (Node* node : result) {
        node->setValue(true);
    }

    print_node(root, 0);
}
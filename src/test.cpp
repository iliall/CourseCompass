#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

#include "nodes.cpp"

using namespace std;

void test1() {
    cout << "Running test1" << endl;
    /*
    Test1:
                     root
                    /    \
                course1  OR1
                        /    \
                    course2  course4
                    /    \ 
                course5  course3
    */
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

    cout << endl << endl;

}

void test2() {
    cout << "Running test2" << endl;
    /*
    Test2:
            CS480  CS485
              |      |
             OR1    OR2
            /  \    /  \
          CS380 CS240  CS385
            |   |       | 
         CS280 CS136   CS285
                |
              CS135
          
    */
    Node* cs480 = new Node(NodeType::AND, "CS 480", "1");
    Node* cs485 = new Node(NodeType::AND, "CS 485", "2");
    Node* cs380 = new Node(NodeType::AND, "CS 380", "3");
    Node* cs385 = new Node(NodeType::AND, "CS 385", "4");
    Node* cs280 = new Node(NodeType::AND, "CS 280", "5");
    Node* cs285 = new Node(NodeType::AND, "CS 285", "6");
    Node* cs240 = new Node(NodeType::AND, "CS 240", "7");
    Node* cs136 = new Node(NodeType::AND, "CS 136", "8");
    Node* cs135 = new Node(NodeType::AND, "CS 135", "9");
    Node* or1 = new Node(NodeType::OR, "OR1", "10");
    Node* or2 = new Node(NodeType::OR, "OR2", "11");

    cs480->addChild(or1);
    cs485->addChild(or2);
    or1->addChild(cs380);
    cs380->addChild(cs280);
    or1->addChild(cs240);
    cs240->addChild(cs136);
    cs136->addChild(cs135);
    or2->addChild(cs385);
    cs385->addChild(cs285);
    or2->addChild(cs240);

    vector<Node*> processed = {};
    vector<Node*> toBeProcessed = {cs480, cs485};

    vector<Node*> result = find_prereqs(processed, toBeProcessed);

    for (Node* node : result) {
        cout << node->getCourseTitle() << " ";
    }
    cout << endl;

    for (Node* node : result) {
        node->setValue(true);
    }

    print_node(cs480, 0);
    print_node(cs485, 0);

    cout << endl << endl;

}


int main() {
    test1();
    test2();
    return 0;

}
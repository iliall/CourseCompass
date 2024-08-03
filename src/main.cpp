#include <vector>
#include "crow.h"
#include "nodes.cpp"

using namespace std;

vector<Node*> nodes;

void setup() {
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

    nodes.push_back(cs480);
    nodes.push_back(cs485);
    nodes.push_back(cs380);
    nodes.push_back(cs385);
    nodes.push_back(cs280);
    nodes.push_back(cs285);
    nodes.push_back(cs240);
    nodes.push_back(cs136);
    nodes.push_back(cs135);
    nodes.push_back(or1);
    nodes.push_back(or2);
}

Node* find_node(string courseId) {
    for (Node* node : nodes) {
        if (node->getCourseId() == courseId) {
            return node;
        }
    }
    return nullptr;
}

int main()
{
    setup();

    crow::SimpleApp app;

    // Define a simple route
    CROW_ROUTE(app, "/")([](){
        crow::json::wvalue wval;
        wval["message"] = "Hello, World!";
        return wval;
    });

    CROW_ROUTE(app, "/api").methods(crow::HTTPMethod::GET)([](const crow::request& req){
        // Node* course = find_node(req.url_params.get("course"));
        std::string course_name = req.get_body_params().get("course");
        Node* course = find_node(course_name);
        vector<Node*> processed = {};
        vector<Node*> toBeProcessed = {course};

        vector<Node*> result = find_prereqs(processed, toBeProcessed);

        crow::json::wvalue wval;
        vector<crow::json::wvalue> prereqs;
        for (Node* node : result) {
            crow::json::wvalue course;
            course["courseTitle"] = node->getCourseTitle();
            course["courseId"] = node->getCourseId();
            prereqs.push_back(course);
        }
        wval["prereqs"] = crow::json::wvalue(prereqs);
        return crow::json::wvalue(wval);
    });

    // Run the app on port 8080
    app.port(8080).multithreaded().run();

    return 0;
}

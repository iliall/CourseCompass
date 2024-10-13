package models

type NodeType bool

const (
	AND NodeType = true
	OR  NodeType = false
)

type Node struct {
	node_type    NodeType
	course_title string
	course_id    string
	children     []*Node
	value        bool
}

func NewNode(node_type NodeType, course_title string, course_id string) *Node {
	return &Node{
		node_type:    node_type,
		course_title: course_title,
		course_id:    course_id,
		children:     []*Node{},
		value:        false,
	}
}

func (n *Node) AddChild(child *Node) {
	if child.node_type == AND {
		n.children = append([]*Node{child}, n.children...)
	} else {
		n.children = append(n.children, child)
	}
}

func (n *Node) SetValue(value bool) {
	n.value = value
}

func (n *Node) GetValue() bool {
	return n.value
}

func (n *Node) GetType() NodeType {
	return n.node_type
}

func (n *Node) GetCourseTitle() string {
	return n.course_title
}

func (n *Node) GetCourseId() string {
	return n.course_id
}

func (n *Node) GetChildren() []*Node {
	return n.children
}

func FindPrereqs(processed []*Node, toBeProcessed []*Node) []*Node {
	if len(toBeProcessed) == 0 {
		return processed
	}

	current := toBeProcessed[0]
	toBeProcessed = toBeProcessed[1:]

	// If the current node is already satisfied, skip further processing
	if current.GetValue() {
		return FindPrereqs(processed, toBeProcessed)
	}

	// Check if already processed
	if !Contains(processed, current) {
		processed = append(processed, current)
	}

	if current.GetType() == AND {

		for _, child := range current.GetChildren() {
			if child.GetType() == AND {
				toBeProcessed = append([]*Node{child}, toBeProcessed...)
			} else {
				toBeProcessed = append(toBeProcessed, child)
			}
		}
		return FindPrereqs(processed, toBeProcessed)
	} else {
		var mins []*Node
		for _, child := range current.GetChildren() {
			tempToBeProcessed := append([]*Node{}, toBeProcessed...)
			tempProcessed := append([]*Node{}, processed...)

			if child.GetType() == AND {
				tempToBeProcessed = append([]*Node{child}, tempToBeProcessed...)
			} else {
				tempToBeProcessed = append(tempToBeProcessed, child)
			}

			tempMins := FindPrereqs(tempProcessed, tempToBeProcessed)
			if len(tempMins) < len(mins) || len(mins) == 0 {
				mins = tempMins
			}
		}
		return mins
	}
}

func Contains(nodes []*Node, target *Node) bool {
	for _, n := range nodes {
		if n == target {
			return true
		}
	}
	return false
}

func PrintNode(n *Node, level int) {
	for i := 0; i < level; i++ {
		print("  ")
	}
	println(n.GetCourseTitle(), n.GetValue())
	for _, child := range n.GetChildren() {
		PrintNode(child, level+1)
	}
}

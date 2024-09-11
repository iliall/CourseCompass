package main

import (
	"net/http"
	"api/models"
	"github.com/gin-gonic/gin"
)

var nodes []*models.Node

// Setup initializes the nodes and their relationships
func setup() {
  cs480 := models.NewNode(models.AND, "CS 480", "1")
  cs485 := models.NewNode(models.AND, "CS 485", "2")
	cs380 := models.NewNode(models.AND, "CS 380", "3")
	cs385 := models.NewNode(models.AND, "CS 385", "4")
	cs280 := models.NewNode(models.AND, "CS 280", "5")
	cs285 := models.NewNode(models.AND, "CS 285", "6")
	cs240 := models.NewNode(models.AND, "CS 240", "7")
	cs136 := models.NewNode(models.AND, "CS 136", "8")
	cs135 := models.NewNode(models.AND, "CS 135", "9")
	or1 := models.NewNode(models.OR, "OR1", "10")
	or2 := models.NewNode(models.OR, "OR2", "11")

	// Build relationships
	cs480.AddChild(or1)
	cs485.AddChild(or2)
	or1.AddChild(cs380)
	cs380.AddChild(cs280)
	or1.AddChild(cs240)
	cs240.AddChild(cs136)
	cs136.AddChild(cs135)
	or2.AddChild(cs385)
	cs385.AddChild(cs285)
	or2.AddChild(cs240)

	nodes = []*models.Node{cs480, cs485, cs380, cs385, cs280, cs285, cs240, cs136, cs135, or1, or2}
}



func FindNode(courseId string) *models.Node {
	for _, node := range nodes {
		if node.GetCourseId() == courseId {
			return node
		}
	}
	return nil
}

func main() {
	setup()

	r := gin.Default()

	r.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})

	
	r.GET("/api", func(c *gin.Context) {
		courseId := c.Query("course")

		
		course := FindNode(courseId)
		if course == nil {
			c.JSON(http.StatusNotFound, gin.H{
				"error": "Course not found",
			})
			return
		}

		
		processed := []*models.Node{}
		toBeProcessed := []*models.Node{course}
		result := models.FindPrereqs(processed, toBeProcessed)

		
		var prereqs []gin.H
		for _, node := range result {
			prereqs = append(prereqs, gin.H{
				"courseTitle": node.GetCourseTitle(),
				"courseId":    node.GetCourseId(),
			})
		}

		c.JSON(http.StatusOK, gin.H{
			"prereqs": prereqs,
		})
	})

	// Start the server on port 8080
	r.Run(":8080")
}

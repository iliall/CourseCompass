package utils

import (
	"api/models"
	"database/sql"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"github.com/lib/pq"
	"os"
	"strconv"
)

var Db *sql.DB

func ConnectDatabase() error {
	err := godotenv.Load()
	if err != nil {
		return fmt.Errorf("error occurred while loading .env file: %v", err)
	}

	// Read environment variables
	host := os.Getenv("DB_HOST")
	port, _ := strconv.Atoi(os.Getenv("DB_PORT"))
	user := os.Getenv("DB_USER")
	dbname := os.Getenv("DB_NAME")
	pass := os.Getenv("DB_PASSWORD")
	sslmode := os.Getenv("DB_SSLMODE")

	// Set up PostgreSQL connection
	psqlSetup := fmt.Sprintf("host=%s port=%d user=%s dbname=%s password=%s sslmode=%s", host, port, user, dbname, pass, sslmode)
	db, errSql := sql.Open("postgres", psqlSetup)
	if errSql != nil {
		return fmt.Errorf("error while connecting to the database: %v", errSql)
	}

	err = db.Ping()
	if err != nil {
		return fmt.Errorf("could not ping the database: %v", err)
	}

	Db = db
	fmt.Println("Successfully connected to the database!")

	// Call the function to create the table if it doesn't exist
	err = CreateUsersTableIfNotExists()
	if err != nil {
		return fmt.Errorf("error creating users table: %v", err)
	}

	return nil
}

func CreateUsersTableIfNotExists() error {
	// SQL to create the users table if it doesn't already exist
	query := `
	CREATE TABLE IF NOT EXISTS users (
		username VARCHAR(255) PRIMARY KEY,
		email VARCHAR(255) NOT NULL,
		password VARCHAR(255) NOT NULL,
		course_ids TEXT[]
	);
	`

	_, err := Db.Exec(query)
	if err != nil {
		return fmt.Errorf("failed to create users table: %v", err)
	}

	fmt.Println("Users table created or already exists")
	return nil
}

func AddUser(c *gin.Context) {
	var user models.User
	if err := c.BindJSON(&user); err != nil {
		c.JSON(400, gin.H{"error": "Invalid request body"})
		return
	}

	// Inserting data into the database, including the course_ids array
	_, err := Db.Exec(
		"INSERT INTO users(username, email, password, course_ids) VALUES($1, $2, $3, $4)",
		user.Username, user.Email, models.HashPassword(user.Password), pq.Array(user.CourseIDs),
	)
	if err != nil {
		c.JSON(500, gin.H{"error": "Failed to insert user into database"})
		return
	}

	c.JSON(200, gin.H{"message": "User added successfully"})
}

func GetUserByUsername(c *gin.Context) {
	username := c.Param("username")

	var user models.User
	var courseIDs []string
	err := Db.QueryRow(
		"SELECT username, email, course_ids FROM users WHERE username = $1", username,
	).Scan(&user.Username, &user.Email, pq.Array(&courseIDs))
	if err != nil {
		if err == sql.ErrNoRows {
			c.JSON(404, gin.H{"error": "User not found"})
			return
		}
		c.JSON(500, gin.H{"error": "Error fetching user from database"})
		return
	}

	user.CourseIDs = courseIDs
	c.JSON(200, user)
}

func UpdateUserCourses(c *gin.Context) {
	username := c.Param("username")
	var request struct {
		CourseIDs []string `json:"course_ids"`
	}

	if err := c.BindJSON(&request); err != nil {
		c.JSON(400, gin.H{"error": "Invalid request body"})
		return
	}

	_, err := Db.Exec("UPDATE users SET course_ids = $1 WHERE username = $2", pq.Array(request.CourseIDs), username)
	if err != nil {
		c.JSON(500, gin.H{"error": "Failed to update user courses"})
		return
	}

	c.JSON(200, gin.H{"message": "User courses updated successfully"})
}

func DeleteUser(c *gin.Context) {
	username := c.Param("username")

	_, err := Db.Exec("DELETE FROM users WHERE username = $1", username)
	if err != nil {
		c.JSON(500, gin.H{"error": "Failed to delete user"})
		return
	}

	c.JSON(200, gin.H{"message": "User deleted successfully"})
}

func GetAllUsers(c *gin.Context) {
	rows, err := Db.Query("SELECT username, email, course_ids FROM users")
	if err != nil {
		c.JSON(500, gin.H{"error": "Error fetching users from database"})
		return
	}
	defer rows.Close()

	var users []models.User
	for rows.Next() {
		var user models.User
		var courseIDs []string
		if err := rows.Scan(&user.Username, &user.Email, pq.Array(&courseIDs)); err != nil {
			c.JSON(500, gin.H{"error": "Error scanning user row"})
			return
		}
		user.CourseIDs = courseIDs
		users = append(users, user)
	}

	c.JSON(200, users)
}

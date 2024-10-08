package utils

import (
	"database/sql"
	"fmt"
	"github.com/joho/godotenv"
	_ "github.com/lib/pq" 
	"os"
	"strconv"
	"github.com/gin-gonic/gin"
	"api/models"
)

var Db *sql.DB

func ConnectDatabase() {
	err := godotenv.Load()
	if err != nil {
	   fmt.Println("Error is occurred  on .env file please check")
	}
	//we read our .env file
	host := os.Getenv("HOST")
	port, _ := strconv.Atoi(os.Getenv("PORT")) 
	user := os.Getenv("USER")
	dbname := os.Getenv("DB_NAME")
	pass := os.Getenv("PASSWORD")
 
	// set up postgres sql to open it.
	psqlSetup := fmt.Sprintf("host=%s port=%d user=%s dbname=%s password=%s sslmode=disable",
		host, port, user, dbname, pass)
	db, errSql := sql.Open("postgres", psqlSetup)
	if errSql != nil {
	   fmt.Println("There is an error while connecting to the database ", err)
	   panic(err)
	} else {
	   Db = db
	   fmt.Println("Successfully connected to database!")
	}
}

func AddUser(cix *gin.Context) {
	var user models.User
	cix.BindJSON(&user)
	//inserting data into the database
	_, err := Db.Exec("insert into users(username, email, password) values($1, $2, $3)", user.Username, user.Email, models.HashPassword(user.Password))
	if err != nil {
	   fmt.Println("There is an error while inserting data into the database ", err)
	   panic(err)
	} else {
	   fmt.Println("Data inserted successfully!")
	}
}
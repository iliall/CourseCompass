package models

import (
	"golang.org/x/crypto/bcrypt"
)

type User struct {
	Username  string   `json:"username"`
	Email     string   `json:"email"`
	Password  string   `json:"password"`
	CourseIDs []string `json:"course_ids"`
}

func HashPassword(password string) string {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return ""
	}
	return string(hashedPassword)
}

func NewUser(id int, username string, email string, password string) *User {
	return &User{
		Username:  username,
		Email:     email,
		Password:  HashPassword(password),
		CourseIDs: []string{},
	}
}

func (u *User) AddCourse(course string) {
	u.CourseIDs = append(u.CourseIDs, course)
}

func (u *User) GetCourses() []string {
	return u.CourseIDs
}

func (u *User) GetUsername() string {
	return u.Username
}

func (u *User) GetEmail() string {
	return u.Email
}

func (u *User) CheckPassword(password string) bool {
	return u.Password == HashPassword(password)
}

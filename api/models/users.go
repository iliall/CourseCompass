package models

import (
	"golang.org/x/crypto/bcrypt"
)

type User struct {
	Id int
	Username string
	Email string
	Password string
	courses []*string
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
		Id: id,
		Username: username,
		Email: email,
		Password: HashPassword(password),
		courses: []*string{},
	}
}

func (u *User) AddCourse(course *string) {
	u.courses = append(u.courses, course)
}

func (u *User) GetCourses() []*string {
	return u.courses
}

func (u *User) GetId() int {
	return u.Id
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
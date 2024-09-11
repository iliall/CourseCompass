# CourseCompass

## GO Libraries Used:

[gin-gonic/gin](https://github.com/gin-gonic/gin)

## C++ Libraries Used:

[libpqxx](https://github.com/jtv/libpqxx?tab=readme-ov-file)
<br>
[crow](https://github.com/CrowCpp/Crow) (Already included in the include folder)
<br>
[asio](https://github.com/chriskohlhoff/asio/) (Already included in the include folder)

## Run GO Backend:

```sh
cd api
go run main.go
```

## Run C++ Backend:

```sh
cd backend
mkdir build
cd build
cmake ..
make
./courseCompass
```

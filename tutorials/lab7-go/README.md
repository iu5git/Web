# Методические указания по выполнению лабораторной работы №7

### Команда курса благодарит Коновалова Максима Владиславовича за активное участие в подготовке данного руководства.

В этой лабораторной работе мы разработаем простой веб-сервер на основе языка Golang и фреймворка gin-gonic
, который будет реализовывать следующую функциональность:

- Авторизация по JWT(json web token)
- Ролевая модель, основывающая на JWT

## План

1. Чем отличается авторизация от аутентификации?
2. Вводная часть: по какому принципу работает авторизация JWT
3. Пишем простейшую авторизацию на JWT. Middlewares.
4. Устанавливаем redis
5. Разрабатываем ролевую модель. Разрабатываем регистрацию.
6. Реализуем ролевую модель на основе JWT
7. Refresh Token
8. Полезные ссылки

## 1. Чем отличается авторизация от аутентификации?

**Аутентификация** — процедура проверки подлинности,
например проверка подлинности пользователя путем сравнения введенного им пароля с паролем, сохраненным в базе данных.

**Авторизация** — предоставление определенному лицу или группе лиц прав на выполнение определенных действий.

**Идентификация** — процедура,
в результате выполнения которой для субъекта идентификации выявляется его идентификатор, однозначно определяющий этого
субъекта в информационной системе.

Простые примеры:

Система определяет что логин ivanivanich,
введенный пользователем в системе существует и принадлежит Ивану Ивановичу Петрову,
у которого есть 3 банковские карты. Таким образом мы **идентифицировали** пользователя.

Система проверяет что помимо логина пользователя пользователь нам так же при залогинивании в систему
отправляет пароль ivanichpassword.
Проверив что этот пароль действительно принадлежит Ивану Иванычу мы уверены,
что это именно тот пользователь - это **аутентификация**.

Система знает что иван иванычу можно смотреть видео с котиками,
но нельзя смотреть видео с собачками.
Мы определили его права в системе после аутентификации
и не даем смотреть видео с собачками - это **авторизация**.

# 2. Вводная часть: по какому принципу работает авторизация JWT

1. Сперва пользователь отправляет на сервер логин и пароль.
2. Сервер проверяет их. Затем сервер создает JWT и отправляет его пользователю.
3. Когда пользователь делает запрос к API приложения, он добавляет к нему в заголовок Authorization с префиксом Bearer
   полученный ранее JWT.
4. Когда пользователь делает API запрос, приложение может проверить по переданному с запросом JWT является ли
   пользователь тем, за кого себя выдает.
5. В JWT схему можно также добавить /logout. Однако для этого будет необходимо хранить некоторый blacklist.

JWT состоит из трех частей: заголовок header,
полезные данные payload и подпись signature.
Где payload - ваши данные, signature - подпись шифрования, header - алгоритм шифрования и тип.

Подробнее вы можете прочитать в статье https://habr.com/en/post/340146/.

### Как происходит создание jwt?

По сути jwt - некотороая структура данных, которая кодируется в json,
а затем подписывается некоторым секретным токеном. Когда к нам в следующий раз придет пользователь,
мы попроубем расшифровать эту подпись, ведь токен у нас. Если получилось - пользователь авторизован.
![Создание проекта](docs/1.png)

# 3. Пишем простейшую авторизацию на JWT

Воспользуемся ранее написанным нам эндпоинтом ping
и сделаем так что он будет отдавать наш статус авторизации.

```json
// для авторизованных 
{
  "auth": true
}
// для неавторизованных
403 код ответа
```

Для начала захардкодим (хардкод - код написанный неправильно, в обход какой-то долгой работы)
пароль и логин. Ведь пока мы не разрабатываем ролевую модель!

Далее положим секрет(ключ, которым мы будем шифровать и расшифровывать JWT),
который мы считали из .env в конфигурацию. Это может быть любая строка! У меня это ```test```.
Также советую попробывать выбирать алгоритм шифрования JWT и время его истечения также в зависимости от конфигурации,
это очень удобно!

Научимся создавать JWT. Будем использовать библиотеку    "github.com/golang-jwt/jwt"

Создадим новый endpoint login. Обязательно POST запрос. Параметры GET запроса не шифруются.

```go
    r.POST("/login", a.Login) // там где мы ранее уже заводили эндпоинты

...
type loginReq struct {
Login    string `json:"login"`
Password string `json:"password"`
}

type loginResp struct {
ExpiresIn   int    `json:"expires_in"`
AccessToken string `json:"access_token"`
TokenType   string `json:"token_type"`
}

func (a *Application) Login(gCtx *gin.Context) {
...
}
```

Создадим свои собственные Claims для JWT на основе уже базовых и необходимых в JWT.
Для этого создадим новую структуру,
в которую заэмбдим(встроим/embed) структуру стандартных Claims.
Добавим в пакет ds в нашем проекте новый файл ```/internal/app/ds/jwt.go```

```go
package ds

import (
	"github.com/golang-jwt/jwt"
	"github.com/google/uuid"
)

type JWTClaims struct {
	jwt.StandardClaims           // все что точно необходимо по RFC
	UserUUID           uuid.UUID `json:"user_uuid"` // наши данные - uuid этого пользователя в базе данных
	Scopes             []string  `json:"scopes" json:"scopes"` // список доступов в нашей системе
}
```

Дописываем логику проверки в эндпоинт:

```go
type loginReq struct {
Login    string `json:"login"`
Password string `json:"password"`
}

type loginResp struct {
ExpiresIn   time.Duration `json:"expires_in"`
AccessToken string        `json:"access_token"`
TokenType   string        `json:"token_type"`
}

func (a *Application) Login(gCtx *gin.Context) {
cfg := a.config
req := &loginReq{}

err := json.NewDecoder(gCtx.Request.Body).Decode(req)
if err != nil {
gCtx.AbortWithError(http.StatusBadRequest, err)

return
}

if req.Login == login && req.Password == password {
// значит проверка пройдена
// генерируем ему jwt
token := jwt.NewWithClaims(cfg.JWT.SigningMethod, &ds.JWTClaims{
StandardClaims: jwt.StandardClaims{
ExpiresAt: time.Now().Add(cfg.JWT.ExpiresIn).Unix(),
IssuedAt:  time.Now().Unix(),
Issuer:    "bitop-admin",
},
UserUUID: uuid.New(), // test uuid
Scopes:   []string{}, // test data
})

if token == nil {
gCtx.AbortWithError(http.StatusInternalServerError, fmt.Errorf("token is nil"))

return
}

strToken, err := token.SignedString([]byte(cfg.JWT.Token))
if err != nil {
gCtx.AbortWithError(http.StatusInternalServerError, fmt.Errorf("cant create str token"))

return
}

gCtx.JSON(http.StatusOK, loginResp{
ExpiresIn:   cfg.JWT.ExpiresIn,
AccessToken: strToken,
TokenType:   "Bearer",
})
}

gCtx.AbortWithStatus(http.StatusForbidden) // отдаем 403 ответ в знак того что доступ запрещен
}
```

Теперь на нашем эндпоинте `/ping` мы должны проверять валидность токена.
Однако, если мы будем создавать такую проверку в каждый из эндпоинтов,
то код станет крайне громоздким! Для того чтобы это избежать придумали middlewares(промежуточный код).
По сути вы пишете функцию которая будет вызываться перед обработкой эндпоинтов на которые вы навесили
"мидлварь".

И так. Middleware (промежуточное или связующее программное обеспечение)
— это фрагмент кода в конвейере приложения,
используемый для обработки запросов и ответов.

Это очень удобно для нас разграничивать эндпоинты, к которым пользователь имеет полный доступ вне зависимости от
авторизации
и эндпоинты которым нужна авторизация!

Напишем такую мидлварь, которая будет прерывать запрос к эндпоинту, если авторизация не пройдена!

Добавим файл в ```/internal/pkg/app/middlewares.go```. И напишем в нем мидлварь.

```go
package app

import (
	"awesomeProject/internal/app/ds"
	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt"
	"log"
	"net/http"
	"strings"
)

const jwtPrefix = "Bearer "

func (a *Application) WithAuthCheck(gCtx *gin.Context) {
	jwtStr := gCtx.GetHeader("Authorization")
	if !strings.HasPrefix(jwtStr, jwtPrefix) { // если нет префикса то нас дурят!
		gCtx.AbortWithStatus(http.StatusForbidden) // отдаем что нет доступа

		return // завершаем обработку
	}

	// отрезаем префикс
	jwtStr = jwtStr[len(jwtPrefix):]

	_, err := jwt.ParseWithClaims(jwtStr, &ds.JWTClaims{}, func(token *jwt.Token) (interface{}, error) {
		return []byte(a.config.JWT.Token), nil
	})
	if err != nil {
		gCtx.AbortWithStatus(http.StatusForbidden)
		log.Println(err)

		return
	}
}
```

Добавим авторизацию на наш эндпоинт ```/ping```

```go
...
r.Use(a.WithAuthCheck).GET("/ping", a.Ping)
...
```

### Проверим что все работает как мы задумывали

403 ответ если пароль и логин не подходят

```shell
$ curl -v --location --request POST 'http://127.0.0.1:8080/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "login": "login",
    "password": "check1223"
}'
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> POST /login HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.84.0
> Accept: */*
> Content-Type: application/json
> Content-Length: 53
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 403 Forbidden
< Date: Sun, 20 Nov 2022 19:09:16 GMT
< Content-Length: 0
< 
* Connection #0 to host 127.0.0.1 left intact
```

403 ответ если нет Authorization заголовка в запросе к `/ping`

```shell
$ curl -v --location --request GET 'http://127.0.0.1:8080/ping' \
--header 'Content-Type: application/json' \
--data-raw '{
    "login": "login",
    "password": "check1223"
}'
*   Trying 127.0.0.1:8080...
* Connected to 127.0.0.1 (127.0.0.1) port 8080 (#0)
> GET /ping HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/7.84.0
> Accept: */*
> Content-Type: application/json
> Content-Length: 53
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 403 Forbidden
< Date: Sun, 20 Nov 2022 19:10:16 GMT
< Content-Length: 0
< 
* Connection #0 to host 127.0.0.1 left intact
```

200 если мы логинимся с правильным логином и паролем

```shell
$ curl --location --request POST 'http://127.0.0.1:8080/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "login": "login",
    "password": "check123"
}'
{"expires_in":3600000000000,"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2Njg5NzUwNzUsImlhdCI6MTY2ODk3MTQ3NSwiaXNzIjoiYml0b3AtYWRtaW4iLCJ1c2VyX3V1aWQiOiI3ZDEzZmEyMS04OWY1LTQxYmItYTZlYy0xYzYxMTJkNGEzZDEiLCJzY29wZXMiOltdLCJpc19yZWZyZXNoIjpmYWxzZSwibmVlZF9vdHAiOmZhbHNlfQ.Y6qz5AuseDV0I6FiwJPYhL-a3akAwhrlNrIDg6_bmIQ","token_type":"Bearer"}%   
```

200 если мы передаем этот токен в Authorization хедере с префиксом "Bearer " к запросу на /login

```shell
$ curl --location --request GET 'http://127.0.0.1:8080/ping' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2Njg5NzUwNzUsImlhdCI6MTY2ODk3MTQ3NSwiaXNzIjoiYml0b3AtYWRtaW4iLCJ1c2VyX3V1aWQiOiI3ZDEzZmEyMS04OWY1LTQxYmItYTZlYy0xYzYxMTJkNGEzZDEiLCJzY29wZXMiOltdLCJpc19yZWZyZXNoIjpmYWxzZSwibmVlZF9vdHAiOmZhbHNlfQ.Y6qz5AuseDV0I6FiwJPYhL-a3akAwhrlNrIDg6_bmIQ' \
--header 'Content-Type: application/json' \
--data-raw '{
    "login": "login",
    "password": "check123"
}'
{"status":true}%   
```

Все работает как надо! Мы написали самую простую авторизацию!

# 4. Устанавливаем redis

В установке redis действует все то же правило что и в ЛР2.
В случае установок на железо - следуйте инструкциям из документации Redis.
В данном случае мы будем использовать docker-compose все так же.

Найти измененный docker-compose можно в текущей директории.
В нем добавился сервис redis

```yaml
  redis:
    image: redis:6.2-alpine
    restart: always
    ports:
      - '6379:6379'
    command: redis-server --save 20 1 --loglevel warning --requirepass password
    volumes:
      - redis-data:/data
```

А так же volume к нему:

```yaml
volumes:
  postgresdb-data:
    driver: local
  redis-data:
    driver: local
```

Проверим что это работает.

```shell
(base) maxim-konovalov@maksim-konovalov lab7-go % docker compose up -d
[+] Running 2/2
 ⠿ Container lab7-go-redis-1  Started                                                                                                                                  0.4s
 ⠿ Container lab7-go-db-1     Started                                                                                                                                  0.4s
(base) maxim-konovalov@maksim-konovalov lab7-go % docker ps
CONTAINER ID   IMAGE              COMMAND                  CREATED          STATUS        PORTS                    NAMES
51d923166abe   postgres:12        "docker-entrypoint.s…"   15 seconds ago   Up 1 second   0.0.0.0:5432->5432/tcp   lab7-go-db-1
55247dd8307d   redis:6.2-alpine   "docker-entrypoint.s…"   15 seconds ago   Up 1 second   0.0.0.0:6379->6379/tcp   lab7-go-redis-1
(base) maxim-konovalov@maksim-konovalov lab7-go % docker logs 55247dd8307d
1:C 20 Nov 2022 19:20:00.703 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
1:C 20 Nov 2022 19:20:00.703 # Redis version=6.2.7, bits=64, commit=00000000, modified=0, pid=1, just started
1:C 20 Nov 2022 19:20:00.703 # Configuration loaded
1:M 20 Nov 2022 19:20:00.711 # A key '__redis__compare_helper' was added to Lua globals which is not on the globals allow list nor listed on the deny list.
1:M 20 Nov 2022 19:20:00.712 # Server initialized
1:signal-handler (1668972012) Received SIGTERM scheduling shutdown...
1:M 20 Nov 2022 19:20:12.190 # User requested shutdown...
1:M 20 Nov 2022 19:20:12.192 # Redis is now ready to exit, bye bye...
1:C 20 Nov 2022 19:20:14.506 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
1:C 20 Nov 2022 19:20:14.506 # Redis version=6.2.7, bits=64, commit=00000000, modified=0, pid=1, just started
1:C 20 Nov 2022 19:20:14.506 # Configuration loaded
1:M 20 Nov 2022 19:20:14.506 # A key '__redis__compare_helper' was added to Lua globals which is not on the globals allow list nor listed on the deny list.
1:M 20 Nov 2022 19:20:14.507 # Server initialized
1:M 20 Nov 2022 19:20:14.509 # Done loading RDB, keys loaded: 0, keys expired: 0.

```

# 5. Разрабатываем регистрацию и ролевую модель.

### Разрабатываем ролевую модель

Ролевая модель - это описание моделей, которые помогают вам предоставлять пользователям тот или иной доступ.
В нашем случае мы реализуем самую примитивную ролевую модель.
Наша ролевая модель будет масштабироваться лишь новыми записями в коде.
Однако это не помешает нам в изучении понятия "Ролевая модель".
Конечно, в реальных продуктах как правило используется гибко масштабируемая ролевая модель.

Разработем нашу ролевую модель.
Пусть будет 3 роли: администратор, менеджер, покупатель.
Зададим их с помощью аналогии к enum в golang.
``` internal/app/role/role.go```

```go
package role

type Role int

const (
	Buyer   Role = iota // 0
	Manager             // 1
	Admin               // 2
)
```

### Разработаем регистрацию.

Будем хранить наших польователей в Postgresql.
Создадим примитивную таблицу с пользователями.
Для начала добавим в ds файл ```user.go```

```go
package ds

import (
	"awesomeProject/internal/app/role"
	"github.com/google/uuid"
)

type User struct {
	UUID uuid.UUID `gorm:"type:uuid"`
	Name string    `json:"name"`
	Role role.Role `sql:"type:string;"`
	Pass string
}


```

Промигрируем его, добавив новую запись в `cmd/migrate/migrate.go`

```go
package main

import (
	"github.com/joho/godotenv"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"

	"awesomeProject/internal/app/ds"
	"awesomeProject/internal/app/dsn"
)

func main() {
	_ = godotenv.Load()
	db, err := gorm.Open(postgres.Open(dsn.FromEnv()), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}

	// Migrate the schema
	err = db.AutoMigrate(&ds.Stock{})
	err = db.AutoMigrate(&ds.User{})
	if err != nil {
		panic("cant migrate db")
	}
}
```

Проверим что миграция действительно прошла
![Создание проекта](docs/2.png)

Добавим запрос на регистрацию.

Создадим в репозитории новый метод для регистрации:

```go
func (r *Repository) Register(user *ds.User) error {
if user.UUID == uuid.Nil {
user.UUID = uuid.New()
}

return r.db.Create(user).Error
}
```

Добавим новый эндпоинт:

```go
...
r.POST("/sign_up", a.Register)
...

type registerReq struct {
Name string `json:"name"` // лучше назвать то же самое что login
Pass string `json:"pass"`
}

type registerResp struct {
Ok bool `json:"ok"`
}

func (a *Application) Register(gCtx *gin.Context) {
req := &registerReq{}

err := json.NewDecoder(gCtx.Request.Body).Decode(req)
if err != nil {
gCtx.AbortWithError(http.StatusBadRequest, err)

return
}

if req.Pass == "" {
gCtx.AbortWithError(http.StatusBadRequest, fmt.Errorf("pass is empty"))

return
}

if req.Name == "" {
gCtx.AbortWithError(http.StatusBadRequest, fmt.Errorf("name is empty"))

return
}

err = a.repo.Register(&ds.User{
UUID: uuid.New(),
Role: role.Buyer,
Name: req.Name,
Pass: generateHashString(req.Pass), // пароли делаем в хешированном виде и далее будем сравнивать хеши, чтобы их не угнали с базой вместе
})

if err != nil {
gCtx.AbortWithError(http.StatusInternalServerError, err)

return
}

gCtx.JSON(http.StatusOK, &registerResp{
Ok: true,
})
}

func generateHashString(s string) string {
h := sha1.New()
h.Write([]byte(s))
return hex.EncodeToString(h.Sum(nil))
}

```

Проверим его:
![Создание проекта](docs/3.png)
![Создание проекта](docs/4.png)
Все работает!

# 6. Реализуем ролевую модель на основе JWT

Наверное это будет самая быстрая часть наших с вами стараний.
Добавим в нашу структуру JWT новое поле role.
Теперь наш JWT выглядит следующим образом:

```go
type JWTClaims struct {
jwt.StandardClaims
UserUUID uuid.UUID `json:"user_uuid"`
Role     role.Role
}
```

Улучшим нашу авторизационную Middleware:

```go
package app

import (
	"awesomeProject/internal/app/ds"
	"awesomeProject/internal/app/role"
	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt"
	"log"
	"net/http"
	"strings"
)

const jwtPrefix = "Bearer "

func (a *Application) WithAuthCheck(assignedRoles ...role.Role) func(ctx *gin.Context) {
	return func(gCtx *gin.Context) {
		jwtStr := gCtx.GetHeader("Authorization")
		if !strings.HasPrefix(jwtStr, jwtPrefix) { // если нет префикса то нас дурят!
			gCtx.AbortWithStatus(http.StatusForbidden) // отдаем что нет доступа

			return // завершаем обработку
		}

		// отрезаем префикс
		jwtStr = jwtStr[len(jwtPrefix):]

		token, err := jwt.ParseWithClaims(jwtStr, &ds.JWTClaims{}, func(token *jwt.Token) (interface{}, error) {
			return []byte(a.config.JWT.Token), nil
		})
		if err != nil {
			gCtx.AbortWithStatus(http.StatusForbidden)
			log.Println(err)

			return
		}

		myClaims := token.Claims.(*ds.JWTClaims)

		for _, oneOfAssignedRole := range assignedRoles {
			if myClaims.Role == oneOfAssignedRole {
				gCtx.AbortWithStatus(http.StatusForbidden)
				log.Printf("role %s is not assigned in %s", myClaims.Role, assignedRoles)

				return
			}
		}

	}

}
```

Теперь чтобы получить MW с нужным интерфейсом, мы вызываем функцию,
которая нам вернет анонимную функцию, сгенерированную ровно так как мы хотим(будет давать доступ только переданным
роялм):

```go
...
// никто не имеет доступа
r.Use(a.WithAuthCheck()).GET("/ping", a.Ping)
// или ниженаписанное значит что доступ имеют менеджер и админ
r.Use(a.WithAuthCheck(role.Manager, role.Admin)).GET("/ping", a.Ping)
...
```

Аналогичным образом будем ограничивать и другие эндпоинты.
Теперь поправим ранее написанную авторизацию, чтобы использовался только пользователь, который ранее регистрировался.

Важно заметить, что в текущей реализации права могут выдаваться только вручную(но думаю поправить это у вас не составит
проблем).

Правки:

Добавим в репозиторий метод получающий по логину(у нас Name) пользователя.

```go
func (r *Repository) GetUserByLogin(login string) (*ds.User, error) {
user := &ds.User{
Name: "login",
}

err := r.db.First(user).Error
if err != nil {
return nil, err
}

return user, nil
}
```

Добавим в эндпоинт логин логику взятия пользователя из базы данных:

```go
func (a *Application) Login(gCtx *gin.Context) {
cfg := a.config
req := &loginReq{}

err := json.NewDecoder(gCtx.Request.Body).Decode(req)
if err != nil {
gCtx.AbortWithError(http.StatusBadRequest, err)

return
}

user, err := a.repo.GetUserByLogin(req.Login)
if err != nil {
gCtx.AbortWithError(http.StatusInternalServerError, err)

return
}

if req.Login == user.Name && user.Pass == generateHashString(req.Password) {
// значит проверка пройдена
// генерируем ему jwt
token := jwt.NewWithClaims(cfg.JWT.SigningMethod, &ds.JWTClaims{
StandardClaims: jwt.StandardClaims{
ExpiresAt: time.Now().Add(cfg.JWT.ExpiresIn).Unix(),
IssuedAt:  time.Now().Unix(),
Issuer:    "bitop-admin",
},
UserUUID: uuid.New(), // test uuid
Role:     user.Role,

})

if token == nil {
gCtx.AbortWithError(http.StatusInternalServerError, fmt.Errorf("token is nil"))

return
}

strToken, err := token.SignedString([]byte(cfg.JWT.Token))
if err != nil {
gCtx.AbortWithError(http.StatusInternalServerError, fmt.Errorf("cant create str token"))

return
}

gCtx.JSON(http.StatusOK, loginResp{
ExpiresIn:   cfg.JWT.ExpiresIn,
AccessToken: strToken,
TokenType:   "Bearer",
})
}

gCtx.AbortWithStatus(http.StatusForbidden) // отдаем 403 ответ в знак того что доступ запрещен
}
```

Проверим эту комбинацию:

- Завели нового пользователя
- Делаем логин(получили JWT)
- Пробуем сделать пинг с ролью байер(сейчас пинг доступен только менеджеру и админу) - получаем 403
- Обновим роль max до администратора, выставим в бд цифру 2. Повторим авторизацию и получим 200 ответ.
- Обновим доступ к эндпоинту и проверим ее с другой комбинацией прав. Убедитесь что все работет как мы задумали.

```shell
bmstu.public> UPDATE public.users SET role = 2 WHERE uuid = '90461663-12f6-400c-83f1-dca48fe0b84f' AND name LIKE 'max' ESCAPE '#' AND role = 0 AND pass LIKE '40bd001563085fc35165329ea1ff5c5ecbdbbeef' ESCAPE '#' AND ctid = '(0,1)'
```

Таким образом мы получили примитивную ролевую модель. Какие у нее есть минусы и плюсы:

Плюсы:

+ Простота реализации
+ Роль хранится в токене на стороне пользователя и нам не нужно ходить в бд чтобы проверять его права.
+ Удобно передаем в MW роли которые имеют доступ к эндпоинту

Минусы: 
- Чтобы изменились права токена нужно заново авторизовать пользователя
- Нет гибкой настройки, могут быть 2 менеджера с разными права, что делать тогда?
- Пароли храняться в sha хэше и их можно подобрать по радужным таблицам
- Нужно перезагружать сервер чтобы менять доступы к эндпоинтам
- Нет разлогинивания

Однако, все же у нас получилось разграничить доступ и создать пусть и примитивную,
но все же удобную ролевую модель!

# 7. Refresh Token и logout
### Refresh Token
Думаю каждый обратил внимание что токен не может жить вечно. После вызова ```/login```
вам возвращается поле в JSON: ```    "expires_in": 3600000000000```.
Когда истекает токен - он становится недействительным, в этот момент вам придется залогиниваться снова.
Но ведь разные популярные сервисы, которые пользуются JWT не делают этого!
Тогда на помощь вам приходят refresh токены. Они так же имеют срок жизни, это тот же JWT,
только этот токен позволит вам обновить ваш основной токен(ротировать его на новый).
Таким образом фронтенд будет получать 2 токена - рефереш и основной,
по основному он будет запрашивать эндпоинты, по рефреш токену - будет обновлять ваш основной токен(и рефреш тоже).
Подробнее про refresh токены вы можете почитать на https://habr.com/en/post/466929/.
Так же уменьшив время ротирования токена на фронтенде у вас быстрее будут обновляться права(если вы их оставляеете в jwt)

### Logout. Создаем блеклист с использованием redis.
Чтобы реализовать Logout нам необходимо сохранять в хранилище токены, которые были разлогинены.
Для этого будем использовать Redis.
Зачем он нам? 
Ответ прост - если вдруг вы перезагружаете приложение вы не потеряете разлогиненных пользователей.
При этом redis - NoSQL хранилище. Оно работает в разы быстрее реляционных БД.


Redis (Remote Dictionary Service) — это опенсорсный сервер баз данных типа ключ-значение.
Чем-то напоминает хэш мап не так ли?
Обычно его используют в качетсве кеша,
он умеет хранить какие-то значения только определенное время и потом удалять.

Однако иногда его так же используют как хранилище.
В этой части нашей лабораторной работы мы свами научимся им пользоваться и реализуем с помощью него logout.


Ключи в redis. При использовании redis есть золотое правило,
которое помогает значениям в redis из 2 разных сервисов не иметь общего ключа - добавлять префиксы
с разделителем `.`.

В данной части ЛР мы будем использовать пакет `"github.com/go-redis/redis/v8"`

Для редиса как и для любого другого хранилища нужны данные чтобы к нему подключиться(в нашем случае мы не будем использовать пароль,
поскольку работа будет исключительно в образовательных целях).
Добавим в нашу конфигурацию конфигурацию отдельно для Redis:
```config.go```
```go
type Config struct {
	ServiceHost string
	ServicePort int

	BMSTUNewsConfig BMSTUNewsConfig
	FirstParse      FirstParse
	NewsServiceAddr string

	JWT JWTConfig
	Redis RedisConfig
}

type RedisConfig struct {
	Host        string
	Password    string
	Port        int
	User        string
	DialTimeout time.Duration
	ReadTimeout time.Duration
}
...
const (
   envRedisHost = "REDIS_HOST"
   envRedisPort = "REDIS_PORT"
   envRedisUser = "REDIS_USER"
   envRedisPass = "REDIS_PASSWORD"
)
...
/// в New добавим 

cfg.Redis.Host = os.Getenv(envRedisHost)
cfg.Redis.Port, err = strconv.Atoi(os.Getenv(envRedisPort))

if err != nil {
return nil, fmt.Errorf("redis port must be int value: %w", err)
}

cfg.Redis.Password = os.Getenv(envRedisPass)
cfg.Redis.User = os.Getenv(envRedisUser)

```


`config/config.toml`

```toml
# НАСТРОЙКИ РЕДИСКИ
[Redis]

# Таймауты в миллисекундах
DialTimeout = "10s"
ReadTimeout = "10s"
```
`.env`
```dotenv
REDIS_HOST=0.0.0.0
REDIS_PORT=6379
REDIS_USER=""
REDIS_PASSWORD="password"
```

Создадим пакет redis `internal/app/redis/redis.go`
```go
package redis

import (
	"awesomeProject/internal/app/config"
	"context"
	"fmt"
	"github.com/go-redis/redis/v8"
	"strconv"
	"time"
)

const servicePrefix = "awesome_service." // наш префикс сервиса

type Client struct {
	cfg    config.RedisConfig
	client *redis.Client
}

func New(ctx context.Context, cfg config.RedisConfig) (*Client, error) {
	client := &Client{}

	client.cfg = cfg

	redisClient := redis.NewClient(&redis.Options{
		Password:    cfg.Password
		Username:    cfg.User,
		Addr:        cfg.Host + ":" + strconv.Itoa(cfg.Port),
		DB:          0,
		DialTimeout: cfg.DialTimeout,
		ReadTimeout: cfg.ReadTimeout,
	})

	client.client = redisClient

	if _, err := redisClient.Ping(ctx).Result(); err != nil {
		return nil, fmt.Errorf("cant ping redis: %w", err)
	}

	return client, nil
}

func (c *Client) Close() error {
	return c.client.Close()
}
```

Добавим создание redis в `internal/pkg/app/app.go`

`app.go`
```go
package app

import (
	"awesomeProject/internal/app/redis"
	"context"
	"log"

	"awesomeProject/internal/app/config"
	"awesomeProject/internal/app/dsn"
	"awesomeProject/internal/app/repository"
)

type Application struct {
	config *config.Config
	repo   *repository.Repository
	redis *redis.Client
}

func New(ctx context.Context) (*Application, error) {
	cfg, err := config.NewConfig(ctx)
	if err != nil {
		return nil, err
	}

	repo, err := repository.New(dsn.FromEnv())
	if err != nil {
		return nil, err
	}

	redisClient, err := redis.New(ctx, cfg.Redis)
	if err != nil {
		return nil, err
	}
	
	return &Application{
		config: cfg,
		repo:   repo,
		redis: redisClient,
	}, nil
}

func (a *Application) Run() error {
	log.Println("application start running")
	a.StartServer()
	log.Println("application shut down")

	return nil
}
```
Запустите ваш сервис и проверьте что ping к редису при создании вашего сервиса проходит.
Если сервис запустился - значит вы все сделали верно и ваше приложение держит соединение с redis.

Добавим к нашему клиенту к редису методы которые будут добавлять JWT в блеклист на время пока не истечет токен
(чтобы не переполнить Redis, смысл хранить токен в блеклисте есть до тех пор пока он не истечет.).
Это будут 2 метода - запиши, проверь есть ли такой токен в блеклисте:
`internal/app/redis/jwt.go`
```go
package redis

import (
	"context"
	"time"
)

const jwtPrefix = "jwt."

func getJWTKey(token string) string {
	return servicePrefix + jwtPrefix + token
}

func (c *Client) WriteJWTToBlacklist(ctx context.Context, jwtStr string, jwtTTL time.Duration) error {
	return c.client.Set(ctx, getJWTKey(jwtStr), true, jwtTTL).Err()
}

func (c *Client) CheckJWTInBlacklist(ctx context.Context, jwtStr string) error {
	return c.client.Get(ctx, getJWTKey(jwtStr)).Err()
	// если токена нет, то вернется ошибка not exists
}
```

Как проверить записи в Redis? 

Это хороший вопрос и я бы с радостью также посоветовал вам DataGrip. 
[Однако JetBrains обещают добавить поддержку Redis лишь в версии 2022.3 ](https://blog.jetbrains.com/datagrip/2022/11/02/datagrip-2022-3-eap-2-redis-support/). 
(история же тянется уже 6 лет https://youtrack.jetbrains.com/issue/DBE-283).
Потому в нашем случае будем пользоваться любым доступным клиентом(или проверкой на коде).
Я же воспользуюсь ранним релиз кандидатом JetBrains(на свой страх и риск).
Можете установить кандидата в релиз с помощью JetBrains Toolbox ![Создание проекта](docs/5.png)
![Создание проекта](docs/6.png)

Добавим эндпоинт на logout.

```go
func (a *Application) Logout(gCtx *gin.Context) {
	// получаем заголовок
	jwtStr := gCtx.GetHeader("Authorization")
	if !strings.HasPrefix(jwtStr, jwtPrefix) { // если нет префикса то нас дурят!
		gCtx.AbortWithStatus(http.StatusBadRequest) // отдаем что нет доступа

		return // завершаем обработку
	}

	// отрезаем префикс
	jwtStr = jwtStr[len(jwtPrefix):]

	_, err := jwt.ParseWithClaims(jwtStr, &ds.JWTClaims{}, func(token *jwt.Token) (interface{}, error) {
		return []byte(a.config.JWT.Token), nil
	})
	if err != nil {
		gCtx.AbortWithError(http.StatusBadRequest, err)
		log.Println(err)

		return
	}

	// сохраняем в блеклист редиса
	err = a.redis.WriteJWTToBlacklist(gCtx.Request.Context(), jwtStr, a.config.JWT.ExpiresIn)
	if err != nil {
		gCtx.AbortWithError(http.StatusInternalServerError, err)

		return
	}

	gCtx.Status(http.StatusOK)
}
```

Попробуем выполнить авторизацию и сделать logout  с этим токеном. 
После проверим что запись в redis создалась.
![Создание проекта](docs/6.png)

Добавляем в нашу MW проверку на то что токена нет в блеклисте:
```go
package app

import (
   "awesomeProject/internal/app/ds"
   "awesomeProject/internal/app/role"
   "errors"
   "github.com/gin-gonic/gin"
   "github.com/go-redis/redis/v8"
   "github.com/golang-jwt/jwt"
   "log"
   "net/http"
   "strings"
)

const jwtPrefix = "Bearer "

func (a *Application) WithAuthCheck(assignedRoles ...role.Role) func(ctx *gin.Context) {
   return func(gCtx *gin.Context) {
      jwtStr := gCtx.GetHeader("Authorization")
      if !strings.HasPrefix(jwtStr, jwtPrefix) { // если нет префикса то нас дурят!
         gCtx.AbortWithStatus(http.StatusForbidden) // отдаем что нет доступа

         return // завершаем обработку
      }

      // отрезаем префикс
      jwtStr = jwtStr[len(jwtPrefix):]
      // проверяем jwt в блеклист редиса
      err := a.redis.CheckJWTInBlacklist(gCtx.Request.Context(), jwtStr)
      if err == nil { // значит что токен в блеклисте
         gCtx.AbortWithStatus(http.StatusForbidden)

         return
      }
      if !errors.Is(err, redis.Nil) { // значит что это не ошибка отсуствия - внутренняя ошибка
         gCtx.AbortWithError(http.StatusInternalServerError, err)

         return
      }

      token, err := jwt.ParseWithClaims(jwtStr, &ds.JWTClaims{}, func(token *jwt.Token) (interface{}, error) {
         return []byte(a.config.JWT.Token), nil
      })
      if err != nil {
         gCtx.AbortWithStatus(http.StatusForbidden)
         log.Println(err)

         return
      }

      myClaims := token.Claims.(*ds.JWTClaims)

      for _, oneOfAssignedRole := range assignedRoles {
         if myClaims.Role == oneOfAssignedRole {
            gCtx.Next()
         }
      }
      gCtx.AbortWithStatus(http.StatusForbidden)
      log.Printf("role %s is not assigned in %s", myClaims.Role, assignedRoles)

      return

   }

}
```
После вышеперечисленных операций проверьте что вся логика работает - роли назаначаются, токен попадает в блеклист.
После попадания в блеклист он не действителен.

Поздравляю вас! Вы научились писать самую простую ролевую модель и использовать Redis в своих целях!
# 8. Полезные ссылки

- Все про JWT - https://habr.com/en/post/340146/.
- Библиотека, которую мы используем для JWT - github.com/golang-jwt/jwt
- JWT RFC - https://www.rfc-editor.org/rfc/rfc7519
- Что такое RFC - https://ru.wikipedia.org/wiki/RFC
- Refresh Token - https://habr.com/en/post/466929/
- Библиотека redis, которую мы используем - github.com/go-redis/redis
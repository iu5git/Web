# Методические указания по выполнению лабораторной работы №7

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
в результате выполнения которой для субъекта идентификации выявляется его идентификатор, однозначно определяющий этого субъекта в информационной системе.

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
3. Когда пользователь делает запрос к API приложения, он добавляет к нему в заголовок Authorization с префиксом Bearer полученный ранее JWT.
4. Когда пользователь делает API запрос, приложение может проверить по переданному с запросом JWT является ли пользователь тем, за кого себя выдает.
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

Научимся создавать JWT. Будем использовать библиотеку 	"github.com/golang-jwt/jwt"

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
	jwt.StandardClaims                                  // все что точно необходимо по RFC
	UserUUID  uuid.UUID `json:"user_uuid"`             // наши данные - uuid этого пользователя в базе данных
	Scopes    []string  `json:"scopes" json:"scopes"` // список доступов в нашей системе
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

Это очень удобно для нас разграничивать эндпоинты, к которым пользователь имеет полный доступ вне зависимости от авторизации
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
# 5. Разрабатываем ролевую модель и регистрацию.
# 6. Реализуем ролевую модель на основе JWT
# 7. Refresh Token
# 8. Полезные ссылки
- Все про JWT - https://habr.com/en/post/340146/. 
- Библиотека, которую мы используем для JWT - github.com/golang-jwt/jwt
- JWT RFC - https://www.rfc-editor.org/rfc/rfc7519
- Что такое RFC - https://ru.wikipedia.org/wiki/RFC
# Методические указания по выполнению лабораторной работы №2

## Настройка БД
Про настройку БД можно почитать в отдельном разделе.

## Масштабируем проект
### Про конфигурацию и переменные окружения
Так или иначе прежде чем запустить проект хочется менять в нем
какие-то параметры(на каком порту запустить, какую информацию писать в лог)

Потому есть 2 основных способа передачи конфигурации вашему приложению:
- файлы конфигурации
- переменные окружения
#### Поговорим про файлы конфигурации
Файл конфигурации - обычный текстовый файл, в каком-либо общеизвестном 
или общепринятом формате, например: .yml, .yaml, .toml, .json, .hcl, .config

Все эти файлы - просто текстовые, с одним небольшим условием,
что декларативное описание сущностей(каких-то параметров) ведется в определенном
стандартизированном формате, приведем пару примеров файлов конфигурации:

```config.toml```
```toml 
ServiceHost = "0.0.0.0" # просто ключ значение
ServicePort = 80

[BMSTUNewsConfig] # вложенный объект
SiteAddress = "api.www.bmstu.ru" # значения полей этого объекта
Protocol = "https"
DayLimit = 30
```
```config.yaml```
```yaml
service_host: "0.0.0.0" # просто ключ значение
service_port: 80
bmstu_news_config:
  site_address: "api.www.bmstu.ru"
  protocol: "https"
  day_limit: 30
```

Для нашего проекта давайте создадим файл конфигурации в `/config/config.toml`
```dotenv
ServiceHost = "0.0.0.0"
ServicePort = 80 
```
#### Поговорим про переменные окружения
Для начала приведем определение:
Переменные окружения — именованные переменные, содержащие текстовую информацию, которую могут использовать запускаемые программы. Такие переменные могут содержать общие настройки системы, параметры графической или командной оболочки, данные о предпочтениях пользователя и многое другое.

Выведем переменные окружения которые сейчас у нас есть. Для этого в консоли введем(далее мы не будем говорить,
что что-то нужно ввести в коносль, вам об этом говорит знак $ - это просто строка приглашения в Linux терминалах.
Он означает что вы работаете под обычным пользователем, а # - под root. Это и есть его основное назначение, никаких дополнительных функций в этом символе нет):
```shell
$ env
PWD=/Users/maxim-konovalov/MyProj/web-2022/tutorials
OLDPWD=/Users/maxim-konovalov/MyProj/web-2022/tutorials
HOMEBREW_PREFIX=/opt/homebrew
HOMEBREW_CELLAR=/opt/homebrew/Cellar
HOMEBREW_REPOSITORY=/opt/homebrew
MANPATH=/opt/homebrew/share/man::
INFOPATH=/opt/homebrew/share/info:
_=/usr/bin/env
...
```
Запишем свою переменную:
```shell
$ export test=123
```
Проверим ее наличие:
```shell
$ env | grep 123   # | grep 123 значит что вы передаете выходной поток утилите grep, эта утилита позволяет осуществлять поиск
test=123
```

Переменные окружения - key value значния, которые могту быть локальными и глобальными(локальные - видно только в конкретной директории,
глобальные - видно во всех директориях, например переменная PWD или PATH). С помощью них можно так же передавать 
данные вашему сервису, обычно ее используют, чтобы передавать и обмениваться секретными данными пользователь-сервис, сервис - сервис
### Новое устройство проекта и чтение конфигурации
Частично расширим возможности нашего проекта и поменяем его структуру.
Модифицируем расположение папок в нашем проекте:
Добавим:
- internal/app/config # пакет читающий конфигурацию из /config/config.toml (любой формат)
- internal/app/repository # пакет отвечающий за обращения к хранилищам данных(БД)
- internal/pkg/app # Основная часть нашего приложения - оно создает подключение к базе данных, веб сервер, создает конфиг. Может создаваться и стартоваться.
- internal/app/dsn # пакет формирующий DSN - строку подключения к postgresql
- .env  # файл, который определяет переменные окружения в вашей текущей папки(локальный энв)
- internal/app/ds # пакет в котором будут храниться структуры данных, которые мы храним в базе данных

Создадим тип Application в пакете ```app```. Пусть у него будет 1 метод Run.
А в пакете появится публичная функция New(), которая будет возвращать Application.
Функция New должна создавать объект Application, заполнять его конфигом, роутером веб сервера, подключением к базе данных.

В пакете DSN добавим 1 новый публичный метод. 
```go
package dsn

import (
	"fmt"
	"os"
)

// FromEnv собирает DSN строку из переменных окружения
func FromEnv() string {
	host := os.Getenv("DB_HOST")
	if host == "" {
		return ""
	}

	port := os.Getenv("DB_PORT")
	user := os.Getenv("DB_USER")
	pass := os.Getenv("DB_PASS")
	dbname := os.Getenv("DB_NAME")

	return fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable", host, port, user, pass, dbname)
}
```
В пакете config добавим 1 публичный метод:
```go
package config

import (
	"context"
	"os"
	"time"

	"github.com/joho/godotenv"
	log "github.com/sirupsen/logrus"
	"github.com/spf13/viper"
)

// Config Структура конфигурации;
// Содержит все конфигурационные данные о сервисе;
// автоподгружается при изменении исходного файла
type Config struct {
	ServiceHost string
	ServicePort int
}

// NewConfig Создаёт новый объект конфигурации, загружая данные из файла конфигурации
func NewConfig(ctx context.Context) (*Config, error) {
	var err error

	configName := "config"
	_ = godotenv.Load()
	if os.Getenv("CONFIG_NAME") != "" {
		configName = os.Getenv("CONFIG_NAME")
	}

	viper.SetConfigName(configName)
	viper.SetConfigType("toml")
	viper.AddConfigPath("config")
	viper.AddConfigPath(".")
	viper.WatchConfig()

	err = viper.ReadInConfig()
	if err != nil {
		return nil, err
	}

	cfg := &Config{}
	err = viper.Unmarshal(cfg)
	if err != nil {
		return nil, err
	}

	log.Info("config parsed")

	return cfg, nil
}

```

Итого мы получаем следующую цепочку пакетов:
* В main - создаем application, пишем логи что мы запустились
* В app - при вызове New - создаем объект, у которого есть роутер,репозиторий и конфиг, 
* application.Run - запускает веб сервер
* В репозитории - публичный метод New() для создания объекта репозитория
* В конфиге - метод New() для создания метода конфигурации
* В api - описания всех наших эндпоинтов

Важно: далее увеличивать и улучшать наш проект по структуре мы не будем,
потому лучше изначально усвоить назначения каждого пакета.
## Обращаемся к базе из кода
Чтобы создать обращение к базе вам необходима строка DSN.
Давайте договоримся что все данные о базе данных мы будем передавать не через конфиг,
а через .env(будем считать что так безопаснее).
Создадим в корне проекта файл .env:
```dotenv
DB_HOST=0.0.0.0
DB_NAME=bmstu
DB_PORT=5432
DB_USER=bmstu_user
DB_PASS=bmstu_password
```
Будем использовать ORM [gorm](https://gorm.io/docs/index.html).
Прежде чем пойти дальше, давайте скажем что у нас есть предметная область магазин компьютерной техники.
Прежде чем приступать к работе с пакетом Repository, давайте создадим миграции данных, создадим данные в таблице из кода:
Создадим ```internal/app/ds/proudcts.go```. И опишем новую таблицу:
```go
package ds

import (
	"gorm.io/gorm"
)

type Product struct {
	ID        uint `gorm:"primarykey"`
	Code  string
	Price uint
}

```
Создадим ```cmd/migrate/main.go```. 
Это будет наш скрипт, который будет выполнять миграцию.
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
	err = db.AutoMigrate(&ds.Product{})
	if err != nil {
		panic("cant migrate db")
	}
}
```
Проверьте в вашей IDE для БД, что ваша миграция прошла успешно.

Создадим пакет Repository:
По сути для нас этот пакет будет выглядеть следующим образом:
- New() - возвращает новый объект
- repo.GetCPUs() - возвращает список всех cpu
- repo.GetAllProducts() - возвращает вообще весь список товаров
- repo.GetMotherboards() - возвращает все материнские платы
- и другие ГОВОРЯЩИЕ методы.
Будьте к этому внимательны,
иначе можно забыть что делает этот метод и потратить время на изучение кода.
В нашем случае получилось так:
```go
package repository

import (
	"gorm.io/driver/postgres"
	"gorm.io/gorm"

	"awesomeProject/internal/app/ds"
)

type Repository struct {
	db *gorm.DB
}

func New(dsn string) (*Repository, error) {
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		return nil, err
	}

	return &Repository{
		db: db,
	}, nil
}

func (r *Repository) GetProductByID(id int) (*ds.Product, error) {
	product := &ds.Product{}

	err := r.db.First(product, "id = ?", "1").Error // find product with id = 1
	if err != nil {
		return nil, err
	}

	return product, nil
}

func (r *Repository) CreateProduct(product ds.Product) error {
	return r.db.Create(product).Error
}

```
Теперь давайте убедимся, что оно работает и подключим 2 наши части: web server и repository:

`server.go`
```go
package app

import (
	"log"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

func (a *Application) StartServer() {
	log.Println("Server start up")

	r := gin.Default()

	r.GET("/product", func(c *gin.Context) {
		id := c.Query("id") // получаем из запроса query string

		if id != "" {
			log.Printf("id recived %s\n", id)
			intID, err := strconv.Atoi(id) // пытаемся привести это к числу
			if err != nil {                // если не получилось
				log.Printf("cant convert id %v", err)
				c.Error(err)
				return
			}
			// получаем данные по товару
			product, err := a.repo.GetProductByID(uint(intID))
			if err != nil { // если не получилось
				log.Printf("cant get product by id %v", err)
				c.Error(err)
				return
			}

			c.JSON(http.StatusOK, gin.H{
				"product_price": product.Price,
			})
			return
		}
		c.JSON(http.StatusOK, gin.H{
			"message": "try with id",
		})
	})

	r.LoadHTMLGlob("templates/*")

	r.GET("/test", func(c *gin.Context) {
		c.HTML(http.StatusOK, "test.tmpl", gin.H{
			"title": "Main website",
			"test":  []string{"a", "b"},
		})
	})

	r.Static("/image", "./resources")

	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")

	log.Println("Server down")
}

```
Вручную добавим запись с id=1.
Пробуем сделать запрос:  http://127.0.0.1:8080/product?id=1 и получаем ответ:
```json
{"product_price":123}
```

Самостоятельное задание - добавить еще 1 query параметр в запрос  http://127.0.0.1:8080/ping - `?create=true` и если он указан записывать новое значение в таблицу со случайными параметрами.

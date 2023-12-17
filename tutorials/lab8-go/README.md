# Методические указания по выполнению лабораторной работы №8

## Задачи:
- Создать асинхронный сервис для выполнения долгой задачи
- Показать межсервисное взаимодействие между новым сервисом и сервисом из прошлых лабораторных

## Создание приложения на Go
В методических указаниях по [1 лабораторной](https://github.com/iu5git/Web/blob/main/tutorials/lab1-go/README.md) описано, как создать проект на Go.

Создадим приложение с использованием  фреймворка gin-gonic, как это делалось в [3](https://github.com/iu5git/Web/tree/main/tutorials/lab3-go) и [5](https://github.com/iu5git/Web/tree/main/tutorials/lab5-go) лабораторных.

## Синхронный веб-сервер
В этой лабораторной мы хотим показать межсерверное взаимодействие. Мы создадим новый веб-сервер, который будет принимать запросы с pk объекта из БД основного сервера из предыдущих работ. Затем новый веб-сервер "рассчитает" новое значение для какого-то поля этого объекта и отправит PUT-запрос к основному серверу. 

В примере мы будем случайно менять логическое поле `IsGrowing` объектов-акций. Функция для "расчётов" `randomStatus`:

```go
import (
	"math/rand"
	"time"
)

func randomStatus() bool {
	rand.Seed(time.Now().UnixNano())
	return rand.Intn(2) == 0
}
```

Для отправки PUT-запроса будем использовать модуль net/http. Для синхронного сервера напишем функцию `performPUTRequest`:
```go
import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
)

// Ваша структура с булевской переменной
type Result struct {
	IsGrowing bool `json:"is_growing"`
}

func performPUTRequest(url string, data Result) (*http.Response, error) {
	// Сериализация структуры в JSON
	jsonData, err := json.Marshal(data)
	if err != nil {
		return nil, err
	}

	// Создание PUT-запроса
	req, err := http.NewRequest("PUT", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, err
	}

	req.Header.Set("Content-Type", "application/json")

	// Выполнение запроса
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}

	defer resp.Body.Close()

	return resp, nil
}
```
Добавим обработчик POST-метода `set_status`, который: 
- принимает запрос с полем "pk" 
- получает результат "расчётов" от `randomStatus`
- отправляет PUT-запрос к основному серверу с помощью `performPUTRequest`

```go
import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
)

func main() {
...
	// Обработчик POST-запроса для set_status
	r.POST("/set_status", func(c *gin.Context) {
		// Получение значения "pk" из запроса
		pk := c.PostForm("pk")

		// Выполнение расчётов с randomStatus
		result := randomStatus()

		// Отправка PUT-запроса к основному серверу
		url := "https://example.com/put-endpoint" // Замените на ваш реальный URL
		data := Result{IsGrowing: result}
		response, err := performPUTRequest(url, data)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		// Проверка статуса ответа
		if response.StatusCode == http.StatusOK {
			c.JSON(http.StatusOK, gin.H{"message": "PUT request processed successfully"})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{"message": "Failed to process PUT request"})
		}
	})

...
}
```

## Асинхронный веб-сервер 

Может так случиться, что дополнительный веб-сервер выполняет расчёты слишком долго. Это можно сымитировать с помощью time.sleep в `randomStatus` 

```go
// Функция для генерации случайного статуса
func randomStatus() bool {
	time.Sleep(5 * time.Second) // Задержка на 5 секунд
	rand.Seed(time.Now().UnixNano())
	return rand.Intn(2) == 0
}
```
В таком случае основной сервер будет слишком долго дожидаться ответа 200 OK и может быть даже зависнет-в-ожидании (если выполнял запрос к вспомогательному серверу в своём основном потоке, где обрабатывает и всё остальное).

Мы хотим, чтобы сервер быстро отвечал на запрос, а долгая задача randomStatus() запускалась "в фоновом режиме". `performPUTRequest` должна же отправлять PUT-запрос к основному серверу именно тогда, когда долгая задача `randomStatus` закончится.

Для запуска задач в фоновом режиме можно использовать goroutine (Горутины). Горутины обычно используют для распараллеливания задачи на легковесные потоки.

```go
// Функция для отправки статуса в отдельной горутине
func SendStatus(pk string, url string) {
	// Выполнение расчётов с randomStatus
	result := randomStatus()

	// Отправка PUT-запроса к основному серверу
	data := MyData{Flag: result}
	_, err := performPUTRequest(url, data)
	if err != nil {
		fmt.Println("Error sending status:", err)
		return
	}

	fmt.Println("Status sent successfully for pk:", pk)
}
```
Теперь наш обработчик POST-запроса запустит задачу SendStatus (с параметром pk) в фоновом режиме и тут же продолжит выполнение (отправит ответ 200 OK основному серверу).
Помещение задачи `SendStatus` в горутину выглядит как-то так: 
```go
// Обработчик POST-запроса для set_status
	r.POST("/set_status", func(c *gin.Context) {
		// Получение значения "pk" из запроса
		pk := c.PostForm("pk")

		// Запуск горутины для отправки статуса
		go SendStatus(pk, "https://example.com/put-endpoint") // Замените на ваш реальный URL

		c.JSON(http.StatusOK, gin.H{"message": "Status update initiated"})
	})
```

# Методические указания по Асинхронным сервисам

## Задачи:
- Создать асинхронный сервис для выполнения долгой задачи
- Показать межсервисное взаимодействие между новым сервисом и сервисом из прошлых лабораторных

## Создание приложения на Rust
1. **Подготовка окружения.** Ранее мы уже установили Rust на наше устройство для работы с Tauri, так что нам не придется устанавливать что-то новое. 
2. **Инициализация проекта.** Для создания любого проекта на Rust для начала требуется создавать рабочую директорию, для этого выполним в терминале команду `cargo new [название проекта]` для созадния новой папки инициализации прокта уже в ней или команду `npm init [название проекта]` для инициализации проетка в текущей директории. После этого, структура нашего проекта будет выглядеть следующим образом:
```
├── Cargo.toml
└── src
    └── main.rs
```
3. **Установка библиотек.** Как мы уже знаем, для установки библиотек в Rust используется команда `cargo add [имя библиотеки]`. Также мы можем самостоятельно добавить библиотеку в `Cargo.toml` в секцию `[dependencies]`. После этого нам необходимо выполнить команду `cargo update` для обновления зависимостей.
  В нашем асинхронном сервисе мы будем использовать библиотеки:
  - `tokio` - для выполненния асинхронных операций
  - `reqwest` - для выполнения HTTP-запросов
  - `serde` - для сериализации и десериализации данных
  - `serde_json` - для работы с JSON
  - `dotenv` - для работы с переменными окружения
  - `actix-web` - для создания веб-сервера
  - `rand` - для генерации случайного времени выполнения расчета

  Конечный вид будет следующим:

  ``` rust
  [package]
  name = "async_service"
  version = "0.1.0"
  edition = "2024"
  
  [dependencies]
  tokio = { version = "1", features = ["rt-multi-thread", "macros", "time"] }
  reqwest = { version = "0.11", features = ["json"] }
  serde = { version = "1", features = ["derive"] }
  serde_json = "1"
  dotenv = "0.15"
  actix-web = "4"
  rand = "0.8.5"
  ```
## Начало разработки. Структура данных, выполнение расчетов и тесты
Начнем разработку нашего асинхронного сервиса с создания структуры входящих и выходящих данных, а также выполнения расчетов.
Для начала в папке `src` создадим файл `models.rs` с нашими структурами и `.env` файл с переменными окружения. В данном примере в качестве входящих данных я буду использовать массивы `input_fields` и `constants`.
``` rust
// models.rs
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct CalcRequest {
    pub id: i32,
    pub auth_token: String,
    pub input_fields: Vec<f32>, 
    pub constants: Vec<f32>,
}

#[derive(Serialize)]
pub struct CalcResponse {
    pub id: i32,
    pub calculation_result: f32,
}
```
В рамках данной лабораторной работы для конфигурации асинхронного сервиса используется файл `.env`, содержащий параметры окружения (адрес и порт сервера, токен авторизации и т.п.).

Файл `.env` предназначен для:

- хранения конфигурационных параметров, зависящих от среды выполнения;
- исключения жёстко заданных значений (hardcoded) из исходного кода;
- упрощения развертывания сервиса на разных машинах и в разных средах (локальная разработка, тестирование).

Загрузка переменных окружения осуществляется с помощью библиотеки dotenv. Следует учитывать, что:
- файл `.env` не должен добавляться в систему контроля версий;
- значения переменных окружения считаются потенциально чувствительными;

Использование переменных окружения позволяет отделить логику приложения от конфигурации и является общепринятой практикой при разработке серверных приложений и микросервисов.
``` rust
// .env
LISTEN_PORT = 8083
HOST = localhost
ASYNC_TOKEN = secret
```
Далее напишем функцию для выполнения самих расчетов. Для этого создадим файл `calculation.rs` с функцией `calculate`.
``` rust
// calculation.rs
use crate::models::CalcRequest;
use rand::Rng;
use std::env;
use tokio::time::{Duration, sleep};

pub async fn calculate(req: &CalcRequest) -> f32 {
    dotenv::dotenv().ok(); // временное решение загрузки переменной из окружения
    // в дальнейшем мы будем использовать эту фунццию в другом файле, чтобы не загружать ее каждый разработку
    // при вызове функции расчета
    if req.auth_token != env::var("ASYNC_TOKEN").unwrap() {
        return 0.0;
    }
    let delay = rand::thread_rng().gen_range(5..=10);
    let mut result = 0.0;
    for (input, constant) in req.input_fields.iter().zip(req.constants.iter()) {
        result += input * constant;
    }
    sleep(Duration::from_secs(delay)).await;
    return result;
}
```
Также временно добавим все существующие функции в main.rs, чтобы компилятор не жаловался на их неиспользование
``` rust
mod calculation;
mod models;

fn main() {
    let req = models::CalcRequest {
        id: 1,
        auth_token: "".to_string(),
        input_fields: vec![1.0, 2.0, 3.0],
        constants: vec![0.5, 1.0, 1.5],
    };
    let _ = models::CalcResponse {
        id: 1,
        calculation_result: 1.0,
    };
    let _ = calculation::calculate(req);
}

```
Язык Rust предоставляет встроенные средства для модульного тестирования, которые могут использоваться непосредственно в файлах с исходным кодом. Для асинхронных функций применяется специальная форма тестов с использованием асинхронного рантайма. Для этого мы можем использовать макрос `#[cfg(test)]` и функцию `#[test]`. Давайте напишем тест для нашей функции `calculate`.
``` rust
// calculation.rs
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test] // используем библиотеку tokio для асинхронного теста
    async fn test_calculate() {
        let req = CalcRequest {
            id: 1,
            auth_token: "secret".to_string(),
            input_fields: vec![1.0, 2.0, 3.0],
            constants: vec![0.5, 1.0, 1.5],
        };
        let result = calculate(&req).await;
        assert_eq!(result, 7.0);
    }
}
```
Чтобы проверить работу функции с помощью теста воспользуемся командой `cargo test` в терминале. Если тесты прошли успешно, в терминале будет выведено сообщение `test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out`

## Асинхронный сервис
После создания структуры данных можем приступить к разработке самого асинхронного сервиса. В данной лабораторной работе асинхронный сервис предназначен для выполнения длительных вычислений без блокировки обработки HTTP-запросов.
Ключевая идея асинхронности заключается в следующем:
* HTTP-обработчик принимает запрос и немедленно возвращает ответ клиенту;
* сама вычислительная задача запускается в фоновом режиме;
* по завершении вычислений результат отправляется в основной сервис отдельным HTTP-запросом.

Для реализации фонового выполнения используется асинхронная среда выполнения `tokio` и механизм запуска задач (spawn). Это позволяет:
* не блокировать поток обработки запросов;
* обслуживать несколько клиентов одновременно;
* моделировать поведение реального асинхронного сервиса, используемого в микросервисной архитектуре.

Важно отметить, что подобный подход широко применяется в системах, где время выполнения задачи существенно превышает допустимое время ожидания HTTP-ответа (например, обработка данных, генерация отчётов, машинное обучение).
Начнем с создания ручки для получения запроса от бэкенда. Создадим файл `src/handlers.rs` и напишем функцию `handle_request`:
``` rust
// handlers.rs
use crate::models::CalcRequest;
use actix_web::{HttpResponse, post, web};

#[post("/calculateResult")]
async fn handle_request(req: web::Json<CalcRequest>) -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({
        "message": "Data received successfully"
    }))
}
```
Создадим функцию `start_calculation`, которая будет вызываться сразу после получения запроса от бэкенда.
``` rust
// handlers.rs
use crate::{calculation::calculate, models::CalcRequest};
use actix_web::{HttpResponse, post, web};
use tokio::spawn;

#[post("/calculateResult")]
async fn handle_request(req: web::Json<CalcRequest>) -> HttpResponse {
    start_calculation(req.into_inner());
    HttpResponse::Ok().json(serde_json::json!({
        "message": "Data received successfully"
    }))
}

pub fn start_calculation(req: CalcRequest) {
    spawn(async move {
        let result = calculate(req).await;
    });
}
```
Сделаем так, чтобы наш после выполнения расчетов мы отправляли результат расчетов в наш бекэнд.
``` rust
// handlers.rs
use crate::{
    calculation::calculate,
    models::{CalcRequest, CalcResponse},
};
use actix_web::{HttpResponse, post, web};
use reqwest::Client;
use tokio::spawn;

#[post("/calculateResult")]
async fn handle_request(req: web::Json<CalcRequest>) -> HttpResponse {
    start_calculation(req.into_inner());
    HttpResponse::Ok().json(serde_json::json!({
        "message": "Data received successfully"
    }))
}

pub fn start_calculation(req: CalcRequest) {
    spawn(async move {
        let result = calculate(&req).await;
        if let Err(err) = send_result(req.id, result).await {
            eprintln!("Failed to send result to backend: {:?}", err);
        }
    });
}

pub async fn send_result(id: i32, calc_result: f32) -> Result<(), reqwest::Error> {
    let client = Client::new();

    client
        .put("http://localhost:8080/your-handler")
        .json(&CalcResponse {
            id: id,
            calculation_result: calc_result,
        })
        .send()
        .await?
        .error_for_status()?;

    Ok(())
}
```

## Сервер для асинхронного сервиса
Создадим файл `server.rs`.
``` rust
// server.rs
use crate::handlers::init;
use actix_web::{App, HttpServer};
use dotenv::dotenv;
use serde::Deserialize;
use std::env;

#[derive(Deserialize, Clone)]
pub struct Settings {
    pub host: String,
    pub port: u16,
}

impl Settings {
    pub fn new() -> Self {
        dotenv().ok();
        Self {
            host: env::var("HOST").unwrap(),
            port: env::var("LISTEN_PORT").unwrap().parse().unwrap(),
        }
    }
}

pub async fn start_server(settings: Settings) -> std::io::Result<()> {
    HttpServer::new(move || App::new().configure(init))
        .bind((settings.host.clone(), settings.port))?
        .run()
        .await
}

```
Добавим функцию для инициализации нашей ручки в файл `handlers.rs`
``` rust
// handlers.rs
pub fn init(cfg: &mut web::ServiceConfig) {
    cfg.service(handle_request);
}
```

А также изменим `main.rs`, чтобы он запускал сервер
``` rust
// main.rs
mod calculation;
mod handlers;
mod models;
mod server;
use crate::server::Settings;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let settings = Settings::new();
    server::start_server(settings).await
}

```

Теперь мы можем запустить сервер с помощью команды `cargo run`.

После выполнения всех пунктов методических указаний, проект будет иметь следующую структуру:
```
├── Cargo.toml
├── .env
└── src
    ├── main.rs
    ├── calculation.rs
    ├── handlers.rs
    ├── models.rs
    └── server.rs
```

## Тестирование
Для тестирования в качестве примера будет использоваться этот [основной сервис](https://github.com/Zel1k21/IAD-backend)

Проверим работу асинхронного сервера. Отправляем запрос, и нам спустя несколько миллисекунд приходит ответ со статусом 200. 
Спустя примерно 5-10 секунд данные на основном сервере из предыдущих лабораторных обновляются.
![1.PNG](assets/1.PNG)
![2.PNG](assets/2.PNG)

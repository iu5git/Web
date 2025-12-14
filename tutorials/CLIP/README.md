# Методическое пособие по интеграции поиска карточек по изображению.

В данном методическом пособии на примере магазина мебели будет показано применение <a href="https://huggingface.co/docs/transformers.js/index">`transformers.js`</a> для полной реализации поиска карточки с подходящим описанием по картинке через CLIP-модель. 

Для начала мы реализуем простое React-приложение интернет-магазина мебели с простым текстовым происком. Затем мы уже интегрируем поиск по изображению.
Первичное приложение будет во многом повторять ЛР по React, так что задерживаться на создании сильно не будем. 

## Теория про CLIP

Для реализации поиска по изображению в данной работе используются технологии глубокого обучения (Deep Learning), основанные на архитектуре Трансформер (Transformer). Чтобы понять, как именно происходит "магия" сопоставления картинки и текста, разберем ключевые компоненты системы.

#### 1. Трансформер как «черный ящик»
Архитектура Трансформер, совершившая революцию в обработке естественного языка (NLP), состоит из двух основных блоков:
*   **Энкодер (Encoder)** - отвечает за понимание входных данных и перевод их в векторное представление.
*   **Декодер (Decoder)** - отвечает за генерацию новых данных на основе информации от энкодера.

В контексте нашей задачи нас интересует только **Энкодер**. Можно представить его как «черный ящик»: на вход он получает данные (например, предложение), а на выходе выдает **эмбеддинг** - числовой вектор фиксированной длины. Этот вектор является "смысловым слепком" входных данных: если два предложения похожи по смыслу, их векторы-эмбеддинги будут находиться близко друг к другу в математическом пространстве.

#### 2. Визуальные трансформеры (Vision Transformers)
Долгое время трансформеры применялись только к тексту. Однако выяснилось, что Энкодер трансформера - устройство универсальное. Ему неважно, что именно подается на вход, главное - представить данные как последовательность элементов.

Чтобы скормить Энкодеру изображение, применяется следующий алгоритм (Vision Transformer, ViT):
1.  **Нарезка на патчи:** Изображение разбивается на сетку квадратов (например, 16x16 пикселей).
2.  **Линеаризация:** Каждый квадрат (патч) "вытягивается" в плоскую последовательность пикселей. Теперь картинка для модели выглядит как набор фрагментов, аналогично тому, как предложение выглядит как набор слов.
3.  **Позиционное кодирование (Positional Encoding):** Чтобы модель понимала, где находится какой фрагмент (где левый верхний угол, а где центр), к данным каждого патча добавляется специальный вектор позиции.
4.  **Эмбеддинг:** Подготовленная последовательность проходит через слои Энкодера, и на выходе мы получаем один итоговый вектор - **эмбеддинг изображения**.

Для наглядности приведена схема ViT
<img src="https://github.com/David-bomb/CLIP_method/blob/main/additional/ViT.png">

#### 3. Модель CLIP: единое смысловое пространство
Проблема классических подходов в том, что модели для текста и модели для картинок существуют в разных "мирах". Вектор слова "собака" и вектор фотографии собаки, полученные разными нейросетями, математически никак не связаны. Их нельзя просто взять и сравнить.

Здесь на сцену выходит **CLIP (Contrastive Language-Image Pre-training)**.
CLIP - это мультимодальная архитектура, которая обучает два Энкодера одновременно:
1.  **Text Encoder:** превращает текст в вектор.
2.  **Image Encoder:** превращает картинку в вектор.

Главная особенность CLIP заключается в том, что эти два энкодера обучаются так, чтобы **проецировать данные в общее смысловое (векторное) пространство**. В процессе обучения модель видит миллионы пар "картинка + описание" и настраивает свои веса так, чтобы:
*   Вектор изображения собаки и вектор текста "фотография собаки" были **близки**.
*   Вектор изображения собаки и вектор текста "тарелка супа" были **далеки** друг от друга.

Также приведем схему CLIP
<img src="https://github.com/David-bomb/CLIP_method/blob/main/additional/CLIP.jpeg">

#### 4. Применение для поиска
Благодаря тому, что CLIP (и его современные вариации, такие как SigLIP) создает единое пространство для разных модальностей, мы можем реализовать поиск без использования сложной классификации и разметки данных:
1.  Берем изображение от пользователя и прогоняем через **Image Encoder** $\rightarrow$ получаем вектор $V_{img}$.
2.  Берем описания всех товаров в базе и прогоняем через **Text Encoder** $\rightarrow$ получаем набор векторов $V_{text\_1}, V_{text\_2}, \dots$.
3.  Считаем **косинусное сходство** (Cosine Similarity) между $V_{img}$ и каждым из текстовых векторов.
4.  Товары, чьи текстовые векторы оказались "ближе" всего к вектору картинки, и являются искомыми объектами.

В данной лабораторной работе мы используем модель <a href="https://huggingface.co/Xenova/siglip-base-patch16-224">SigLIP</a> (улучшенную версию CLIP от Google), которая работает по тому же принципу, но обладает более высокой точностью и поддержкой множества языков.

### Что такое transfomers.js?

Простыми словами, `transformers.js` - это перевод библиотеки <a href="https://huggingface.co/docs/transformers/index">HF Transformers</a> с python на JavaScript. Сущности из оригинальной библиотеки постарались перенести в JS, также некоторые модели, которые раньше запускались **только** через python, теперь могут работать на JavaScript. 

Теперь быстренько перепишем интерфейс под новые функции, и подронбно разберем саму логику работы с `transfomers.js` в нашем проекте. 


## Создание простого React-приложения

### 1. Инициализация проекта

Откройте терминал и выполните следующую команду для создания проекта с использованием Vite:

```bash
npm create vite@latest furniture-shop -- --template react-ts
```

Перейдите в папку проекта:

```bash
cd furniture-shop
```

Установите базовые зависимости:

```bash
npm install
```

Установите дополнительные библиотеки:

```bash
npm install bootstrap react-bootstrap
```

### Структура

В папку src добавье папку modules. 

#### `src/modules/mock.ts`
Определение типов и моковых данных. Убедитесь, что в папке `src/assets` есть изображения `1.jpg` ... `8.jpg`, `default.jpg`. Взять их можно в <a href="https://github.com/David-bomb/CLIP_method/tree/main/card_images">папке</a>. 

**Примечание:** Mock данные **обязательно** описывать на английском языке. Дело в том, что создатель библиотеки `transformers.js`, Xenova, еще не конвертировал под свою библиотеку ни одну поддерживающую русский язык модель типа CLIP. На русском языке векторы будут формироваться неправильно. 

```typescript
import img1 from '../assets/1.jpg';
import img2 from '../assets/2.jpg';
import img3 from '../assets/3.jpg';
import img4 from '../assets/4.jpg';
import img5 from '../assets/5.jpg';
import img6 from '../assets/6.jpg';
import img7 from '../assets/7.jpg';
import img8 from '../assets/8.jpg';
import defaultImg from '../assets/default.jpg'; 

export interface IFurniture {
    id: number;
    name: string;
    description: string;
    price: number;
    image: string;
}

export const FURNITURE_MOCK: IFurniture[] = [
    {
        id: 1,
        name: "Cloud Sofa",
        description: "Soft white three-seater sofa with high-quality upholstery.",
        price: 45990,
        image: img1
    },
    {
        id: 2,
        name: "Retro Armchair",
        description: "Comfortable armchair with wooden legs and red upholstery.",
        price: 12500,
        image: img2
    },
    {
        id: 3,
        name: "Dining Table",
        description: "Solid natural oak table. Seats up to 6 people.",
        price: 28000,
        image: img3
    },
    {
        id: 4,
        name: "Plastic Chair",
        description: "Gray plastic chair with plastic legs.",
        price: 3500,
        image: img4
    },
    {
        id: 5,
        name: "Floor Lamp",
        description: "Gray metal loft-style floor lamp.",
        price: 5900,
        image: img5
    },
    {
        id: 6,
        name: "White Dresser",
        description: "White dresser with three handle-less drawers.",
        price: 15990,
        image: img6
    },
    {
        id: 7,
        name: "Double Bed",
        description: "White double bed with a padded headboard.",
        price: 32000,
        image: img7
    },
    {
        id: 8,
        name: "Wall Shelf",
        description: "Wooden shelf with an unusual S-shaped design.",
        price: 1900,
        image: img8
    },
    // Карточки без картинок. Это показательный пример того, что поиск идет именно по описанию.
    {
        id: 9,
        name: "Sliding Wardrobe",
        description: "Large oak sliding-door wardrobe with a full-length mirror.",
        price: 45000,
        image: defaultImg
    },
    {
        id: 10,
        name: "Bedside Table",
        description: "Small oak bedside table for the bedroom.",
        price: 4500,
        image: defaultImg
    },
    {
        id: 11,
        name: "Wall Mirror",
        description: "Round mirror in a gold frame.",
        price: 3200,
        image: defaultImg
    }
];
```

#### `src/App.css`

Изменим файл App.css

```css
.app-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: system-ui, -apple-system, sans-serif;
}

.search-section {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  margin-bottom: 40px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
}

.preview-image {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
  border: 2px solid #dee2e6;
}

.placeholder-image {
  width: 150px;
  height: 150px;
  background: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  color: #adb5bd;
  border: 2px dashed #dee2e6;
}

.furniture-row {
  display: flex;
  gap: 20px;
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  margin-bottom: 15px;
  align-items: center;
  background: white;
  transition: box-shadow 0.2s;
}

.furniture-row:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.row-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 6px;
  flex-shrink: 0;
}

.row-content {
  flex-grow: 1;
}

.row-stats {
  width: 250px;
  padding-left: 20px;
  border-left: 1px solid #eee;
  font-family: monospace;
  font-size: 0.85rem;
  color: #666;
}
```

#### `src/App.tsx`

Теперь создадим страницу с карточками с нашими стилями

```tsx
import { useState, useRef } from 'react';
import { Button } from 'react-bootstrap';
import { FURNITURE_MOCK } from './modules/mock';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  // Состояние для отображения выбранной картинки
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  
  // Список товаров (пока просто берем все из мока)
  const [items] = useState(FURNITURE_MOCK);

  // Ссылка на скрытый input для загрузки файла
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Обработка выбора файла
  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Создаем URL для предпросмотра
      const imageUrl = URL.createObjectURL(file);
      setSelectedImage(imageUrl);
      
      // TODO: Здесь будем отправлять картинку в нейросеть на следующем этапе
    }
  };

  // Очистка поиска
  const handleClear = () => {
    setSelectedImage(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="app-container">
      <h1>AI Поиск мебели</h1>
      <p className="text-muted">Загрузите фото, чтобы найти похожий товар</p>

      {/* Секция поиска */}
      <div className="search-section">
        {/* Скрытый инпут */}
        <input 
          type="file" 
          accept="image/*" 
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleImageUpload}
        />

        {/* Область предпросмотра или кнопка загрузки */}
        <div style={{ flexShrink: 0 }}>
            {selectedImage ? (
                <img src={selectedImage} alt="Query" className="preview-image" />
            ) : (
                <div className="placeholder-image">Нет фото</div>
            )}
        </div>

        <div className="d-flex flex-column gap-2">
            <Button 
                variant="primary" 
                onClick={() => fileInputRef.current?.click()}
            >
                Загрузить фото
            </Button>
            
            {selectedImage && (
                <Button variant="outline-danger" onClick={handleClear}>
                    Сбросить
                </Button>
            )}
        </div>
      </div>

      {/* Список карточек (в 1 столбец) */}
      <div className="items-list">
        {items.map((item) => (
            <div key={item.id} className="furniture-row">
                <img src={item.image} alt={item.name} className="row-image" />
                
                <div className="row-content">
                    <h5>{item.name}</h5>
                    <p className="text-muted mb-1">{item.description}</p>
                    <strong className="text-primary">{item.price.toLocaleString()} ₽</strong>
                </div>

                {/* Место для вывода данных нейросети */}
                <div className="row-stats">
                    <div>Similarity: <span className="text-muted">-</span></div>
                    <div style={{ fontSize: '10px', marginTop: '5px', wordBreak: 'break-all' }}>
                        Embedding: [ ... ]
                    </div>
                </div>
            </div>
        ))}
      </div>
    </div>
  );
}

export default App;
```


### Запуск проекта

```bash
npm run dev
```

Тут у вас должно получиться простое React-приложение интернет магазина.

**Главная**
<img src="https://github.com/David-bomb/CLIP_method/blob/main/screens/index.png">


## Интерграция SigLIP

В этом этапе мы создадим новый файл, где будет прописана логика работы SigLIP, а также внедрим подсчет эмбеддингов для карточек. Сортировка по эмбеддингам будет интегрирована позже. 

### Подготовка

Для начала нужно установить саму библиотеку `@huggingface/transformers`. Это может занять время.

```bash
npm install @huggingface/transformers
```

### Разработка search.worker.js

Здесь мы разработаем главную часть нашей работы. Этот файл несет в себе логику нарботы с SigLIP. 

#### Импорты и настройки окружения

```ts
import { 
    env, 
    AutoTokenizer, 
    AutoProcessor, 
    SiglipTextModel, 
    SiglipVisionModel,
    RawImage 
} from '@huggingface/transformers';

env.allowLocalModels = false;
env.allowRemoteModels = true;

const MODEL_ID = 'Xenova/siglip-base-patch16-224';
```

Мы импортируем env для настроек библиотеки, токенизатор и процессор. Также мы импортируем SiglipTextModel и SoglipVisionModel, это те энкодеры, которые помогут нам векторизовать тексты описаний и картинку поиска. А вот RawImage - это спициальный тип, к которому приводят картинку, чтобы Porcessor не воспринял картинку как текст. RawImage напрямую указывает, что процессору дана именно картинка.

Далее мы задаем локальные настройки и обозначаем какую модель мы используем.

#### Singleton сервис

```tsx
class SiglipService {
    static tokenizer: any = null;
    static processor: any = null;
    static textModel: any = null;
    static visionModel: any = null;

    static async init(progress_callback?: (data: any) => void) {
        if (!this.tokenizer) {
            // Используем q8 для баланса качества и скорости
            const options = { device: 'wasm', dtype: 'q8' } as const;

            this.tokenizer = await AutoTokenizer.from_pretrained(MODEL_ID, { progress_callback });
            this.processor = await AutoProcessor.from_pretrained(MODEL_ID, { progress_callback });
            this.textModel = await SiglipTextModel.from_pretrained(MODEL_ID, {...options, progress_callback });
            this.visionModel = await SiglipVisionModel.from_pretrained(MODEL_ID, {...options, progress_callback });
        }
    }
}
```

Это класс-синглтон. Его задача — загрузить модель один раз и хранить её в памяти.
Если бы мы загружали модель при каждом нажатии кнопки "Искать", пользователю приходилось бы ждать загрузку каждый раз. Здесь мы проверяем if (!this.tokenizer): если модели уже в памяти, мы пропускаем загрузку.
Мы загружаем 4 компонента, необходимых для работы мультимодальной нейросети.

Также стоит упомянть о настройках запуска. В данном случае запускается квантизованная модель и CPU. В качестве device запуска можно также указывать `webgpu`, и тогда модель будет работать на GPU. А про доступные степени квантизации в ветодичке написано следующее:
> While the available options may vary depending on the specific model, typical choices include "fp32" (default for WebGPU), "fp16", "q8" (default for WASM), and "q4".

Подробней про квантизацию в `transformers.js` можно прочитать <a href="https://huggingface.co/docs/transformers.js/guides/dtypes">здесь</a>, а про то, что такое квантизация в принципе - <a href="https://habr.com/ru/articles/887466/">тут</a>.

#### Обработчик сообщений

```tsx
self.addEventListener('message', async (event) => {
    const { type, data } = event.data;

    try {
        if (type === 'init') {
            await SiglipService.init((msg) => {
                self.postMessage({ type: 'progress', data: msg });
            });

            const items = data;
            const embeddings: Record<number, number[]> = {};

            // Все описания РАЗОМ
            const descriptions = items.map((item: any) => item.description);
            
            // max_length нужен для одинаковой длины 
            const text_inputs = await SiglipService.tokenizer(descriptions, { 
                padding: 'max_length', 
                truncation: true,
            });

            // Получаем выход текстовой модели, мы заэмбеддили все описания за раз, сделав 1 эмбеддинг
            const { pooler_output: textOutput } = await SiglipService.textModel(text_inputs);

            // Размерность выхода SigLIP base = 768
            const embeddingSize = 768; 

            for (let i = 0; i < items.length; i++) {
                const start = i * embeddingSize;
                const end = start + embeddingSize;
                // Этот кусок - вектор для одного описания
                const textVector = textOutput.data.slice(start, end);
                
                const itemId = items[i].id; 
                embeddings[itemId] = Array.from(textVector);
            }

            self.postMessage({ type: 'text_embeddings_ready', data: embeddings });
        }

        // Если загрузили картинку
        if (type === 'image') {
            // Считываем
            const imageUrl = URL.createObjectURL(data); 
            // RawImage - утилита для работы с изображениями, без нее процессор может воспринять картинку как текст, и visionModel выдаст ошибку
            const image = await RawImage.read(imageUrl);
            
            // Обрабатываем картинку и получаем вектор
            const imageInputs = await SiglipService.processor(image);
            const { pooler_output } = await SiglipService.visionModel(imageInputs);
            
            self.postMessage({ 
                type: 'image_embedding_ready', 
                data: Array.from(pooler_output.data) 
            });
            
            URL.revokeObjectURL(imageUrl);
        }

    } catch (error) {
        console.error(error);
        self.postMessage({ type: 'error', data: error });
    }
});
```

Обработчик ждет команды от основного приложения (App.tsx).
event.data содержит данные, которые мы передали через postMessage. Мы смотрим на поле type, чтобы понять, что от нас хотят: инициализацию или обработку картинки.

Здесь расположена логика работы поиска. Эмбеддинги описаний карточек рассчитываются сразу, как и обе модели SigLIP загружаются сразу. А вот эмбеддинг картинки рассчитыватся только при ее загрузке, что логично. 

В нашем проекте карточек немного, поэтому мы можем себе позволить векторизовать все описания разом. В случае большого количества карточек в индустрии принято проводить "корзиночную" (batch) обработку, обычно в одном батче обрабатывается 16 или 32 объекта.

#### Полный код

```tsx
import { 
    env, 
    AutoTokenizer, 
    AutoProcessor, 
    SiglipTextModel, 
    SiglipVisionModel,
    RawImage 
} from '@huggingface/transformers';

env.allowLocalModels = false;
env.allowRemoteModels = true;

const MODEL_ID = 'Xenova/siglip-base-patch16-224';

class SiglipService {
    static tokenizer: any = null;
    static processor: any = null;
    static textModel: any = null;
    static visionModel: any = null;

    static async init(progress_callback?: (data: any) => void) {
        if (!this.tokenizer) {
            // Используем q8 для баланса качества и скорости
            const options = { device: 'wasm', dtype: 'q8' } as const;

            this.tokenizer = await AutoTokenizer.from_pretrained(MODEL_ID, { progress_callback });
            this.processor = await AutoProcessor.from_pretrained(MODEL_ID, { progress_callback });
            this.textModel = await SiglipTextModel.from_pretrained(MODEL_ID, {...options, progress_callback });
            this.visionModel = await SiglipVisionModel.from_pretrained(MODEL_ID, {...options, progress_callback });
        }
    }
}

self.addEventListener('message', async (event) => {
    const { type, data } = event.data;

    try {
        if (type === 'init') {
            await SiglipService.init((msg) => {
                self.postMessage({ type: 'progress', data: msg });
            });

            const items = data;
            const embeddings: Record<number, number[]> = {};

            // Все описания РАЗОМ
            const descriptions = items.map((item: any) => item.description);
            
            // max_length нужен для одинаковой длины 
            const text_inputs = await SiglipService.tokenizer(descriptions, { 
                padding: 'max_length', 
                truncation: true,
            });

            // Получаем выход текстовой модели, мы заэмбеддили все описания за раз, сделав 1 эмбеддинг
            const { pooler_output: textOutput } = await SiglipService.textModel(text_inputs);

            // Размерность выхода SigLIP base = 768
            const embeddingSize = 768; 

            for (let i = 0; i < items.length; i++) {
                const start = i * embeddingSize;
                const end = start + embeddingSize;
                // Этот кусок - вектор для одного описания
                const textVector = textOutput.data.slice(start, end);
                
                const itemId = items[i].id; 
                embeddings[itemId] = Array.from(textVector);
            }

            self.postMessage({ type: 'text_embeddings_ready', data: embeddings });
        }

        // Если загрузили картинку
        if (type === 'image') {
            // Считываем
            const imageUrl = URL.createObjectURL(data); 
            // RawImage - утилита для работы с изображениями, без нее процессор может воспринять картинку как текст, и visionModel выдаст ошибку
            const image = await RawImage.read(imageUrl);
            
            // Обрабатываем картинку и получаем вектор
            const imageInputs = await SiglipService.processor(image);
            const { pooler_output } = await SiglipService.visionModel(imageInputs);
            
            self.postMessage({ 
                type: 'image_embedding_ready', 
                data: Array.from(pooler_output.data) 
            });
            
            URL.revokeObjectURL(imageUrl);
        }

    } catch (error) {
        console.error(error);
        self.postMessage({ type: 'error', data: error });
    }
});
```


### Теперь обновим `src/App.tsx`

#### Обновление импортов

Добавим импортирование useEffect и ProgressBar. 

```tsx
import { useState, useRef, useEffect } from 'react'; 
import { Button, ProgressBar } from 'react-bootstrap'; 
```

#### Добавление новых состояний

Мы добавляем состояния для хранения эмбеддингов текста (помним, что мы их рассчитываем при инициализации), картинки (это состояние уже заполняется при вводе картинки) и нужные состояния для progressBar. 

Также важным является создание воркера, он и будет выполнять ML-задачи. 

```tsx
function App() {
  // Состояние для отображения выбранной картинки
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  
  // Список товаров (пока просто берем все из мока)
  const [items] = useState(FURNITURE_MOCK);

  // --- НОВЫЕ СОСТОЯНИЯ ---
  // Храним вектора текстов: id товара -> массив чисел
  const [textEmbeddings, setTextEmbeddings] = useState<Record<number, number[]>>({});
  // Храним вектор текущей картинки
  const [imageEmbedding, setImageEmbedding] = useState<number[] | null>(null);
  // Состояние загрузки модели
  const [ready, setReady] = useState(false);
  const [progress, setProgress] = useState(0);

  // Web Worker  
  const workerRef = useRef<Worker | null>(null);
  // -----------------------

  // Ссылка на скрытый input для загрузки файла
  const fileInputRef = useRef<HTMLInputElement>(null);
  ```


#### Добавление UseEffect для запуска воркера

Здесь мы по факту инициализируем воркур и запускамет расчет текстовых векторов. Этот код должен стоять перед handleImageUpload, потому что в handleImageUpload мы будем использовать инициализированный воркер.

```tsx
useEffect(() => {
    // Инициализация воркера
    workerRef.current = new Worker(new URL('./workers/search.worker.ts', import.meta.url), {
      type: 'module'
    });

    // Обработка сообщений от воркера
    workerRef.current.onmessage = (e) => {
      const { type, data } = e.data;

      if (type === 'progress') {
        // Обновляем прогресс-бар загрузки модели
        if (data.status === 'progress') {
            setProgress(data.progress);
        } else if (data.status === 'ready') {
            setReady(true);
        }
      } 
      else if (type === 'text_embeddings_ready') {
        console.log("Векторы текстов получены:", data);
        setTextEmbeddings(data);
        setReady(true);
      }
      else if (type === 'image_embedding_ready') {
        console.log("Вектор картинки получен:", data);
        setImageEmbedding(data);
      }
    };

    // Запускаем инициализацию и расчет текстовых векторов
    workerRef.current.postMessage({ type: 'init', data: FURNITURE_MOCK });

    return () => workerRef.current?.terminate();
  }, []);
  ```


#### Обновление handleImageUpload 

Вместо TODO комментария в handleImageUpload в конце условного блока `if (file)` мы ставим строчку:

```tsx
workerRef.current?.postMessage({ type: 'image', data: file });
```

Здесь мы подаем нашу картинку на обработку воркеру, который посчитает ее эмбеддинг.


#### Обновление handleClear

После удаления картинки при сбросе мы также очищаем вектор картинки

```tsx
    setSelectedImage(null);
    setImageEmbedding(null); // Очищаем вектор картинки
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
```

#### Обновим верстку

```tsx
  return (
    <div className="app-container">
      <h1>AI Поиск мебели</h1>
      <p className="text-muted">Загрузите фото, чтобы найти похожий товар</p>

      {/* Секция поиска */}
      <div className="search-section">
        {/* Скрытый инпут */}
        <input 
          type="file" 
          accept="image/*" 
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleImageUpload}
        />

        {/* Область предпросмотра или кнопка загрузки */}
        <div style={{ flexShrink: 0 }}>
            {selectedImage ? (
                <img src={selectedImage} alt="Query" className="preview-image" />
            ) : (
                <div className="placeholder-image">Нет фото</div>
            )}
        </div>

        <div className="d-flex flex-column gap-2">
                    <Button 
                        variant="primary" 
                        onClick={() => fileInputRef.current?.click()}
                        disabled={!ready} // Блокируем пока модель не загрузится
                    >
                        {ready ? "Загрузить фото" : "Загрузка нейросети..."}
                    </Button>
                    
                    {/* Прогресс бар загрузки модели */}
                    {!ready && <ProgressBar now={progress} label={`${Math.round(progress)}%`} animated />}

                    {/* Вывод вектора картинки */}
                    {imageEmbedding && (
                        <div style={{ fontSize: '10px', color: 'blue', maxWidth: '200px', wordBreak: 'break-all' }}>
                            <strong>Image Vector (first 5):</strong><br/>
                            [{imageEmbedding.slice(0, 5).map(n => n.toFixed(3)).join(', ')}...]
                        </div>
                    )}
                    
                    {selectedImage && (
                        <Button variant="outline-danger" onClick={handleClear}>
                            Сбросить
                        </Button>
                    )}
          </div>
      </div>

      {/* Список карточек (в 1 столбец) */}
      <div className="items-list">
        {items.map((item) => (
            <div key={item.id} className="furniture-row">
                <img src={item.image} alt={item.name} className="row-image" />
                
                <div className="row-content">
                    <h5>{item.name}</h5>
                    <p className="text-muted mb-1">{item.description}</p>
                    <strong className="text-primary">{item.price.toLocaleString()} ₽</strong>
                </div>

                {/* Место для вывода данных нейросети */}
                <div className="row-stats">
                    <div>Similarity: <span className="text-muted">-</span></div>
                    
                    {/* Выводим вектор, если он посчитан */}
                    {textEmbeddings[item.id] ? (
                        <div style={{ fontSize: '10px', marginTop: '5px', wordBreak: 'break-all' }}>
                            <strong>Text Vector:</strong><br/>
                            [{textEmbeddings[item.id].slice(0, 5).map(n => n.toFixed(3)).join(', ')}...]
                        </div>
                    ) : (
                        <div style={{ fontSize: '10px' }} className="text-muted">Calculating...</div>
                    )}
                </div>
            </div>
        ))}
      </div>
    </div>
  );
```


#### Полный код `scr/App.tsx`

Вот полный код файла App.tsx

```tsx
import { useState, useRef, useEffect } from 'react'; 
import { Button, ProgressBar } from 'react-bootstrap'; 
import { FURNITURE_MOCK } from './modules/mock';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  // Состояние для отображения выбранной картинки
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  
  // Список товаров (пока просто берем все из мока)
  const [items] = useState(FURNITURE_MOCK);

  // --- НОВЫЕ СОСТОЯНИЯ ---
  // Храним вектора текстов: id товара -> массив чисел
  const [textEmbeddings, setTextEmbeddings] = useState<Record<number, number[]>>({});
  // Храним вектор текущей картинки
  const [imageEmbedding, setImageEmbedding] = useState<number[] | null>(null);
  // Состояние загрузки модели
  const [ready, setReady] = useState(false);
  const [progress, setProgress] = useState(0);

  const workerRef = useRef<Worker | null>(null);
  // -----------------------

  // Ссылка на скрытый input для загрузки файла
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Инициализация воркера
    workerRef.current = new Worker(new URL('./workers/search.worker.ts', import.meta.url), {
      type: 'module'
    });

    // Обработка сообщений от воркера
    workerRef.current.onmessage = (e) => {
      const { type, data } = e.data;

      if (type === 'progress') {
        // Обновляем прогресс-бар загрузки модели
        if (data.status === 'progress') {
            setProgress(data.progress);
        } else if (data.status === 'ready') {
            setReady(true);
        }
      } 
      else if (type === 'text_embeddings_ready') {
        console.log("Векторы текстов получены:", data);
        setTextEmbeddings(data);
        setReady(true);
      }
      else if (type === 'image_embedding_ready') {
        console.log("Вектор картинки получен:", data);
        setImageEmbedding(data);
      }
    };

    // Запускаем инициализацию и расчет текстовых векторов
    workerRef.current.postMessage({ type: 'init', data: FURNITURE_MOCK });

    return () => workerRef.current?.terminate();
  }, []);

  // Обработка выбора файла
  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Создаем URL для предпросмотра
      const imageUrl = URL.createObjectURL(file);
      setSelectedImage(imageUrl);
      
      // TODO: Здесь будем отправлять картинку в нейросеть на следующем этапе
      workerRef.current?.postMessage({ type: 'image', data: file });
    }
  };

  // Очистка поиска
const handleClear = () => {
    setSelectedImage(null);
    setImageEmbedding(null); // Очищаем вектор картинки
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="app-container">
      <h1>AI Поиск мебели</h1>
      <p className="text-muted">Загрузите фото, чтобы найти похожий товар</p>

      {/* Секция поиска */}
      <div className="search-section">
        {/* Скрытый инпут */}
        <input 
          type="file" 
          accept="image/*" 
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleImageUpload}
        />

        {/* Область предпросмотра или кнопка загрузки */}
        <div style={{ flexShrink: 0 }}>
            {selectedImage ? (
                <img src={selectedImage} alt="Query" className="preview-image" />
            ) : (
                <div className="placeholder-image">Нет фото</div>
            )}
        </div>

        <div className="d-flex flex-column gap-2">
                    <Button 
                        variant="primary" 
                        onClick={() => fileInputRef.current?.click()}
                        disabled={!ready} // Блокируем пока модель не загрузится
                    >
                        {ready ? "Загрузить фото" : "Загрузка нейросети..."}
                    </Button>
                    
                    {/* Прогресс бар загрузки модели */}
                    {!ready && <ProgressBar now={progress} label={`${Math.round(progress)}%`} animated />}

                    {/* Вывод вектора картинки */}
                    {imageEmbedding && (
                        <div style={{ fontSize: '10px', color: 'blue', maxWidth: '200px', wordBreak: 'break-all' }}>
                            <strong>Image Vector (first 5):</strong><br/>
                            [{imageEmbedding.slice(0, 5).map(n => n.toFixed(3)).join(', ')}...]
                        </div>
                    )}
                    
                    {selectedImage && (
                        <Button variant="outline-danger" onClick={handleClear}>
                            Сбросить
                        </Button>
                    )}
          </div>
      </div>

      {/* Список карточек (в 1 столбец) */}
      <div className="items-list">
        {items.map((item) => (
            <div key={item.id} className="furniture-row">
                <img src={item.image} alt={item.name} className="row-image" />
                
                <div className="row-content">
                    <h5>{item.name}</h5>
                    <p className="text-muted mb-1">{item.description}</p>
                    <strong className="text-primary">{item.price.toLocaleString()} ₽</strong>
                </div>

                {/* Место для вывода данных нейросети */}
                <div className="row-stats">
                    <div>Similarity: <span className="text-muted">-</span></div>
                    
                    {/* Выводим вектор, если он посчитан */}
                    {textEmbeddings[item.id] ? (
                        <div style={{ fontSize: '10px', marginTop: '5px', wordBreak: 'break-all' }}>
                            <strong>Text Vector:</strong><br/>
                            [{textEmbeddings[item.id].slice(0, 5).map(n => n.toFixed(3)).join(', ')}...]
                        </div>
                    ) : (
                        <div style={{ fontSize: '10px' }} className="text-muted">Calculating...</div>
                    )}
                </div>
            </div>
        ))}
      </div>
    </div>
  );
}

export default App;
```

## Внедрение ранжирования

На текущем этапе наше приложение умеет превращать и текст, и картинки в наборы чисел (векторы). Но сами по себе эти числа нам ничего не дают. Нам нужно научить приложение отвечать на вопрос: **"Насколько вектор картинки А близок к вектору описания Б?"**.

### `src/modules/math.ts`

В машинном обучении для сравнения векторов чаще всего используется **Косинусное сходство (Cosine Similarity)**.
Если не вдаваться в глубокую геометрию: это вычисление косинуса угла между двумя векторами.
*   **1.0**: Векторы сонаправлены (идеальное совпадение).
*   **0.0**: Векторы перпендикулярны (ничего общего).
*   **-1.0**: Векторы противоположны.

Создадим файл для математических функций.

```typescript
export function cosineSimilarity(vecA: number[], vecB: number[]): number {
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;

    for (let i = 0; i < vecA.length; i++) {
        dotProduct += vecA[i] * vecB[i];
        normA += vecA[i] * vecA[i];
        normB += vecB[i] * vecB[i];
    }

    if (normA === 0 || normB === 0) return 0;
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}
```

### `src/App.tsx`

#### Состояния для отображения
Теперь перейдем в `App.tsx`. Нам нужно изменить то, как мы храним список товаров. Раньше это был статический массив, теперь нам нужно динамическое состояние, которое хранит для каждого товара его **рейтинг соответствия (score)** и **видимость (isVisible)**.

Добавим новый интерфейс и импортируем функцию сравнения:

```tsx
import { cosineSimilarity } from './modules/math'; // Новый импорт

// ...

// Расширяем интерфейс товара.
interface IProcessedItem extends IFurniture {
    score: number;      // Степень схожести (от -1 до 1)
    isVisible: boolean; // Флаг для фильтрации неподходящих результатов
}
```

Внутри компонента `App` изменим инициализацию `items`:

```tsx
function App() {
  // ... (остальные стейты)

  // Состояние теперь хранит "Обработанные товары"
  // По умолчанию score = 0, isVisible = true (показываем все)
  const [items, setItems] = useState<IProcessedItem[]>(
    FURNITURE_MOCK.map(item => ({ ...item, score: 0, isVisible: true }))
  );
  
  // ...
}
```

#### Логика сравнения

Самая важная часть. Мы добавим `useEffect`, который будет следить за изменениями вектора картинки (`imageEmbedding`).
Как только пользователь загружает фото и Worker возвращает вектор:
1.  Мы проходимся по всем товарам.
2.  Берем вектор описания товара (который мы посчитали при старте).
3.  Сравниваем его с вектором картинки через `cosineSimilarity`.
4.  Сортируем массив: товары с наибольшим сходством поднимаются наверх.

```tsx
  useEffect(() => {
    if (imageEmbedding && Object.keys(textEmbeddings).length > 0) {
        
        const threshold = 0.005; 

        const processed = items.map(item => {
            const textVec = textEmbeddings[item.id];
            if (!textVec) return item;

            // Считаем сходство
            const similarity = cosineSimilarity(imageEmbedding, textVec);

            return {
                ...item,
                score: similarity,
                // Eсли сходство выше порога, то отображаем товар
                isVisible: similarity > threshold
            };
        });

        // Сортируем: сначала самые похожие
        processed.sort((a, b) => b.score - a.score);

        setItems(processed);
    }
  }, [imageEmbedding, textEmbeddings]);
```

> **Примечание про Threshold (порог):** Порог был взят маленький в силу особенности SigLIP, так как в нем вместо softmax используется Sigmoid. Подробнее про то, почему так сделано (да и про весь CLIP в целом) можно посмотреть в <a href="https://habr.com/ru/articles/908168/">статье</a>, а наглядное сравнение выходных формул CLIP и SigLIP можно посмотреть в виде <a href="https://github.com/David-bomb/CLIP_method/blob/main/additional/CLIP_meme.jpg">мема</a>. 

### 4. Обновление интерфейса и функция сброса

Нам нужно обновить функцию `handleClear`, чтобы при нажатии "Сбросить" товары возвращались в исходный порядок (по ID), а рейтинги обнулялись.

```tsx
  const handleClear = () => {
    setSelectedImage(null);
    setImageEmbedding(null);
    // При сбросе возвращаем список в исходное состояние (сортировка по ID, все видимы)
    setItems(FURNITURE_MOCK.map(item => ({ ...item, score: 0, isVisible: true })));
    if (fileInputRef.current) fileInputRef.current.value = '';
  };
```

И, наконец, обновим `return` (JSX), чтобы визуально выделять победителей поиска. Мы добавим подсветку зеленого цвета для самого релевантного товара и будем выводить процент сходства. Это уже реализовано в итоговом коде. 

### Итоговый код `src/App.tsx`

Вот финальная версия компонента, объединяющая все части:

```tsx
import { useState, useRef, useEffect } from 'react';
import { Button, ProgressBar } from 'react-bootstrap';
import { FURNITURE_MOCK } from './modules/mock';
import type { IFurniture } from './modules/mock';
import { cosineSimilarity } from './modules/math'; 
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

interface IProcessedItem extends IFurniture {
    score: number;      
    isVisible: boolean; 
}

function App() {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  
  // Состояние теперь хранит "Обработанные товары" (с рейтингом и галочкой)
  // По умолчанию score = 0, isVisible = true (показываем все)
  const [items, setItems] = useState<IProcessedItem[]>(
    FURNITURE_MOCK.map(item => ({ ...item, score: 0, isVisible: true }))
  );

  const [textEmbeddings, setTextEmbeddings] = useState<Record<number, number[]>>({});
  const [imageEmbedding, setImageEmbedding] = useState<number[] | null>(null);
  const [ready, setReady] = useState(false);
  const [progress, setProgress] = useState(0);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const workerRef = useRef<Worker | null>(null);

  useEffect(() => {
    workerRef.current = new Worker(new URL('./workers/search.worker.ts', import.meta.url), {
      type: 'module'
    });

    workerRef.current.onmessage = (e) => {
      const { type, data } = e.data;

      if (type === 'progress') {
        if (data.status === 'progress') setProgress(data.progress);
        else if (data.status === 'ready') setReady(true);
      } 
      else if (type === 'text_embeddings_ready') {
        setTextEmbeddings(data);
        setReady(true);
      }
      else if (type === 'image_embedding_ready') {
        setImageEmbedding(data);
      }
    };

    workerRef.current.postMessage({ type: 'init', data: FURNITURE_MOCK });
    return () => workerRef.current?.terminate();
  }, []);

  useEffect(() => {
    if (imageEmbedding && Object.keys(textEmbeddings).length > 0) {
        
        const threshold = 0.005; // Порог (если сходство меньше, isVisible будет false)

        const processed = items.map(item => {
            const textVec = textEmbeddings[item.id];
            if (!textVec) return item;

            // Считаем сходство
            const similarity = cosineSimilarity(imageEmbedding, textVec);

            return {
                ...item,
                score: similarity,
                // Eсли сходство выше порога, то отображаем товар
                isVisible: similarity > threshold
            };
        });

        // Сортируем: сначала самые похожие
        processed.sort((a, b) => b.score - a.score);

        setItems(processed);
    }
  }, [imageEmbedding, textEmbeddings]);

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setSelectedImage(imageUrl);
      workerRef.current?.postMessage({ type: 'image', data: file });
    }
  };

  const handleClear = () => {
    setSelectedImage(null);
    setImageEmbedding(null);
    // При сбросе возвращаем список в исходное состояние (сортировка по ID, все видимы)
    setItems(FURNITURE_MOCK.map(item => ({ ...item, score: 0, isVisible: true })));
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="app-container">
      <h1>AI Поиск мебели</h1>
      <p className="text-muted">Загрузите фото, чтобы найти похожий товар</p>

      <div className="search-section">
        <input 
          type="file" 
          accept="image/*" 
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleImageUpload}
        />

        <div style={{ flexShrink: 0 }}>
            {selectedImage ? (
                <img src={selectedImage} alt="Query" className="preview-image" />
            ) : (
                <div className="placeholder-image">Нет фото</div>
            )}
        </div>

        <div className="d-flex flex-column gap-2">
            <Button variant="primary" onClick={() => fileInputRef.current?.click()} disabled={!ready}>
                {ready ? "Загрузить фото" : "Загрузка нейросети..."}
            </Button>
            
            {!ready && <ProgressBar now={progress} label={`${Math.round(progress)}%`} animated />}
            
            {imageEmbedding && (
                <div style={{ fontSize: '10px', color: 'blue', maxWidth: '200px', wordBreak: 'break-all' }}>
                    <strong>Image Embed (5 dims):</strong><br/>
                    [{imageEmbedding.slice(0, 5).map(n => n.toFixed(3)).join(', ')}...]
                </div>
            )}
            
            {selectedImage && <Button variant="outline-danger" onClick={handleClear}>Сбросить</Button>}
        </div>
      </div>

      <div className="items-list">
        {items.map((item) => {
            // ОТОБРАЖЕНИЕ ПО ГАЛОЧКЕ
            // Если галочка false, мы просто возвращаем null (не рендерим товар)
            if (!item.isVisible) return null;

            return (
                <div key={item.id} className="furniture-row" style={{ 
                    // Подсветим топ-1 результат легким зеленым фоном
                    background: item.score > 0 && item === items[0] ? '#f0fff4' : 'white',
                    borderColor: item.score > 0 && item === items[0] ? '#48bb78' : '#e0e0e0'
                }}>
                    <img src={item.image} alt={item.name} className="row-image" />
                    
                    <div className="row-content">
                        <h5>{item.name}</h5>
                        <p className="text-muted mb-1">{item.description}</p>
                        <strong className="text-primary">{item.price.toLocaleString()} ₽</strong>
                    </div>

                    <div className="row-stats">
                        {/* Вывод Сходства */}
                        <div>
                            Similarity: 
                            <span style={{ fontWeight: 'bold', color: item.score > 0.15 ? 'green' : 'black' }}>
                                {item.score > 0 ? ` ${(item.score * 100).toFixed(1)}%` : ' -'}
                            </span>
                        </div>
                        
                        {/* Вывод Эмбеддинга */}
                        {textEmbeddings[item.id] && (
                            <div style={{ fontSize: '10px', marginTop: '5px', wordBreak: 'break-all', color: '#666' }}>
                                <strong>Text Embed:</strong><br/>
                                [{textEmbeddings[item.id].slice(0, 5).map(n => n.toFixed(3)).join(', ')}...]
                            </div>
                        )}
                    </div>
                </div>
            );
        })}
      </div>
    </div>
  );
}

export default App;
```

## Запуск

Теперь запускаем приложение:
```bash
npm run dev
```

Теперь мы можем проводить полноценный поиск! В целом за одну сессию использования браузера можно перезапускать проект и модели будут сохраняться. Если вы хотите вручную удалить модели из памяти, то зайдите в режим разработчика => `Application` => `Storage` => `Clear Site Data`. После этого модели будут загружаться заново. 


Для проверки работы подготовлены картинки в <a href="https://github.com/David-bomb/CLIP_method/tree/main/search_examples">папке</a>. 

Вот пример поиска при вводе картинки с белой кроватью:

<img src="https://github.com/David-bomb/CLIP_method/blob/main/screens/image_search.png">

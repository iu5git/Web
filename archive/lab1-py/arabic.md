
# الإرشادات المنهجية لتنفيذ العمل المخبري رقم 1  

لتنفيذ هذا العمل المخبري، ستحتاج إلى [VS Code](https://code.visualstudio.com) أو [PyCharm Professional](https://www.jetbrains.com/pycharm/download/).

## إنشاء المشروع محليًا
مثال لـ PyCharm:
اذهب إلى  New Project -> File
في قائمة ...،New Project
اختر Django، ثم حدد مسار المشروع في Location
وأدخل اسم التطبيق في Application name.

![إنشاء المشروع](assets/1.png)

## إنشاء المشروع على الجهاز الافتراضي (عن بُعد)
للاتصال بالجهاز الافتراضي وإنشاء المشروع عليه، اتبع الخطوات التالية:
- افتح VS Code وثبت إضافة **Remote Development**.

![الاتصال بالمضيف البعيد](assets/14.png)

**ملاحظة: في هذه الخطوة، يجب أن يكون الجهاز الافتراضي مشغلاً بالفعل!**
- بعد تثبيت الإضافة، سيظهر رمز في الزاوية السفلية اليسرى، اضغط عليه.

![الاتصال بالمضيف البعيد](assets/15.png)

- اختر **...Connect to Host**

### كيفية معرفة IP الجهاز الافتراضي
أدخل الأمر **ifconfig** على الجهاز الافتراضي، وابحث عن واجهة ،Ethernet في هذه الحالة - enp0s3، وراجع IP في السطر الثاني مقابل .inet يرجى ملاحظة أن نوع الاتصال في إعدادات "الشبكة" للجهاز الافتراضي يجب أن يكون مضبوطاً على "الجسر الشبكي" (Bridge Network).

![IP](assets/27.png)

![نوع الاتصال](assets/16.png)

- ستكون صيغة الاتصال كالتالي - **user_name@remote_host_ip**

![صيغة الاتصال](assets/17.png)

- في الخطوة التالية، حدد المكان الذي سيتم وضع مشروعك فيه. يُفضل إنشاء دليل مخصص للمشاريع، على سبيل المثال **pythonProjects**.

![دليل المشاريع](assets/18.png)

- اضغط على **OK** وأدخل كلمة المرور.
- إذا تم الاتصال بنجاح، ستظهر النتيجة التالية:

![اتصال ناجح](assets/19.png)

### إنشاء مشروع Django
- أنشئ مجلدًا بالاسم المطلوب للمشروع وانتقل إليه.

![إنشاء مجلد للمشروع](assets/20.png)

- أنشئ بيئة افتراضية باستخدام أداة **venv** وقم بتفعيلها.

![بيئة افتراضية](assets/21.png)

- بعد تفعيل البيئة الافتراضية، قم بتثبيت Django (في وقت كتابة هذا الدليل، النسخة المتاحة هي 4.2.4).

![تثبيت Django](assets/22.png)

- أنشئ المشروع باستخدام الأمر `<django-admin startproject <your_project_name> .`

![إنشاء مشروع Django](assets/23.png)

- بعد إنشاء المشروع، انتقل إلى ملف **settings.py** وأضف علامة النجمة **\*** إلى **ALLOWED_HOSTS**.

![](assets/24.png)

- شغّل المشروع باستخدام الأمر `python manage.py runserver 0.0.0.0:8000`    **ملاحظة:** لتكون الخدمة متاحة من النظام الأساسي، يجب تشغيلها على عنوان البث **0.0.0.0**. يمكن أن يكون المنفذ أي رقم، وفي هذه الحالة هو 8000.

![](assets/25.png)

- أجرِ طلبًا من النظام الأساسي، وذلك بإدخال عنوان الجهاز الافتراضي + المنفذ الذي حددته عند تشغيل المشروع في المتصفح.

![](assets/26.png)

باقي العمل يُنفذ بنفس الطريقة كما في الجهاز الأساسي.


هيكل المشروع
في مجلد المشروع bmstu:
<div dir="rtl">
    settings.py - إعدادات المشروع، ويمكن أن يحتوي المشروع على عدة تطبيقات.
</div>
<div dir="rtl">
       urls.py - توجيه الروابط إلى المعالجات (views).    
</div>



في المجلد bmstu_lab: 
<div dir="rtl" style="direction: rtl; text-align: right;">
  <code>views</code> - معالجة التطبيق
</div>
<div dir ="rtl">
    templates - مجلد القوالب (ملفات HTML).
</div>



![هيكل المشروع](assets/2.png)

تشغيل التطبيق
اضغط على زر Run في القائمة اليمنى لتشغيل التطبيق.


![تشغيل](assets/3.png)

في هذه الحالة، يجب أن تعرض وحدة التحكم سجل تتبع حول التطبيق الذي يعمل على **localhost** على المنفذ **:8000**
![وحدة التحكم](assets/4.png)

يجب أن تظهر الصفحة القياسية لتطبيق Django في المتصفح على العنوان `http://127.0.0.1:8000/`.

![المتصفح](assets/5.png)

## كيفية العمل مع View وUrls
`views.py`
```python
from django.http import HttpResponse

def hello(request):
    return HttpResponse('Hello world!')
```

`urls.py`
```python
from bmstu_lab import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello),
]
```

بعد تشغيل الخادم على المسار `http://127.0.0.1:8000/hello/` يجب أن ترى

![مرحبا بالعالم!](assets/6.png)

وبالتالي، سيتم استدعاء كود **hello** عند الوصول إلى الخادم عبر URL **/hello**.

## القوالب

القالب هو ملف نصي عادي، وغالبًا ما يكون بتنسيق HTML، يحتوي على متغيرات وعلامات.
يتم استبدال هذه التركيبات أثناء عرض القالب بالبيانات التي يقدمها المستخدم كمعلمات للقالب. 
في النهاية، نحصل على ملف HTML يمكن عرضه في متصفح المستخدم.

للشروع، سنقوم بتقديم صفحة HTML ثابتة للمستخدم، ولن تحتوي على أي تركيبات من نظام القوالب.

لننشئ ملف HTML في الدليل ‘templates’.


`index.html`
```html
<!doctype html>
<html lang="en" class="h-100">
<head>
  <meta charset="utf-8">
    <title>BMSTU</title>
</head>
<body>
    Hello BMSTU students!
</body>
</html>
```

لإرشاد Django إلى مكان البحث عن القوالب، تحقق من ملف settings.py. يجب أن يحتوي الحقل DIRS داخل المتغير TEMPLATES على المسار المؤدي إلى قوالبك.







```python
TEMPLATES = [
    {
        # ...
        "DIRS": [BASE_DIR / "bmstu_lab/templates"],
        # ...
    },
]
```

لإرجاع الملف الذي تم إنشاؤه للمستخدم، استخدم طريقة `render`.
على سبيل المثال، يُرجع هذا الكود الصفحة `index.html`، التي تم إنشاؤها في مجلد `templates`.


`views.py`
```python
from django.shortcuts import render

def hello(request):
    return render(request, 'index.html')
```

بعد تشغيل الخادم على المسار `http://127.0.0.1:8000/hello/` يجب أن ترى

![Привет студенты!](assets/7.png)

## المتغيرات في القوالب

في القالب، يظهر المتغير بالشكل: `{{ some_variable }}`.
عندما يقوم نظام القوالب بعرض الصفحة ويعثر على متغير،
فإنه يستبدله بالنتيجة التي يتم حسابها في هذا المتغير.

لنقم بإضافة متغيرات إلى الصفحة الثابتة.

`index.html`
```html
<!doctype html>
<html lang="en" class="h-100">
<head>
  <meta charset="utf-8">
    <title>BMSTU</title>
</head>
<body>
    Hello BMSTU students!
    Today is {{ current_date }}
</body>
</html>
```

لتمرير قيمة المتغير من الكود:

`views.py`
```python
from datetime import date

def hello(request):
    return render(request, 'index.html', {
        'current_date': date.today()
    })
```

إذا لم يتم تمرير قيمة المتغير، فسيتم استبداله بسلسلة فارغة. 
لا يمكن أن تحتوي أسماء المتغيرات على مسافات أو علامات ترقيم.

بعد تشغيل الخادم على المسار `http://127.0.0.1:8000/hello/` يجب أن ترى


![Привет студенты!](assets/8.png)

يمكن أن يكون المتغير قاموسًا، وبالتالي يمكن الوصول إلى الحقول الفرعية عبر النقطة.


```python
def hello(request):
    return render(request, 'index.html', { 'data' : {'current_date': date.today()}})
```

```python
    Today is {{ data.current_date }}
```

## العلامات في القوالب

في القالب، تبدو العلامات بالشكل `{% tag %}`. 
باستخدام العلامات، يمكنك تنفيذ الشروط، والحلقات، ومنطقك الخاص. يجب أن يتم إغلاق معظم العلامات:
`{% tag %} المحتوى {% endtag %}`

افترض أننا بحاجة إلى عرض قائمة بالعناصر. للقيام بذلك، سنستخدم `{% for %}`


`index.html`
```html
<!doctype html>
<html lang="en" class="h-100">
<head>
  <meta charset="utf-8">
    <title>BMSTU</title>
</head>
<body>
    Hello BMSTU students!
    Today is {{ data.current_date }}
<ul>
    {% for var in data.list %}
        <li>We like {{ var }}</li>
    {% endfor %}
</ul>
</body>
</html>
```

`views.py`
```python
from datetime import date

def hello(request):
    return render(request, 'index.html', { 'data' : {
        'current_date': date.today(),
        'list': ['python', 'django', 'html']
    }})
```

بعد تشغيل الخادم على المسار `http://127.0.0.1:8000/hello/` يجب أن ترى


![Привет студенты!](assets/9.png)
<div dir = "rtl">
     For  تقوم  بتكرار القائمة، ويمكن الوصول إلى العناصر من خلال المتغير المُنشأ، في هذه الحالة var.
</div>





`{% if variable %}` يتيح لك عرض محتوى الكتلة إذا كانت قيمة المتغير "صحيحة" (أو إذا كانت القيمة موجودة، أو إذا كانت القائمة غير فارغة). 
يمكن استخدام `{% elif %}` و`{% else %}` مع هذه العلامة.


`index.html`
```html
<ul>
    {% for var in data.list %}
        {% if var == 'python' %}
            <li>We like {{ var }}</li>
        {% elif var == 'django' %}
            <li>We like {{ var }} a lot!</li>
        {% else %}
            <li>We do not like {{ var }}</li>
        {% endif %}
    {% endfor %}
</ul>
```

بعد تشغيل الخادم على المسار `http://127.0.0.1:8000/hello/` يجب أن ترى

![Привет студенты!](assets/10.png)

 في علامة **if** يمكن استخدام:
 <div dir = "rtl">
- and
 </div>
 <div dir = "rtl">
 - or
 </div>
 <div dir = "rtl">
 - not
 </div>
 
-مشغلات المقارنة
 <div dir = "rtl">
- in (للتحقق مما إذا كانت القيمة موجودة في القائمة)
 </div>


## وراثة القوالب

تسمح وراثة القوالب بإنشاء قالب أساسي يحتوي على العناصر المشتركة، 
بينما ستقوم القوالب الفرعية بتجاوز الأماكن المحددة. 
تُحدد الأماكن التي يمكن تجاوزها بعلامات `{% block %}`.

افترض أن هناك قالبًا أساسيًا باسم `base.html`:

`base.html`
```html
<!doctype html>
<html lang="en" class="h-100">
<head>
  <meta charset="utf-8">
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    Hello BMSTU students!
    {% block content %}{% endblock %}
</body>
</html>
```
هنا يتم تحديد الجزء الذي سيكون موجودًا في كل صفحة ترث منه. 
سنقوم بإنشاء قالب فرعي باسم `orders.html` الذي سيعرض قائمة الطلبات:

`orders.html`
```html
{% extends 'base.html' %}

{% block title %}Список заказов{% endblock %}

{% block content %}
<ul>
    {% for order in data.orders %}
        <li><a href="{% url 'order_url' order.id %}">{{ order.title }}</a> </li>
    {% empty %}
        <li>Список пуст</li>
    {% endfor %}
</ul>
{% endblock %}
```

`views.py`
```python
def GetOrders(request):
    return render(request, 'orders.html', {'data' : {
        'current_date': date.today(),
        'orders': [
            {'title': 'Книга с картинками', 'id': 1},
            {'title': 'Бутылка с водой', 'id': 2},
            {'title': 'Коврик для мышки', 'id': 3},
        ]
    }})
```

لدى كل منتج، أضفنا رابطًا إلى صفحته الفردية بصيغة `{% url 'order_url' order.id %}`.

في ملف `urls.py`، يجب تحديد URL باسم 'order_url' الذي سيستقبل معرف الطلب:


`urls.py`
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.GetOrders),
    path('order/<int:id>/', views.GetOrder, name='order_url'),
]
```

سنقوم بإنشاء قالب لصفحة المنتج `order.html` وعرضها.

`order.html`
```html
{% extends 'base.html' %}

{% block title %}Заказ №{{ data.id }}{% endblock %}

{% block content %}
    <div>Информация о заказе №{{ data.id }}</div>
{% endblock %}
```

`views.py`
```python
def GetOrder(request, id):
    return render(request, 'order.html', {'data' : {
        'current_date': date.today(),
        'id': id
    }})
```

بعد تشغيل الخادم على المسار `http://127.0.0.1:8000/` يجب أن ترى

![Привет студенты!](assets/11.png)

على المسار `http://127.0.0.1:8000/order/2` يجب أن ترى

![Привет студенты!](assets/12.png)

## Include في القوالب

يسمح بعرض قالب آخر في مكان استخدام العلامة.

`orders.html`
```html
{% extends 'base.html' %}

{% block title %}Список заказов{% endblock %}

{% block content %}
<ul>
    {% for order in data.orders %}
       {% include 'order_element.html' with element=order %}
    {% empty %}
        <li>Список пуст</li>
    {% endfor %}
</ul>
{% endblock %}
```

`order_element.html`
```html
 <li><a href="{% url 'order_url' element.id %}">{{ element.title }}</a> </li>
```
<div dir="rtl">
with يسمح بتغيير السياق. أي في قالب order_element.html، لن يكون الوصول متاحاً فقط لـ order وorders، ولكن أيضًا لـ element.
</div>

## إضافة الملفات الثابتة

في `settings.py`، يتم تحديد المسار إلى الملفات الثابتة.

```python
STATIC_URL = '/bmstu_lab/static/'
```

```python
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

في التطبيق، نقوم بإنشاء مجلد ونضع فيه الملفات:

![Привет студенты!](assets/13.png)

نضع ملفات `.css` في مجلد منفصل `static/css`.

قبل استخدام الرابط إلى ملف ثابت، في القالب:

```html
{% load static %}
```

نستخدم الرابط:
```html
<link rel="stylesheet" type="text/css" href="{% static 'css/examp.css' %}">
```

مثال على `.css`
```css
.order-text {
  font-size: 40px;
}
```

مثال على قالب مع `css`

```html
<div class="order-text">Информация о заказе №{{ data.id }}</div>
```
## الحصول على البيانات من الطلب، input

لإرسال البيانات من المتصفح إلى خادم Django، يجب إضافة نموذج، وزر، وحقول إدخال إلى قالبنا.

```html
<form action="sendText" method="post" enctype="multipart/form-data">
    {% csrf_token %}
    <input name="text" type="text"><br><br>
    <input type="submit" value="Submit" >
</form>
```

أضف إلى `urls.py` معالج طلب POST الخاص بنا `views.sendText` للرابط [/sendText]() 
```python
path('sendText', views.sendText, name='sendText'),

```python
def sendText(request):
    input_text = request.POST['text']
    ...
```

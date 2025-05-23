# Linux

# 1.	Установка Python
Сначала посмотрите какая версия Python установлена в вашей системе. Для этого выполните команду:
```sh
 python3 --version
```

Новая версия, Python 3.9 доступна в репозиториях universe. Поэтому вам нет необходимости добавлять PPA, достаточно просто обновить систему и установить пакет нужной версии. Для этого наберите:
```sh
 sudo apt update
 sudo apt install python3.9
 ```
Обратите внимание, что старая версия никуда не делась, она по-прежнему доступна по имени python3, а новая теперь может быть загружена командой python 3.9. Если вы хотите использовать эту версию вместо 3.8 для запуска всех программ нужно выбрать её в качестве версии по умолчанию. Но я бы не рекомендовал этого делать. Множество системных программ написаны на Python и протестированы именно с версией, поставляемой по умолчанию. Если вы измените версию что-то может перестать работать. Если вы всё же решились надо сначала добавить альтернативы:

# 2.	Установка пакетов
Для управления программными пакетами Python используется инструмент pip, предназначенный для установки и управления пакетами программирования.
```sh
sudo apt install -y python3-pip
```
Пакеты Python можно установить с помощью следующей команды:
```sh
pip3 install package_name
```

# 3.	Виртуальное окружение (https://blog.sedicomm.com/2021/06/29/chto-takoe-venv-i-virtualenv-v-python-i-kak-ih-ispolzovat/#1) 
Чтобы создать виртуальную среду, мы используем модуль venv. Это удобный инструмент для управления зависимостями и изоляции проектов, который выстроен в Python, начиная с версии Python 3.3+. Поэтому модуль venv нельзя использовать для изоляции программ Python 2.
Установка venv:
```sh
sudo apt-get install python3-venv -y
```
## Создание проекта
Приступим к созданию проекта. Первым делом следует создать папку проекта и перейти в нее, в Linux это можно сделать при помощи следующих команд:
```sh
$ mkdir my_python_project
cd my_python_project
```

## Создание виртуальной среды
Теперь создадим в этой папке виртуальную среду:
```sh
python3 -m venv project_name_myproject
```
## Активация виртуальной среды
Осталось активировать виртуальную среду при помощи команды:
```sh
source project_name_myproject/bin/activate
```
## Проверка установленных пакетов
Теперь проверим установленные пакеты pip внутри виртуальной среды:
```sh
pip3 list
```
## Выход из виртуальной среды
Для выхода из виртуальной среды необходимо выполнить команду:
```sh
deactivate
```
## Перенос установленных пакетов
Для переноса установленных пакетов в другую среду на Linux можно использовать простую команду:
```sh
python3 -m pip freeze > requirements.txt
```
Она создаст файл requirements.txt, в котором будет находится список всех установленных пакетов.
## Импорт пакетов в другую среду
Теперь можно перейти в другую виртуальную среду и импортировать пакеты следующей командой:
```sh
pip3 install -r requirements.txt
```

## Pip-compile
Файл requirements.txt содержит сырой список зависимостей с жестко объявленными версиями. По этому списку часто сложно понять набор действительно необходимых пакетов для работы системы, а также управлять перекрестными зависимостями (теми, которые необходимы для работы пакетов первой необходимости).

Для подобных целей существует инструмент pip-compile. Он позволяет разделить требования к виртуальному окружению и список устанавливаемых зависимостей. Для этого требуется сформировать файл requirements.in, где записывается набор пакетов с необходимыми ограничениями по версиям (при необходимости). Пример requirements.in:
```sh
# requirements.in
django
```
Далее путем применения отдельной команды `pip-compile` данный файл "компилируется" и преобразуется в набор неконфликтующих зависимостей с зафиксированными версиями (файл requirements.txt).

Подробнее в [документации](https://pypi.org/project/pip-tools/)

# macOS

для установки Python на macOS используйте [Homebrew](https://brew.sh)

# Windows

С официального [сайта](https://www.python.org/downloads/windows/) скачайте необходимую версию Python на Windows

# 4.	SetPolicy (https://winrcmd.wordpress.com/2019/01/23/razreshit-powershell-scripty-powershell-execution-policy/)
По умолчанию скрипты Powershell блокируются для запуска. Механизм этот называется Execution Policy. Однако, зачастую необходимо разрешить выполнение скриптов, чтобы, например, иметь возможность выполнять их по расписанию в планировщике заданий.
Чтобы узнать, какая сейчас установлено политика, нужно воспользоваться командой
```sh
Get-ExecutionPolicy
```
Значения этой политики хранятся в реестре по следующему пути:
```
Компьютер\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\PowerShell\1\ShellIds\Microsoft.PowerShell
```
строковый параметр «ExecutionPolicy»
По умолчанию значение этого параметра выставлено в «Restricted» (ограниченный), что и запрещает выполнение скриптов.
На самом деле, область применения политики различная — она может устанавливаться на разных уровнях системы, таким образом она будет распространяться на компьютер (будет действовать для всех пользователей), только на текущего пользователя и т.п. Посмотреть эту информацию можно, добавив параметр -list
```
Get-ExecutionPolicy -list
```

## ИЗМЕНЕНИЕ ПОЛИТИКИ
Чтобы сменить политику, необходимо воспользоваться командой:
```
Set-ExecutionPolicy
```
Доступные значения:
Unrestricted, RemoteSigned, AllSigned, Restricted, Default, Bypass, Undefined
Наиболее интересны для нас первые четыре:
• Restricted — выполнение сценариев запрещено. Эта опция установлена по умолчанию. Команды в таком случае можно выполнять только в интерактивном режиме.
• All Signed — разрешено выполнение только сценариев, подписанных доверенным издателем.
• RemoteSigned — разрешено выполнение любых сценариев, созданных локально, а сценарии, созданные на удаленных системах, выполняются только в том случае, если подписаны доверенным издателем.
• Unrestricted — разрешено выполнение абсолютно любых сценариев.
Наиболее безопасным будет параметр RemoteSigned, который будет выполнять только сценарии, созданные вами локально.
Чтобы изменить политику, запустите Powershell от имени администратора и введите:
```
Set-ExecutionPolicy RemoteSigned
```
Видим запрос
```
Изменение политики выполнения
Политика выполнения защищает компьютер от ненадежных сценариев. Изменение политики выполнения может поставить под угрозу безопасность системы, как описано в разделе справки, вызываемом командой about_Execution_Policies и расположенном по адресу https:/go.microsoft.com/fwlink/?LinkID=135170 . Вы хотите изменить политику выполнения?
[Y] Да — Y [A] Да для всех — A [N] Нет — N [L] Нет для всех — L [S] Приостановить — S [?] Справка
(значением по умолчанию является «N»):
```
Выбираем пункт A .




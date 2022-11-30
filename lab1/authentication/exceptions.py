from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
    # Если возникает исключение, которые мы не обрабатываем здесь явно, мы
    # хотим передать его обработчику исключений по-умолчанию, предлагаемому
    # DRF. И все же, если мы обрабатываем такой тип исключения, нам нужен
    # доступ к сгенерированному DRF - получим его заранее здесь.
    response = exception_handler(exc, context)
    handlers = {
        'ValidationError': _handle_generic_error
    }
    # Определить тип текущего исключения. Мы воспользуемся этим сразу далее,
    # чтобы решить, делать ли это самостоятельно или отдать эту работу DRF.
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        # Если это исключение можно обработать - обработать :) В противном
        # случае, вернуть ответ сгенерированный стандартными средствами заранее
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):
    # Это самый простой обработчик исключений, который мы можем создать. Мы
    # берем ответ сгенерированный DRF и заключаем его в ключ 'errors'.
    response.data = {
        'errors': response.data
    }

    return response
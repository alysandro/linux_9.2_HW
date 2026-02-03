from collections.abc import Callable
import functools
from pathlib import Path
from typing import Any, TypeVar, cast


F = TypeVar('F', bound=Callable[..., Any])

LOGS_DIR = Path('logs')


def log(filename: str | None = None) -> Callable[[F], F]:
    """
    Декоратор для логирования вызова функций.

    Логирует:
    - начало выполнения функции (started);
    - успешное завершение (ok);
    - ошибку с типом исключения и входными параметрами.

    Все файлы логов сохраняются в директории logs/.
    Если filename не указан — вывод осуществляется в консоль.
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__

            # Формируем путь к лог-файлу
            log_file_path: Path | None = None
            if filename:
                path_obj = Path(filename)

                # ИСПРАВЛЕННОЕ УСЛОВИЕ:
                # Если путь абсолютный ИЛИ уже начинается с папки 'logs'
                if path_obj.is_absolute() or (path_obj.parts and path_obj.parts[0] == 'logs'):
                    log_file_path = path_obj
                else:
                    log_file_path = LOGS_DIR / path_obj

                # Создаем папку непосредственно перед записью
                log_file_path.parent.mkdir(exist_ok=True, parents=True)

            def write_log(message: str) -> None:
                if log_file_path:
                    with log_file_path.open('a', encoding='utf-8') as f:
                        f.write(message + '\n')
                else:
                    print(message)

            write_log(f'{func_name} started')

            try:
                result = func(*args, **kwargs)
                write_log(f'{func_name} ok')
                return result
            except Exception as exc:
                error_type = type(exc).__name__
                inputs = f'Inputs: {args}, {kwargs}'
                write_log(f'{func_name} error: {error_type}. {inputs}')  # Убрали таймстамп
                raise

        return cast('F', wrapper)

    return decorator

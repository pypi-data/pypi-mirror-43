# TELEGRAM-LOG

telegram_log - handler, для настройки логгирования в Telegram.

# Установка:

```bash
sudo pip install telegram_log
```

# Использование:
Пример конфигурации логгера с использованием телеграма:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] [{0} %(name)s:%(lineno)s] %(message)s'.format(HOSTNAME)
        }
    },
    'handlers': {
	    'console_handler':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'telegram_handler': {
            'level': 'DEBUG',
            'class': 'telegram_log.handler.TelegramHandler',
            'token': BOT_ID,
            'chat_ids': CHAT_IDS,
            'err_log_name': 'console',
            'formatter': 'verbose',
        },
    },

    'loggers': {
        'telegram_bot': {
            'handlers': ['telegram_handler'],
            'level': 'INFO',
            'propagate': False,
        },
        'console': {
            'handlers': ['console_handler'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}
```


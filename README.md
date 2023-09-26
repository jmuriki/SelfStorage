# Учебный проект devman SelfStorage

Сайт предлагает сервис по аренде складских ячеек для сезонного хранения или для вещей, которые выкинуть жалко,
авось пригодятся, а место дома занимают и на Авито фиг продашь.

## Как запустить проект в режиме разработчика
- Скачайте код
```bash
git clone https://github.com/jmuriki/SelfStorage.git
cd self_storage
```
- Создайте виртуальное окружение (необязательно)
*nix или MacOS:
```bash
python3 -m venv env
source env/bin/activate
```
Windows:
```bash
python -m venv env
source env/bin/activate
```
- Установите зависимости
```bash
pip install -r requirements.txt
```

- Установите [RollBar](https://docs.rollbar.com/docs/setup) и получите токен
- [Зарегистрируйтесь в ЮКасса](https://yookassa.ru/yooid/signup/step/phone)

  Создайте тестовый или реальный магазин и получите его ID и ключ

- Создайте файл .env и вставьте в него следующие строки:
```bash
DJANGO_DEBUG=True
ROLLBAR_ACCESS_TOKEN=<токен RollBar>
PAY_ACC=<ID магазина ЮКассы>
PAY_KEY=<ключ ЮКассы>
```

# Использование сайта 
- Пользование услугами, предлагаемыми на сайте, доступно только для зарегистрированных пользователей.

  В данный момент расчёт стоимости услуги хранения не производится. Сайт лишь демонстрирует работоспособность механизма
  проведения оплаты.

  Для выполнения тестовой оплаты войдите в ЛК, кликните по ссылке "Моя аренда" и произведите платёж.
  Используйте для оплаты [номер тестовой карты](https://yookassa.ru/developers/payment-acceptance/testing-and-going-live/testing#test-bank-card).
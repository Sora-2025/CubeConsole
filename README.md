# CubeConsole

[![Telegram](https://badgen.net/badge/Telegram/@CubeConsole/black/?icon=telegram "@CubeConsole")](https://t.me/CubeConsole)
[![Telegram](https://badgen.net/badge/Github/sora-2025%2FCubeConsole/purple/?icon=github "sora-2025/CubeConsole")](https://github.com/sora-2025/CubeConsole)

### Простой создатель Minecraft-серверов с GUI интерфейсом и открытым исходным кодом

## Идея

CubeConsole был создан для упрощения создания серверов при помощи GUI интерфейса, генерации команд запуска, менеджера плагинов и удобного редактора конфигурационных файлов в одном приложении. 

## Скриншоты
<figure>
    <img src="./screenshots/1.png" width="500">
    <figcaption><i>Главная страница</i></figcaption>
</figure>

<figure>
    <img src="./screenshots/2.png" width="500">
    <figcaption><i>Страница оформления</i></figcaption>
</figure>

## Роадмап

```mermaid
flowchart TD
    A1[Настройка оформления✅]:::done ==> A2[Сохранение в конфигах✅]:::done
    A2 ==> A3[Навигация✅]:::done
    A3 ==> A4[Смена языка✅]:::done

    A4 ==> B1[Перевод всех элементов UI на английский⏳]:::active
    B1 ==> B2[Загрузка файлов сервера и плагинов с API⏳]:::active
    B2 ==> B3[Рефакторинг всего кода⏳]:::active

    B3 ==> C1[Страница первого запуска📌]:::todo
    C1 ==> C2[Просмотр и редактирование файлов📌]:::todo
    C2 ==> C3[Поддержка большего числа языков📌]:::todo

    C3 ==> D1[Плагины для редактирования конфигов]:::future

    classDef done fill:#1f6feb,stroke:#58a6ff,color:#ffffff
    classDef active fill:#f1e05a,stroke:#d4c22b,color:#000000
    classDef todo fill:#30363d,stroke:#8b949e,color:#ffffff
    classDef future fill:#8957e5,stroke:#bc8cff,color:#ffffff
```

#### Лицензия

GPL-3.0
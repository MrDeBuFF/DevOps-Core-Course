# Lab 3: Continuous Integration (CI/CD)

## 1. Overview

### Testing framewor

pytest и это легко обосновать:
современный стандарт де-факто
минимум шаблонного кода
удобные фикстуры
отлично работает с Flask
поддерживается в CI без боли

Я выбрал pytest, так как он предоставляет простой синтаксис, удобные фикстуры и является стандартом для современных Python-проектов.




3 best practices (примеры)

Fail fast — Docker job зависит от тестов
Dependency caching — ускоряет CI
Conditional push — Docker только из master
Secrets management — без хардкода
import random
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Chat, Message, MessageType
from seeds.user_chats import chats

messages = [
    {
        'text': 'Разработан и поддерживается компанией Ericsson. Haskell — стандартизированный чистый функциональный язык программирования общего назначения. Парадигма программирования — это совокупность идей и понятий, определяющих стиль написания компьютерных программ. Приложения Java обычно транслируются в специальный байт-код, поэтому они могут работать на любой компьютерной архитектуре, с помощью виртуальной Java-машины. Например, определение функции, которое использует сопоставление с образцом, для выбора одного из вариантов вычисления или извлечения элемента данных из составной структуры, напоминает уравнение.'},
    {
        'text': 'В то же время стандартная библиотека включает большой объём полезных функций. Это способ концептуализации, определяющий организацию вычислений и структурирование работы, выполняемой компьютером. Полнотиповое программирование может поддерживаться на уровне системы типов языка или вводиться программистом идиоматически. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. Это способ концептуализации, определяющий организацию вычислений и структурирование работы, выполняемой компьютером.'},
    {
        'text': 'Haskell — стандартизированный чистый функциональный язык программирования общего назначения. Отличительная черта языка — серьёзное отношение к типизации. Например, определение функции, которое использует сопоставление с образцом, для выбора одного из вариантов вычисления или извлечения элемента данных из составной структуры, напоминает уравнение. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. Популярность Erlang начала расти в связи с расширением его области применения (телекоммуникационные системы) на высоконагруженные параллельные распределённые системы, обслуживающие миллионы пользователей WWW, такие как чаты, системы управления содержимым, веб-серверы и распределённые, требующие масштабирования базы данных.'},
    {
        'text': 'Python поддерживает несколько парадигм программирования, в том числе структурное, объектно-ориентированное, функциональное, императивное и аспектно-ориентированное. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. Это способ концептуализации, определяющий организацию вычислений и структурирование работы, выполняемой компьютером. Например, определение функции, которое использует сопоставление с образцом, для выбора одного из вариантов вычисления или извлечения элемента данных из составной структуры, напоминает уравнение. Свой синтаксис и некоторые концепции Erlang унаследовал от языка логического программирования Пролог.'},
    {
        'text': 'Синтаксис ядра Python минималистичен. Erlang применяется в нескольких NoSQL-базах данных высокой доступности. Приложения Java обычно транслируются в специальный байт-код, поэтому они могут работать на любой компьютерной архитектуре, с помощью виртуальной Java-машины. Синтаксис ядра Python минималистичен. Популярность Erlang начала расти в связи с расширением его области применения (телекоммуникационные системы) на высоконагруженные параллельные распределённые системы, обслуживающие миллионы пользователей WWW, такие как чаты, системы управления содержимым, веб-серверы и распределённые, требующие масштабирования базы данных.'},
    {
        'text': 'Парадигма программирования — это совокупность идей и понятий, определяющих стиль написания компьютерных программ. Это способ концептуализации, определяющий организацию вычислений и структурирование работы, выполняемой компьютером. Свой синтаксис и некоторые концепции Erlang унаследовал от языка логического программирования Пролог. Python — высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Erlang применяется в нескольких NoSQL-базах данных высокой доступности.'},
    {
        'text': 'Полнотиповое программирование — стиль программирования, отличающийся обширным использованием информации о типах с тем, чтобы механизм проверки согласования типов обеспечил раннее выявление максимального количества всевозможных разновидностей багов. Erlang применяется в нескольких NoSQL-базах данных высокой доступности. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. Erlang был целенаправленно разработан для применения в распределённых, отказоустойчивых, параллельных системах реального времени, для которых кроме средств самого языка имеется стандартная библиотека модулей и библиотека шаблонных решений (так называемых поведений) — фреймворк OTP. В то же время стандартная библиотека включает большой объём полезных функций.'},
    {
        'text': 'Полнотиповое программирование — стиль программирования, отличающийся обширным использованием информации о типах с тем, чтобы механизм проверки согласования типов обеспечил раннее выявление максимального количества всевозможных разновидностей багов. В то же время стандартная библиотека включает большой объём полезных функций. REPL — форма организации простой интерактивной среды программирования в рамках средств интерфейса командной строки. Полнотиповое программирование может поддерживаться на уровне системы типов языка или вводиться программистом идиоматически. Например, определение функции, которое использует сопоставление с образцом, для выбора одного из вариантов вычисления или извлечения элемента данных из составной структуры, напоминает уравнение.'},
    {
        'text': 'Является одним из самых распространённых языков программирования с поддержкой отложенных вычислений. Erlang является декларативным языком программирования, который скорее используется для описания того, что должно быть вычислено нежели как. Полнотиповое программирование может поддерживаться на уровне системы типов языка или вводиться программистом идиоматически. Полнотиповое программирование — стиль программирования, отличающийся обширным использованием информации о типах с тем, чтобы механизм проверки согласования типов обеспечил раннее выявление максимального количества всевозможных разновидностей багов. Является одним из самых распространённых языков программирования с поддержкой отложенных вычислений.'},
    {
        'text': 'Отличительная черта языка — серьёзное отношение к типизации. Является одним из самых распространённых языков программирования с поддержкой отложенных вычислений. Полнотиповое программирование — стиль программирования, отличающийся обширным использованием информации о типах с тем, чтобы механизм проверки согласования типов обеспечил раннее выявление максимального количества всевозможных разновидностей багов. Популярность Erlang начала расти в связи с расширением его области применения (телекоммуникационные системы) на высоконагруженные параллельные распределённые системы, обслуживающие миллионы пользователей WWW, такие как чаты, системы управления содержимым, веб-серверы и распределённые, требующие масштабирования базы данных. Python — высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода.'},
    {
        'text': 'Erlang применяется в нескольких NoSQL-базах данных высокой доступности. Python поддерживает несколько парадигм программирования, в том числе структурное, объектно-ориентированное, функциональное, императивное и аспектно-ориентированное. Это способ концептуализации, определяющий организацию вычислений и структурирование работы, выполняемой компьютером. Синтаксис ядра Python минималистичен. Haskell — стандартизированный чистый функциональный язык программирования общего назначения.'},
    {
        'text': 'Python поддерживает несколько парадигм программирования, в том числе структурное, объектно-ориентированное, функциональное, императивное и аспектно-ориентированное. Синтаксис ядра Python минималистичен. Python поддерживает несколько парадигм программирования, в том числе структурное, объектно-ориентированное, функциональное, императивное и аспектно-ориентированное. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. Популярность Erlang начала расти в связи с расширением его области применения (телекоммуникационные системы) на высоконагруженные параллельные распределённые системы, обслуживающие миллионы пользователей WWW, такие как чаты, системы управления содержимым, веб-серверы и распределённые, требующие масштабирования базы данных.'},
    {
        'text': 'Приложения Java обычно транслируются в специальный байт-код, поэтому они могут работать на любой компьютерной архитектуре, с помощью виртуальной Java-машины. Erlang был целенаправленно разработан для применения в распределённых, отказоустойчивых, параллельных системах реального времени, для которых кроме средств самого языка имеется стандартная библиотека модулей и библиотека шаблонных решений (так называемых поведений) — фреймворк OTP. Java — строго типизированный объектно-ориентированный язык программирования, разработанный компанией Sun Microsystems. Python поддерживает несколько парадигм программирования, в том числе структурное, объектно-ориентированное, функциональное, императивное и аспектно-ориентированное. Python — высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода.'},
    {
        'text': 'Полнотиповое программирование может поддерживаться на уровне системы типов языка или вводиться программистом идиоматически. Синтаксис ядра Python минималистичен. В то же время стандартная библиотека включает большой объём полезных функций. Erlang — функциональный язык программирования с сильной динамической типизацией, предназначенный для создания распределённых вычислительных систем. Полнотиповое программирование — стиль программирования, отличающийся обширным использованием информации о типах с тем, чтобы механизм проверки согласования типов обеспечил раннее выявление максимального количества всевозможных разновидностей багов.'},
    {
        'text': 'Отличительная черта языка — серьёзное отношение к типизации. Например, определение функции, которое использует сопоставление с образцом, для выбора одного из вариантов вычисления или извлечения элемента данных из составной структуры, напоминает уравнение. Синтаксис ядра Python минималистичен. Язык включает в себя средства порождения параллельных легковесных процессов и их взаимодействия через обмен асинхронными сообщениями в соответствии с моделью акторов. Полнотиповое программирование может поддерживаться на уровне системы типов языка или вводиться программистом идиоматически.'},
    {
        'text': 'Язык включает в себя средства порождения параллельных легковесных процессов и их взаимодействия через обмен асинхронными сообщениями в соответствии с моделью акторов. В то же время стандартная библиотека включает большой объём полезных функций. Java — строго типизированный объектно-ориентированный язык программирования, разработанный компанией Sun Microsystems. Python — высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Haskell — стандартизированный чистый функциональный язык программирования общего назначения.'},
    {
        'text': 'Язык включает в себя средства порождения параллельных легковесных процессов и их взаимодействия через обмен асинхронными сообщениями в соответствии с моделью акторов. В наш век информации слишком много, чтобы понять кто прав, а кто лукавит. REPL — форма организации простой интерактивной среды программирования в рамках средств интерфейса командной строки. Например, определение функции, которое использует сопоставление с образцом, для выбора одного из вариантов вычисления или извлечения элемента данных из составной структуры, напоминает уравнение. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов.'},
    {
        'text': 'Язык включает в себя средства порождения параллельных легковесных процессов и их взаимодействия через обмен асинхронными сообщениями в соответствии с моделью акторов. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. Python поддерживает несколько парадигм программирования, в том числе структурное, объектно-ориентированное, функциональное, императивное и аспектно-ориентированное. Популярность Erlang начала расти в связи с расширением его области применения (телекоммуникационные системы) на высоконагруженные параллельные распределённые системы, обслуживающие миллионы пользователей WWW, такие как чаты, системы управления содержимым, веб-серверы и распределённые, требующие масштабирования базы данных. В то же время стандартная библиотека включает большой объём полезных функций.'},
    {
        'text': 'В то же время стандартная библиотека включает большой объём полезных функций. Python — высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Приложения Java обычно транслируются в специальный байт-код, поэтому они могут работать на любой компьютерной архитектуре, с помощью виртуальной Java-машины. Разработан и поддерживается компанией Ericsson. Erlang применяется в нескольких NoSQL-базах данных высокой доступности.'},
    {
        'text': 'Синтаксис ядра Python минималистичен. Полнотиповое программирование может поддерживаться на уровне системы типов языка или вводиться программистом идиоматически. Python — высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. Язык включает в себя средства порождения параллельных легковесных процессов и их взаимодействия через обмен асинхронными сообщениями в соответствии с моделью акторов.'},
    {
        'text': 'В наш век информации слишком много, чтобы понять кто прав, а кто лукавит. Полнотиповое программирование — стиль программирования, отличающийся обширным использованием информации о типах с тем, чтобы механизм проверки согласования типов обеспечил раннее выявление максимального количества всевозможных разновидностей багов. Erlang — функциональный язык программирования с сильной динамической типизацией, предназначенный для создания распределённых вычислительных систем. Язык включает в себя средства порождения параллельных легковесных процессов и их взаимодействия через обмен асинхронными сообщениями в соответствии с моделью акторов. Haskell — стандартизированный чистый функциональный язык программирования общего назначения.'},
    {
        'text': 'Python поддерживает несколько парадигм программирования, в том числе структурное, объектно-ориентированное, функциональное, императивное и аспектно-ориентированное. Синтаксис ядра Python минималистичен. Приложения Java обычно транслируются в специальный байт-код, поэтому они могут работать на любой компьютерной архитектуре, с помощью виртуальной Java-машины. Например, определение функции, которое использует сопоставление с образцом, для выбора одного из вариантов вычисления или извлечения элемента данных из составной структуры, напоминает уравнение. Популярность Erlang начала расти в связи с расширением его области применения (телекоммуникационные системы) на высоконагруженные параллельные распределённые системы, обслуживающие миллионы пользователей WWW, такие как чаты, системы управления содержимым, веб-серверы и распределённые, требующие масштабирования базы данных.'},
    {
        'text': 'Отличительная черта языка — серьёзное отношение к типизации. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. Erlang — функциональный язык программирования с сильной динамической типизацией, предназначенный для создания распределённых вычислительных систем. Полнотиповое программирование может поддерживаться на уровне системы типов языка или вводиться программистом идиоматически. Является одним из самых распространённых языков программирования с поддержкой отложенных вычислений.'},
    {
        'text': 'Синтаксис ядра Python минималистичен. Python — высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Язык включает в себя средства порождения параллельных легковесных процессов и их взаимодействия через обмен асинхронными сообщениями в соответствии с моделью акторов. Отличительная черта языка — серьёзное отношение к типизации. Язык включает в себя средства порождения параллельных легковесных процессов и их взаимодействия через обмен асинхронными сообщениями в соответствии с моделью акторов.'},
    {
        'text': 'Полнотиповое программирование — стиль программирования, отличающийся обширным использованием информации о типах с тем, чтобы механизм проверки согласования типов обеспечил раннее выявление максимального количества всевозможных разновидностей багов. REPL — форма организации простой интерактивной среды программирования в рамках средств интерфейса командной строки. В наш век информации слишком много, чтобы понять кто прав, а кто лукавит. Например, определение функции, которое использует сопоставление с образцом, для выбора одного из вариантов вычисления или извлечения элемента данных из составной структуры, напоминает уравнение. В то же время стандартная библиотека включает большой объём полезных функций.'},
    {
        'text': 'Erlang был целенаправленно разработан для применения в распределённых, отказоустойчивых, параллельных системах реального времени, для которых кроме средств самого языка имеется стандартная библиотека модулей и библиотека шаблонных решений (так называемых поведений) — фреймворк OTP. Erlang — функциональный язык программирования с сильной динамической типизацией, предназначенный для создания распределённых вычислительных систем. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. Является одним из самых распространённых языков программирования с поддержкой отложенных вычислений. Полнотиповое программирование может поддерживаться на уровне системы типов языка или вводиться программистом идиоматически.'},
    {
        'text': 'Haskell — стандартизированный чистый функциональный язык программирования общего назначения. Приложения Java обычно транслируются в специальный байт-код, поэтому они могут работать на любой компьютерной архитектуре, с помощью виртуальной Java-машины. Java — строго типизированный объектно-ориентированный язык программирования, разработанный компанией Sun Microsystems. Язык включает в себя средства порождения параллельных легковесных процессов и их взаимодействия через обмен асинхронными сообщениями в соответствии с моделью акторов. Erlang — функциональный язык программирования с сильной динамической типизацией, предназначенный для создания распределённых вычислительных систем.'},
    {
        'text': 'В наш век информации слишком много, чтобы понять кто прав, а кто лукавит. В наш век информации слишком много, чтобы понять кто прав, а кто лукавит. Например, определение функции, которое использует сопоставление с образцом, для выбора одного из вариантов вычисления или извлечения элемента данных из составной структуры, напоминает уравнение. Свой синтаксис и некоторые концепции Erlang унаследовал от языка логического программирования Пролог. Приложения Java обычно транслируются в специальный байт-код, поэтому они могут работать на любой компьютерной архитектуре, с помощью виртуальной Java-машины.'},
    {
        'text': 'Это способ концептуализации, определяющий организацию вычислений и структурирование работы, выполняемой компьютером. Erlang применяется в нескольких NoSQL-базах данных высокой доступности. Разработан и поддерживается компанией Ericsson. В наш век информации слишком много, чтобы понять кто прав, а кто лукавит. Отличительная черта языка — серьёзное отношение к типизации.'},
    {
        'text': 'Приложения Java обычно транслируются в специальный байт-код, поэтому они могут работать на любой компьютерной архитектуре, с помощью виртуальной Java-машины. Python поддерживает несколько парадигм программирования, в том числе структурное, объектно-ориентированное, функциональное, императивное и аспектно-ориентированное. Популярность Erlang начала расти в связи с расширением его области применения (телекоммуникационные системы) на высоконагруженные параллельные распределённые системы, обслуживающие миллионы пользователей WWW, такие как чаты, системы управления содержимым, веб-серверы и распределённые, требующие масштабирования базы данных. Приложения Java обычно транслируются в специальный байт-код, поэтому они могут работать на любой компьютерной архитектуре, с помощью виртуальной Java-машины. Разработан и поддерживается компанией Ericsson.'},
    {
        'text': 'Язык включает в себя средства порождения параллельных легковесных процессов и их взаимодействия через обмен асинхронными сообщениями в соответствии с моделью акторов. REPL — форма организации простой интерактивной среды программирования в рамках средств интерфейса командной строки. В то же время стандартная библиотека включает большой объём полезных функций. Полнотиповое программирование может поддерживаться на уровне системы типов языка или вводиться программистом идиоматически. Отличительная черта языка — серьёзное отношение к типизации.'},
    {
        'text': 'В то же время стандартная библиотека включает большой объём полезных функций. Синтаксис ядра Python минималистичен. Полнотиповое программирование может поддерживаться на уровне системы типов языка или вводиться программистом идиоматически. Например, определение функции, которое использует сопоставление с образцом, для выбора одного из вариантов вычисления или извлечения элемента данных из составной структуры, напоминает уравнение. Erlang является декларативным языком программирования, который скорее используется для описания того, что должно быть вычислено нежели как.'},
    {
        'text': 'Популярность Erlang начала расти в связи с расширением его области применения (телекоммуникационные системы) на высоконагруженные параллельные распределённые системы, обслуживающие миллионы пользователей WWW, такие как чаты, системы управления содержимым, веб-серверы и распределённые, требующие масштабирования базы данных. Python — высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Синтаксис ядра Python минималистичен. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. REPL — форма организации простой интерактивной среды программирования в рамках средств интерфейса командной строки.'},
    {
        'text': 'Синтаксис ядра Python минималистичен. Полнотиповое программирование может поддерживаться на уровне системы типов языка или вводиться программистом идиоматически. Популярность Erlang начала расти в связи с расширением его области применения (телекоммуникационные системы) на высоконагруженные параллельные распределённые системы, обслуживающие миллионы пользователей WWW, такие как чаты, системы управления содержимым, веб-серверы и распределённые, требующие масштабирования базы данных. Синтаксис ядра Python минималистичен. Полнотиповое программирование — стиль программирования, отличающийся обширным использованием информации о типах с тем, чтобы механизм проверки согласования типов обеспечил раннее выявление максимального количества всевозможных разновидностей багов.'},
    {
        'text': 'Это способ концептуализации, определяющий организацию вычислений и структурирование работы, выполняемой компьютером. Синтаксис ядра Python минималистичен. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. Свой синтаксис и некоторые концепции Erlang унаследовал от языка логического программирования Пролог. Приложения Java обычно транслируются в специальный байт-код, поэтому они могут работать на любой компьютерной архитектуре, с помощью виртуальной Java-машины.'},
    {
        'text': 'Python поддерживает несколько парадигм программирования, в том числе структурное, объектно-ориентированное, функциональное, императивное и аспектно-ориентированное. Является одним из самых распространённых языков программирования с поддержкой отложенных вычислений. Синтаксис ядра Python минималистичен. Свой синтаксис и некоторые концепции Erlang унаследовал от языка логического программирования Пролог. В то же время стандартная библиотека включает большой объём полезных функций.'},
    {
        'text': 'Java — строго типизированный объектно-ориентированный язык программирования, разработанный компанией Sun Microsystems. Разработан и поддерживается компанией Ericsson. Синтаксис ядра Python минималистичен. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. Является одним из самых распространённых языков программирования с поддержкой отложенных вычислений.'},
    {
        'text': 'Полнотиповое программирование может поддерживаться на уровне системы типов языка или вводиться программистом идиоматически. Erlang является декларативным языком программирования, который скорее используется для описания того, что должно быть вычислено нежели как. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. Python — высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Erlang был целенаправленно разработан для применения в распределённых, отказоустойчивых, параллельных системах реального времени, для которых кроме средств самого языка имеется стандартная библиотека модулей и библиотека шаблонных решений (так называемых поведений) — фреймворк OTP.'},
    {
        'text': 'В то же время стандартная библиотека включает большой объём полезных функций. Java — строго типизированный объектно-ориентированный язык программирования, разработанный компанией Sun Microsystems. Популярность Erlang начала расти в связи с расширением его области применения (телекоммуникационные системы) на высоконагруженные параллельные распределённые системы, обслуживающие миллионы пользователей WWW, такие как чаты, системы управления содержимым, веб-серверы и распределённые, требующие масштабирования базы данных. Популярность Erlang начала расти в связи с расширением его области применения (телекоммуникационные системы) на высоконагруженные параллельные распределённые системы, обслуживающие миллионы пользователей WWW, такие как чаты, системы управления содержимым, веб-серверы и распределённые, требующие масштабирования базы данных. Например, определение функции, которое использует сопоставление с образцом, для выбора одного из вариантов вычисления или извлечения элемента данных из составной структуры, напоминает уравнение.'},
    {
        'text': 'Erlang применяется в нескольких NoSQL-базах данных высокой доступности. Erlang является декларативным языком программирования, который скорее используется для описания того, что должно быть вычислено нежели как. Например, определение функции, которое использует сопоставление с образцом, для выбора одного из вариантов вычисления или извлечения элемента данных из составной структуры, напоминает уравнение. Python — высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Haskell — стандартизированный чистый функциональный язык программирования общего назначения.'},
    {
        'text': 'Является одним из самых распространённых языков программирования с поддержкой отложенных вычислений. Является одним из самых распространённых языков программирования с поддержкой отложенных вычислений. Является одним из самых распространённых языков программирования с поддержкой отложенных вычислений. Отличительная черта языка — серьёзное отношение к типизации. Является одним из самых распространённых языков программирования с поддержкой отложенных вычислений.'},
    {
        'text': 'Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. В то же время стандартная библиотека включает большой объём полезных функций. Erlang является декларативным языком программирования, который скорее используется для описания того, что должно быть вычислено нежели как. Полнотиповое программирование может поддерживаться на уровне системы типов языка или вводиться программистом идиоматически. Свой синтаксис и некоторые концепции Erlang унаследовал от языка логического программирования Пролог.'},
    {
        'text': 'В наш век информации слишком много, чтобы понять кто прав, а кто лукавит. Полнотиповое программирование — стиль программирования, отличающийся обширным использованием информации о типах с тем, чтобы механизм проверки согласования типов обеспечил раннее выявление максимального количества всевозможных разновидностей багов. Python поддерживает несколько парадигм программирования, в том числе структурное, объектно-ориентированное, функциональное, императивное и аспектно-ориентированное. Erlang был целенаправленно разработан для применения в распределённых, отказоустойчивых, параллельных системах реального времени, для которых кроме средств самого языка имеется стандартная библиотека модулей и библиотека шаблонных решений (так называемых поведений) — фреймворк OTP. Erlang применяется в нескольких NoSQL-базах данных высокой доступности.'},
    {
        'text': 'Является одним из самых распространённых языков программирования с поддержкой отложенных вычислений. Python — высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Свой синтаксис и некоторые концепции Erlang унаследовал от языка логического программирования Пролог. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. Erlang применяется в нескольких NoSQL-базах данных высокой доступности.'},
    {
        'text': 'Свой синтаксис и некоторые концепции Erlang унаследовал от языка логического программирования Пролог. Haskell — стандартизированный чистый функциональный язык программирования общего назначения. Например, определение функции, которое использует сопоставление с образцом, для выбора одного из вариантов вычисления или извлечения элемента данных из составной структуры, напоминает уравнение. Является одним из самых распространённых языков программирования с поддержкой отложенных вычислений. Erlang является декларативным языком программирования, который скорее используется для описания того, что должно быть вычислено нежели как.'},
    {
        'text': 'Java — строго типизированный объектно-ориентированный язык программирования, разработанный компанией Sun Microsystems. Python поддерживает несколько парадигм программирования, в том числе структурное, объектно-ориентированное, функциональное, императивное и аспектно-ориентированное. Erlang был целенаправленно разработан для применения в распределённых, отказоустойчивых, параллельных системах реального времени, для которых кроме средств самого языка имеется стандартная библиотека модулей и библиотека шаблонных решений (так называемых поведений) — фреймворк OTP. Популярность Erlang начала расти в связи с расширением его области применения (телекоммуникационные системы) на высоконагруженные параллельные распределённые системы, обслуживающие миллионы пользователей WWW, такие как чаты, системы управления содержимым, веб-серверы и распределённые, требующие масштабирования базы данных. Например, определение функции, которое использует сопоставление с образцом, для выбора одного из вариантов вычисления или извлечения элемента данных из составной структуры, напоминает уравнение.'},
    {
        'text': 'Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. Erlang применяется в нескольких NoSQL-базах данных высокой доступности. Erlang был целенаправленно разработан для применения в распределённых, отказоустойчивых, параллельных системах реального времени, для которых кроме средств самого языка имеется стандартная библиотека модулей и библиотека шаблонных решений (так называемых поведений) — фреймворк OTP. В то же время стандартная библиотека включает большой объём полезных функций. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов.'},
    {
        'text': 'Python — высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Например, определение функции, которое использует сопоставление с образцом, для выбора одного из вариантов вычисления или извлечения элемента данных из составной структуры, напоминает уравнение. В то же время стандартная библиотека включает большой объём полезных функций. Приложения Java обычно транслируются в специальный байт-код, поэтому они могут работать на любой компьютерной архитектуре, с помощью виртуальной Java-машины. Erlang применяется в нескольких NoSQL-базах данных высокой доступности.'},
    {
        'text': 'Отличительная черта языка — серьёзное отношение к типизации. Сопоставление с образцом распространено даже на битовые строки, что упрощает реализацию телекоммуникационных протоколов. Полнотиповое программирование может поддерживаться на уровне системы типов языка или вводиться программистом идиоматически. Java — строго типизированный объектно-ориентированный язык программирования, разработанный компанией Sun Microsystems. Java — строго типизированный объектно-ориентированный язык программирования, разработанный компанией Sun Microsystems.'},
    {
        'text': 'Язык включает в себя средства порождения параллельных легковесных процессов и их взаимодействия через обмен асинхронными сообщениями в соответствии с моделью акторов. Python — высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. REPL — форма организации простой интерактивной среды программирования в рамках средств интерфейса командной строки. Python поддерживает несколько парадигм программирования, в том числе структурное, объектно-ориентированное, функциональное, императивное и аспектно-ориентированное. Парадигма программирования — это совокупность идей и понятий, определяющих стиль написания компьютерных программ.'
    }
]

replies = [
    {'text': 'Возможно'},
    {'text': 'Нет'},
    {'text': 'Возможно'},
    {'text': 'Возможно'},
    {'text': 'Неизвестно'},
    {'text': 'Нет'},
    {'text': 'Возможно'},
    {'text': 'Да'},
    {'text': 'Неизвестно'},
    {'text': 'Возможно'},
    {'text': 'Неизвестно'},
    {'text': 'Нет'},
    {'text': 'Нет'},
    {'text': 'Нет'},
    {'text': 'Неизвестно'},
    {'text': 'Неизвестно'},
    {'text': 'Нет'},
    {'text': 'Нет'},
    {'text': 'Возможно'},
    {'text': 'Неизвестно'},
    {'text': 'Нет'},
    {'text': 'Возможно'},
    {'text': 'Неизвестно'},
    {'text': 'Возможно'},
    {'text': 'Неизвестно'},
    {'text': 'Нет'},
    {'text': 'Да'},
    {'text': 'Неизвестно'},
    {'text': 'Возможно'},
    {'text': 'Да'},
    {'text': 'Нет'},
    {'text': 'Возможно'},
    {'text': 'Нет'},
    {'text': 'Нет'},
    {'text': 'Неизвестно'},
    {'text': 'Нет'},
    {'text': 'Возможно'},
    {'text': 'Да'},
    {'text': 'Неизвестно'},
    {'text': 'Нет'},
    {'text': 'Возможно'},
    {'text': 'Да'},
    {'text': 'Да'},
    {'text': 'Нет'},
    {'text': 'Нет'},
    {'text': 'Неизвестно'},
    {'text': 'Да'},
    {'text': 'Возможно'},
    {'text': 'Возможно'},
    {'text': 'Да'},
    {'text': 'Неизвестно'},
    {'text': 'Неизвестно'},
    {'text': 'Да'},
    {'text': 'Да'},
    {'text': 'Нет'},
    {'text': 'Да'},
    {'text': 'Да'},
    {'text': 'Возможно'},
    {'text': 'Нет'},
    {'text': 'Да'},
    {'text': 'Неизвестно'},
    {'text': 'Нет'},
    {'text': 'Возможно'},
    {'text': 'Да'},
    {'text': 'Нет'},
    {'text': 'Нет'},
    {'text': 'Нет'},
    {'text': 'Нет'},
    {'text': 'Да'},
    {'text': 'Возможно'},
    {'text': 'Нет'},
    {'text': 'Нет'},
    {'text': 'Да'},
    {'text': 'Неизвестно'},
    {'text': 'Нет'},
    {'text': 'Неизвестно'},
    {'text': 'Да'},
    {'text': 'Возможно'},
    {'text': 'Да'},
    {'text': 'Возможно'},
    {'text': 'Да'},
    {'text': 'Да'},
    {'text': 'Нет'},
    {'text': 'Неизвестно'},
    {'text': 'Нет'},
    {'text': 'Неизвестно'},
    {'text': 'Возможно'},
    {'text': 'Нет'},
    {'text': 'Неизвестно'},
    {'text': 'Неизвестно'},
    {'text': 'Неизвестно'},
    {'text': 'Нет'},
    {'text': 'Неизвестно'},
    {'text': 'Возможно'},
    {'text': 'Неизвестно'},
    {'text': 'Нет'},
    {'text': 'Да'},
    {'text': 'Неизвестно'},
    {'text': 'Да'},
    {'text': 'Нет'}
]


async def get_messages(session: AsyncSession):
    result = []

    for seed_chat in chats:
        chat = await session.get(Chat, seed_chat['id'])
        users = (await session.scalars(chat.users.statement)).all()

        reply_count = 0
        reply_uuid = None
        msg_created_at = chat.created_at

        for i in range(1):
            for user in users:
                msg_created_at = msg_created_at + timedelta(minutes=10)

                if reply_count > 3:
                    reply_count = 0

                if reply_count == 0:
                    message = Message(
                        user_id=user.id,
                        type=MessageType.text.value,
                        external={
                            'text': random.choice(messages)['text']
                        },
                        created_at=msg_created_at,
                        updated_at=msg_created_at,
                    )
                    chat.messages.append(message)

                    # После добавления возращается присвоенный uuid
                    session.add(message)
                    await session.commit()

                    reply_msg: Message = message
                    reply_count += 1
                else:
                    message = Message(
                        user_id=user.id,
                        parent_id=reply_msg.id,
                        type=MessageType.text.value,
                        external={
                            'reply': reply_msg.external,
                            'text': random.choice(replies)['text']
                        },
                        created_at=msg_created_at,
                        updated_at=msg_created_at,
                    )
                    chat.messages.append(message)

                    # После добавления возращается присвоенный uuid
                    session.add(message)
                    await session.commit()

                    reply_count += 1

    return result
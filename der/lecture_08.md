---
layout: default
---

# Лекция 8



<a name="linear_linked_list_in_heap">
## Линейный односвязный список в динамической памяти
</a>

 
Воспользуемся для создания линейного списка [шаблон](lecture_07.html#13) структурой `node` из 7 лекции:

```cpp
template<typename T>
struct node
{
    T data;
    node<T>* next;

    node(T data, node<T>* next)
    {
        // this указатель на себя
        this->data = data;
        this->node = next;
    }
};
```

При объявлении нового экземпляра структуры `node`, как это описано 
в предыдущей лекции, этот объект создается в статической памяти.
То есть объект `n1` будет храниться на стеке:

```cpp
node<int> n1(5, nullptr);
```

В реальных программах, ввиду сильной ограниченности размера стека, 
объекты размещают в динамической памяти.

#### Как создать node<T> в динамической памяти

```cpp
node<int>* pn = new node<int>(5, nullptr);
```

В C++ динамическую память выделяет не конструктор, а оператор `new`. 
Конструктор только создает объект в выделенной памяти. 

В отличии от **.NET** в C++ нет сборщика мусора, и ответственным
за удаление объекта из динамической памяти, является программист.

В C++ _размерная модель_ объектов, а ссылочную можно 
моделировать с помощью указателей.



<a name="adding_element_to_beginning_of_linked_list">
## Добавление элемента в начало односвязного списка
</a>

 
```cpp
node<int>* pn = nullptr;
pn = new node<int>(5, pn);
```

Операцию добавления первого элемента в односвязный список мы
оформим в виде отдельной функции. Создадим шаблон такой функции.

```cpp
tempate <typename T>
void add_first(node<T>* &pn, T x)
{
    pn = new node<T>(x, pn);
}
```

Запись `node<T>* &pn` означает, что `pn` это ссылка на указатель 
типа `node<T>`, и изменения происходящие с ней внутри фунцкии 
повлияют и на изменение фактического параметра.

```cpp
node<int>* pn = nullptr;

add_first(pn, 5);
add_first(pn, 3);
...
```

![singly_linked_list](../img/singly_linked_list.png "Создание односвязного списка")

Надо обратить внимание на то, что в отличии от шаблона структуры, 
в шаблоне функции указывать тип не надо, он автоматически 
выводится по типам фактических параметров.




<a name="where_to_store_template_funcs_structs_and_classes">
### Где хранить шаблоны функций, структур и классов.
</a>

 
В результате компиляции шаблона генерируется 0 байт, поскольку 
конкретный тип не указан. Если описать шаблон функции в одном 
`*.cpp` файле, то при многофайловой компоновке программы эта функция 
не будет доступна в другом файле.

**Решение.** Все шаблоны функций, классов и структур должны быть помещены в 
заголовочные файлы.

Для шаблонов функций конкретный код генерируется при вызове функции, 
когда становится известен конкретный тип `Т`. Подстановка конкретного 
типа в шаблон называется **инстанцированием** шаблона.
Количество инстанций зависит от количества используемых типов.

В C++ шаблоны компилируются в два этапа:

1. Компиляция собствено шаблона
2. Компиляция шаблона инстанцированного конкретным типом.

И на каждом этапе могут возникнуть ошибки. 




<a name="unlike_cpp_templates_generalizations_dot_net">
### Отличие шаблонов C++ от обобщений .NET
</a>

 
* В С++ компиляция шаблонов проходит в два этапа, а в **.NET** обобщения компилируются 1 раз.

* В С++ в результате компиляции шаблона получается исполняемый код инстанцированных 
функций, структур и классов. В **.NET** в результате компиляции обобщения создается 
исполняемый код самого обобщения т.е в **.NET** можно создать dll с обобщенным классом.

```cpp
template<typename T>
T inc(T t)
{
    return t + 1;
}
```

* В C++ разрешаются все действия с типом T, а в .NET и Java запрещаются все действия 
которые явно не разрешены (разрешения делаются в where). 

```cpp
Student s(...);
inc(s);  // В C++ произойдет ошибка на этапе компиляции
         // А в динамических языках это ошибка времени исполнения
```



<a name="loop_through_linked_list">
## Цикл по односвязному списку
</a>

 
```cpp
template <typename T>
void print(node<T>* p)
{
    while(p)
    {
        cout << p -> data << ' ';
        p = p -> next;
    }
}
```



<a name="function_pointers">
## Указатели на функции
</a>

 
В PascalABC.NET работа с указателями на функции осуществляется следующим образом:

```pas
type BitOp = function (a, b: real): real;

var op: BinOp;
write(op(3, 5));
op := mult;
write(op(3, 5));
```

Аналогичный код на C++ выглядит так:

```cpp
// Указатель на функцию с таким прототипом
typedef double (*BinOp) (double, double);

BinOp bop = &add;
(*bop)(3, 5);


// Или как и описание переменной
double (*op)(double, double)

op = mult;
op(3, 5);    // Так тоже можно вызывать template <typename T>
```



<a name="callback">
### Действие передаваемое параметром (callback)
</a>

 
```cpp
template <typename T>
// action — переменная типа "указатель на функцию"
void for_each(node<T>* p, void (*action)(T&))
{
    while(p)
    {
        action(p -> data);
        p = p -> next;
    }
}

void print(int &x)
{
    cout << x << ' ';
}

void inc(int &x)
{
    x++;
}

for_each(pn, print);
for_each(pn, inc);
for_each(pn, print);
```

В языке C/C++ структурная эквивалентность типов, а не именная.
# Лекция 22
 
## Set и Map

#### Внутреннее представление

`set<T>` и `map<K, V>` являются БДП O(log n).<br/>
unordered_set<T>, `unordered_map<K, V>` — O(1), хэш таблица.

Операции (таблица нужна со ссылками на доки):

```cpp
#include <set>
using namespace std;

set<int> s;
s.insert(1);  // Вставка элемента
s.erase(1);   // Удаление
s.find(1);    // Поиск элемента, возвращает s.end(), если не найден.
```

#### Об insert
auto a = s.insert(1);

`pair<it, bool>`

```cpp
if (a.second)  // проверяем, вставлено или нет
    cout << *(a.first);
```

#### О find

```cpp
auto it = s.find(1);  // auto ~ set<int>::iterator
if (it == s.end());
    cout << "Не нашли!";
else {
    cout << *it;
    *it = 5; // Запрещено!!1
}
```


### Итерация по set

```cpp
for (auto x = begin(s); x != end(s); ++x)
    cout << *x << ", ";
```

Какова стоимость обхождения БДП? 
begin(s) ~ n log n

Так как каждый узел обходится один раз. По каждому ребру мы движемся либо в прямом порядке, либо в обратном (когда возвращаемся). Поэтому проход по дереву будет ~ 2n, т.е. O(n).


### Требования от множества

```cpp
class Person
{
    string name;
    int age;
    ...
};

set<Person> s;
```

Так как множество упорядочено, то нужно в `Person` определить операцию <. 

```cpp
    friend
    bool operator<(const Person & p1, const Person & p2) {
        return p1.name < p2.name;
    }
```

Можно также написать компаратор, который будет уметь сравнивать объекты типа Person:

```cpp
class PersonComp
{
    bool operator() (const Person & p1, const Person & p2)
    {
        return p1.name < p2.name;
    }
}

set<Person, PersonComp> s1;
```

#### Равенство и эквивалентность

> Вопрос: куда делась операция `==` ?

Заменим `==(x, y)`  ->  `Equiv(x, y)`  ~  `!(x < y) & (y < x)`.

То есть операции `<` достаточно.



### Ассоциативный словарь

```cpp
#include<map>

map<string, int> m;
m["бегемот"] = 3;
m["крокодил"] = m["какаду"] - 1;
```

В .NET если в множестве не было пары ("какаду", x), то возникает исключение.
Но в C++ вернёт 0. Соответственно необходимо для типа написать конструктор по умолчанию.

#### Цикл по карте

```cpp
for (auto x = begin(m); x != end(m); ++x) {
    cout << *x;  // x типа pair<string, int>
    (*x).second = 5;  // можно
}


auto it = m.find("крокодил");
if (it == m.end())
    cout << "Крокодилов нет";
else
    (*it).second += 2;  // завезли два крокодила
```

m.erase(it);  // дерево будет перестраиваться

map<Person, int, PersonLessName>



```cpp
Graph g;

g["Ростов"]["Батайск"] = 10;
g["Ростов"]["Москва"] = 1100;

typedef map<string, maostring, int>> Graph;
```

Ростов -> Москва (1100)
Ростов -> Батайск (10)


//### какая-то фигня

unordered_set<int> s;

как добавится так и будет выводится, хэш таблица
операции выполняются быстро

Как хранить там студентов?
unordered_set<Person, Hasher> s;

```cpp
struct Hasher 
{
    size_t operator() (const Person & p)
    {
        return hash<string>()(p.name) ^ hash<int>()(p.age);
    }
}
```

Хэш функция вычисляется быстро, для одинаковых персон возваращает одно и то же значения. Но для разных можно одно и тоже, но лучше редко. (Скопировать с вики).

`hash<string>()(p.name)` — обощенный класс hash с типом string, для которого вызывается конструктор и вызывается оператор `()`.

Можно указать свою специализацию класса hash и радоваться, но мы не будем этого делать.
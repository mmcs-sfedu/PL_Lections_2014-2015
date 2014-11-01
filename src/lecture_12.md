# Лекция 12


## Конструктор копий

Рассмотрим, для начала, следующую реализацию класса `myvector`:

```cpp
class myvector {
    int size;
    int * data;
    string name;
  
public:
    myvector(string const & name = "id1")
        : size(10), name(name)
    {
        data = new int [size];
        cout << name << " created\n";
    }
  
    ~myvector()
    {
        delete []data;
        cout << name << " killed\n";
    }  
};
```

Проверим работу нашего класса, выполнив следующий код в функции `main`:

```cpp
    myvector myv1;
    myvector myv2 = myv1;
```

Когда мы пишем `myvector myv2 = myv1;`, мы подразумеваем, что происходит копирование объекта `myv1`, а в конце выполнения функции `main()` удаление двух объектов `myv1` и `myv2`.

В действительности, при запуске программы происходит ошибка:

> id1 created
> id1 killed
> *** Error in `./main': double free or corruption (fasttop): …


Данная проблема возникает из-за того, что команда `myvector myv2 = myv1;` выполняет копирование указателя на объект. В итоге, в конце программы дважды вызывается деструктор одного и того же объекта.

![double_free](../img/ "Возникновение ошибки double free")

Для того чтобы добиться желаемого поведения существует конструктор копий.
Конструктор копирования ― специальный конструктор применяемый для создания нового объекта как копии уже существующего.
Реализуем такой конструктор для класса `myvector`:

```cpp
myvector(myvector const & other): size(other.size), name(other.name)
{
    data = new int[size];
    copy(other.data, other.data + size, data);
    ++name[2];
    
    cout << "copy ctor from " << other.name << " to " << name << endl;
}
```

Теперь выхлоп программы выглядит следующим образом:

>id1 created
>copy ctor from id1 to id2
>id2 killed
>id1 killed

### Три случая когда вызывается конструктор копий

1. `myvector myv2 = myv1`;
2. Вызов функции с передачей параметра по значению `void f(Student st) {/* … */}`
3. Возвращение объекта по значению `Student g() {/* .. */}`

**Пример**


### Return Value Optimization

```cpp
class myvector {
    …
public:
    myvector g() { return myvector(); }  
};


int main()
{
    myvector myv1 = g();
} 
```

Вопрос: сколько будет вызвано конструкторов копий? 
Здесь присутствуют 1 и 3 случаи вызова конструктора копий. То есть создается 2 объекта.

На самом деле запуск данного примера покажет, что во время выполнения программы не будет создано ни одного конструктора копий. Это результат работы оптимизирующего компилятора. Эта оптимизация производится подавляющим большинством современных компиляторов так как она определена в стандарте языка. Эта оптимизация носит название **Return Value Optimization(RVO).**

 
## Функции-члены, которые генерируются "молча"

Рассмотрим класс `Empty`

```cpp
class Empty{
public:
    Empty() {}

    Empty(Empty const &) {/* … */}

    Empty & operator=(Empty const &) {/* … */}

    ~Empty() {/* … */}
};
```

Видим, что здесь присутствуют 4 функции:

* `Empty()` ― конструктор по-умолчанию
* `Empty(Empty const &)` ― конструктор копий
* `Empty & operator=(Empty const &)` ― операция копирующего присваивания
* `~Empty()` ― деструктор

Такое описание класса эквивалентно `class Empty {};`. Т.е эти 4 функции генерируются автоматически.


## Конструктор по-умолчанию

Конструктор по-умолчанию - конструктор без параметров, который генерируется автоматически, только тогда, кода не определено ни одного конструктора в классе.

Это свойство конструктора по-умолчанию может стать причиной не очевидной ошибки.

Для примера рассмотрим класс `Student`:

```cpp
class Student
{
    string name;
public:
    Student(string const & name) : name(name){}
}
```

При попытке объявить экземпляр этого класса, компилятор выдаст ошибку.

```cpp
main()
{
    Student s;
}
```

Это произойдет, из-за того, что после объявления конструктора `Student(string const & name) : name(name){}`, конструктор по-умолчанию не будет сгенерирован.

Аналогичная ошибка возникнет при попытке объявить массив типа `Student`.

```cpp
main()
{
    Student students[10];
}
```


## Операция копирующего присваивания

Реализация функции-члена `operator=` класса `myvector` такова, что при выполнении следующего кода происходит копирование указателя, а не объекта:

```cpp
    myvector myv1;
    myvector myv2;
    myv2 = myv1;
```

Если в этом случае нам необходимо копировать сам объект, тогда выполняется реализация операции копирующего присваивания:

```cpp
myvector & operator=(myvector const & other)
{
    if (this != &other) {    // "Обязательное" клише
        delete [] data;     // Нам потребуется новый размер поля data
        
        size = other.size;
        data = new int[size];
        copy(other.data, other.data + size, data);
        name = other.name;
        ++name[2];
    }
    
    return *this;
}
```

Данная реализация далека от идеала. Например выполнение `delete [] data;` может привести к тому, что при возникновении исключения на этапе копирования данных поле `data` может остаться "сломанным". Для избежания такой ситуации можно завести переменную `newdata`, а операцию удаления `data` перенести в конец функции.

```cpp
myvector & operator=(myvector const & other)
{
    if (this != &other) {
        size = other.size;
        newdata = new int[size];
        copy(other.data, other.data + size, data);
        name = other.name;
        ++name[2];
        
        delete [] data;
        data = newdata;
    }
      
    return *this;
}
```

### Идиома copy-and-swap

Идиома **copy-and-swap** позволяет разрабатывать устойчивые к исключениям операторы присваивания.
**Сopy-and-swap** предполагает реализацию операции копирующего присваивания с использованием конструктора копий и созданием функции-члена `void swap(myvector & other)`, принимающего ссылку на объект. 

```cpp
class myvector {
    …
public:
    myvector & operator=(myvector const & other)
    {
        myvector tmp(other); // Вызов конструктора копий
        this -> swap(tmp);
        
        cout << "copy assigment" << endl;
        return *this;
    }
    
    void swap(myvector & other)
    {
        std::swap(data, other.data);
        std::swap(size, other.size); 
        std::swap(name, other.name); 
    }
};
```

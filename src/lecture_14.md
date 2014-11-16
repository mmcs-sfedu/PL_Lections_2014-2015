# Лекция 14

## Moving-конструкторы и moving-operator= (C++11)

```cpp
/* main.cpp */
myvector<int> v(3), v1(3);
myvector<int> vv(v+v);
```

```cpp
/* myvector.h */
template<typename T>
class myvectror
{
public:
  friend
  myvector<T> operator+(const myvectror<T>& v1, const myvectror<T>& v2) 
  {
    myvector<T> v(v1.sz);
    for(int i=0;i<v1.sz; i++)
      v[i] = v1[i] + v2[i]
    return v;
  }
}
```

В стандарте **C++11** Бьярн Страуструп предложил вынести **RVO** на уровень языка.

`v+v1` - rvalue
мы не можем завписать `v1 + v2 = v`

Ссылка на rvalue `T && t`
 
Деструкторы для временных переменных вызываются в тот момент, когда эти переменные уже не используются для вычислений.

Вопрос в том, как уменьшить накладные расходы на копирование переменных.


```cpp
class myvector
{
  …
public:
  myvector(myvector<T>&& v)
  {
    sz = v.sz;
    data = v.data;
    v.data = nullptr;
  }

  // Переписываем деструктор
  ~myvector()
  {
    if(data != nullptr)
      delete[] data;
  }
}
```

`myvector<int> vv(v+v);`
Что выберет компилятор КК или moving-конструктор?

```cpp
class myvector
{
  …
public:
  myvector<T>& operator=(myvector<T>&& v)
  {
    if(data != nullptr)
      delete[] data;
    sz = v.sz;
    data = v.data;
    v.data = nullptr;
    return *this;
  }
}
```

Ввиду наличия большого количества стандартных классов использовать mooving-конструкторы приходится редко, однако знание такого механизма необходимо.


## Запрет генерации стандартный операторов

Как говорилось [ранее](12.html#member_funcs_generated_silently) существуют функции-члены, которые генерируются "молча", без явного описания. 
На практике, иногда, такие функции могут создать нежелательную функциональность, от которой нужно избавиться.

Для этих целей в C++ предусмотрен механизм запрета генерации стандартных конструкторов и функций. Рассмотрим его на примере класса `A`:

```cpp
class A
{
public:
	A(int i) {…}

	// Данная запись указывает на необходимость сгенерировать
	// конструктор по умолчанию
	A() = default;

	// Запретить генерацию конструктора по умолчанию
	A(const A&) = delete;

	// А так можно запретить генерацию operator=
	A& operator=(const A&) = delete; 
}  
```

## Класс frac дроби

**f = m/n;**  **m**,**n** - `int`

double -> frac

`double d = 1/3.0;`<br>
`frac f(1, 3);`

функция `Gauss`, которая решала бы уравнение **Ax = b** методом Гаусса

Совершенно вектор

```cpp
// T может быть равен double
// T может быть равен frac
template <typename T>
Gauss(const matrix<T> &A, const myvector<T> & b)
{
	
}
```

[img](формула m1/n1+m2/n2)

```cpp
class frac
{
	// n - натуральное
	// m - целое
	int m, n;
public:
	frac(int mm = 2, int nn = 1): m(mm), n(nn)
	{
		// Дроби надо хранить в несократимом виде, поэтому:
		int nd = nod(m, n);
		m /= nd; n /= nd;
	}
	friend frac operator+(const frac f1, const frac f2)
	{
		int nd = nod(f1.n, f2.n);
		return(f2.n/nd*f1.m + f1.n/nd*f2.m, f1.n/nd*f2.n)
	}
	// реализовать operator*
}
```

Посмотрим на те возможности которые можно реализовать с помощю frac

Мы хотим писать так: `frac f = 1;` `f = 2; ~ f = frac(2);`

## Конструктор преобразования

Любой конструктор, который может быть вызван с одним параметром является конструктором преобразования. и служит для неявного преобразования параметра к типу объекта данного класса.

`f = f1 + 3;` ~ `f = f1 + frac(3);`
`f = 2 * f2;` ~ `f = frac(2) * f2; ~ f = frac(2,1) * f2;`


Иногда умножить целое число на дробь эффективнее, чем умножать дробь на дробь.

Поэтому перегрузим `operator*`:

```cpp
friend operator*(int n, const frac &f)
{
	return n*f
}
```

### Подвох в конструктора с одним параметром (преобразования)

```cpp
myvector<int> v(10), v1(10); // 10 нулей
v1 = v + 1; ~ v1 = v + myvector<int>(10);
```

Здесь необходимо запретить преобразовывать **10** к `myvector<int>(10)`.


## Явные конструкторы преобразования

```cpp
class myvector
{
public:
	explicit myvector(int n)
	{
	}
}
```
## Операции приведения типа

`frac(2, 3);`
`double d = f;` // Этот код не сработает
Необходимо `f` ~ `double(f);`
На деле `f` ~ `double d = operator double();` // Оператор приведения типа


```cpp
class frac
{
public:
	operator double()
	{
		return m/(double)n;
	}
};
```

`double d = f;` ~ `double d = f.m/(double)f.n;`
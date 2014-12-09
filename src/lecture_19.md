# Лекция 19


```cpp
vector<int> v {3, 5, 2};
list<int> l {2, 7, 8, 9}; 
int a[10];
auto pa = copy(v.begin(), v.end(), a);
```
[img](a array)

```cpp
pa = copy(l.begin(), l.end(), pa);
```

Что будет, если в том контейнере куда мы копируем будет недостаточно места? Будет перезаписана чужая память из-за отсутствия контроля выхода за границу.

Если написать так:

```cpp
pa = copy(l.end(), l.begin(), pa);
```

Тогда `copy` от такой ошибки не застрахован, так же он не застрахован от ошибок в случае такого кода:

```cpp
pa = copy(l.end(), l.begin(), pa);
pa = copy(l.begin(), l1.end(), pa);
```

[b, e)


## Итератор списка

Мы хотим, что `copy` работал и для списка.

Для работы класса `list_iterator` нужен `listnode<T>`

Перегружая операции в `copy` мы изменяем работу `copy`. Сколько типов мы определим, столько будет создано `copy`

```cpp
template<typename T>
class list_iterator
{
	listnode<T> * cur;
public:
	list_iterator(listnode<T>* c):cur(c){}
	T& operator*() {eturn cur->data;}
	listierator<T>& operator++()
	{
		cur = cur->next;
		return *this;
	}
	template<typename S>
	friend bool operator!=(list_iterator<S>i1, list_iterator<S>i2)
	{
		return i1.cur != i2.cur;
	}
};
```

Теперь `copy` будет выглядеть следующим образом

```cpp
template<typename It, typename It1>
OutIt copy(InIt b, InIt e, OutIt b1)
{
	while(b.cur != e.cur)
		*b1 = b.cut->data;
	++b1;
	b.cur = b.cur->next;
	return b1;
}
```





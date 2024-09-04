
---

# Go (Golang) Cheat Sheet

This cheat sheet covers the essential aspects of Go programming, including variable declarations, types, common operations, iteration, string operations, pointers, and functions.

---

## 1. Variable Declaration

### 1.1 Declare a Variable
```go
var x int = 10      // Explicit type declaration
var y = 20          // Type inferred
z := 30             // Short variable declaration (within a function)
```

### 1.2 Multiple Variable Declaration
```go
var a, b, c int = 1, 2, 3
d, e, f := 4, 5, "hello"
```

### 1.3 Constants
```go
const pi = 3.14
const greeting = "Hello, World!"
```

---

## 2. Variable Types

### 2.1 Basic Types
- **Integer**: `int`, `int8`, `int16`, `int32`, `int64`
- **Unsigned Integer**: `uint`, `uint8`, `uint16`, `uint32`, `uint64`
- **Floating Point**: `float32`, `float64`
- **Complex**: `complex64`, `complex128`
- **Boolean**: `bool`
- **String**: `string`
- **Rune**: `rune` (alias for `int32`)
- **Byte**: `byte` (alias for `uint8`)

### 2.2 Composite Types
- **Array**: `[n]Type` (fixed size)
- **Slice**: `[]Type` (dynamic size)
- **Map**: `map[KeyType]ValueType`
- **Struct**: `type StructName struct {...}`
- **Pointer**: `*Type`
- **Function**: `func(Type1, Type2) ReturnType`

### 2.3 Type Conversion
```go
i := 42
f := float64(i)           // Convert int to float64
s := strconv.Itoa(i)      // Convert int to string
```

---

## 3. Common Operations

### 3.1 Length of a Variable
- **String**: `len(str)`
- **Array/Slice**: `len(arr)`
- **Map**: `len(mapVar)`

### 3.2 Searching

#### String
```go
strings.Contains(str, "substring")  // Check if substring exists
strings.Index(str, "substring")     // Get index of substring (-1 if not found)
```

#### Array/Slice
```go
for i, v := range arr {
    if v == target {
        // Found at index i
    }
}
```

#### Map
```go
value, exists := mapVar[key]
if exists {
    // Key exists in the map
}
```

### 3.3 Comparing Variables
- **Numbers**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Strings**: `==`, `!=`
- **Arrays/Slices**: `reflect.DeepEqual(arr1, arr2)`  // Returns true if they are equal
- **Maps**: `reflect.DeepEqual(map1, map2)`  // Returns true if they are equal

### 3.4 Adding/Concatenating

#### Numbers
```go
sum := a + b   // Add numbers
```

#### Strings
```go
str1 := "Hello, "
str2 := "World!"
result := str1 + str2  // Concatenate strings
```

#### Arrays/Slices
```go
arr := []int{1, 2, 3}
arr = append(arr, 4, 5, 6)  // Add elements to slice
```

### 3.5 Modifying Variables

#### Strings (Immutable)
```go
str := "Hello"
modifiedStr := str + ", World!"  // Concatenate to modify
```

#### Arrays/Slices
```go
arr := []int{1, 2, 3}
arr[1] = 20  // Modify element at index 1
```

#### Maps
```go
mapVar["key"] = "newValue"  // Update value for a key
```

### 3.6 Removing Elements

#### Slice (Removing an element at a specific index)
```go
arr := []int{1, 2, 3, 4}
arr = append(arr[:2], arr[3:]...)  // Remove element at index 2
```

#### Map
```go
delete(mapVar, "key")  // Remove key-value pair
```

### 3.7 Iteration

#### Array/Slice
```go
for i, v := range arr {
    fmt.Println(i, v)  // index, value
}
```

#### Map
```go
for key, value := range mapVar {
    fmt.Println(key, value)
}
```

---

## 4. Common String Operations

```go
strings.ToUpper(str)                    // Convert to uppercase
strings.ToLower(str)                    // Convert to lowercase
strings.TrimSpace(str)                  // Remove leading and trailing whitespace
strings.Replace(str, "old", "new", n)   // Replace 'old' with 'new' n times (-1 for all)
strings.Split(str, "sep")               // Split string by separator
```

---

## 5. Pointer Operations

### 5.1 Declare and Initialize
```go
var p *int
var x = 10
p = &x  // p now holds the address of x
```

### 5.2 Dereference
```go
fmt.Println(*p)  // Access the value at the address stored in p
```

---

## 6. Functions

### 6.1 Function Declaration
```go
func add(a int, b int) int {
    return a + b
}
```

### 6.2 Multiple Return Values
```go
func swap(x, y string) (string, string) {
    return y, x
}
```

### 6.3 Named Return Values
```go
func split(sum int) (x, y int) {
    x = sum * 4 / 9
    y = sum - x
    return
}
```

---

## 7. Iteration in Go

### 7.1 Simple `for` Loop
```go
for i := 0; i < 10; i++ {
    fmt.Println(i)
}
```

### 7.2 `for` as a While Loop
```go
i := 0
for i < 10 {
    fmt.Println(i)
    i++
}
```

### 7.3 Infinite Loop
```go
for {
    fmt.Println("Infinite Loop")
    break  // Break the loop to avoid an infinite loop
}
```

### 7.4 `for range` Loop

#### Iterating Over a Slice or Array
```go
nums := []int{2, 4, 6, 8, 10}
for i, num := range nums {
    fmt.Printf("Index: %d, Value: %d\n", i, num)
}

for _, num := range nums {
    fmt.Println(num)
}
```

#### Iterating Over a Map
```go
m := map[string]int{"a": 1, "b": 2, "c": 3}
for key, value := range m {
    fmt.Printf("Key: %s, Value: %d\n", key, value)
}
```

#### Iterating Over a String
```go
str := "hello"
for i, ch := range str {
    fmt.Printf("Index: %d, Character: %c\n", i, ch)
}
```

#### Iterating Over a Channel
```go
ch := make(chan int, 5)
ch <- 1
ch <- 2
ch <- 3
close(ch)

for v := range ch {
    fmt.Println(v)
}
```

### 7.5 `for` with Condition and Break
```go
for i := 0; i < 10; i++ {
    if i == 5 {
        break  // Exit the loop when i is 5
    }
    fmt.Println(i)
}
```

### 7.6 `for` with Continue
```go
for i := 0; i < 10; i++ {
    if i%2 == 0 {
        continue  // Skip even numbers
    }
    fmt.Println(i)
}
```

### 7.7 Nested `for` Loops
```go
for i := 0; i < 3; i++ {
    for j := 0; j < 3; j++ {
        fmt.Printf("i: %d, j: %d\n", i, j)
    }
}
```

---

This cheat sheet provides a comprehensive guide to fundamental Go concepts and operations, organized for quick reference and easy understanding.

---

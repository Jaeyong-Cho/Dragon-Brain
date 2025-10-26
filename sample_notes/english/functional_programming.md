# Functional Programming

Functional programming treats computation as the evaluation of mathematical functions, avoiding mutable state.

## Core Principles

### Pure Functions

Functions without **side effects**:

```javascript
// Pure function
function add(a, b) {
    return a + b;
}

// Impure function (modifies external state)
let total = 0;
function addToTotal(x) {
    total += x;  // Side effect
    return total;
}
```

**Benefits:**
- Predictable behavior
- Easier to test
- Cacheable (memoization)
- Parallelizable

### Immutability

Data cannot be changed after creation:

```python
# Immutable approach
numbers = (1, 2, 3)
new_numbers = numbers + (4,)  # Create new tuple

# Mutable approach (avoid in FP)
numbers = [1, 2, 3]
numbers.append(4)  # Modifies original
```

### First-Class Functions

Functions as values:

- Pass as arguments
- Return from functions
- **Assign to variables**
- Store in data structures

## Key Concepts

### Higher-Order Functions

Functions that take or return functions:

#### Map

Transform each element:

```haskell
map (*2) [1, 2, 3, 4]
-- Result: [2, 4, 6, 8]
```

#### Filter

Select elements meeting criteria:

```python
numbers = [1, 2, 3, 4, 5, 6]
evens = filter(lambda x: x % 2 == 0, numbers)
# Result: [2, 4, 6]
```

#### Reduce/Fold

Combine elements into single value:

```javascript
const sum = [1, 2, 3, 4].reduce((acc, x) => acc + x, 0);
// Result: 10
```

### Function Composition

Combine functions to create new ones:

```haskell
f :: Int -> Int
f x = x + 1

g :: Int -> Int
g x = x * 2

h = g . f  -- Composition: h(x) = g(f(x))
h 5  -- Result: 12
```

### Currying

Transform multi-argument function into sequence of single-argument functions:

```javascript
// Regular function
function add(x, y) {
    return x + y;
}

// Curried function
const curriedAdd = x => y => x + y;

const add5 = curriedAdd(5);
add5(3);  // Result: 8
```

### Partial Application

Fix some arguments, create specialized function:

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
square(5)  # Result: 25
```

## Recursion

Functions calling themselves:

### Tail Recursion

Recursive call is the **last operation**:

```scheme
; Tail-recursive factorial
(define (factorial n)
  (define (fact-iter n acc)
    (if (= n 0)
        acc
        (fact-iter (- n 1) (* acc n))))
  (fact-iter n 1))
```

**Benefits:**
- Can be optimized to iteration
- Constant stack space

## Pattern Matching

Destructure data based on shape:

```elixir
defmodule Math do
  def factorial(0), do: 1
  def factorial(n) when n > 0 do
    n * factorial(n - 1)
  end
end
```

## Algebraic Data Types

### Sum Types (Tagged Unions)

Value is one of several types:

```haskell
data Shape = Circle Float
           | Rectangle Float Float
           | Triangle Float Float Float

area :: Shape -> Float
area (Circle r) = pi * r * r
area (Rectangle w h) = w * h
area (Triangle a b c) = 
    let s = (a + b + c) / 2
    in sqrt (s * (s-a) * (s-b) * (s-c))
```

### Product Types (Records/Structs)

Combination of multiple values:

```typescript
type Person = {
    name: string;
    age: number;
    email: string;
};
```

## Monads

Container type with **composition rules**:

### Maybe/Option Monad

Handle nullable values:

```haskell
safeDivide :: Float -> Float -> Maybe Float
safeDivide _ 0 = Nothing
safeDivide x y = Just (x / y)

result = do
    x <- safeDivide 10 2  -- Just 5
    y <- safeDivide x 0   -- Nothing
    return (y + 1)        -- Nothing propagates
```

### List Monad

Non-deterministic computation:

```haskell
pairs = do
    x <- [1, 2, 3]
    y <- [4, 5]
    return (x, y)
-- Result: [(1,4), (1,5), (2,4), (2,5), (3,4), (3,5)]
```

## Lazy Evaluation

Compute values only when needed:

```haskell
-- Infinite list
naturals = [1..]

-- Only computes first 10
take 10 naturals
-- Result: [1,2,3,4,5,6,7,8,9,10]
```

**Benefits:**
- Define infinite data structures
- Avoid unnecessary computation
- **Better performance**

## Functional Languages

### Haskell

Pure functional language:

- **Lazy by default**
- Strong static typing
- Type inference
- Powerful type system

### Scala

Hybrid functional-OO language:

- **JVM-based**
- Pattern matching
- For-comprehensions
- Actor model (Akka)

### Clojure

Lisp dialect on JVM:

- **Dynamic typing**
- Immutable data structures
- Software transactional memory
- Homoiconicity

### Elixir

Functional language on Erlang VM:

- **Concurrency**
- Pattern matching
- Metaprogramming
- Distributed systems

### F#

.NET functional language:

- Type inference
- Pattern matching
- **Computation expressions**
- .NET interop

## Benefits

- **Easier reasoning**: No hidden state
- **Concurrency**: No race conditions
- **Testability**: Pure functions easy to test
- **Modularity**: Small, composable functions
- **Maintainability**: Less complex code

## Challenges

- **Learning curve**: Different paradigm
- **Performance**: Immutability overhead
- **Debugging**: Stack traces in recursion
- **Ecosystem**: Fewer libraries

## Functional Techniques in Imperative Languages

### JavaScript

```javascript
// Array methods
const doubled = arr.map(x => x * 2);
const evens = arr.filter(x => x % 2 === 0);
const sum = arr.reduce((acc, x) => acc + x, 0);

// Immutability with spread
const newState = {...oldState, count: oldState.count + 1};
```

### Python

```python
# List comprehensions
squares = [x**2 for x in range(10)]

# Generator expressions (lazy)
evens = (x for x in range(1000) if x % 2 == 0)

# functools
from functools import reduce
product = reduce(lambda x, y: x * y, [1, 2, 3, 4])
```

## Applications

- **Data processing**: ETL pipelines
- **Concurrent systems**: Erlang/Elixir
- **Finance**: Risk modeling (Haskell)
- **Web development**: React (functional concepts)
- **Scientific computing**: Mathematical abstractions

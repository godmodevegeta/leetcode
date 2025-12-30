def fib(n, memo = {}):
    if n in memo: return memo[n]
    if n <= 2: return 1
    a = fib(n - 1, memo)
    b = fib(n - 2, memo)
    memo[n] = a + b
    return memo[n]

print(fib(79))
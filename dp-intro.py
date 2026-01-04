def fib(n, memo = {}):
    if n in memo: return memo[n]
    if n <= 2: return 1
    a = fib(n - 1, memo)
    b = fib(n - 2, memo)
    memo[n] = a + b
    return memo[n]

def gridTraveller(m, n, memo = {}):
    key = str(m) + "," + str(n)
    # check memo
    if key in memo: return memo[key]
    if m == 0 or n == 0:
        return 0
    if m == 1 and n == 1:
        return 1
    # go down
    ways_down = gridTraveller(m - 1, n)
    # go right
    ways_right = gridTraveller(m, n - 1)
    memo[key] = ways_down + ways_right
    return memo[key]
    
def howSum(target, numbers, memo = {}):
    key = target
    if key in memo: return memo[key]
    if target == 0: return []
    if target < 0: return None
    for n in numbers:
        remainder = target - n
        li = howSum(remainder, numbers)
        if li is not None:
            memo[key] = li + [n]
            return memo[key]
    memo[key] = None
    return None

def bestSum(target, numbers) :
    if target == 0: return []
    if target < 0: return None

    resultCombination = None
    for num in numbers:
        remainder = target - num
        combination = bestSum(remainder, numbers)
        remainderCombination = 1
        if (resultCombination == None) or len(remainderCombination) < len(resultCombination):
            resultCombination = remainderCombination
    return resultCombination

def canConstruct(target, wordBank, memo = {}):
    if target in memo: return memo[target]
    if target == "": return True
    
    memo[target] = False
    for word in wordBank:
        wordLength = len(word)
        if word == target[:wordLength]:
            remainderTarget = target[wordLength:]
            if canConstruct(remainderTarget, wordBank):
                memo[target] = True
                return memo[target]
    return memo[target]
    


if __name__ == "__main__":
    print(canConstruct("abcdef", ["ab", "abc", "cd", "def", "abcd"]))
    print(canConstruct("skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"]))
    print(canConstruct("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeef", [
        "e",
        "ee", 
        "eee", 
        "eeee", 
        "eeeeeee"]))
    
    pass


class stack:
    def __init__(self):  # 스택 객체 생성
        self.items = []

    def push(self, item):  # 스택 요소 추가 push(.append())
        self.items.append(item)

    def pop(self):  # 스택 요소 삭제 pop()
        return self.items.pop()

    def peek(self):  # 스택 맨 앞 요소 리턴
        return self.items[0]

    def isEmpty(self):  # 스택이 비었는지 확인(비었으면 True 리턴)
        return not self.items


stk = stack()
print(stk)
print(stk.isEmpty())
stk.push(1)
stk.push(2)
stk.push(6)
stk.push(9)
stk.push(10)
stk.push(0.9)
stk.push(6.5)
stk.pop()

print(stk.items)
print(stk.isEmpty())
print(stk.peek())



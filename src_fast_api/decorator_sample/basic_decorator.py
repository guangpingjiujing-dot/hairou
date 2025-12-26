"""
基本的なデコレーターのサンプル
"""

# ========== 1. 最もシンプルなデコレーター ==========

def simple_decorator(func):
    """関数をラップするだけのシンプルなデコレーター"""
    def wrapper():
        print("関数を実行する前に何か処理を追加")
        result = func()
        print("関数を実行した後に何か処理を追加")
        return result
    return wrapper


@simple_decorator
def greet():
    print("こんにちは！")


# ========== 2. 引数を受け取る関数をデコレートする ==========
#
# *args と **kwargs について:
# - *args: 位置引数をタプルとして受け取る（アスタリスク1つ）
#   例: func(1, 2, 3) → args = (1, 2, 3)
# - **kwargs: キーワード引数を辞書として受け取る（アスタリスク2つ）
#   例: func(a=1, b=2) → kwargs = {'a': 1, 'b': 2}
# 
# これらを使うことで、どんな引数を受け取る関数でもデコレートできます

def log_decorator(func):
    """関数の実行をログに記録するデコレーター"""
    def wrapper(*args, **kwargs):
        # *args: 位置引数がタプルとして渡される
        # **kwargs: キーワード引数が辞書として渡される
        print(f"関数 {func.__name__} を実行します")
        print(f"引数: args={args}, kwargs={kwargs}")
        # 元の関数に引数をそのまま渡す（*args, **kwargs で展開）
        result = func(*args, **kwargs)
        print(f"関数 {func.__name__} の実行が完了しました")
        return result
    return wrapper


@log_decorator
def add(a, b):
    return a + b


@log_decorator
def greet_person(name, age=20):
    return f"{name}さん、{age}歳ですね！"


# ========== 3. 引数を受け取るデコレーター ==========
#
# なぜ repeat と decorator を分ける必要があるのか？
# 
# @repeat(times=3) という構文を使うためには：
# 1. repeat(times) が呼ばれる → デコレーター関数を返す
# 2. その返されたデコレーター関数が @ の後ろに来る
# 3. デコレーター関数が func を受け取って wrapper を返す
#
# もし1つの関数にまとめると、@ 記号を使ったデコレーター構文が使えません。
# 例: @repeat(times=3) は「repeat(times=3)の結果をデコレーターとして使う」という意味です。

def repeat(times):
    """関数を指定回数繰り返し実行するデコレーター"""
    # repeat(times) が呼ばれると、この decorator 関数が返される
    def decorator(func):
        # decorator(func) が呼ばれると、この wrapper 関数が返される
        def wrapper(*args, **kwargs):
            results = []
            for i in range(times):
                print(f"{i+1}回目の実行")
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator


@repeat(times=3)
def say_hello():
    print("Hello!")
    return "Hello!"


# ========== 実行例 ==========

if __name__ == "__main__":
    print("=" * 50)
    print("1. シンプルなデコレーター")
    print("=" * 50)
    greet()
    
    print("\n" + "=" * 50)
    print("2. 引数を受け取る関数をデコレート")
    print("=" * 50)
    result = add(3, 5)
    print(f"結果: {result}\n")
    
    result = greet_person("太郎", age=25)
    print(f"結果: {result}\n")
    
    print("=" * 50)
    print("3. 引数を受け取るデコレーター")
    print("=" * 50)
    results = say_hello()
    print(f"結果: {results}\n")

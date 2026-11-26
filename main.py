from pyscript import document
from book_bst import PriceBST

# 初始化 BST 並放入幾本預設教科書（方便網頁一打開就有資料）
bst = PriceBST()
bst.insert(350, "工程數學(上)", "必修", "王同學")
bst.insert(200, "C語言程式設計", "必修", "林同學")
bst.insert(500, "資料結構與演算法", "必修", "陳同學")
bst.insert(150, "數位邏輯設計", "必修", "張同學")
bst.insert(350, "電路學", "必修", "李同學")  # 測試同價格節點

def render_books(book_list):
    tbody = document.querySelector("#book-list")
    tbody.innerHTML = ""
    if not book_list:
        tbody.innerHTML = "<tr><td colspan='4'>找不到符合此價格區間的書籍</td></tr>"
        return
    for b in book_list:
        row = f"""
        <tr>
            <td>${b['price']}</td>
            <td>{b['title']}</td>
            <td>{b['subject']}</td>
            <td>{b['seller']}</td>
        </tr>
        """
        tbody.innerHTML += row

def update_tree_view():
    tree_box = document.querySelector("#bst-visual")
    tree_box.innerText = bst.get_tree_structure()

def add_book(event):
    title = document.querySelector("#title").value
    price = document.querySelector("#price").value
    subject = document.querySelector("#subject").value
    seller = document.querySelector("#seller").value

    if title and price:
        bst.insert(int(price), title, subject or "一般", seller or "匿名")
        # 清空輸入框並重新渲染
        document.querySelector("#title").value = ""
        document.querySelector("#price").value = ""
        render_books(bst.get_sorted_books())
        update_tree_view()

def filter_books(event):
    min_p = document.querySelector("#min-price").value or 0
    max_p = document.querySelector("#max-price").value or 99999
    filtered = bst.search_range(min_p, max_p)
    render_books(filtered)

def reset_filter(event):
    document.querySelector("#min-price").value = ""
    document.querySelector("#max-price").value = ""
    render_books(bst.get_sorted_books())

# 網頁載入時先執行一次初始化畫面
render_books(bst.get_sorted_books())
update_tree_view()
# 完全無任何 import，100% 純手刻 Python 價格 BST

class BookNode:
    def __init__(self, price, title, subject, seller):
        self.price = price
        # 相同價格的書籍存在同一個節點的串列中
        self.books = [{"title": title, "subject": subject, "seller": seller}]
        self.left = None
        self.right = None


class PriceBST:
    def __init__(self):
        self.root = None

    # 1. 插入書籍節點
    def insert(self, price, title, subject, seller):
        if self.root is None:
            self.root = BookNode(price, title, subject, seller)
        else:
            self._insert_recursive(self.root, price, title, subject, seller)

    def _insert_recursive(self, current, price, title, subject, seller):
        if price < current.price:
            if current.left is None:
                current.left = BookNode(price, title, subject, seller)
            else:
                self._insert_recursive(current.left, price, title, subject, seller)
        elif price > current.price:
            if current.right is None:
                current.right = BookNode(price, title, subject, seller)
            else:
                self._insert_recursive(current.right, price, title, subject, seller)
        else:
            # 價格相同，加入該價格節點的清單
            current.books.append({"title": title, "subject": subject, "seller": seller})

    # 2. 中序走訪（價格由低到高排序）
    def inorder_sort(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node is not None:
            self._inorder_recursive(node.left, result)
            for book in node.books:
                result.append({
                    "price": node.price,
                    "title": book["title"],
                    "subject": book["subject"],
                    "seller": book["seller"]
                })
            self._inorder_recursive(node.right, result)

    # 3. 價格區間搜尋（利用 BST 大小特性剪枝）
    def search_range(self, min_price, max_price):
        result = []
        self._search_range_recursive(self.root, min_price, max_price, result)
        return result

    def _search_range_recursive(self, node, min_p, max_p, result):
        if node is None:
            return
        if node.price > min_p:
            self._search_range_recursive(node.left, min_p, max_p, result)
        if min_p <= node.price <= max_p:
            for book in node.books:
                result.append({
                    "price": node.price,
                    "title": book["title"],
                    "subject": book["subject"],
                    "seller": book["seller"]
                })
        if node.price < max_p:
            self._search_range_recursive(node.right, min_p, max_p, result)

    # 4. 刪除書籍（售出下架）
    def delete_book(self, price, title):
        self.root = self._delete_recursive(self.root, price, title)

    def _delete_recursive(self, node, price, title):
        if node is None:
            return None

        if price < node.price:
            node.left = self._delete_recursive(node.left, price, title)
        elif price > node.price:
            node.right = self._delete_recursive(node.right, price, title)
        else:
            # 找到對應價格節點，先移除指定書名
            new_books = []
            for b in node.books:
                if b["title"] != title:
                    new_books.append(b)
            node.books = new_books

            # 若該價格還有其他書，保留節點不刪除
            if len(node.books) > 0:
                return node

            # 若該價格已無任何書，執行標準 BST 節點刪除
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # 左右子樹皆存在：找右子樹最小值（中序後繼者）替補
            min_larger_node = self._get_min_node(node.right)
            node.price = min_larger_node.price
            node.books = min_larger_node.books
            node.right = self._delete_node_by_price(node.right, min_larger_node.price)

        return node

    def _get_min_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _delete_node_by_price(self, node, price):
        if node is None:
            return None
        if price < node.price:
            node.left = self._delete_node_by_price(node.left, price)
        elif price > node.price:
            node.right = self._delete_node_by_price(node.right, price)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
        return node

    # 5. 印出樹狀結構
    def print_tree(self):
        self._print_recursive(self.root, "", True)

    def _print_recursive(self, node, prefix, is_tail):
        if node is None:
            return
        if node.right is not None:
            self._print_recursive(node.right, prefix + ("│   " if is_tail else "    "), False)
        titles = ", ".join([b["title"] for b in node.books])
        print(prefix + ("└── " if is_tail else "┌── ") + f"${node.price} ({titles})")
        if node.left is not None:
            self._print_recursive(node.left, prefix + ("    " if is_tail else "│   "), True)


# ================= 終端機測試區 =================
if __name__ == "__main__":
    bst = PriceBST()
    bst.insert(350, "工程數學(上)", "必修", "王同學")
    bst.insert(200, "C語言程式設計", "必修", "林同學")
    bst.insert(500, "資料結構與演算法", "必修", "陳同學")
    bst.insert(150, "數位邏輯設計", "必修", "張同學")
    bst.insert(350, "電路學", "必修", "李同學")

    print("=== 1. 目前價格 BST 樹狀結構 ===")
    bst.print_tree()

    print("\n=== 2. 價格由低到高排序（中序走訪） ===")
    for item in bst.inorder_sort():
        print(f"${item['price']} - {item['title']} ({item['subject']}) / 賣家: {item['seller']}")

    print("\n=== 3. 預算 $200 ~ $400 區間搜尋 ===")
    for item in bst.search_range(200, 400):
        print(f"${item['price']} - {item['title']}")
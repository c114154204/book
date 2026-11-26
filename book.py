class BookNode
    def __init__(self, price, title, subject, seller)
        self.price = price
        # 同一價格可能有多本不同的書，用 list 存起來避免被覆蓋
        self.books = [{title title, subject subject, seller seller}]
        self.left = None
        self.right = None

class PriceBST
    def __init__(self)
        self.root = None

    # 1. 新增書籍（依價格建立 BST）
    def insert(self, price, title, subject, seller)
        price = int(price)
        if self.root is None
            self.root = BookNode(price, title, subject, seller)
        else
            self._insert_recursive(self.root, price, title, subject, seller)

    def _insert_recursive(self, current, price, title, subject, seller)
        if price  current.price
            if current.left is None
                current.left = BookNode(price, title, subject, seller)
            else
                self._insert_recursive(current.left, price, title, subject, seller)
        elif price  current.price
            if current.right is None
                current.right = BookNode(price, title, subject, seller)
            else
                self._insert_recursive(current.right, price, title, subject, seller)
        else
            # 價格相同，直接加入該節點的書籍清單
            current.books.append({title title, subject subject, seller seller})

    # 2. 中序走訪（In-order Traversal）：輸出價格由低到高的所有書籍
    def get_sorted_books(self)
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result)
        if node
            self._inorder(node.left, result)
            for book in node.books
                result.append({
                    price node.price,
                    title book[title],
                    subject book[subject],
                    seller book[seller]
                })
            self._inorder(node.right, result)

    # 3. 價格區間搜尋（利用 BST 特性剪枝，加速篩選預算內的書）
    def search_range(self, min_price, max_price)
        result = []
        self._search_range_recursive(self.root, int(min_price), int(max_price), result)
        return result

    def _search_range_recursive(self, node, min_p, max_p, result)
        if not node
            return
        # 只有當前價格大於最小值時，左子樹才可能有符合條件的書
        if node.price  min_p
            self._search_range_recursive(node.left, min_p, max_p, result)
        # 落在區間內，加入結果
        if min_p = node.price = max_p
            for book in node.books
                result.append({
                    price node.price,
                    title book[title],
                    subject book[subject],
                    seller book[seller]
                })
        # 只有當前價格小於最大值時，右子樹才可能有符合條件的書
        if node.price  max_p
            self._search_range_recursive(node.right, min_p, max_p, result)

    # 4. 視覺化輸出樹狀結構（方便 Demo 展示給老師或組員看）
    def get_tree_structure(self)
        lines = []
        self._build_tree_text(self.root, , True, lines)
        return n.join(lines) if lines else 目前樹為空

    def _build_tree_text(self, node, prefix, is_tail, lines)
        if not node
            return
        if node.right
            self._build_tree_text(node.right, prefix + (│    if is_tail else     ), False, lines)
        titles = , .join([b[title] for b in node.books])
        lines.append(f{prefix}{'└── ' if is_tail else '┌── '}${node.price} ({titles}))
        if node.left
            self._build_tree_text(node.left, prefix + (     if is_tail else │   ), True, lines)
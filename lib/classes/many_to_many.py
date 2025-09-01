class Article:
    all = []  # Class attribute to store all articles
    
    def __init__(self, author, magazine, title):
        if not isinstance(author, Author):
            raise Exception("Article author must be an Author instance")
        if not isinstance(magazine, Magazine):
            raise Exception("Article magazine must be a Magazine instance")
        if not isinstance(title, str):
            raise Exception("Article title must be a string")
        title = title.strip()
        if not (5 <= len(title) <= 50):
            raise Exception("Title must be between 5 and 50 characters")

        self._author = author
        self._magazine = magazine
        self._title = title

        # maintain relationships
        author._articles.append(self)
        magazine._articles.append(self)
        Article.all.append(self)

    @property
    def title(self):
        return self._title
    # No setter - title is immutable

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise Exception("Author must be an Author instance")
        # Remove from old author's articles list
        if self in self._author._articles:
            self._author._articles.remove(self)
        self._author = value
        # Add to new author's articles list
        if self not in value._articles:
            value._articles.append(self)

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise Exception("Magazine must be a Magazine instance")
        # Remove from old magazine's articles list
        if self in self._magazine._articles:
            self._magazine._articles.remove(self)
        self._magazine = value
        # Add to new magazine's articles list
        if self not in value._articles:
            value._articles.append(self)


class Author:
    def __init__(self, name):
        if not isinstance(name, str):
            raise Exception("Author name must be a string")
        name = name.strip()
        if len(name) == 0:
            raise Exception("Author name must be longer than 0 characters")
        self._name = name
        self._articles = []

    @property
    def name(self):
        return self._name
    # No setter - name is immutable

    def articles(self):
        return self._articles

    def magazines(self):
        return list({article.magazine for article in self._articles})

    def add_article(self, magazine, title):
        if not isinstance(magazine, Magazine):
            raise Exception("Magazine must be a Magazine instance")
        return Article(self, magazine, title)

    def topic_areas(self):
        if not self._articles:
            return None
        return list({mag.category for mag in self.magazines()})


class Magazine:
    all = []

    def __init__(self, name, category):
        self._articles = []
        
        # Validate name
        if not isinstance(name, str):
            raise Exception("Magazine name must be a string")
        name = name.strip()
        if not (2 <= len(name) <= 16):
            raise Exception("Magazine name must be between 2 and 16 characters")
        self._name = name
        
        # Validate category
        if not isinstance(category, str):
            raise Exception("Category must be a string")
        category = category.strip()
        if len(category) == 0:
            raise Exception("Category must be longer than 0 characters")
        self._category = category
        
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise Exception("Magazine name must be a string")
        stripped_value = value.strip()
        if not (2 <= len(stripped_value) <= 16):
            raise Exception("Magazine name must be between 2 and 16 characters")
        self._name = stripped_value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise Exception("Category must be a string")
        stripped_value = value.strip()
        if len(stripped_value) == 0:
            raise Exception("Category must be longer than 0 characters")
        self._category = stripped_value

    def articles(self):
        return self._articles

    def contributors(self):
        return list({article.author for article in self._articles})

    def article_titles(self):
        if not self._articles:
            return None
        return [article.title for article in self._articles]

    def contributing_authors(self):
        from collections import Counter
        author_counts = Counter(article.author for article in self._articles)
        result = [author for author, count in author_counts.items() if count > 2]
        return result if result else None

    @classmethod
    def top_publisher(cls):
        if not any(mag._articles for mag in cls.all):
            return None
        return max(cls.all, key=lambda mag: len(mag._articles))
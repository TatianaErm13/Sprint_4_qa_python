import pytest
from main import BooksCollector

class TestBooksCollector:

    def test_add_new_book_add_two_books(self):
       
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        assert len(collector.get_books_rating()) == 2

class TestBooksCollector:

    @pytest.mark.parametrize("book_name,expected_added", [
        ('Гордость и предубеждение', True),
        ('', False),
        ('a' * 41, False),
    ])
    def test_add_new_book(self, book_name, expected_added):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        if expected_added:
            assert book_name in collector.get_books_genre()
        else:
            assert book_name not in collector.get_books_genre()

    @pytest.mark.parametrize("genre,expected_genre", [
        ('Фантастика', 'Фантастика'),
        ('Неизвестный жанр', ''),
    ])
    def test_set_book_genre(self, genre, expected_genre):
        collector = BooksCollector()
        collector.add_new_book('Фантастическая книга')
        collector.set_book_genre('Фантастическая книга', genre)
        assert collector.get_book_genre('Фантастическая книга') == expected_genre

    def test_get_book_genre_existing_book(self):
        collector = BooksCollector()
        collector.add_new_book('Детектив')
        collector.set_book_genre('Детектив', 'Детективы')
        assert collector.get_book_genre('Детектив') == 'Детективы'

    @pytest.mark.parametrize("target_genre,expected_count", [
        ('Мультфильмы', 2),
        ('Фантастика', 0),
    ])
    def test_get_books_with_specific_genre(self, target_genre, expected_count):
        collector = BooksCollector()
        collector.add_new_book('Мультфильм 1')
        collector.add_new_book('Мультфильм 2')
        collector.set_book_genre('Мультфильм 1', 'Мультфильмы')
        collector.set_book_genre('Мультфильм 2', 'Мультфильмы')

        result = collector.get_books_with_specific_genre(target_genre)
        assert len(result) == expected_count

    def test_get_books_genre_returns_dict(self):
        collector = BooksCollector()
        books_genre = collector.get_books_genre()
        assert isinstance(books_genre, dict)

    def test_get_books_for_children_age_rating_exclusion(self):
        collector = BooksCollector()
        collector.add_new_book('Мультфильм')
        collector.set_book_genre('Мультфильм', 'Мультфильмы')
        collector.add_new_book('Ужас')
        collector.set_book_genre('Ужас', 'Ужасы')

        result = collector.get_books_for_children()
        assert 'Мультфильм' in result
        assert 'Ужас' not in result

    @pytest.mark.parametrize("book_name,should_be_added", [
        ('Любимая книга', True),
        ('Неизвестная книга', False),
    ])
    def test_add_book_in_favorites(self, book_name, should_be_added):
        collector = BooksCollector()
        if should_be_added:
            collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)

        if should_be_added:
            assert book_name in collector.get_list_of_favorites_books()
        else:
            assert book_name not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_success(self):
        collector = BooksCollector()
        collector.add_new_book('Книга для удаления')
        collector.add_book_in_favorites('Книга для удаления')
        collector.delete_book_from_favorites('Книга для удаления')
        assert 'Книга для удаления' not in collector.get_list_of_favorites_books()

    def test_get_list_of_favorites_books_empty_initially(self):
        collector = BooksCollector()
        assert collector.get_list_of_favorites_books() == []

    def test_get_list_of_favorites_books_after_adding(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_book_in_favorites('Книга 1')
        favorites = collector.get_list_of_favorites_books()
        assert 'Книга 1' in favorites
        assert len(favorites) == 1
        
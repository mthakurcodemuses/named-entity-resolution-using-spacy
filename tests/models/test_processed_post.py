from app.models.processed_post import ProcessedPost


def test_addition_of_processed_posts():
    post1 = ProcessedPost('Hello, world!', {'entities': ['world']})
    post2 = ProcessedPost('Hello, GitHub!', {'entities': ['GitHub']})
    result = post1 + post2
    assert result.text == 'Hello, world! Hello, GitHub!'
    assert result.entities == {'entities': ['world', 'GitHub']}
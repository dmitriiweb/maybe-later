from maybe_later import models


def test_article_to_markdown(article: models.Article):
    md = article.to_markdown()
    assert md.startswith("# Test title")

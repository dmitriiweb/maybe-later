from maybe_later import models


def test_article_to_markdown(article: models.Article):
    md = article.to_markdown()
    assert md.startswith("# Test title")


def test_source_url_in_markdown(article: models.Article):
    md = article.to_markdown()
    assert "**Source:** Test source" in md

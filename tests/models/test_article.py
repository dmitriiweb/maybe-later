from maybe_later.savers import models


def test_article_to_markdown(article: models.ArticleModel):
    md = article.to_markdown()
    assert md.startswith("# Test title")


def test_source_url_in_markdown(article: models.ArticleModel):
    md = article.to_markdown()
    assert "**Source:** Test source" in md

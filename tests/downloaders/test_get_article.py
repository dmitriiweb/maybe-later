from maybe_later.downloaders import get_article


async def test_get_article(httpx_mock, article_html: str):
    httpx_mock.add_response(text=article_html)
    article = await get_article(
        "https://example.com", category="python", subcategory="python", tags=["tag"]
    )

    assert article.title == "Технологии использования пространства"
    assert article.text.startswith("Технологии использования")
    assert article.text.endswith("в историю развития технологий.")
    assert article.source == "https://example.com"
    assert article.category == "python"
    assert article.subcategory == "python"
    assert article.tags == ["tag"]

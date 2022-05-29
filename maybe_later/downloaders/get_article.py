from typing import List, Optional

import httpx

from newspaper import Article, Config

from maybe_later.savers import models


async def get_article(
    url: str, category: Optional[str], subcategory: Optional[str], tags: List[str]
) -> models.ArticleModel:
    print(f"Getting article from URL: {url}")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url, headers={"User-Agent": "Maybe-Later: tools for saving articles"}
        )
        conf = Config()
        conf.fetch_images = True
        conf.keep_article_html = True
        article = Article(url, config=conf)
        article.set_html(response.text)
        article.parse()
        meta = models.MetaModel(
            title=article.title,
            source=url,
            category=category,
            subcategory=subcategory,
            tags=tags,
        )
        return models.ArticleModel(
            text=article.text,
            article_html=article.article_html,
            meta=meta,
        )

from typing import List, Optional

import httpx

from newspaper import Article

from . import models


async def get_article(
    url: str, category: Optional[str], subcategory: Optional[str], tags: List[str]
) -> models.Article:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url, headers={"User-Agent": "Maybe-Later: tools for saving articles"}
        )
        article = Article(url)
        article.set_html(response.text)
        article.parse()
        return models.Article(
            title=article.title,
            text=article.text,
            source=url,
            category=category,
            subcategory=subcategory,
            tags=tags,
        )
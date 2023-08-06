#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `framler` package."""

import pytest

from framler.parsers import (
    AutoCrawlParser
)


@pytest.fixture
def article_auto_requests():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    url = "https://laodong.vn/bong-da-quoc-te/lukaku-lap-cu-dup-man-united-nguoc-dong-kinh-dien-truoc-psg-660940.ldo"  # noqa
    ac = AutoCrawlParser()

    article = ac.parse(url)
    return article


def test_response_article_auto_requests(article_auto_requests):

    article = article_auto_requests
    assert "https://laodong.vn" in article.url
    assert "Lukaku lập cú đúp, " \
        "Man United ngược dòng kinh điển trước PSG" == article.title
    assert len(article.text) > 0
    assert len(article.tags) > 0
    assert len(article.image_urls) > 0
    assert len(article.authors) > 0


def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4

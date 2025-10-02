import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.scoring import score_article


def test_score_article_increases_with_topics():
    base = score_article("Title", "Summary", [])
    with_topics = score_article("Title", "Summary", ["art", "museum"])
    assert with_topics > base
    assert with_topics <= 1.0

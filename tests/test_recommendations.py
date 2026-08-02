from src.recommendations import RECOMMENDATIONS, get_recommendation


def test_all_categories_have_consistent_recommendations() -> None:
    assert set(RECOMMENDATIONS) == {
        "cardboard",
        "glass",
        "metal",
        "paper",
        "plastic",
        "trash",
    }
    assert all(
        item.action and item.local_alternative for item in RECOMMENDATIONS.values()
    )


def test_normalizes_category() -> None:
    assert get_recommendation("  PLASTIC ") == RECOMMENDATIONS["plastic"]


def test_unknown_category_has_safe_fallback() -> None:
    fallback = get_recommendation("organic")
    assert "manual" in fallback.action.lower()
    assert "membakar" in fallback.warning.lower()


def test_plastic_warns_against_burning() -> None:
    assert "membakar" in RECOMMENDATIONS["plastic"].warning.lower()

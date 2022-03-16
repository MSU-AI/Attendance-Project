import pytest

from ..hand import Hand, MediapipeHands, HandGestureClassifier

class TestHand:
    def test____init__(self):
        pass

    def test___eq__(self):
        hand1 = Hand('thumbs up', 1)
        hand2 = Hand('thumbs up', 2)
        assert hand1 == hand2

        hand1 = Hand('thumbs up', 1)
        hand2 = Hand('thumbs down', 2)
        assert hand1 != hand2

    def test_get_all_available_gestures(self):
        assert Hand.get_all_available_gestures() == Hand.gestures

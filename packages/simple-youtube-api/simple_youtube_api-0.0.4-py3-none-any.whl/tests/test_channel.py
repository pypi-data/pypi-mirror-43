from simple_youtube_api.Channel import Channel
from simple_youtube_api.Video import Video


import pytest
import os


def test_channel_regular_function():
    channel = Channel()

    assert channel is not None


if __name__ == "__main__":
    pytest.main()

